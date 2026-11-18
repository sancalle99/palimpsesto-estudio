"""Subida a YouTube del Editor (DEC-0016): subir en PRIVADO, y publicar o programar solo con la orden del Director.

Uso:
    python3 scripts/youtube_subir.py subir <ID> <master.mp4> <metadatos.md> [--miniatura img.jpg] [--etapa 9]
    python3 scripts/youtube_subir.py publicar <ID> <video_id>
    python3 scripts/youtube_subir.py programar <ID> <video_id> <fecha ISO 8601 con zona, p. ej. 2026-12-01T19:00:00-05:00>
    python3 scripts/youtube_subir.py comprobar               # dice qué credenciales faltan (sin mostrarlas)

Reglas que el script hace cumplir:
  * `subir` siempre usa privacyStatus=private. No existe opción para subir en público.
  * `publicar` y `programar` se niegan si la base no tiene `APRUEBO <ID> 12` registrado por el hook
    (decisión aprobacion_etapa_12 del Director, en el flujo de 13 etapas).
  * Las credenciales (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN) se leen del entorno o de `.env`
    (fuera de git). Nunca se imprimen. Se configuran en la Fase 7 (ver docs/decisiones.md, DEC-0016).

Limitación de Google: mientras el proyecto de la API no pase la auditoría de YouTube Data API, los vídeos
subidos por API quedan bloqueados en privado; el Director publica subiendo una copia a mano.
Solo usa la biblioteca estándar (urllib).
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from estudio import core  # noqa: E402

TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
CLAVES = ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")
CATEGORIAS = {"educación": "27", "educacion": "27", "ciencia y tecnología": "28", "entretenimiento": "24"}


class ErrorSubida(Exception):
    pass


def credenciales() -> dict:
    vals = {k: os.environ.get(k) for k in CLAVES}
    env = RAIZ / ".env"
    if env.exists():
        for linea in env.read_text(encoding="utf-8").splitlines():
            k, _, v = linea.partition("=")
            if k.strip() in CLAVES and not vals.get(k.strip()):
                vals[k.strip()] = v.strip().strip('"').strip("'")
    faltan = [k for k, v in vals.items() if not v]
    if faltan:
        raise ErrorSubida(f"Faltan credenciales de YouTube: {', '.join(faltan)}. Configúrelas en la Fase 7 "
                          "(.env o gestor de secretos); nunca en el chat ni en git.")
    return vals


def _pedir(url, datos=None, metodo=None, cabeceras=None, token=None):
    cab = dict(cabeceras or {})
    if token:
        cab["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=datos, method=metodo, headers=cab)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")[:500]
        raise ErrorSubida(f"YouTube respondió {e.code}: {cuerpo}") from None


def token_acceso() -> str:
    c = credenciales()
    datos = urllib.parse.urlencode({"client_id": c["YT_CLIENT_ID"], "client_secret": c["YT_CLIENT_SECRET"],
                                    "refresh_token": c["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    _, _, cuerpo = _pedir(TOKEN_URL, datos, "POST", {"Content-Type": "application/x-www-form-urlencoded"})
    return json.loads(cuerpo)["access_token"]


def leer_metadatos(ruta: Path) -> dict:
    """Lee metadatos.md del Editor: la tabla (Título, Categoría, Etiquetas, Contenido sintético) y el bloque
    de código bajo '## Descripción'. El título definitivo es la primera fila que empieza por 'Título'."""
    texto = ruta.read_text(encoding="utf-8")
    filas = {}
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$", texto, re.M):
        filas.setdefault(m.group(1), m.group(2))
    campo = lambda pref: next((v for k, v in filas.items() if k.lower().startswith(pref)), "")
    titulo = re.sub(r"[*`]", "", campo("título")).strip()
    if not titulo or len(titulo) > 100:
        raise ErrorSubida("metadatos.md: falta el título o supera 100 caracteres.")
    desc = re.search(r"^## Descripción\s*```\w*\n(.*?)```", texto, re.S | re.M)
    if not desc:
        raise ErrorSubida("metadatos.md: falta el bloque de código bajo '## Descripción'.")
    etiquetas = [t.strip() for t in re.sub(r"[*`]", "", campo("etiquetas")).split(",") if t.strip()]
    sintetico = campo("contenido alterado").lower()
    return {"titulo": titulo, "descripcion": desc.group(1).strip()[:5000], "etiquetas": etiquetas,
            "categoria": CATEGORIAS.get(re.sub(r"[*`]", "", campo("categoría")).strip().lower(), "27"),
            "sintetico": sintetico.startswith(("**sí", "sí", "**si", "si"))}


def cuerpo_subida(meta: dict) -> dict:
    return {"snippet": {"title": meta["titulo"], "description": meta["descripcion"], "tags": meta["etiquetas"],
                        "categoryId": meta["categoria"], "defaultLanguage": "es", "defaultAudioLanguage": "es"},
            "status": {"privacyStatus": "private",  # siempre privado (regla 2)
                       "selfDeclaredMadeForKids": False, "containsSyntheticMedia": meta["sintetico"]}}


def subir(pid, master: Path, metadatos: Path, miniatura: Path | None, etapa: int) -> str:
    con = core.conectar()
    core.produccion(con, pid)
    meta = leer_metadatos(metadatos)
    token = token_acceso()
    cuerpo = json.dumps(cuerpo_subida(meta)).encode()
    _, cab, _ = _pedir(f"{UPLOAD}/videos?uploadType=resumable&part=snippet,status", cuerpo, "POST",
                       {"Content-Type": "application/json; charset=UTF-8", "X-Upload-Content-Type": "video/*",
                        "X-Upload-Content-Length": str(master.stat().st_size)}, token)
    destino = cab.get("Location") or cab.get("location")
    _, _, resp = _pedir(destino, master.read_bytes(), "PUT", {"Content-Type": "video/*"}, token)
    vid = json.loads(resp)["id"]
    if miniatura:
        tipo = mimetypes.guess_type(miniatura.name)[0] or "image/jpeg"
        _pedir(f"{UPLOAD}/thumbnails/set?videoId={vid}", miniatura.read_bytes(), "POST", {"Content-Type": tipo}, token)
    registro = core.carpeta_etapa(pid, etapa) / "youtube.json"
    registro.write_text(json.dumps({"video_id": vid, "privacidad": "private", "titulo": meta["titulo"],
                                    "subido": core.ahora()}, ensure_ascii=False, indent=2), encoding="utf-8")
    aid = core.registrar_artefacto(con, pid, "youtube_video", str(registro.relative_to(RAIZ)), "editor", etapa)
    return f"✔ Subido en PRIVADO: video_id {vid} · artefacto {aid}"


def orden_del_director(con, pid) -> str:
    """ID de la decisión APRUEBO <ID> 12 (flujo de 13 etapas) o error si no existe."""
    mig = core.migrada_13(con, pid)
    for d in con.execute("SELECT * FROM decisiones WHERE produccion_id=? AND decidio='director'"
                         " AND tipo='aprobacion_etapa_12' ORDER BY creado", (pid,)):
        if core.etapa_de_decision(d["tipo"], d["creado"], mig) == 12:
            return d["id"]
    raise ErrorSubida(f"No hay orden de publicación del Director (APRUEBO {pid} 12). No se publica nada.")


def cambiar_estado(pid, vid, publish_at=None) -> str:
    con = core.conectar()
    dec = orden_del_director(con, pid)
    status = {"privacyStatus": "private", "publishAt": publish_at} if publish_at else {"privacyStatus": "public"}
    status["selfDeclaredMadeForKids"] = False
    token = token_acceso()
    _pedir(f"{API}/videos?part=status", json.dumps({"id": vid, "status": status}).encode(), "PUT",
           {"Content-Type": "application/json; charset=UTF-8"}, token)
    accion = f"programado para {publish_at}" if publish_at else "publicado"
    registro = core.carpeta_etapa(pid, 12) / "publicacion.json"
    registro.write_text(json.dumps({"video_id": vid, "accion": accion, "orden": dec, "hecho": core.ahora()},
                                   ensure_ascii=False, indent=2), encoding="utf-8")
    aid = core.registrar_artefacto(con, pid, "publicacion", str(registro.relative_to(RAIZ)), "editor", 12)
    return f"✔ Vídeo {vid} {accion} por orden {dec} · artefacto {aid}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("subir"); s.add_argument("pid"); s.add_argument("master", type=Path)
    s.add_argument("metadatos", type=Path); s.add_argument("--miniatura", type=Path); s.add_argument("--etapa", type=int, default=9)
    s = sub.add_parser("publicar"); s.add_argument("pid"); s.add_argument("video_id")
    s = sub.add_parser("programar"); s.add_argument("pid"); s.add_argument("video_id"); s.add_argument("fecha")
    sub.add_parser("comprobar")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "comprobar":
            credenciales()
            print("✔ Credenciales de YouTube presentes (no se muestran).")
        elif a.cmd == "subir":
            print(subir(a.pid, a.master, a.metadatos, a.miniatura, a.etapa))
        elif a.cmd == "publicar":
            print(cambiar_estado(a.pid, a.video_id))
        else:
            if not re.match(r"^\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d)?(Z|[+-]\d\d:\d\d)$", a.fecha):
                raise ErrorSubida("Fecha inválida: use ISO 8601 con zona, p. ej. 2026-12-01T19:00:00-05:00.")
            print(cambiar_estado(a.pid, a.video_id, a.fecha))
    except (ErrorSubida, core.ErrorEstudio) as e:
        print(f"✖ {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
