"""Shorts verticales (9:16) a partir del máster: cada Short es un tramo de párrafos completos de la narración
con arco propio (pregunta → giro → revelación), un título arriba y subtítulos grandes quemados.

Uso:
    python3 scripts/shorts.py producciones/<ID>/09-edicion/shorts.json
shorts.json: {"shorts": [{"id": "S1", "titulo": "…", "seccion": 1, "pares": [0, 2], "cierre": "…"}]}
`pares` son índices de párrafo dentro de la sección (0 = primero), tal como los numera recursos/audio/tiempos.json.
Produce render/shorts/<ID>-S1.mp4 (1080×1920, 30 fps, H.264 + AAC) y su .srt. Sin servicios de pago.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SERIF = RAIZ / "canales/palimpsesto/fuentes/CormorantGaramond[wght].ttf"
SANS_B = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
MARGEN = 0.25  # s antes y después del tramo de voz
MIN_S, MAX_S = 20, 60


def hms(t):
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def frases(texto, max_c=34):
    """Corta un párrafo en trozos cortos para subtítulos verticales (≤ max_c caracteres)."""
    out, linea = [], ""
    for pal in texto.split():
        if linea and len(linea) + 1 + len(pal) > max_c:
            out.append(linea)
            linea = pal
        else:
            linea = f"{linea} {pal}".strip()
    return out + ([linea] if linea else [])


def srt_tramo(pars, t0):
    """Subtítulos del tramo: cada párrafo se reparte en trozos proporcionales a su número de caracteres."""
    bloques, k = [], 1
    for p in pars:
        trozos = frases(p["texto"])
        total = sum(len(x) for x in trozos)
        t = p["ini"] - t0
        for x in trozos:
            d = (p["fin"] - p["ini"]) * len(x) / total
            bloques.append(f"{k}\n{hms(t)} --> {hms(t + d)}\n{x}\n")
            t += d
            k += 1
    return "\n".join(bloques)


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


def main(plan_json):
    plan_json = Path(plan_json).resolve()
    pdir = plan_json.parent.parent if re.match(r"\d\d-", plan_json.parent.name) else plan_json.parent
    plan = json.loads(plan_json.read_text(encoding="utf-8"))
    montaje = json.loads((plan_json.parent / "montaje.json").read_text(encoding="utf-8"))
    tiempos = json.loads((pdir / "recursos/audio/tiempos.json").read_text(encoding="utf-8"))
    master = pdir / "render/master.mp4"
    salida = pdir / "render/shorts"
    salida.mkdir(parents=True, exist_ok=True)
    pid = pdir.name
    for s in plan["shorts"]:
        sec = [t for t in tiempos if t["seccion"] == s["seccion"]]
        pars = sec[s["pares"][0]: s["pares"][1] + 1]
        ini = pars[0]["ini"] + montaje["entrada"] - MARGEN
        fin = pars[-1]["fin"] + montaje["entrada"] + MARGEN
        dur = fin - ini
        if not MIN_S <= dur <= MAX_S:
            raise SystemExit(f"{s['id']}: dura {dur:.1f} s; debe estar entre {MIN_S} y {MAX_S} s.")
        nombre = f"{pid}-{s['id']}"
        srt = salida / f"{nombre}.srt"
        srt.write_text(srt_tramo([{**p, "ini": p["ini"] + montaje["entrada"], "fin": p["fin"] + montaje["entrada"]}
                                  for p in pars], ini), encoding="utf-8")
        estilo = ("FontName=Inter SemiBold,FontSize=13,PrimaryColour=&H00F0E6D9,OutlineColour=&H000D0B0B,"
                  "BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=70")
        filtro = (
            f"[0:v]split=2[a][b];"
            f"[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.18[fondo];"
            f"[b]scale=1080:-2[frente];"
            f"[fondo][frente]overlay=0:(H-h)/2,"
            f"drawtext=fontfile='{SERIF}':text='{esc(s['titulo'])}':fontsize=72:fontcolor=0xE6DDCB:"
            f"x=(w-text_w)/2:y=300:box=0,"
            f"drawtext=fontfile='{SANS_B}':text='PALIMPSESTO':fontsize=34:fontcolor=0x9E2B25:x=(w-text_w)/2:y=220,"
            f"drawtext=fontfile='{SANS_B}':text='{esc(s.get('cierre', 'Episodio completo en el canal'))}':"
            f"fontsize=36:fontcolor=0xA39A89:x=(w-text_w)/2:y=h-170:enable='gte(t,{dur - 4:.2f})',"
            f"subtitles='{srt}':force_style='{estilo}',fps=30[v]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ini:.3f}", "-t", f"{dur:.3f}", "-i", str(master),
                        "-filter_complex", filtro, "-map", "[v]", "-map", "0:a",
                        "-af", f"afade=t=in:d=0.15,afade=t=out:st={dur - 0.4:.2f}:d=0.4",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(salida / f"{nombre}.mp4")],
                       check=True)
        print(f"✔ {nombre}: {dur:.1f} s · {s['titulo']}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
