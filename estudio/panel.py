"""Genera el panel del estudio (docs/panel.html) a partir de la base de datos.

La plantilla es docs/organigrama.html: el marcador /*ESTADO*/null/*FIN*/ se reemplaza por el
estado real (qué hace cada agente, avance por etapas, consumo del plan). El resultado se publica
como artefacto (ver CLAUDE.md, sección Panel).
"""
from __future__ import annotations

import html
import json
from urllib.parse import quote

from . import core

REPO_URL = "https://github.com/sancalle99/palimpsesto-estudio/blob/main/"
AGENTES = ("director", "ceo", "investigador", "guionista", "productor", "editor", "auditor", "cfo", "analista")
ESTADOS_LEGIBLES = {"pendiente": "pendiente", "en_curso": "en curso", "entregado": "entregado",
                    "en_revision": "en revisión", "aprobado": "aprobado", "correcciones": "correcciones",
                    "rechazado": "rechazado", "cerrado": "cerrado"}


def estado(con, slug_canal="palimpsesto", cuota=20.0) -> dict:
    c = core.canal(con, slug_canal)
    mes = core.ahora()[:7]
    reparto = {pid: frac for pid, frac, _ in core.consumo_plan(con, slug_canal, mes, cuota)}
    agentes = {k: {"estado": "espera", "detalle": "", "historial": []} for k in AGENTES}
    prods = []
    for p in con.execute("SELECT * FROM producciones WHERE canal_id=? AND estado NOT IN ('cancelada','publicada')"
                         " ORDER BY creado", (c["id"],)):
        tareas = con.execute("SELECT * FROM tareas WHERE produccion_id=? ORDER BY etapa", (p["id"],)).fetchall()
        pendiente = ""
        for t in tareas:
            ref = f"etapa {t['etapa']} · {t['nombre']} ({p['id']})"
            if t["estado"] == "en_revision" and t["puerta"] == "humana":
                agentes["director"].update(estado="decidir", detalle=ref)
                pendiente = f"{ref}. Escriba APRUEBO {p['id']} {t['etapa']} (o CORRECCIONES / RECHAZO con el motivo)."
            elif t["estado"] == "en_revision" and t["puerta"] == "auditoria":
                agentes["auditor"].update(estado="revisando", detalle=ref)
            elif t["estado"] in ("en_curso", "correcciones", "rechazado"):
                quien = t["responsable"] if t["responsable"] in agentes else "ceo"
                if quien == "director":
                    agentes["director"].update(estado="decidir", detalle=ref)
                else:
                    agentes[quien].update(estado="trabajando", detalle=ref)
        prods.append({
            "id": p["id"], "titulo": html.escape(p["titulo"]), "etapa_actual": p["etapa_actual"],
            "cerradas": sum(t["estado"] == "cerrado" for t in tareas),
            "etapas": [{"n": t["etapa"], "estado": t["estado"]} for t in tareas],
            "consumo_pct": f"{reparto.get(p['id'], 0):.0%} del uso del mes",
            "api_eq": f"{core.valor_api_equivalente(con, p['id']):.2f}",
            "gasto": f"{con.execute('SELECT COALESCE(SUM(costo_usd),0) FROM v_costos_vigentes WHERE produccion_id=? AND tipo_costo IN (\"real\",\"estimado\")', (p['id'],)).fetchone()[0]:.2f}",
            "pendiente_director": html.escape(pendiente),
            "linea": linea(con, p["id"], tareas),
        })
    # historial por agente: cambios de estado, artefactos y decisiones
    eventos = []
    for h in con.execute("SELECT h.*, t.etapa, t.nombre, t.produccion_id FROM historial_tareas h JOIN tareas t ON t.id=h.tarea_id"):
        if h["actor"] in agentes:
            txt = f"Etapa {h['etapa']} ({h['nombre']}): {ESTADOS_LEGIBLES.get(h['de_estado'], h['de_estado'])} → {ESTADOS_LEGIBLES.get(h['a_estado'], h['a_estado'])}"
            eventos.append((h["actor"], h["creado"], txt))
    for a in con.execute("SELECT * FROM artefactos"):
        if a["autor"] in agentes:
            eventos.append((a["autor"], a["creado"], f"Entregó {a['tipo'].replace('_', ' ')} ({a['id']})"))
    for d in con.execute("SELECT * FROM decisiones"):
        if d["decidio"] in agentes:
            eventos.append((d["decidio"], d["creado"], f"{d['id']}: {d['descripcion'][:110]}"))
    for actor, t, txt in sorted(eventos, key=lambda e: e[1], reverse=True):
        if len(agentes[actor]["historial"]) < 5:
            agentes[actor]["historial"].append({"t": t, "txt": html.escape(txt)})
    return {"generado": core.ahora(), "canal": c["slug"], "producciones": prods, "agentes": agentes}


