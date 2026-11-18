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


class ErrorEstudio(Exception):
    """Error de regla de negocio (mensaje legible para el Director y los agentes)."""


def ahora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def conectar(ruta: str | os.PathLike | None = None) -> sqlite3.Connection:
    ruta = Path(ruta or os.environ.get("ESTUDIO_DB", DB_POR_DEFECTO))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(ruta)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA.read_text(encoding="utf-8"))
    return con


# ---------------------------------------------------------------------------
# Flujo de producción: 21 etapas
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Etapa:
    n: int
    nombre: str
    responsable: str
    puerta: str = "ninguna"  # ninguna | humana | auditoria | presupuesto


ETAPAS: list[Etapa] = [
    Etapa(1, "Investigación de oportunidades", "investigador"),
    Etapa(2, "Presentación de temas al CEO", "ceo"),
    Etapa(3, "Selección del tema", "director", "humana"),
    Etapa(4, "Propuesta de tres perspectivas narrativas", "investigador"),
    Etapa(5, "Observaciones editoriales del Director", "director"),
    Etapa(6, "Aprobación de la perspectiva", "director", "humana"),
    Etapa(7, "Investigación profunda", "investigador"),
    Etapa(8, "Expediente de fuentes", "investigador", "auditoria"),
    Etapa(9, "Escritura del guion", "guionista"),
    Etapa(10, "Storyboard", "productor"),
    Etapa(11, "Generación de prompts", "productor"),
    Etapa(12, "Producción audiovisual", "productor", "presupuesto"),
    Etapa(13, "Edición", "editor"),
    Etapa(14, "Auditoría independiente", "auditor", "auditoria"),
    Etapa(15, "Correcciones", "ceo"),
    Etapa(16, "Aprobación humana del video", "director", "humana"),
    Etapa(17, "Publicación", "director", "humana"),
    Etapa(18, "Creación y distribución de Shorts", "editor", "humana"),
    Etapa(19, "Análisis de métricas", "analista"),
    Etapa(20, "Informe financiero", "cfo"),
    Etapa(21, "Retroalimentación al sistema", "ceo"),
]
ETAPA = {e.n: e for e in ETAPAS}
ETAPAS_QUE_EXIGEN_APORTES_RESUELTOS = {9, 16}
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
    if etapa == 16 and resultado == "aprobado":
        _exigir_aportes_resueltos(con, pid)
    _cambiar_estado(con, t, resultado, actor, nota)
    if resultado == "aprobado":
        _cambiar_estado(con, tarea(con, pid, etapa), "cerrado", actor)
        if etapa == 14:
            t15 = tarea(con, pid, 15)
            if t15["estado"] == "pendiente":
                for s in ("en_curso", "entregado", "cerrado"):
                    _cambiar_estado(con, tarea(con, pid, 15), s, "sistema",
                                    "sin correcciones pendientes" if s == "cerrado" else None)
        if e.puerta == "humana":
            registrar_decision(con, pid=pid, tipo=f"aprobacion_etapa_{etapa}",
                               descripcion=f"Aprobada etapa {etapa}: {e.nombre}",
                               decidio="director", justificacion=nota, commit=False)
    elif etapa == 14:
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
    l += ["", "## Por tipo de costo", "| Tipo | USD |", "|---|---|"]
    l += [f"| {r['tipo_costo']} | {r['c']:.2f} |" for r in por_tipo]
    return "\n".join(l) + "\n"


def cargar_tarifas_csv(con, ruta):
    import csv
    with open(ruta, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            existe = con.execute("SELECT 1 FROM tarifas WHERE proveedor=? AND producto=? AND unidad=? AND vigente_desde=?",
                                 (fila["proveedor"], fila["producto"], fila["unidad"], fila["vigente_desde"])).fetchone()
            if not existe:
                agregar_tarifa(con, fila["proveedor"], fila["producto"], fila["unidad"],
                               float(fila["precio_usd"]), fila["vigente_desde"], fila.get("fuente"))
