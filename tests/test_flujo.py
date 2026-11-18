"""Prueba de aceptación: una producción "en seco" recorre las 13 etapas
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
    def test_recorre_13_etapas(self):
        c, pid = self.con, self.pid
        self.assertEqual(core.N_ETAPAS, 13)
        humanas = {e.n for e in core.ETAPAS if e.puerta == "humana"}
        self.assertEqual(humanas, {2, 4, 11, 12})
        for e in core.ETAPAS:
            actor = "ceo" if e.responsable == "director" else e.responsable
            self.paso(e.n, actor)
            if e.n == 4:  # observaciones del Director, dentro de la puerta del enfoque
                aid = core.registrar_aporte(c, "¿Y si el protagonista real es el escriba?", "pregunta", pid=pid)
            if e.n == 5:
                core.revisar(c, pid, 5, "aprobado", "auditor", "fuentes verificadas")
                # la etapa 6 (guion) exige aportes resueltos
                core.resolver_aporte(c, aid, "integrado", "Integrado como tesis del acto 3 (guion §3).", "guionista")
            if e.n == 10:  # auditoría y correcciones en la misma etapa
                core.revisar(c, pid, 10, "correcciones", "auditor", "fecha errónea en 03:12")
                core.reabrir(c, pid, 10, "auditor")
                core.entregar(c, pid, 10, "auditor", ["v2"])
                core.revisar(c, pid, 10, "aprobado", "auditor", "corregido")
            if e.n in humanas:
                with self.assertRaises(ErrorEstudio):  # un agente no puede abrir una puerta humana
                    core.revisar(c, pid, e.n, "aprobado", "ceo", "intento de agente")
                core.revisar(c, pid, e.n, "aprobado", "director", "ok", director=True)
        estados = {t["estado"] for t in core.estado_produccion(c, pid)[1]}
        self.assertEqual(estados, {"cerrado"})
        decisiones = c.execute("SELECT COUNT(*) FROM decisiones WHERE produccion_id=?", (pid,)).fetchone()[0]
        self.assertEqual(decisiones, len(humanas))
        self.assertEqual(core.produccion(c, pid)["ciclos_correccion"], 1)
        self.assertEqual(core.siguiente(c, pid)["accion"], "completa")


class TestReglas(Base):
    def test_no_se_salta_etapas(self):
        with self.assertRaises(ErrorEstudio):
            core.iniciar(self.con, self.pid, 2, "ceo")

    def test_aportes_pendientes_bloquean_guion(self):
        core.registrar_aporte(self.con, "Objeción sin responder", "objecion", pid=self.pid)
        for n in range(1, 6):
            actor = "ceo" if core.ETAPA[n].responsable == "director" else core.ETAPA[n].responsable
            self.paso(n, actor)
            if core.ETAPA[n].puerta == "humana":
                core.revisar(self.con, self.pid, n, "aprobado", "director", "", director=True)
            if core.ETAPA[n].puerta == "auditoria":
                core.revisar(self.con, self.pid, n, "aprobado", "auditor", "ok")
        self.assertEqual(core.siguiente(self.con, self.pid)["accion"], "resolver_aportes")
        with self.assertRaises(ErrorEstudio):
            core.iniciar(self.con, self.pid, 6, "guionista")

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
        self.paso(1, "investigador")
        core.iniciar(self.con, self.pid, 2, "ceo"); core.entregar(self.con, self.pid, 2, "ceo", ["ficha"])
        self.assertIsNone(procesar("Hola, ¿cómo va? apruebo luego", self.con))
        self.assertIn("no es una puerta humana", procesar(f"APRUEBO {self.pid} 3", self.con))
        r = procesar(f"APRUEBO {self.pid} 2 me gusta el tema del escriba", self.con)
        self.assertIn("registrada", r)
        self.assertEqual(core.tarea(self.con, self.pid, 2)["estado"], "cerrado")
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
        self.paso(1, "investigador")
        r = core.siguiente(c, pid)
        self.assertEqual((r["etapa"], r["ejecutor"]), (2, "director"))
        self.paso(2, "ceo")
        r = core.siguiente(c, pid)
        self.assertEqual(r["accion"], "detenerse")
        core.revisar(c, pid, 2, "correcciones", "director", "otro tema", director=True)
        r = core.siguiente(c, pid)
        self.assertEqual((r["accion"], r["nota"]), ("reabrir", "otro tema"))

    def test_siguiente_auditoria_y_ejecutores(self):
        c, pid = self.con, self.pid
        for n in range(1, 6):
            actor = "ceo" if core.ETAPA[n].responsable == "director" else core.ETAPA[n].responsable
            self.paso(n, actor)
            if core.ETAPA[n].puerta == "humana":
                core.revisar(c, pid, n, "aprobado", "director", "ok", director=True)
        self.assertEqual(core.siguiente(c, pid)["accion"], "auditar")
        self.assertEqual(core.ejecutor(5), "subagente:investigador")
        self.assertEqual(core.ejecutor(6), "skill:guionista")
        self.assertEqual(core.ejecutor(9), "skill:editor")
        self.assertEqual(core.ejecutor(10), "subagente:auditor")
        self.assertEqual(core.ejecutor(12), "director")

    def test_panel_linea(self):
        from estudio import panel
        c, pid = self.con, self.pid
        core.iniciar(c, pid, 1, "investigador")
        aid = core.registrar_artefacto(c, pid, "informe", "producciones/x/a b.md", "investigador", 1)
        core.entregar(c, pid, 1, "investigador", [aid])
        l = panel.estado(c, "prueba")["producciones"][0]["linea"]
        self.assertEqual(len(l), 13)
        self.assertEqual(l[0]["entregables"][0]["url"], panel.REPO_URL + "producciones/x/a%20b.md")
        self.assertEqual(l[0]["estado"], "cerrado")

    def test_reorganizar_e_indice(self):
        c, pid = self.con, self.pid
        raiz = core.RAIZ / "producciones" / pid
        (raiz / "guion.md").write_text("x", encoding="utf-8")
        core.registrar_artefacto(c, pid, "guion", f"producciones/{pid}/guion.md", "guionista", 6)
        plan = core.reorganizar(c, pid)
        self.assertEqual(plan, [(f"producciones/{pid}/guion.md", f"producciones/{pid}/06-guion/guion.md")])
        self.assertTrue((raiz / "guion.md").exists())  # sin aplicar no mueve nada
        core.reorganizar(c, pid, aplicar=True)
        self.assertTrue((raiz / "06-guion" / "guion.md").exists())
        self.assertEqual(c.execute("SELECT ruta FROM artefactos").fetchone()[0], f"producciones/{pid}/06-guion/guion.md")
        self.assertIn("[guion v1](06-guion/guion.md)", (raiz / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(core.carpeta_etapa(pid, 9).name, "09-edicion")


class TestMigracion13(Base):
    """Una producción con el flujo antiguo de 21 etapas pasa al de 13 sin perder historial."""
    def antigua(self):
        c, pid = self.con, self.pid
        c.execute("DELETE FROM tareas WHERE produccion_id=?", (pid,))
        for n in range(1, 22):
            puerta = "humana" if n in (3, 6, 16, 17, 18) else "auditoria" if n in (8, 14) else "ninguna"
            c.execute("INSERT INTO tareas (produccion_id, etapa, nombre, responsable, puerta, creado)"
                      " VALUES (?,?,?,?,?,?)", (pid, n, f"antigua {n}", "ceo", puerta, core.ahora()))
        for n in range(1, 14):
            for s in ("en_curso", "entregado", "cerrado"):
                core._cambiar_estado(c, core.tarea(c, pid, n), s, "ceo")
        t3 = core.tarea(c, pid, 3)["id"]
        c.execute("INSERT INTO artefactos (id, produccion_id, tarea_id, tipo, ruta, version, autor, sha256, creado)"
                  " SELECT 'A1', ?, ?, 'ficha', ?, 1, 'ceo', 'h', ? ", (pid, t3, f"producciones/{pid}/03-seleccion-tema/ficha.md", core.ahora()))
        core.registrar_decision(c, pid=pid, tipo="aprobacion_etapa_3", decidio="director", descripcion="tema")
        carpeta = core.RAIZ / "producciones" / pid / "03-seleccion-tema"
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / "ficha.md").write_text("x", encoding="utf-8")
        c.commit()

    def test_migrar(self):
        c, pid = self.con, self.pid
        self.antigua()
        plan = core.migrar_13(c, pid)  # sin aplicar no cambia nada
        self.assertEqual(c.execute("SELECT COUNT(*) FROM tareas WHERE produccion_id=?", (pid,)).fetchone()[0], 21)
        self.assertTrue(any("→" in x for x in plan))
        hist_antes = c.execute("SELECT COUNT(*) FROM historial_tareas").fetchone()[0]
        core.migrar_13(c, pid, aplicar=True)
        _, tareas = core.estado_produccion(c, pid)
        self.assertEqual([t["estado"] for t in tareas], ["cerrado"] * 9 + ["pendiente"] * 4)
        self.assertEqual([t["etapa"] for t in tareas], list(range(1, 14)))
        self.assertEqual(c.execute("SELECT COUNT(*) FROM historial_tareas").fetchone()[0], hist_antes)
        self.assertEqual(core.produccion(c, pid)["etapa_actual"], 10)
        ruta = c.execute("SELECT ruta FROM artefactos WHERE id='A1'").fetchone()[0]
        self.assertEqual(ruta, f"producciones/{pid}/02-seleccion-tema/ficha.md")
        self.assertTrue((core.RAIZ / ruta).exists())
        self.assertFalse((core.RAIZ / "producciones" / pid / "03-seleccion-tema").exists())
        mig = core.migrada_13(c, pid)
        d = c.execute("SELECT * FROM decisiones WHERE tipo='aprobacion_etapa_3'").fetchone()
        self.assertEqual(core.etapa_de_decision(d["tipo"], d["creado"], mig), 2)
        with self.assertRaises(ErrorEstudio):
            core.migrar_13(c, pid, aplicar=True)
        self.assertEqual(core.siguiente(c, pid)["etapa"], 10)


class TestYoutube(Base):
    def test_metadatos_y_privado(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("yt", core.RAIZ / "scripts" / "youtube_subir.py")
        yt = importlib.util.module_from_spec(spec); spec.loader.exec_module(yt)
        md = self.dir / "metadatos.md"
        md.write_text("| Campo | Valor |\n|---|---|\n| Título (definitivo) | **Un título** |\n| Categoría | Educación |\n"
                      "| Contenido alterado o sintético | **Sí**: recreaciones |\n| Etiquetas | a, b |\n\n"
                      "## Descripción\n\n```\nTexto\n```\n", encoding="utf-8")
        meta = yt.leer_metadatos(md)
        self.assertEqual((meta["titulo"], meta["etiquetas"], meta["categoria"], meta["sintetico"]),
                         ("Un título", ["a", "b"], "27", True))
        self.assertEqual(yt.cuerpo_subida(meta)["status"]["privacyStatus"], "private")
        with self.assertRaises(yt.ErrorSubida):  # sin APRUEBO <ID> 12 no se publica
            yt.orden_del_director(self.con, self.pid)
