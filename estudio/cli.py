"""CLI del estudio:  python -m estudio <comando> ...

Los agentes usan esta CLI para mover tareas, registrar artefactos, recursos y costos.
Los comandos marcados [DIRECTOR] exigen una terminal interactiva y confirmación tecleada:
un agente (que ejecuta comandos sin terminal) no puede abrirlos.
"""
from __future__ import annotations

import argparse
import sys

from . import core
from .core import ErrorEstudio

AGENTES = ("ceo", "investigador", "guionista", "productor", "editor", "auditor", "analista", "cfo", "director")


def _confirmar_director(que: str, clave: str) -> bool:
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        raise ErrorEstudio("Este comando es exclusivo del Director y requiere una terminal interactiva. "
                           "Los agentes no pueden ejecutarlo.")
    print(f"\n[DIRECTOR] Va a {que}.")
    resp = input(f"Para confirmar, escriba exactamente '{clave}': ").strip()
    if resp != clave:
        print("Confirmación incorrecta. No se hizo ningún cambio.")
        return False
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(prog="estudio", description="Estudio de documentales — sistema de producción")
    ap.add_argument("--db", help="ruta alternativa de la base de datos")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("canal-crear"); s.add_argument("slug"); s.add_argument("prefijo"); s.add_argument("nombre")
    s.add_argument("--presupuesto-mensual", type=float, required=True); s.add_argument("--tope-produccion", type=float, required=True)
    s.add_argument("--handle"); s.add_argument("--youtube-id"); s.add_argument("--idioma", default="es")

    s = sub.add_parser("canales")

    s = sub.add_parser("tarifas-cargar"); s.add_argument("csv")

    s = sub.add_parser("prod-nueva"); s.add_argument("canal"); s.add_argument("titulo"); s.add_argument("--tema")
    s.add_argument("--presupuesto", type=float)

    s = sub.add_parser("prods"); s.add_argument("--canal")
    s = sub.add_parser("estado"); s.add_argument("pid")

    for nombre in ("iniciar", "reabrir"):
        s = sub.add_parser(nombre); s.add_argument("pid"); s.add_argument("etapa", type=int)
        s.add_argument("--actor", required=True, choices=AGENTES)

    s = sub.add_parser("entregar"); s.add_argument("pid"); s.add_argument("etapa", type=int)
    s.add_argument("--actor", required=True, choices=AGENTES); s.add_argument("--artefacto", action="append", default=[])
    s.add_argument("--nota")

    s = sub.add_parser("auditar", help="resuelve etapas con puerta de auditoría (8, 14)")
    s.add_argument("pid"); s.add_argument("etapa", type=int)
    s.add_argument("resultado", choices=("aprobado", "correcciones", "rechazado")); s.add_argument("--nota", required=True)

    s = sub.add_parser("aprobar", help="[DIRECTOR] resuelve puertas humanas (3, 6, 16, 17, 18)")
    s.add_argument("pid"); s.add_argument("etapa", type=int)
    s.add_argument("resultado", choices=("aprobado", "correcciones", "rechazado")); s.add_argument("--nota", default="")

    s = sub.add_parser("artefacto"); s.add_argument("pid"); s.add_argument("tipo"); s.add_argument("ruta")
    s.add_argument("--actor", required=True, choices=AGENTES); s.add_argument("--etapa", type=int)

    s = sub.add_parser("recurso"); s.add_argument("pid"); s.add_argument("tipo")
    s.add_argument("--origen", required=True, choices=("dominio_publico", "ia", "licencia", "propio"))
    s.add_argument("--licencia", required=True); s.add_argument("--proveedor"); s.add_argument("--url")
    s.add_argument("--prompt"); s.add_argument("--archivo")

    s = sub.add_parser("nota", help="registra un aporte del Director en el Cuaderno")
    s.add_argument("destino", help="ID de producción o slug de canal (aporte general)")
    s.add_argument("tipo", choices=core.TIPOS_APORTE); s.add_argument("texto")

    s = sub.add_parser("aportes"); s.add_argument("pid"); s.add_argument("--pendientes", action="store_true")
    s = sub.add_parser("aporte-resolver"); s.add_argument("aporte_id"); s.add_argument("estado", choices=("integrado", "descartado"))
    s.add_argument("resolucion"); s.add_argument("--actor", required=True, choices=AGENTES)

    s = sub.add_parser("decision"); s.add_argument("descripcion"); s.add_argument("--tipo", required=True)
    s.add_argument("--actor", required=True, choices=AGENTES); s.add_argument("--pid"); s.add_argument("--canal")
    s.add_argument("--justificacion")
    s = sub.add_parser("decisiones"); s.add_argument("--pid")

    s = sub.add_parser("presupuesto-verificar"); s.add_argument("pid"); s.add_argument("estimado", type=float)
    s = sub.add_parser("presupuesto-ampliar", help="[DIRECTOR]"); s.add_argument("pid"); s.add_argument("monto", type=float)
    s.add_argument("justificacion")

    s = sub.add_parser("costo"); s.add_argument("pid"); s.add_argument("--agente", required=True, choices=AGENTES)
    s.add_argument("--proveedor", required=True); s.add_argument("--producto", required=True)
    s.add_argument("--id-externo", required=True); s.add_argument("--tipo", default="estimado", choices=("real", "estimado"))
    s.add_argument("--modalidad", default="api", choices=("api", "suscripcion"))
    for k in ("tokens-in", "tokens-out", "tokens-cache-w", "tokens-cache-r"):
        s.add_argument(f"--{k}", type=int, default=0)
    s.add_argument("--unidades", type=float, default=0); s.add_argument("--unidad"); s.add_argument("--usd", type=float)
    s.add_argument("--etapa", type=int); s.add_argument("--short")

    s = sub.add_parser("conciliar"); s.add_argument("costo_id", type=int); s.add_argument("usd_real", type=float)
    s.add_argument("factura")
    s = sub.add_parser("prorratear"); s.add_argument("canal"); s.add_argument("mes"); s.add_argument("proveedor")
    s.add_argument("producto"); s.add_argument("usd", type=float)
    s = sub.add_parser("informe-video"); s.add_argument("pid")
    s = sub.add_parser("alertas"); s.add_argument("--todas", action="store_true")
    s = sub.add_parser("consumo-importar", help="importa el uso de tokens de Claude Code desde los registros de sesión")
    s.add_argument("canal"); s.add_argument("--pid"); s.add_argument("--desde"); s.add_argument("--hasta")
    s = sub.add_parser("consumo-plan", help="cuánto del plan de Claude consumió cada producción en el mes")
    s.add_argument("canal"); s.add_argument("mes"); s.add_argument("--cuota", type=float, default=20.0)
    s = sub.add_parser("respaldo", help="vuelca la base a db/respaldo.sql (versionado en git)")

    a = ap.parse_args(argv)
    con = core.conectar(a.db)
    try:
        return _ejecutar(con, a)
    except ErrorEstudio as e:
        print(f"✖ {e}", file=sys.stderr)
        return 2


