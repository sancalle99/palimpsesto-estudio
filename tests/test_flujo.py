"""Prueba de aceptación de la Fase 2: una producción "en seco" recorre las 21 etapas
con artefactos simulados, y se verifican las reglas (puertas, aportes, presupuesto, doble conteo).
Ejecutar:  python -m unittest discover -s tests -v
"""
import shutil
import tempfile
import unittest
from pathlib import Path

from estudio import core
from estudio.core import ErrorEstudio


class Base(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.con = core.conectar(self.dir / "t.sqlite")
        core.cargar_tarifas_csv(self.con, core.RAIZ / "finanzas" / "tarifas.csv")
        core.crear_canal(self.con, "prueba", "TST", "Canal de prueba", 150, 50, "@prueba")
        self.pid = core.crear_produccion(self.con, "prueba", "Episodio en seco")

    def tearDown(self):
        self.con.close()
        shutil.rmtree(self.dir, ignore_errors=True)
        shutil.rmtree(core.RAIZ / "producciones" / self.pid, ignore_errors=True)

    def paso(self, etapa, actor):
        core.iniciar(self.con, self.pid, etapa, actor)
        core.entregar(self.con, self.pid, etapa, actor, [f"simulado-{etapa}"])


class TestFlujoCompleto(Base):
    def test_recorre_21_etapas(self):
        c, pid = self.con, self.pid
        humanas = {e.n for e in core.ETAPAS if e.puerta == "humana"}
        for e in core.ETAPAS:
            if e.n == 15:  # se cierra sola cuando la auditoría 14 aprueba sin correcciones
                self.assertEqual(core.tarea(c, pid, 15)["estado"], "cerrado")
                continue
            actor = "ceo" if e.responsable == "director" else e.responsable
            self.paso(e.n, actor)
            if e.n == 5:
                aid = core.registrar_aporte(c, "¿Y si el protagonista real es el escriba?", "pregunta", pid=pid)
            if e.n == 8:
                core.revisar(c, pid, 8, "aprobado", "auditor", "fuentes verificadas")
            if e.n == 9:
                pass
            if e.n == 14:
                core.revisar(c, pid, 14, "correcciones", "auditor", "fecha errónea en 03:12")
                core.reabrir(c, pid, 14, "auditor")
                core.entregar(c, pid, 14, "auditor", ["v2"])
                core.revisar(c, pid, 14, "aprobado", "auditor", "corregido")
            if e.n in humanas:
                with self.assertRaises(ErrorEstudio):  # un agente no puede abrir una puerta humana
                    core.revisar(c, pid, e.n, "aprobado", "ceo", "intento de agente")
                core.revisar(c, pid, e.n, "aprobado", "director", "ok", director=True)
            # la etapa 9 exige aportes resueltos: se resuelve tras el aporte de la etapa 5
            if e.n == 7:
                core.resolver_aporte(c, aid, "integrado", "Integrado como tesis del acto 3 (guion §3).", "guionista")
        estados = {t["estado"] for t in core.estado_produccion(c, pid)[1]}
        self.assertEqual(estados, {"cerrado"})
        decisiones = c.execute("SELECT COUNT(*) FROM decisiones WHERE produccion_id=?", (pid,)).fetchone()[0]
        self.assertEqual(decisiones, len(humanas))
        self.assertEqual(core.produccion(c, pid)["ciclos_correccion"], 1)


class TestReglas(Base):
    def test_no_se_salta_etapas(self):
        with self.assertRaises(ErrorEstudio):
            core.iniciar(self.con, self.pid, 2, "ceo")

    def test_aportes_pendientes_bloquean_guion(self):
        core.registrar_aporte(self.con, "Objeción sin responder", "objecion", pid=self.pid)
        for n in range(1, 9):
            actor = "ceo" if core.ETAPA[n].responsable == "director" else core.ETAPA[n].responsable
            self.paso(n, actor)
            if core.ETAPA[n].puerta == "humana":
                core.revisar(self.con, self.pid, n, "aprobado", "director", "", director=True)
            if core.ETAPA[n].puerta == "auditoria":
                core.revisar(self.con, self.pid, n, "aprobado", "auditor", "ok")
        with self.assertRaises(ErrorEstudio):
            core.iniciar(self.con, self.pid, 9, "guionista")

    def test_resolver_aporte_exige_justificacion(self):
        aid = core.registrar_aporte(self.con, "Idea", "idea", pid=self.pid)
        with self.assertRaises(ErrorEstudio):
            core.resolver_aporte(self.con, aid, "descartado", "no", "investigador")

    def test_costos_tokens_a_dolares_y_doble_conteo(self):
        _, usd = core.registrar_costo(self.con, self.pid, "investigador", "anthropic", "claude-opus-5-5",
                                      "msg_001", tokens_in=1_000_000, tokens_out=100_000, tokens_cache_r=500_000)
        self.assertAlmostEqual(usd, 4.0 + 2.0 + 0.10)
        with self.assertRaises(ErrorEstudio):
            core.registrar_costo(self.con, self.pid, "investigador", "anthropic", "claude-opus-5-5",
                                 "msg_001", tokens_in=1_000_000)

    def test_suscripcion_registra_tokens_sin_dolares(self):
        _, usd = core.registrar_costo(self.con, self.pid, "guionista", "anthropic", "claude-opus-5-5",
                                      "sess_1", tokens_in=50_000, tokens_out=5_000, modalidad="suscripcion")
        self.assertEqual(usd, 0)
        mes = core.ahora()[:7]
        core.prorratear_suscripcion(self.con, "prueba", mes, "anthropic", "claude-pro", 20.0)
        core.prorratear_suscripcion(self.con, "prueba", mes, "anthropic", "claude-pro", 20.0)  # idempotente
        self.assertAlmostEqual(core.gasto_produccion(self.con, self.pid), 20.0)

    def test_consumo_incluye_subagentes(self):
        import json
        logs = self.dir / "logs" / "-proyecto"
        sub = logs / "sesion1" / "subagents"
        sub.mkdir(parents=True)
        uso = lambda i, o: {"input_tokens": i, "output_tokens": o}  # noqa: E731
        lin = lambda mid, u, ts="2026-11-18T10:00:00Z": json.dumps(  # noqa: E731
            {"timestamp": ts, "message": {"id": mid, "model": "claude-opus-5-5", "usage": u}})
        (logs / "sesion1.jsonl").write_text(lin("m1", uso(10, 1)) + "\n" + lin("m1", uso(10, 5)) + "\n")
        (sub / "agent-a1.jsonl").write_text(lin("m2", uso(100, 20)) + "\n")
        (sub / "agent-a1.meta.json").write_text(json.dumps({"agentType": "auditor"}))
        (sub / "agent-a2.jsonl").write_text(lin("m3", uso(7, 3)) + "\n")  # sin meta
        n, d = core.importar_consumo_claude(self.con, "prueba", self.pid, logs=self.dir / "logs")
        self.assertEqual((n, d), (3, 0))
        filas = {r["id_externo"]: r for r in self.con.execute(
            "SELECT id_externo, agente, tokens_in, tokens_out FROM costos WHERE produccion_id=?", (self.pid,))}
        self.assertEqual(filas["m1"]["tokens_out"], 5)
        self.assertEqual(filas["m1"]["agente"], "claude-code")
        self.assertEqual(filas["m2"]["agente"], "auditor")
        self.assertEqual(filas["m3"]["agente"], "subagente")
        self.assertEqual(core.importar_consumo_claude(self.con, "prueba", self.pid, logs=self.dir / "logs"), (0, 3))

    def test_conciliacion_reemplaza_no_suma(self):
        cid, _ = core.registrar_costo(self.con, self.pid, "productor", "google", "veo-3.1-fast",
                                      "op_9", unidades=30, unidad="segundo")
        core.conciliar(self.con, cid, 3.4, "INV-2026-11")
        self.assertAlmostEqual(core.gasto_produccion(self.con, self.pid), 3.4)

    def test_presupuesto_alerta_y_congelacion(self):
        core.registrar_costo(self.con, self.pid, "productor", "google", "gemini-3.1-flash-image",
                             "lote_1", unidades=600, unidad="imagen")  # 40.2 USD = 80 %
        self.assertTrue(self.con.execute("SELECT 1 FROM alertas WHERE nivel='aviso'").fetchone())
        ok, _ = core.verificar_presupuesto(self.con, self.pid, 15)
        self.assertFalse(ok)
        core.registrar_costo(self.con, self.pid, "productor", "google", "veo-3.1-fast",
                             "op_2", unidades=100, unidad="segundo")  # +10 => 50.2
        self.assertEqual(core.produccion(self.con, self.pid)["estado"], "congelada")
        with self.assertRaises(ErrorEstudio):
            core.ampliar_presupuesto(self.con, self.pid, 70, "más vídeo")  # sin director
        core.ampliar_presupuesto(self.con, self.pid, 70, "más vídeo", director=True)
        self.assertEqual(core.produccion(self.con, self.pid)["estado"], "activa")

    def test_presupuesto_inicial_no_supera_tope(self):
        with self.assertRaises(ErrorEstudio):
            core.crear_produccion(self.con, "prueba", "Caro", presupuesto=80)

    def test_recurso_ia_es_recreacion_y_exige_prompt(self):
        with self.assertRaises(ErrorEstudio):
            core.registrar_recurso(self.con, self.pid, "imagen", "ia", "términos del proveedor")
        rid = core.registrar_recurso(self.con, self.pid, "imagen", "ia", "términos del proveedor",
                                     proveedor="google", prompt="scriptorium medieval, luz de vela")
        self.assertEqual(self.con.execute("SELECT es_recreacion FROM recursos WHERE id=?", (rid,)).fetchone()[0], 1)

    def test_canales_aislados(self):
        core.crear_canal(self.con, "otro", "OTR", "Otro canal", 100, 40)
        otra = core.crear_produccion(self.con, "otro", "Ep otro")
        core.registrar_costo(self.con, otra, "productor", "google", "veo-3.1-fast", "x1", unidades=10, unidad="segundo")
        self.assertEqual(core.gasto_produccion(self.con, self.pid), 0)
        self.assertTrue(otra.startswith("OTR-"))
        shutil.rmtree(core.RAIZ / "producciones" / otra, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()


class TestHookDirector(Base):
    def test_aprobacion_por_chat(self):
        from estudio.hook_aprobacion import procesar
        self.paso(1, "investigador"); self.paso(2, "ceo")
        core.iniciar(self.con, self.pid, 3, "ceo"); core.entregar(self.con, self.pid, 3, "ceo", ["ficha"])
        self.assertIsNone(procesar("Hola, ¿cómo va? apruebo luego", self.con))
        self.assertIn("no es una puerta humana", procesar(f"APRUEBO {self.pid} 2", self.con))
        r = procesar(f"APRUEBO {self.pid} 3 me gusta el tema del escriba", self.con)
        self.assertIn("registrada", r)
        self.assertEqual(core.tarea(self.con, self.pid, 3)["estado"], "cerrado")
        d = self.con.execute("SELECT justificacion FROM decisiones WHERE produccion_id=?", (self.pid,)).fetchone()[0]
        self.assertIn("Mensaje literal del Director", d)

    def test_ampliar_presupuesto_por_chat_exige_justificacion(self):
        from estudio.hook_aprobacion import procesar
        self.assertIn("justificación", procesar(f"AMPLÍO PRESUPUESTO {self.pid} 70", self.con))
        self.assertIn("ampliado", procesar(f"AMPLÍO PRESUPUESTO {self.pid} 70 más planos de vídeo", self.con))


class TestAvanzarYPanel(Base):
    def test_siguiente_recorre_y_se_detiene_en_puertas(self):
        c, pid = self.con, self.pid
        r = core.siguiente(c, pid)
        self.assertEqual((r["etapa"], r["accion"]), (1, "iniciar"))
        self.paso(1, "investigador"); self.paso(2, "ceo")
        r = core.siguiente(c, pid)
        self.assertEqual((r["etapa"], r["ejecutor"]), (3, "director"))
        self.paso(3, "ceo")
        r = core.siguiente(c, pid)
        self.assertEqual(r["accion"], "detenerse")
        core.revisar(c, pid, 3, "correcciones", "director", "otro tema", director=True)
        r = core.siguiente(c, pid)
        self.assertEqual((r["accion"], r["nota"]), ("reabrir", "otro tema"))

    def test_siguiente_auditoria_y_etapa_5(self):
        c, pid = self.con, self.pid
        for n in range(1, 5):
            actor = "ceo" if core.ETAPA[n].responsable == "director" else core.ETAPA[n].responsable
            self.paso(n, actor)
            if n == 3:
                core.revisar(c, pid, 3, "aprobado", "director", "ok", director=True)
        self.assertEqual(core.siguiente(c, pid)["accion"], "iniciar_y_detenerse")
        self.assertEqual(core.ejecutor(7), "subagente:investigador")
        self.assertEqual(core.ejecutor(2), "skill:ceo")
        self.assertEqual(core.ejecutor(14), "subagente:auditor")

    def test_panel_linea(self):
        from estudio import panel
        c, pid = self.con, self.pid
        core.iniciar(c, pid, 1, "investigador")
        aid = core.registrar_artefacto(c, pid, "informe", "producciones/x/a b.md", "investigador", 1)
        core.entregar(c, pid, 1, "investigador", [aid])
        l = panel.estado(c, "prueba")["producciones"][0]["linea"]
        self.assertEqual(len(l), 21)
        self.assertEqual(l[0]["entregables"][0]["url"], panel.REPO_URL + "producciones/x/a%20b.md")
        self.assertEqual(l[0]["estado"], "cerrado")

    def test_reorganizar_e_indice(self):
        c, pid = self.con, self.pid
        raiz = core.RAIZ / "producciones" / pid
        (raiz / "guion.md").write_text("x", encoding="utf-8")
        for n in range(1, 9):
            core.tarea(c, pid, n)  # existe
        core.registrar_artefacto(c, pid, "guion", f"producciones/{pid}/guion.md", "guionista", 9)
        plan = core.reorganizar(c, pid)
        self.assertEqual(plan, [(f"producciones/{pid}/guion.md", f"producciones/{pid}/09-guion/guion.md")])
        self.assertTrue((raiz / "guion.md").exists())  # sin aplicar no mueve nada
        core.reorganizar(c, pid, aplicar=True)
        self.assertTrue((raiz / "09-guion" / "guion.md").exists())
        self.assertEqual(c.execute("SELECT ruta FROM artefactos").fetchone()[0], f"producciones/{pid}/09-guion/guion.md")
        self.assertIn("[guion v1](09-guion/guion.md)", (raiz / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(core.carpeta_etapa(pid, 13).name, "13-edicion")