def linea(con, pid, tareas) -> list:
    """Las etapas de una producción con responsable, fechas, entregables y decisiones del Director."""
    esc = lambda x: html.escape(x or "")
    arts, hist, decs = {}, {}, {}
    for a in con.execute("SELECT * FROM artefactos WHERE produccion_id=? ORDER BY creado", (pid,)):
        arts.setdefault(a["tarea_id"], []).append({
            "id": a["id"], "tipo": esc(a["tipo"].replace("_", " ")), "v": a["version"], "autor": a["autor"],
            "ruta": esc(a["ruta"]), "url": REPO_URL + quote(a["ruta"]), "t": a["creado"]})
    for h in con.execute("SELECT * FROM historial_tareas WHERE tarea_id IN (SELECT id FROM tareas WHERE produccion_id=?)"
                         " ORDER BY creado, id", (pid,)):
        hist.setdefault(h["tarea_id"], []).append({
            "t": h["creado"], "actor": h["actor"], "nota": esc(h["nota"]),
            "txt": f"{ESTADOS_LEGIBLES.get(h['de_estado'], h['de_estado'] or '—')} → {ESTADOS_LEGIBLES.get(h['a_estado'], h['a_estado'])}"})
    mig = core.migrada_13(con, pid)
    for d in con.execute("SELECT * FROM decisiones WHERE produccion_id=? ORDER BY creado", (pid,)):
        n = core.etapa_de_decision(d["tipo"], d["creado"], mig)
        decs.setdefault(n, []).append({"id": d["id"], "decidio": d["decidio"], "desc": esc(d["descripcion"]),
                                       "just": esc(d["justificacion"]), "t": d["creado"]})
    aportes = [{"id": x["id"], "tipo": x["tipo"], "texto": esc(x["texto"]), "estado": x["estado"],
                "resolucion": esc(x["resolucion"])}
               for x in con.execute("SELECT * FROM aportes WHERE produccion_id=? ORDER BY creado", (pid,))]
    filas = []
    for t in tareas:
        h = hist.get(t["id"], [])
        actores = []
        for x in [t["responsable"]] + [e["actor"] for e in h] + [a["autor"] for a in arts.get(t["id"], [])]:
            if x in AGENTES and x not in actores:
                actores.append(x)
        filas.append({
            "n": t["etapa"], "nombre": esc(t["nombre"]), "resp": t["responsable"], "puerta": t["puerta"],
            "estado": t["estado"], "iniciado": t["iniciado"], "entregado": t["entregado"], "cerrado": t["cerrado"],
            "actores": actores, "entregables": arts.get(t["id"], []), "historial": h,
            "decisiones": decs.get(t["etapa"], []),
            "aportes": aportes if t["etapa"] == 4 else [],
        })
    # decisiones de la producción sin etapa propia: van a la primera etapa que seguía abierta cuando se tomaron
    for d in decs.get(None, []):
        destino = next((f for f in filas if not f["cerrado"] or f["cerrado"] > d["t"]), filas[-1])
        destino.setdefault("otras", []).append(d)
    return filas


def generar(con, salida=None) -> str:
    plantilla = (core.RAIZ / "docs" / "organigrama.html").read_text(encoding="utf-8")
    datos = json.dumps(estado(con), ensure_ascii=False).replace("</", "<\\/")
    salida = salida or core.RAIZ / "docs" / "panel.html"
    salida.write_text(plantilla.replace("/*ESTADO*/null/*FIN*/", datos), encoding="utf-8")
    return str(salida)
