"""Núcleo del estudio: base de datos, flujo de producción, Cuaderno del Director,
decisiones y control financiero.

Reglas que este módulo hace cumplir (no dependen de que un agente "se porte bien"):
  * Las puertas humanas solo se abren con director=True, que solo concede la CLI
    cuando hay una terminal interactiva con confirmación tecleada (ver cli.py).
  * Ninguna etapa empieza sin que la anterior esté cerrada.
  * El guion y la aprobación final exigen que todos los aportes del Director estén resueltos.
  * Cada gasto tiene hash único (anti doble conteo); al 100 % del tope la producción se congela.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DB_POR_DEFECTO = RAIZ / "db" / "estudio.sqlite"
SCHEMA = RAIZ / "db" / "schema.sql"
RESPALDO = RAIZ / "db" / "respaldo.sql"   # volcado de texto versionado en git


class ErrorEstudio(Exception):
    """Error de regla de negocio (mensaje legible para el Director y los agentes)."""


def ahora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def conectar(ruta: str | os.PathLike | None = None) -> sqlite3.Connection:
    ruta = Path(ruta or os.environ.get("ESTUDIO_DB", DB_POR_DEFECTO))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    restaurar = ruta == DB_POR_DEFECTO and not ruta.exists() and RESPALDO.exists()
    con = sqlite3.connect(ruta)
    if restaurar:  # sesión nueva: se reconstruye la base desde el respaldo versionado
        con.executescript(RESPALDO.read_text(encoding="utf-8"))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA.read_text(encoding="utf-8"))
    return con


def restaurar_desde_respaldo(ruta=None) -> Path:
    """Reconstruye la base desde db/respaldo.sql (p. ej., tras traer trabajo de otra sesión con git).
    La base anterior se conserva como copia con fecha; no se borra nada."""
    ruta = Path(ruta or DB_POR_DEFECTO)
    copia = ruta.with_name(f"{ruta.stem}.antes-{ahora()[:19].replace(':', '')}.sqlite")
    nueva = ruta.with_name(ruta.stem + ".nueva.sqlite")
    if nueva.exists():
        nueva.unlink()
    con = sqlite3.connect(nueva)
    con.executescript(RESPALDO.read_text(encoding="utf-8"))
    con.close()
    if ruta.exists():
        ruta.replace(copia)
    nueva.replace(ruta)
    return copia


def respaldar(con) -> Path:
    """Escribe un volcado SQL de texto (legible y versionable) de toda la base."""
    RESPALDO.write_text("\n".join(con.iterdump()) + "\n", encoding="utf-8")
    return RESPALDO


# ---------------------------------------------------------------------------
# Flujo de producción: 13 etapas (DEC-0014; antes eran 21, ver MAPA_21_A_13)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Etapa:
    n: int
    nombre: str
    responsable: str
    puerta: str = "ninguna"  # ninguna | humana | auditoria | presupuesto


ETAPAS: list[Etapa] = [
    Etapa(1, "Oportunidades y temas", "investigador"),
    Etapa(2, "Selección del tema", "director", "humana"),
    Etapa(3, "Tres enfoques narrativos", "investigador"),
    Etapa(4, "Aprobación del enfoque y observaciones", "director", "humana"),
    Etapa(5, "Investigación y expediente", "investigador", "auditoria"),
    Etapa(6, "Guion y títulos", "guionista"),
    Etapa(7, "Storyboard y prompts", "productor"),
    Etapa(8, "Producción audiovisual", "productor", "presupuesto"),
    Etapa(9, "Edición, Shorts y subida privada", "editor"),
    Etapa(10, "Auditoría y correcciones", "auditor", "auditoria"),
    Etapa(11, "Aprobación del vídeo, Shorts y título final", "director", "humana"),
    Etapa(12, "Publicación a la hora recomendada", "director", "humana"),
    Etapa(13, "Cierre: métricas, costos y lecciones", "analista"),
]
ETAPA = {e.n: e for e in ETAPAS}
N_ETAPAS = len(ETAPAS)
ETAPAS_QUE_EXIGEN_APORTES_RESUELTOS = {6, 11}
ETAPA_AUDITORIA_FINAL, ETAPA_APROBACION_FINAL = 10, 11

# Migración desde el flujo antiguo de 21 etapas (DEC-0014). Los Shorts (antes 18) se hacen en la 9
# y se aprueban en la 11; al migrar, la tarea antigua 18 se funde con la 11 (aún pendiente).
MAPA_21_A_13 = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 7, 11: 7, 12: 8, 13: 9,
                14: 10, 15: 10, 16: 11, 17: 12, 18: 11, 19: 13, 20: 13, 21: 13}
CARPETAS_21 = {1: "01-oportunidades", 2: "02-temas", 3: "03-seleccion-tema", 4: "04-enfoques", 5: "05-observaciones",
               6: "06-aprobacion-enfoque", 7: "07-investigacion", 8: "08-expediente", 9: "09-guion",
               10: "10-storyboard", 11: "11-prompts", 12: "12-produccion", 13: "13-edicion", 14: "14-auditoria",
               15: "15-correcciones", 16: "16-aprobacion-video", 17: "17-publicacion", 18: "18-shorts",
               19: "19-metricas", 20: "20-informe-financiero", 21: "21-retroalimentacion"}

# Carpeta de entregables de cada etapa: producciones/<ID>/NN-nombre/ (recursos/ y render/ quedan en la raíz).
CARPETAS = {1: "01-oportunidades", 2: "02-seleccion-tema", 3: "03-enfoques", 4: "04-aprobacion-enfoque",
            5: "05-expediente", 6: "06-guion", 7: "07-storyboard", 8: "08-produccion", 9: "09-edicion",
            10: "10-auditoria", 11: "11-aprobacion", 12: "12-publicacion", 13: "13-cierre"}


def carpeta_etapa(pid, etapa, crear=True) -> Path:
    c = RAIZ / "producciones" / pid / CARPETAS[etapa]
    if crear:
        c.mkdir(parents=True, exist_ok=True)
    return c
MAX_CICLOS_CORRECCION = 2

ESTADOS = ("pendiente", "en_curso", "entregado", "en_revision",
           "aprobado", "correcciones", "rechazado", "cerrado")
TRANSICIONES = {
    "pendiente": {"en_curso"},
    "en_curso": {"entregado"},
    "entregado": {"en_revision", "cerrado"},
    "en_revision": {"aprobado", "correcciones", "rechazado"},
    "correcciones": {"en_curso"},
    "rechazado": {"en_curso"},
    "aprobado": {"cerrado"},
    "cerrado": set(),
}


# ---------------------------------------------------------------------------
# Canales
# ---------------------------------------------------------------------------
def crear_canal(con, slug, prefijo, nombre, presupuesto_mensual, tope_produccion,
                handle=None, youtube_channel_id=None, idioma="es", umbral=0.8):
    con.execute(
        "INSERT INTO canales (slug, prefijo, nombre, handle, youtube_channel_id, idioma,"
        " presupuesto_mensual_usd, tope_produccion_usd, umbral_alerta, creado)"
        " VALUES (?,?,?,?,?,?,?,?,?,?)",
        (slug, prefijo.upper(), nombre, handle, youtube_channel_id, idioma,
         presupuesto_mensual, tope_produccion, umbral, ahora()))
    con.commit()
    return canal(con, slug)


def canal(con, slug_o_id):
    fila = con.execute("SELECT * FROM canales WHERE slug=? OR id=?",
                       (str(slug_o_id), slug_o_id)).fetchone()
    if not fila:
        raise ErrorEstudio(f"Canal '{slug_o_id}' no existe.")
    return fila


def presupuesto_mes(con, canal_id, mes):
    fila = con.execute("SELECT monto_usd FROM presupuestos WHERE canal_id=? AND mes=?",
                       (canal_id, mes)).fetchone()
    if fila:
        return fila["monto_usd"]
    return con.execute("SELECT presupuesto_mensual_usd FROM canales WHERE id=?",
                       (canal_id,)).fetchone()[0]


# ---------------------------------------------------------------------------
# Producciones y tareas
# ---------------------------------------------------------------------------
def crear_produccion(con, slug_canal, titulo, tema=None, presupuesto=None):
    c = canal(con, slug_canal)
    anio = datetime.now(timezone.utc).year
    prefijo = f"{c['prefijo']}-{anio}-"
    n = con.execute("SELECT COUNT(*) FROM producciones WHERE id LIKE ?",
                    (prefijo + "%",)).fetchone()[0] + 1
    pid = f"{prefijo}{n:03d}"
    tope = c["tope_produccion_usd"]
    presupuesto = tope if presupuesto is None else presupuesto
    if presupuesto > tope:
        raise ErrorEstudio(f"El presupuesto ({presupuesto}) supera el tope por producción "
                           f"del canal ({tope}). Requiere aprobación del Director (presupuesto ampliar).")
    t = ahora()
    con.execute("INSERT INTO producciones (id, canal_id, titulo, tema, presupuesto_usd, creado, actualizado)"
                " VALUES (?,?,?,?,?,?,?)", (pid, c["id"], titulo, tema, presupuesto, t, t))
    for e in ETAPAS:
        con.execute("INSERT INTO tareas (produccion_id, etapa, nombre, responsable, puerta, creado)"
                    " VALUES (?,?,?,?,?,?)", (pid, e.n, e.nombre, e.responsable, e.puerta, t))
    con.commit()
    carpeta = RAIZ / "producciones" / pid
    carpeta.mkdir(parents=True, exist_ok=True)
    cuaderno = carpeta / "cuaderno_director.md"
    if not cuaderno.exists():
        cuaderno.write_text(
            f"# Cuaderno del Director — {pid}\n\n**{titulo}**\n\n"
            "Escriba aquí sus notas libremente; para que queden registradas y trazables use:\n"
            f"`python -m estudio nota {pid} <tipo> \"texto\"` (tipos: pregunta, perspectiva, objecion, idea, decision).\n\n"
            "## Aportes registrados\n\n", encoding="utf-8")
    escribir_indice(con, pid)
    return pid


def produccion(con, pid):
    fila = con.execute("SELECT * FROM producciones WHERE id=?", (pid,)).fetchone()
    if not fila:
        raise ErrorEstudio(f"Producción '{pid}' no existe.")
    return fila


def tarea(con, pid, etapa):
    fila = con.execute("SELECT * FROM tareas WHERE produccion_id=? AND etapa=?",
                       (pid, etapa)).fetchone()
    if not fila:
        raise ErrorEstudio(f"No existe la etapa {etapa} en {pid}.")
    return fila


def _cambiar_estado(con, t, nuevo, actor, nota=None):
    actual = t["estado"]
    if nuevo not in TRANSICIONES[actual]:
        raise ErrorEstudio(f"Transición no permitida en etapa {t['etapa']}: {actual} → {nuevo}.")
    campos = {"en_curso": "iniciado", "entregado": "entregado", "cerrado": "cerrado"}
    sets, vals = ["estado=?"], [nuevo]
    if nuevo in campos:
        sets.append(f"{campos[nuevo]}=?")
        vals.append(ahora())
    con.execute(f"UPDATE tareas SET {', '.join(sets)} WHERE id=?", (*vals, t["id"]))
    con.execute("INSERT INTO historial_tareas (tarea_id, de_estado, a_estado, actor, nota, creado)"
                " VALUES (?,?,?,?,?,?)", (t["id"], actual, nuevo, actor, nota, ahora()))
    con.execute("UPDATE producciones SET actualizado=? WHERE id=?", (ahora(), t["produccion_id"]))


def iniciar(con, pid, etapa, actor):
    p = produccion(con, pid)
    if p["estado"] == "congelada" and ETAPA[etapa].puerta == "presupuesto":
        raise ErrorEstudio(f"{pid} está CONGELADA por presupuesto. Solo el Director puede ampliarlo.")
    if p["estado"] in ("cancelada",):
        raise ErrorEstudio(f"{pid} está cancelada.")
    if etapa > 1:
        previa = tarea(con, pid, etapa - 1)
        if previa["estado"] != "cerrado":
            raise ErrorEstudio(f"No se puede iniciar la etapa {etapa}: la etapa {etapa - 1} "
                               f"('{previa['nombre']}') está en '{previa['estado']}'.")
    if etapa in ETAPAS_QUE_EXIGEN_APORTES_RESUELTOS:
        _exigir_aportes_resueltos(con, pid)
    t = tarea(con, pid, etapa)
    _cambiar_estado(con, t, "en_curso", actor)
    con.execute("UPDATE producciones SET etapa_actual=? WHERE id=?", (etapa, pid))
    con.commit()


def entregar(con, pid, etapa, actor, artefactos=(), nota=None):
    t = tarea(con, pid, etapa)
    if ETAPA[etapa].responsable not in (actor, "director") and actor != "ceo":
        raise ErrorEstudio(f"La etapa {etapa} es responsabilidad de '{ETAPA[etapa].responsable}', no de '{actor}'.")
    previos = json.loads(t["entregables"])
    nuevos = previos + [a for a in artefactos if a not in previos]
    con.execute("UPDATE tareas SET entregables=? WHERE id=?", (json.dumps(nuevos), t["id"]))
    _cambiar_estado(con, t, "entregado", actor, nota)
    t = tarea(con, pid, etapa)
    if ETAPA[etapa].puerta == "ninguna" or ETAPA[etapa].puerta == "presupuesto":
        _cambiar_estado(con, t, "cerrado", actor, "cierre automático (sin puerta)")
    else:
        _cambiar_estado(con, t, "en_revision", actor)
    con.commit()


def revisar(con, pid, etapa, resultado, actor, nota, director=False):
    """Resuelve una tarea en revisión. Puertas humanas: solo el Director. Auditoría: solo el auditor."""
    e = ETAPA[etapa]
    t = tarea(con, pid, etapa)
    if t["estado"] != "en_revision":
        raise ErrorEstudio(f"La etapa {etapa} no está en revisión (estado: {t['estado']}).")
    if e.puerta == "humana" and not director:
        raise ErrorEstudio(f"La etapa {etapa} ('{e.nombre}') es una PUERTA HUMANA: solo el Director "
                           "puede aprobarla, desde una terminal interactiva.")
    if e.puerta == "auditoria" and actor != "auditor":
        raise ErrorEstudio(f"La etapa {etapa} la resuelve únicamente el agente auditor.")
    if resultado not in ("aprobado", "correcciones", "rechazado"):
        raise ErrorEstudio("Resultado debe ser aprobado | correcciones | rechazado.")
    if etapa == ETAPA_APROBACION_FINAL and resultado == "aprobado":
        _exigir_aportes_resueltos(con, pid)
    _cambiar_estado(con, t, resultado, actor, nota)
    if resultado == "aprobado":
        _cambiar_estado(con, tarea(con, pid, etapa), "cerrado", actor)
        if e.puerta == "humana":
            registrar_decision(con, pid=pid, tipo=f"aprobacion_etapa_{etapa}",
                               descripcion=f"Aprobada etapa {etapa}: {e.nombre}",
                               decidio="director", justificacion=nota, commit=False)
    elif etapa == ETAPA_AUDITORIA_FINAL:
        p = produccion(con, pid)
        ciclos = p["ciclos_correccion"] + 1
        con.execute("UPDATE producciones SET ciclos_correccion=? WHERE id=?", (ciclos, pid))
        if ciclos > MAX_CICLOS_CORRECCION:
            crear_alerta(con, p["canal_id"], pid, "aviso",
                         f"{pid}: más de {MAX_CICLOS_CORRECCION} ciclos de corrección. Escala al CEO.")
    con.commit()


def reabrir(con, pid, etapa, actor):
    """Tras 'correcciones' o 'rechazado', el responsable retoma la tarea."""
    _cambiar_estado(con, tarea(con, pid, etapa), "en_curso", actor)
    con.commit()


def estado_produccion(con, pid):
    p = produccion(con, pid)
    tareas = con.execute("SELECT etapa, nombre, responsable, puerta, estado FROM tareas"
                         " WHERE produccion_id=? ORDER BY etapa", (pid,)).fetchall()
    return p, tareas


# Etapas que corren en un subagente (independencia o volumen); el resto, en la sesión principal (modo económico).
ETAPAS_EN_SUBAGENTE = {5, 10}


def ejecutor(etapa: int) -> str:
    """Quién ejecuta la etapa en /avanzar: una skill del responsable si existe; si no, subagente o sesión principal."""
    e = ETAPA[etapa]
    if e.responsable == "director":
        return "director"
    if (RAIZ / ".claude" / "skills" / e.responsable / "SKILL.md").exists() and e.responsable != "auditor":
        return f"skill:{e.responsable}"
    return f"subagente:{e.responsable}" if etapa in ETAPAS_EN_SUBAGENTE else f"sesion:{e.responsable}"


def siguiente(con, pid) -> dict:
    """Siguiente paso de una producción para /avanzar: la primera etapa no cerrada y la acción que toca."""
    p = produccion(con, pid)
    t = con.execute("SELECT * FROM tareas WHERE produccion_id=? AND estado!='cerrado' ORDER BY etapa LIMIT 1",
                    (pid,)).fetchone()
    if t is None:
        return {"pid": pid, "accion": "completa", "detalle": f"Las {N_ETAPAS} etapas están cerradas."}
    e = ETAPA[t["etapa"]]
    r = {"pid": pid, "etapa": e.n, "nombre": e.nombre, "responsable": e.responsable, "puerta": e.puerta,
         "estado": t["estado"], "ejecutor": ejecutor(e.n), "nota": None}
    ultima = con.execute("SELECT nota FROM historial_tareas WHERE tarea_id=? AND nota IS NOT NULL ORDER BY id DESC LIMIT 1",
                         (t["id"],)).fetchone()
    if t["estado"] in ("correcciones", "rechazado"):
        r["nota"] = ultima["nota"] if ultima else None
    if p["estado"] == "congelada" and e.puerta == "presupuesto":
        r.update(accion="detenerse", detalle="Producción CONGELADA por presupuesto: solo el Director puede ampliarlo.")
    elif t["estado"] == "en_revision" and e.puerta == "humana":
        r.update(accion="detenerse", detalle=f"Puerta 🔒: mostrar la Ficha de decisión y esperar APRUEBO / CORRECCIONES / RECHAZO {pid} {e.n}.")
    elif t["estado"] == "en_revision" and e.puerta == "auditoria":
        r.update(accion="auditar", detalle="Lanzar el subagente auditor solo con los entregables; él resuelve con 'auditar'.")
    elif e.n in ETAPAS_QUE_EXIGEN_APORTES_RESUELTOS and t["estado"] == "pendiente" and aportes_pendientes(con, pid):
        r.update(accion="resolver_aportes",
                 detalle="Hay aportes del Director sin resolver: integrarlos o descartarlos con justificación antes de iniciar.")
    elif t["estado"] == "pendiente":
        r.update(accion="iniciar", detalle=f"python3 -m estudio iniciar {pid} {e.n} --actor "
                                           f"{'ceo' if e.responsable == 'director' else e.responsable}")
    elif t["estado"] in ("correcciones", "rechazado"):
        r.update(accion="reabrir", detalle="Reabrir y rehacer según la nota de la revisión.")
    elif t["estado"] == "en_curso":
        r.update(accion="trabajar", detalle="Producir el entregable, registrarlo con 'artefacto' y 'entregar'.")
    else:
        r.update(accion="revisar_estado", detalle=f"Estado transitorio '{t['estado']}': revisar con 'estado'.")
    if e.responsable == "director" and e.puerta != "humana" and r["accion"] in ("iniciar", "trabajar"):
        r["detalle"] += " Etapa del Director: pedirle sus observaciones (/nota) y detenerse; si dice que no tiene, el CEO la entrega."
        r["accion"] += "_y_detenerse"
    return r


def migrada_13(con, pid):
    """Fecha en que la producción pasó del flujo de 21 al de 13 etapas (None si nació con 13)."""
    d = con.execute("SELECT creado FROM decisiones WHERE produccion_id=? AND tipo='migracion_13_etapas'",
                    (pid,)).fetchone()
    return d["creado"] if d else None


def etapa_de_decision(tipo, creado, migracion):
    """Etapa (flujo de 13) a la que pertenece una decisión 'aprobacion_etapa_N'; las anteriores a la
    migración usan la numeración antigua de 21 etapas y se traducen con MAPA_21_A_13."""
    if not tipo.startswith("aprobacion_etapa_"):
        return None
    n = int(tipo.rsplit("_", 1)[1])
    return MAPA_21_A_13.get(n, n) if migracion and creado <= migracion else n


def migrar_13(con, pid, aplicar=False) -> list:
    """Pasa una producción del flujo de 21 etapas al de 13 (DEC-0014) sin perder historial:
    las tareas antiguas que se funden ceden sus artefactos e historial a la nueva; la etapa queda
    cerrada si todas sus partes lo estaban. Mueve las carpetas NN-etapa. Sin aplicar=True solo informa."""
    import subprocess
    produccion(con, pid)
    tareas = con.execute("SELECT * FROM tareas WHERE produccion_id=? ORDER BY etapa", (pid,)).fetchall()
    if len(tareas) == N_ETAPAS or migrada_13(con, pid):
        raise ErrorEstudio(f"{pid} ya usa el flujo de {N_ETAPAS} etapas.")
    if len(tareas) != 21:
        raise ErrorEstudio(f"{pid} tiene {len(tareas)} etapas; se esperaban 21.")
    grupos = {}
    for t in tareas:
        grupos.setdefault(MAPA_21_A_13[t["etapa"]], []).append(t)
    plan, movs = [], []
    for e in ETAPAS:
        partes = grupos[e.n]
        abiertas = [t for t in partes if t["estado"] != "cerrado"]
        estado = abiertas[0]["estado"] if abiertas else "cerrado"
        if abiertas and abiertas[0]["estado"] == "pendiente" and len(abiertas) < len(partes):
            estado = "en_curso"  # parte hecha y parte pendiente: la etapa nueva está en curso
        plan.append((e, partes, estado))
    raiz = RAIZ / "producciones" / pid
    for vieja, nombre in CARPETAS_21.items():
        o = raiz / nombre
        if o.is_dir():
            for f in sorted(x for x in o.rglob("*") if x.is_file()):
                d = raiz / CARPETAS[MAPA_21_A_13[vieja]] / f.relative_to(o)
                if d != f:
                    movs.append((f, d))
    destinos = [d for _, d in movs]
    if len(set(destinos)) != len(destinos) or any(d.exists() for d in destinos):
        raise ErrorEstudio("Dos archivos irían al mismo destino o el destino ya existe; renombre antes de migrar.")
    informe = [f"{e.n:>2} {e.nombre} ← antes {'+'.join(str(t['etapa']) for t in partes)}: {estado}"
               for e, partes, estado in plan]
    informe += [f"mover {f.relative_to(RAIZ)} → {d.relative_to(RAIZ)}" for f, d in movs]
    if not aplicar:
        return informe
    con.execute("UPDATE tareas SET etapa=etapa+100 WHERE produccion_id=?", (pid,))
    for e, partes, estado in plan:
        base, resto = partes[0], partes[1:]
        ents = []
        for t in partes:
            ents += [a for a in json.loads(t["entregables"]) if a not in ents]
        fechas = lambda c, f: f([t[c] for t in partes if t[c]], default=None)
        for t in resto:
            con.execute("UPDATE historial_tareas SET tarea_id=? WHERE tarea_id=?", (base["id"], t["id"]))
            con.execute("UPDATE artefactos SET tarea_id=? WHERE tarea_id=?", (base["id"], t["id"]))
            con.execute("DELETE FROM tareas WHERE id=?", (t["id"],))
        con.execute("UPDATE tareas SET etapa=?, nombre=?, responsable=?, puerta=?, estado=?, entregables=?,"
                    " iniciado=?, entregado=?, cerrado=? WHERE id=?",
                    (e.n, e.nombre, e.responsable, e.puerta, estado, json.dumps(ents), fechas("iniciado", min),
                     fechas("entregado", max) if estado == "cerrado" else None,
                     fechas("cerrado", max) if estado == "cerrado" else None, base["id"]))
    for vieja, nueva in MAPA_21_A_13.items():
        con.execute("UPDATE costos SET etapa=? WHERE produccion_id=? AND etapa=?", (nueva + 100, pid, vieja))
    con.execute("UPDATE costos SET etapa=etapa-100 WHERE produccion_id=? AND etapa>100", (pid,))
    actual = next((e.n for e, _, est in plan if est != "cerrado"), N_ETAPAS)
    con.execute("UPDATE producciones SET etapa_actual=? WHERE id=?", (actual, pid))
    for f, d in movs:
        viejo, nuevo = str(f.relative_to(RAIZ)), str(d.relative_to(RAIZ))
        d.parent.mkdir(parents=True, exist_ok=True)
        if subprocess.run(["git", "ls-files", "--error-unmatch", viejo], cwd=RAIZ, capture_output=True).returncode == 0:
            subprocess.run(["git", "mv", viejo, nuevo], cwd=RAIZ, check=True)
        else:
            f.rename(d)
        con.execute("UPDATE artefactos SET ruta=? WHERE ruta=?", (nuevo, viejo))
        con.execute("UPDATE recursos SET archivo=? WHERE archivo=?", (nuevo, viejo))
    for nombre in CARPETAS_21.values():
        o = raiz / nombre
        if o.is_dir() and not any(o.rglob("*")):
            for sub in sorted(o.rglob("*"), reverse=True):
                sub.rmdir()
            o.rmdir()
    registrar_decision(con, pid=pid, tipo="migracion_13_etapas", decidio="ceo",
                       descripcion=f"{pid} migrada del flujo de 21 etapas al de 13 (DEC-0014). Etapa actual: {actual}.",
                       justificacion="Aprobado por el Director: «Apruebo las 13 etapas, el título y la subida autónoma».",
                       commit=False)
    con.commit()
    escribir_indice(con, pid)
    return informe


# ---------------------------------------------------------------------------
# Índice y orden de archivos por etapa
# ---------------------------------------------------------------------------
def escribir_indice(con, pid) -> Path:
    """producciones/<ID>/README.md: índice de etapas, entregables y decisiones, generado desde la base."""
    p = produccion(con, pid)
    raiz = RAIZ / "producciones" / pid
    marca = {"humana": " 🔒", "auditoria": " 🔍", "presupuesto": " 💲"}
    arts = {}
    for a in con.execute("SELECT a.*, t.etapa FROM artefactos a JOIN tareas t ON t.id=a.tarea_id"
                         " WHERE a.produccion_id=? ORDER BY a.creado", (pid,)):
        arts.setdefault(a["etapa"], {})[a["ruta"]] = a  # una fila por archivo: su última versión
    decs, mig = {}, migrada_13(con, pid)
    for d in con.execute("SELECT * FROM decisiones WHERE produccion_id=? AND tipo LIKE 'aprobacion_etapa_%'", (pid,)):
        decs.setdefault(etapa_de_decision(d["tipo"], d["creado"], mig), []).append(d["id"])
    pref = f"producciones/{pid}/"
    lin = [f"# {pid} · {p['titulo']}", "",
           "_Índice generado desde la base de datos (`python3 -m estudio indice`). No editar a mano._", "",
           f"Estado: **{p['estado']}** · etapa actual **{p['etapa_actual']}** · "
           "[Cuaderno del Director](cuaderno_director.md)", "",
           "| Etapa | Carpeta | Responsable | Estado | Entregables | Decisión |", "|---|---|---|---|---|---|"]
    for t in con.execute("SELECT * FROM tareas WHERE produccion_id=? ORDER BY etapa", (pid,)):
        n = t["etapa"]
        ents = []
        for ruta, a in arts.get(n, {}).items():
            rel = ruta[len(pref):] if ruta.startswith(pref) else "../../" + ruta
            nombre = f"{a['tipo'].replace('_', ' ')} v{a['version']}"
            ents.append(f"[{nombre}]({rel.replace(' ', '%20')})" if (RAIZ / ruta).exists() or not
                        rel.startswith(("render/", "recursos/")) else f"{nombre} (`{rel}`, fuera de git)")
        carpeta = CARPETAS[n]
        enlace = f"[{carpeta}/]({carpeta}/)" if (raiz / carpeta).is_dir() else "—"
        lin.append(f"| {n}{marca.get(t['puerta'], '')} · {t['nombre']} | {enlace} | {t['responsable']} | {t['estado']} | "
                   f"{'<br>'.join(ents) or '—'} | {', '.join(decs.get(n, [])) or '—'} |")
    lin += ["", "`recursos/` (imágenes, audio) y `render/` (máster, subtítulos, miniaturas) quedan en la raíz "
            "de la producción y no se versionan (ver CLAUDE.md, sección de recursos pesados).", ""]
    raiz.mkdir(parents=True, exist_ok=True)
    salida = raiz / "README.md"
    salida.write_text("\n".join(lin), encoding="utf-8")
    return salida


def plan_reorganizacion(con, pid) -> dict:
    """Destino de cada entregable registrado que aún no está en su carpeta de etapa: la primera etapa que lo registró."""
    pref = f"producciones/{pid}/"
    mapa = {}
    for a in con.execute("SELECT a.ruta, MIN(t.etapa) AS etapa FROM artefactos a JOIN tareas t ON t.id=a.tarea_id"
                         " WHERE a.produccion_id=? GROUP BY a.ruta", (pid,)):
        rel = a["ruta"][len(pref):] if a["ruta"].startswith(pref) else None
        if not rel or rel.split("/")[0] in set(CARPETAS.values()) | {"recursos", "render"}:
            continue
        mapa[a["ruta"]] = f"{pref}{CARPETAS[a['etapa']]}/{Path(rel).name}"
    return mapa


def reorganizar(con, pid, mapa=None, aplicar=False) -> list:
    """Mueve entregables a producciones/<ID>/NN-etapa/ (git mv si están versionados) y actualiza las rutas
    en artefactos y recursos. Sin aplicar=True solo devuelve el plan."""
    import subprocess
    mapa = mapa if mapa is not None else plan_reorganizacion(con, pid)
    hechos = []
    for viejo, nuevo in mapa.items():
        o, d = RAIZ / viejo, RAIZ / nuevo
        if not o.exists():
            raise ErrorEstudio(f"No existe {viejo}.")
        if d.exists():
            raise ErrorEstudio(f"El destino {nuevo} ya existe.")
        hechos.append((viejo, nuevo))
        if not aplicar:
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        versionado = subprocess.run(["git", "ls-files", "--error-unmatch", viejo], cwd=RAIZ,
                                    capture_output=True).returncode == 0
        if versionado:
            subprocess.run(["git", "mv", viejo, nuevo], cwd=RAIZ, check=True)
        else:
            o.rename(d)
        con.execute("UPDATE artefactos SET ruta=? WHERE ruta=?", (nuevo, viejo))
        con.execute("UPDATE recursos SET archivo=? WHERE archivo=?", (nuevo, viejo))
    if aplicar:
        for vacia in sorted({(RAIZ / v).parent for v, _ in hechos}, reverse=True):
            if vacia != RAIZ / "producciones" / pid and vacia.is_dir() and not any(vacia.iterdir()):
                vacia.rmdir()
        con.commit()
        escribir_indice(con, pid)
    return hechos


# ---------------------------------------------------------------------------
# Artefactos y recursos
# ---------------------------------------------------------------------------
def registrar_artefacto(con, pid, tipo, ruta, autor, etapa=None):
    produccion(con, pid)
    ruta_abs = (RAIZ / ruta) if not Path(ruta).is_absolute() else Path(ruta)
    sha = hashlib.sha256(ruta_abs.read_bytes()).hexdigest() if ruta_abs.exists() else None
    version = con.execute("SELECT COUNT(*) FROM artefactos WHERE produccion_id=? AND tipo=?",
                          (pid, tipo)).fetchone()[0] + 1
    n = con.execute("SELECT COUNT(*) FROM artefactos WHERE produccion_id=?", (pid,)).fetchone()[0] + 1
    aid = f"{pid}-A{n:03d}"
    tid = tarea(con, pid, etapa)["id"] if etapa else None
    con.execute("INSERT INTO artefactos (id, produccion_id, tarea_id, tipo, ruta, version, sha256, autor, creado)"
                " VALUES (?,?,?,?,?,?,?,?,?)", (aid, pid, tid, tipo, str(ruta), version, sha, autor, ahora()))
    con.commit()
    return aid


def registrar_recurso(con, pid, tipo, origen, licencia, proveedor=None, url_fuente=None,
                      prompt=None, es_recreacion=False, archivo=None):
    produccion(con, pid)
    if origen == "ia" and not prompt:
        raise ErrorEstudio("Un recurso generado por IA debe registrar su prompt.")
    if origen == "ia" and tipo in ("imagen", "clip"):
        es_recreacion = True  # regla editorial: toda imagen/clip IA es recreación
    n = con.execute("SELECT COUNT(*) FROM recursos WHERE produccion_id=?", (pid,)).fetchone()[0] + 1
    rid = f"{pid}-R{n:04d}"
    con.execute("INSERT INTO recursos (id, produccion_id, tipo, origen, proveedor, licencia, url_fuente,"
                " prompt, es_recreacion, archivo, creado) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (rid, pid, tipo, origen, proveedor, licencia, url_fuente, prompt,
                 int(es_recreacion), archivo, ahora()))
    con.commit()
    return rid


# ---------------------------------------------------------------------------
# Cuaderno del Director y decisiones
# ---------------------------------------------------------------------------
TIPOS_APORTE = ("pregunta", "perspectiva", "objecion", "idea", "decision")


def registrar_aporte(con, texto, tipo, pid=None, slug_canal=None):
    if tipo not in TIPOS_APORTE:
        raise ErrorEstudio(f"Tipo de aporte inválido. Use: {', '.join(TIPOS_APORTE)}.")
    if pid:
        canal_id = produccion(con, pid)["canal_id"]
        base = f"DIR-{pid}"
    else:
        canal_id = canal(con, slug_canal)["id"]
        base = f"DIR-GENERAL-{canal(con, canal_id)['prefijo']}"
    n = con.execute("SELECT COUNT(*) FROM aportes WHERE id LIKE ?", (base + "-%",)).fetchone()[0] + 1
    aid = f"{base}-{n:02d}"
    con.execute("INSERT INTO aportes (id, canal_id, produccion_id, tipo, texto, creado) VALUES (?,?,?,?,?,?)",
                (aid, canal_id, pid, tipo, texto, ahora()))
    con.commit()
    if pid:
        cuaderno = RAIZ / "producciones" / pid / "cuaderno_director.md"
        if cuaderno.exists():
            with cuaderno.open("a", encoding="utf-8") as f:
                f.write(f"- **{aid}** · {tipo} · {ahora()[:10]}\n  > {texto}\n")
    return aid


def resolver_aporte(con, aporte_id, estado, resolucion, actor):
    if estado not in ("integrado", "descartado"):
        raise ErrorEstudio("Estado debe ser 'integrado' o 'descartado'.")
    if not resolucion or len(resolucion.strip()) < 10:
        raise ErrorEstudio("Debe indicar dónde se integró o por qué se descartó (mín. 10 caracteres).")
    cur = con.execute("UPDATE aportes SET estado=?, resolucion=?, resuelto_por=?, resuelto=? WHERE id=?",
                      (estado, resolucion, actor, ahora(), aporte_id))
    if cur.rowcount == 0:
        raise ErrorEstudio(f"Aporte {aporte_id} no existe.")
    con.commit()


def aportes_pendientes(con, pid):
    return con.execute("SELECT * FROM aportes WHERE produccion_id=? AND estado='pendiente'",
                       (pid,)).fetchall()


def _exigir_aportes_resueltos(con, pid):
    pend = aportes_pendientes(con, pid)
    if pend:
        ids = ", ".join(a["id"] for a in pend)
        raise ErrorEstudio(f"Hay aportes del Director sin resolver en {pid}: {ids}. "
                           "Cada uno debe integrarse o descartarse con justificación.")


def registrar_decision(con, descripcion, tipo, decidio, pid=None, slug_canal=None,
                       justificacion=None, commit=True):
    canal_id = produccion(con, pid)["canal_id"] if pid else (canal(con, slug_canal)["id"] if slug_canal else None)
    n = con.execute("SELECT COUNT(*) FROM decisiones").fetchone()[0] + 1
    did = f"DEC-{n:04d}"
    con.execute("INSERT INTO decisiones (id, canal_id, produccion_id, tipo, descripcion, decidio, justificacion, creado)"
                " VALUES (?,?,?,?,?,?,?,?)", (did, canal_id, pid, tipo, descripcion, decidio, justificacion, ahora()))
    if commit:
        con.commit()
    return did


# ---------------------------------------------------------------------------
# Finanzas (CFO): cálculo determinista
# ---------------------------------------------------------------------------
def agregar_tarifa(con, proveedor, producto, unidad, precio, vigente_desde, fuente=None):
    # cierra la tarifa vigente anterior del mismo producto/unidad
    con.execute("UPDATE tarifas SET vigente_hasta=? WHERE proveedor=? AND producto=? AND unidad=?"
                " AND vigente_hasta IS NULL AND vigente_desde < ?",
                (vigente_desde, proveedor, producto, unidad, vigente_desde))
    con.execute("INSERT INTO tarifas (proveedor, producto, unidad, precio_usd, vigente_desde, fuente)"
                " VALUES (?,?,?,?,?,?)", (proveedor, producto, unidad, precio, vigente_desde, fuente))
    con.commit()


def tarifa_vigente(con, proveedor, producto, unidad, fecha=None):
    fecha = (fecha or ahora())[:10]
    fila = con.execute(
        "SELECT * FROM tarifas WHERE proveedor=? AND producto=? AND unidad=? AND vigente_desde<=?"
        " AND (vigente_hasta IS NULL OR vigente_hasta>?) ORDER BY vigente_desde DESC LIMIT 1",
        (proveedor, producto, unidad, fecha, fecha)).fetchone()
    if not fila:
        raise ErrorEstudio(f"No hay tarifa vigente para {proveedor}/{producto}/{unidad}. "
                           "Regístrela en finanzas/tarifas.csv (nunca se asume que algo es gratis).")
    return fila


def gasto_produccion(con, pid):
    return con.execute("SELECT COALESCE(SUM(costo_usd),0) FROM v_costos_vigentes WHERE produccion_id=?",
                       (pid,)).fetchone()[0]


def gasto_mes(con, canal_id, mes):
    return con.execute("SELECT COALESCE(SUM(costo_usd),0) FROM v_costos_vigentes WHERE canal_id=?"
                       " AND substr(creado,1,7)=?", (canal_id, mes)).fetchone()[0]


def verificar_presupuesto(con, pid, estimado_usd):
    """Lo llaman los adaptadores ANTES de gastar. Devuelve (ok, mensaje)."""
    p = produccion(con, pid)
    if p["estado"] == "congelada":
        return False, f"{pid} está congelada por presupuesto."
    gastado = gasto_produccion(con, pid)
    if gastado + estimado_usd > p["presupuesto_usd"]:
        return False, (f"{pid}: gasto {gastado:.2f} + estimado {estimado_usd:.2f} supera el presupuesto "
                       f"{p['presupuesto_usd']:.2f}. Requiere ampliación del Director.")
    mes = ahora()[:7]
    tope_mes = presupuesto_mes(con, p["canal_id"], mes)
    gm = gasto_mes(con, p["canal_id"], mes)
    if gm + estimado_usd > tope_mes:
        return False, f"Tope mensual del canal ({tope_mes:.2f}) se superaría: gastado {gm:.2f}."
    return True, "ok"


def registrar_costo(con, pid, agente, proveedor, producto, id_externo, tipo_costo="estimado",
                    tokens_in=0, tokens_out=0, tokens_cache_w=0, tokens_cache_r=0,
                    unidades=0, unidad=None, costo_usd=None, etapa=None, short_id=None,
                    factura_id=None, modalidad="api"):
    """Registra un gasto. Si costo_usd es None se calcula con la tarifa vigente.
    modalidad='suscripcion' registra tokens con costo 0 (la cuota se prorratea aparte)."""
    if pid.startswith("GENERAL-"):
        prefijo = pid.split("-")[1]
        canal_id = con.execute("SELECT id FROM canales WHERE prefijo=?", (prefijo,)).fetchone()[0]
    else:
        canal_id = produccion(con, pid)["canal_id"]
    tarifa_ids = []
    if modalidad == "suscripcion":
        costo_usd, tipo_costo = 0.0, "suscripcion"
    elif costo_usd is None:
        costo_usd = 0.0
        for cantidad, u, div in ((tokens_in, "mtok_in", 1e6), (tokens_out, "mtok_out", 1e6),
                                 (tokens_cache_w, "mtok_cache_w", 1e6), (tokens_cache_r, "mtok_cache_r", 1e6),
                                 (unidades, unidad, 1)):
            if cantidad and u:
                t = tarifa_vigente(con, proveedor, producto, u)
                costo_usd += cantidad / div * t["precio_usd"]
                tarifa_ids.append(t["id"])
    hash_dedupe = hashlib.sha256(f"{proveedor}|{id_externo}|{tipo_costo}".encode()).hexdigest()
    try:
        cur = con.execute(
            "INSERT INTO costos (canal_id, produccion_id, short_id, agente, etapa, proveedor, producto,"
            " tokens_in, tokens_out, tokens_cache_w, tokens_cache_r, unidades, unidad, costo_usd,"
            " tipo_costo, tarifa_ids, id_externo, hash_dedupe, factura_id, creado)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (canal_id, pid, short_id, agente, etapa, proveedor, producto, tokens_in, tokens_out,
             tokens_cache_w, tokens_cache_r, unidades, unidad, round(costo_usd, 6), tipo_costo,
             json.dumps(tarifa_ids), id_externo, hash_dedupe, factura_id, ahora()))
    except sqlite3.IntegrityError:
        raise ErrorEstudio(f"Gasto duplicado ignorado: {proveedor}/{id_externo} ya está registrado.")
    con.commit()
    if not pid.startswith("GENERAL-"):
        _evaluar_alertas(con, pid)
    return cur.lastrowid, costo_usd


def conciliar(con, costo_id, costo_real, factura_id):
    """El costo real (factura) REEMPLAZA al estimado: el estimado se anula, nunca se suman."""
    est = con.execute("SELECT * FROM costos WHERE id=? AND anulado=0", (costo_id,)).fetchone()
    if not est or est["tipo_costo"] != "estimado":
        raise ErrorEstudio("Solo se concilian costos estimados vigentes.")
    con.execute("UPDATE costos SET anulado=1 WHERE id=?", (costo_id,))
    hash_dedupe = hashlib.sha256(f"{est['proveedor']}|{est['id_externo']}|real".encode()).hexdigest()
    con.execute(
        "INSERT INTO costos (canal_id, produccion_id, short_id, agente, etapa, proveedor, producto,"
        " tokens_in, tokens_out, tokens_cache_w, tokens_cache_r, unidades, unidad, costo_usd, tipo_costo,"
        " tarifa_ids, id_externo, hash_dedupe, factura_id, reemplaza_id, creado)"
        " SELECT canal_id, produccion_id, short_id, agente, etapa, proveedor, producto, tokens_in, tokens_out,"
        " tokens_cache_w, tokens_cache_r, unidades, unidad, ?, 'real', tarifa_ids, id_externo, ?, ?, id, ?"
        " FROM costos WHERE id=?", (costo_real, hash_dedupe, factura_id, ahora(), costo_id))
    con.commit()


def prorratear_suscripcion(con, slug_canal, mes, proveedor, producto, monto_usd):
    """Reparte una cuota fija mensual entre las producciones del mes, ponderado por tokens
    (o a partes iguales si no hay tokens). Idempotente: una sola vez por canal/mes/proveedor."""
    c = canal(con, slug_canal)
    filas = con.execute(
        "SELECT produccion_id, SUM(tokens_in+tokens_out+tokens_cache_w+tokens_cache_r) tok FROM v_costos_vigentes"
        " WHERE canal_id=? AND substr(creado,1,7)=? AND produccion_id NOT LIKE 'GENERAL-%'"
        " GROUP BY produccion_id", (c["id"], mes)).fetchall()
    destino = [(f["produccion_id"], f["tok"] or 0) for f in filas]
    if not destino:
        destino = [(f"GENERAL-{c['prefijo']}-{mes}", 1)]
    total = sum(t for _, t in destino) or len(destino)
    for pid, tok in destino:
        peso = (tok / total) if total else 1 / len(destino)
        try:
            registrar_costo(con, pid, "cfo", proveedor, producto,
                            id_externo=f"prorrateo:{c['prefijo']}:{mes}:{proveedor}:{producto}:{pid}",
                            tipo_costo="prorrateado", costo_usd=monto_usd * (peso if total else 1 / len(destino)),
                            unidades=1, unidad="mes")
        except ErrorEstudio:
            pass  # ya prorrateado ese mes: idempotente
    return destino


def crear_alerta(con, canal_id, pid, nivel, mensaje):
    ya = con.execute("SELECT 1 FROM alertas WHERE produccion_id IS ? AND mensaje=? AND resuelta=0",
                     (pid, mensaje)).fetchone()
    if not ya:
        con.execute("INSERT INTO alertas (canal_id, produccion_id, nivel, mensaje, creado) VALUES (?,?,?,?,?)",
                    (canal_id, pid, nivel, mensaje, ahora()))
        con.commit()


def _evaluar_alertas(con, pid):
    p = produccion(con, pid)
    c = canal(con, p["canal_id"])
    gastado = gasto_produccion(con, pid)
    ratio = gastado / p["presupuesto_usd"] if p["presupuesto_usd"] else 1
    if ratio >= 1:
        con.execute("UPDATE producciones SET estado='congelada' WHERE id=?", (pid,))
        crear_alerta(con, c["id"], pid, "bloqueo",
                     f"{pid} alcanzó el 100 % de su presupuesto ({gastado:.2f}/{p['presupuesto_usd']:.2f} USD). Congelada.")
    elif ratio >= c["umbral_alerta"]:
        crear_alerta(con, c["id"], pid, "aviso",
                     f"{pid} superó el {int(c['umbral_alerta']*100)} % de su presupuesto ({gastado:.2f}/{p['presupuesto_usd']:.2f} USD).")
    mes = ahora()[:7]
    gm, tm = gasto_mes(con, c["id"], mes), presupuesto_mes(con, c["id"], mes)
    if gm >= 0.9 * tm:
        crear_alerta(con, c["id"], None, "aviso", f"Canal {c['slug']}: gasto del mes {mes} al {gm/tm:.0%} del tope ({tm:.2f} USD).")
    con.commit()


def ampliar_presupuesto(con, pid, nuevo_monto, justificacion, director=False):
    if not director:
        raise ErrorEstudio("Solo el Director puede ampliar un presupuesto (presupuesto extraordinario).")
    p = produccion(con, pid)
    con.execute("UPDATE producciones SET presupuesto_usd=?, estado=CASE WHEN estado='congelada' THEN 'activa' ELSE estado END"
                " WHERE id=?", (nuevo_monto, pid))
    con.execute("UPDATE alertas SET resuelta=1 WHERE produccion_id=? AND nivel='bloqueo'", (pid,))
    registrar_decision(con, f"Presupuesto de {pid}: {p['presupuesto_usd']:.2f} → {nuevo_monto:.2f} USD",
                       "presupuesto", "director", pid=pid, justificacion=justificacion, commit=False)
    con.commit()


def informe_video(con, pid) -> str:
    p = produccion(con, pid)
    q = lambda sql: con.execute(sql, (pid,)).fetchall()  # noqa: E731
    total = gasto_produccion(con, pid)
    por_agente = q("SELECT agente, SUM(costo_usd) c, SUM(tokens_in) ti, SUM(tokens_out) tout,"
                   " SUM(tokens_cache_r) tcr FROM v_costos_vigentes WHERE produccion_id=? GROUP BY agente ORDER BY c DESC")
    por_prov = q("SELECT proveedor, producto, SUM(costo_usd) c FROM v_costos_vigentes WHERE produccion_id=?"
                 " GROUP BY proveedor, producto ORDER BY c DESC")
    por_tipo = q("SELECT tipo_costo, SUM(costo_usd) c FROM v_costos_vigentes WHERE produccion_id=? GROUP BY tipo_costo")
    shorts = con.execute("SELECT COALESCE(SUM(costo_usd),0) FROM v_costos_vigentes WHERE produccion_id=?"
                         " AND short_id IS NOT NULL", (pid,)).fetchone()[0]
    inv = con.execute("SELECT COALESCE(SUM(costo_usd),0) FROM v_costos_vigentes WHERE produccion_id=?"
                      " AND agente='investigador'", (pid,)).fetchone()[0]
    av = con.execute("SELECT COALESCE(SUM(costo_usd),0) FROM v_costos_vigentes WHERE produccion_id=?"
                     " AND agente='productor'", (pid,)).fetchone()[0]
    dur = p["duracion_s"]
    por_min = f"{total / (dur / 60):.2f} USD" if dur else "— (duración no registrada)"
    desv = total - p["presupuesto_usd"]
    tok = sum((r["ti"] or 0) + (r["tout"] or 0) for r in por_agente)
    l = [f"# Informe financiero — {pid}", "", f"**Título:** {p['titulo']}  ",
         f"**Duración:** {dur // 60 if dur else '—'} min  ", f"**Tokens (entrada+salida):** {tok:,}  ",
         f"**Costo total:** {total:.2f} USD  ", f"**Costo por minuto terminado:** {por_min}  ",
         f"**Investigación:** {inv:.2f} USD · **Generación audiovisual:** {av:.2f} USD · **Shorts:** {shorts:.2f} USD  ",
         f"**Presupuesto:** {p['presupuesto_usd']:.2f} USD · **Desviación:** {desv:+.2f} USD "
         f"({(desv / p['presupuesto_usd'] * 100) if p['presupuesto_usd'] else 0:+.1f} %)", "",
         "## Por agente", "| Agente | Tokens in | Tokens out | Cache leídos | USD |", "|---|---|---|---|---|"]
    l += [f"| {r['agente']} | {r['ti'] or 0:,} | {r['tout'] or 0:,} | {r['tcr'] or 0:,} | {r['c']:.2f} |" for r in por_agente]
    l += ["", "## Por proveedor", "| Proveedor | Producto | USD |", "|---|---|---|"]
    l += [f"| {r['proveedor']} | {r['producto']} | {r['c']:.2f} |" for r in por_prov]
    eq = valor_api_equivalente(con, pid)
    if eq:
        l += ["", f"**Uso de Claude (plan de suscripción):** valor equivalente en API ≈ {eq:.2f} USD "
              "(referencia; no es un cargo real: el plan es una cuota fija)."]
    l += ["", "## Por tipo de costo", "| Tipo | USD |", "|---|---|"]
    l += [f"| {r['tipo_costo']} | {r['c']:.2f} |" for r in por_tipo]
    return "\n".join(l) + "\n"


# ---------------------------------------------------------------------------
# Consumo del plan de Claude (suscripción): tokens reales de los registros de sesión
# ---------------------------------------------------------------------------
LOGS_CLAUDE = Path.home() / ".claude" / "projects"


def _agente_de_registro(f):
    """Nombre del agente dueño de un registro de sesión. Los subagentes guardan su transcripción en
    `<sesión>/subagents/agent-<id>.jsonl`, con un `agent-<id>.meta.json` al lado que indica su tipo."""
    if f.parent.name != "subagents":
        return "claude-code"
    meta = f.with_name(f.stem + ".meta.json")
    try:
        d = json.loads(meta.read_text(encoding="utf-8"))
        tipo = d.get("agentType") or d.get("subagent_type") or d.get("agent_type")
        if tipo:
            return str(tipo)
    except (OSError, ValueError, AttributeError):
        pass
    return "subagente"


def _mensajes_con_uso(d):
    """Respuestas con uso de tokens dentro de una línea del registro. Además de la respuesta propia
    de la línea, algunas versiones incrustan las respuestas de un subagente en eventos de progreso
    (`data.message.message`) del registro principal."""
    m = d.get("message")
    if isinstance(m, dict):
        yield m, d.get("timestamp")
    datos = d.get("data")
    if isinstance(datos, dict) and isinstance(datos.get("message"), dict):
        anidado = datos["message"]
        mm = anidado.get("message")
        if isinstance(mm, dict):
            yield mm, anidado.get("timestamp") or d.get("timestamp")


def importar_consumo_claude(con, slug_canal, pid=None, desde=None, hasta=None, logs=None):
    """Lee los registros de sesión de Claude Code (JSONL) —los de la sesión principal y los de sus
    subagentes— y registra el uso de tokens de cada respuesta como costo 'suscripcion' (0 USD; la
    cuota se prorratea aparte). Cada respuesta se identifica por su ID de mensaje: importar dos
    veces no duplica nada. El campo `agente` distingue la sesión principal de cada subagente.
    Atribución: a `pid` las respuestas entre `desde` y `hasta`; si no hay pid, a GENERAL del mes."""
    c = canal(con, slug_canal)
    # Búsqueda recursiva: los subagentes escriben en <proyecto>/<sesión>/subagents/*.jsonl
    archivos = sorted(Path(logs or LOGS_CLAUDE).glob("**/*.jsonl"))
    # Una misma respuesta aparece en varias líneas (una por bloque de contenido) con el uso
    # repetido o parcial: se agrupa por ID de mensaje y se toma el máximo de cada contador.
    campos = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
    msgs = {}
    for f in archivos:
        agente_archivo = _agente_de_registro(f)
        with f.open(encoding="utf-8") as fh:
            for linea in fh:
                try:
                    d = json.loads(linea)
                except json.JSONDecodeError:
                    continue
                if not isinstance(d, dict):
                    continue
                for m, ts in _mensajes_con_uso(d):
                    if not isinstance(m.get("usage"), dict) or not m.get("id"):
                        continue
                    u, prev = m["usage"], msgs.get(m["id"]) or {}
                    vals = {k: max(u.get(k, 0) or 0, prev.get(k, 0)) for k in campos}
                    vals["ts"] = min(ts or "~", prev.get("ts", "~"))
                    vals["model"] = m.get("model") or prev.get("model") or "desconocido"
                    # una respuesta incrustada en el registro principal es de un subagente
                    es_anidado = m is not d.get("message")
                    agente = "subagente" if es_anidado and agente_archivo == "claude-code" else agente_archivo
                    # si la respuesta aparece en varios archivos, gana la etiqueta más específica
                    rango = lambda a: {None: 0, "claude-code": 1, "subagente": 2}.get(a, 3)  # noqa: E731
                    vals["agente"] = max(agente, prev.get("agente"), key=rango)
                    msgs[m["id"]] = vals
    nuevas = dup = 0
    for mid, v in msgs.items():
        ts = v["ts"]
        if (desde and ts < desde) or (hasta and ts >= hasta):
            continue
        destino = pid or f"GENERAL-{c['prefijo']}-{ts[:7]}"
        try:
            registrar_costo(con, destino, v["agente"], "anthropic", v["model"], id_externo=mid,
                            modalidad="suscripcion", tokens_in=v["input_tokens"], tokens_out=v["output_tokens"],
                            tokens_cache_w=v["cache_creation_input_tokens"], tokens_cache_r=v["cache_read_input_tokens"])
            nuevas += 1
        except ErrorEstudio:
            dup += 1
    return nuevas, dup


def valor_api_equivalente(con, pid):
    """Lo que habrían costado los tokens de suscripción con tarifas de API (referencia de eficiencia)."""
    total = 0.0
    for r in con.execute("SELECT producto, SUM(tokens_in) ti, SUM(tokens_out) tout, SUM(tokens_cache_w) tw,"
                         " SUM(tokens_cache_r) tr FROM v_costos_vigentes WHERE produccion_id=? AND tipo_costo='suscripcion'"
                         " AND proveedor='anthropic' GROUP BY producto", (pid,)):
        for cant, u in ((r["ti"], "mtok_in"), (r["tout"], "mtok_out"), (r["tw"], "mtok_cache_w"), (r["tr"], "mtok_cache_r")):
            if cant:
                try:
                    total += cant / 1e6 * tarifa_vigente(con, "anthropic", r["producto"], u)["precio_usd"]
                except ErrorEstudio:
                    pass
    return total


def consumo_plan(con, slug_canal, mes, cuota_usd):
    """Reparto de la cuota mensual del plan entre producciones según sus tokens del mes."""
    c = canal(con, slug_canal)
    filas = con.execute(
        "SELECT produccion_id, SUM(tokens_in+tokens_out+tokens_cache_w) tok, SUM(tokens_cache_r) tcr"
        " FROM v_costos_vigentes WHERE canal_id=? AND tipo_costo='suscripcion' AND substr(creado,1,7)=?"
        " GROUP BY produccion_id", (c["id"], mes)).fetchall()
    # ponderación: tokens nuevos completos + lecturas de caché al 10 % (aprox. su peso relativo en el plan)
    pesos = {f["produccion_id"]: (f["tok"] or 0) + 0.1 * (f["tcr"] or 0) for f in filas}
    total = sum(pesos.values()) or 1
    return [(pid, peso / total, cuota_usd * peso / total) for pid, peso in sorted(pesos.items(), key=lambda x: -x[1])]


def cargar_tarifas_csv(con, ruta):
    import csv
    with open(ruta, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            existe = con.execute("SELECT 1 FROM tarifas WHERE proveedor=? AND producto=? AND unidad=? AND vigente_desde=?",
                                 (fila["proveedor"], fila["producto"], fila["unidad"], fila["vigente_desde"])).fetchone()
            if not existe:
                agregar_tarifa(con, fila["proveedor"], fila["producto"], fila["unidad"],
                               float(fila["precio_usd"]), fila["vigente_desde"], fila.get("fuente"))