def _ejecutar(con, a):
    c = a.cmd
    if c == "canal-crear":
        f = core.crear_canal(con, a.slug, a.prefijo, a.nombre, a.presupuesto_mensual, a.tope_produccion,
                             a.handle, a.youtube_id, a.idioma)
        print(f"✔ Canal {f['slug']} ({f['prefijo']}) creado.")
    elif c == "canales":
        for f in con.execute("SELECT * FROM canales"):
            print(f"{f['slug']:<14} {f['prefijo']}  {f['nombre']:<20} {f['handle'] or '':<22} "
                  f"tope mes {f['presupuesto_mensual_usd']:.0f} · tope prod {f['tope_produccion_usd']:.0f} USD")
    elif c == "tarifas-cargar":
        core.cargar_tarifas_csv(con, a.csv); print("✔ Tarifas cargadas.")
    elif c == "prod-nueva":
        print(f"✔ Producción creada: {core.crear_produccion(con, a.canal, a.titulo, a.tema, a.presupuesto)}")
    elif c == "prods":
        sql = "SELECT p.*, c.slug FROM producciones p JOIN canales c ON c.id=p.canal_id"
        filas = con.execute(sql + (" WHERE c.slug=?" if a.canal else ""), ((a.canal,) if a.canal else ())).fetchall()
        for p in filas:
            print(f"{p['id']}  [{p['estado']}] etapa {p['etapa_actual']:>2}/21  {core.gasto_produccion(con, p['id']):6.2f}/"
                  f"{p['presupuesto_usd']:.0f} USD  {p['titulo']}")
    elif c == "estado":
        p, tareas = core.estado_produccion(con, a.pid)
        print(f"{p['id']} — {p['titulo']}  [{p['estado']}]  gasto {core.gasto_produccion(con, p['id']):.2f}/{p['presupuesto_usd']:.2f} USD")
        for t in tareas:
            marca = {"humana": "🔒", "auditoria": "🔍", "presupuesto": "💲"}.get(t["puerta"], "  ")
            print(f" {t['etapa']:>2} {marca} {t['estado']:<12} {t['responsable']:<12} {t['nombre']}")
        pend = core.aportes_pendientes(con, a.pid)
        if pend:
            print(f"\n⚠ Aportes del Director pendientes: {', '.join(x['id'] for x in pend)}")
    elif c == "iniciar":
        core.iniciar(con, a.pid, a.etapa, a.actor); print(f"✔ Etapa {a.etapa} en curso.")
    elif c == "reabrir":
        core.reabrir(con, a.pid, a.etapa, a.actor); print(f"✔ Etapa {a.etapa} reabierta.")
    elif c == "entregar":
        core.entregar(con, a.pid, a.etapa, a.actor, a.artefacto, a.nota)
        print(f"✔ Etapa {a.etapa}: {core.tarea(con, a.pid, a.etapa)['estado']}.")
    elif c == "auditar":
        core.revisar(con, a.pid, a.etapa, a.resultado, "auditor", a.nota); print(f"✔ Auditoría etapa {a.etapa}: {a.resultado}.")
    elif c == "aprobar":
        if _confirmar_director(f"marcar la etapa {a.etapa} de {a.pid} como '{a.resultado}'", a.pid):
            core.revisar(con, a.pid, a.etapa, a.resultado, "director", a.nota, director=True)
            print(f"✔ Etapa {a.etapa}: {a.resultado} (registrado en decisiones).")
    elif c == "artefacto":
        print(f"✔ Artefacto {core.registrar_artefacto(con, a.pid, a.tipo, a.ruta, a.actor, a.etapa)}")
    elif c == "recurso":
        print(f"✔ Recurso {core.registrar_recurso(con, a.pid, a.tipo, a.origen, a.licencia, a.proveedor, a.url, a.prompt, archivo=a.archivo)}")
    elif c == "nota":
        es_prod = con.execute("SELECT 1 FROM producciones WHERE id=?", (a.destino,)).fetchone()
        aid = core.registrar_aporte(con, a.texto, a.tipo, pid=a.destino if es_prod else None,
                                    slug_canal=None if es_prod else a.destino)
        print(f"✔ Aporte registrado: {aid}")
    elif c == "aportes":
        sql = "SELECT * FROM aportes WHERE produccion_id=?" + (" AND estado='pendiente'" if a.pendientes else "")
        for x in con.execute(sql, (a.pid,)):
            print(f"{x['id']}  [{x['estado']}] {x['tipo']}: {x['texto']}" + (f"\n    → {x['resolucion']}" if x["resolucion"] else ""))
    elif c == "aporte-resolver":
        if a.actor == "director":
            raise ErrorEstudio("Los aportes los resuelven los agentes (integrándolos o justificando el descarte).")
        core.resolver_aporte(con, a.aporte_id, a.estado, a.resolucion, a.actor); print("✔ Aporte resuelto.")
    elif c == "decision":
        if a.actor == "director" or a.tipo in ("tema", "enfoque", "presupuesto", "aprobacion_video", "publicacion"):
            raise ErrorEstudio("Las decisiones reservadas al Director se registran solo mediante 'aprobar' "
                               "o 'presupuesto-ampliar'. Use tipo 'operativa' o 'estrategia' (propuesta).")
        print(f"✔ {core.registrar_decision(con, a.descripcion, a.tipo, a.actor, a.pid, a.canal, a.justificacion)}")
    elif c == "decisiones":
        sql = "SELECT * FROM decisiones" + (" WHERE produccion_id=?" if a.pid else "") + " ORDER BY creado"
        for d in con.execute(sql, ((a.pid,) if a.pid else ())):
            print(f"{d['id']} {d['creado'][:16]} [{d['tipo']}] {d['decidio']}: {d['descripcion']}"
                  + (f" — {d['justificacion']}" if d["justificacion"] else ""))
    elif c == "presupuesto-verificar":
        ok, msg = core.verificar_presupuesto(con, a.pid, a.estimado); print(("✔ " if ok else "✖ ") + msg)
        return 0 if ok else 3
    elif c == "presupuesto-ampliar":
        if _confirmar_director(f"ampliar el presupuesto de {a.pid} a {a.monto:.2f} USD", a.pid):
            core.ampliar_presupuesto(con, a.pid, a.monto, a.justificacion, director=True); print("✔ Presupuesto ampliado.")
    elif c == "costo":
        cid, usd = core.registrar_costo(con, a.pid, a.agente, a.proveedor, a.producto, a.id_externo, a.tipo,
                                        a.tokens_in, a.tokens_out, a.tokens_cache_w, a.tokens_cache_r,
                                        a.unidades, a.unidad, a.usd, a.etapa, a.short, modalidad=a.modalidad)
        print(f"✔ Costo #{cid}: {usd:.4f} USD")
    elif c == "conciliar":
        core.conciliar(con, a.costo_id, a.usd_real, a.factura); print("✔ Conciliado (estimado anulado, real registrado).")
    elif c == "prorratear":
        d = core.prorratear_suscripcion(con, a.canal, a.mes, a.proveedor, a.producto, a.usd)
        print(f"✔ Prorrateado entre: {', '.join(x for x, _ in d)}")
    elif c == "informe-video":
        print(core.informe_video(con, a.pid))
    elif c == "alertas":
        sql = "SELECT * FROM alertas" + ("" if a.todas else " WHERE resuelta=0") + " ORDER BY creado DESC"
        for x in con.execute(sql):
            print(f"[{x['nivel'].upper()}] {x['creado'][:16]} {x['mensaje']}")
    elif c == "respaldo":
        print(f"✔ Respaldo escrito en {core.respaldar(con)}")
    elif c == "consumo-importar":
        n, d = core.importar_consumo_claude(con, a.canal, a.pid, a.desde, a.hasta)
        print(f"✔ {n} respuestas importadas ({d} ya estaban registradas).")
    elif c == "consumo-plan":
        print(f"Plan de Claude — {a.mes} — cuota {a.cuota:.2f} USD")
        for pid, frac, usd in core.consumo_plan(con, a.canal, a.mes, a.cuota):
            print(f"  {pid:<22} {frac:6.1%}  ≈ {usd:5.2f} USD   (valor API equivalente ≈ {core.valor_api_equivalente(con, pid):6.2f} USD)")
    return 0
