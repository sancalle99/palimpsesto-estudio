"""Shorts verticales nativos (9:16): cada Short tiene su propio texto (con una frase de entrada que lo hace
entendible sin el episodio, HAL-02), su propia narración con la voz del canal y planos compuestos en vertical
(HAL-09). Reutiliza el motor de scripts/montaje.py.

Uso:
    python3 scripts/shorts.py producciones/<ID>/09-edicion/shorts.json [S2,S4]
shorts.json: {"shorts": [{"id": "S1", "titulo": "…", "parrafos": ["…"], "planos": [{"par": 0, "tipo": "img", …}]}]}
Los planos usan el mismo formato que montaje.json (`par` = índice del párrafo del Short). Para las imágenes
conviene `"cubrir": true` (llenan el cuadro vertical) y, si hace falta, `recorte`.
Produce render/shorts/<ID>-Sn.mp4 (1080×1920, 25 fps, H.264 + AAC, subtítulos quemados) y su .srt.
La narración se regenera solo si cambia el texto (recursos/audio/shorts/Sn/). Local y gratis.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import montaje  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
KOKORO = Path("/tmp/kenv/bin/python")
SERIF = RAIZ / "canales/palimpsesto/fuentes/CormorantGaramond[wght].ttf"
SANS_B = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
MIN_S, MAX_S = 20, 60
ENTRADA, COLA = 0.4, 3.0


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


def narrar(s, audio):
    """Narra el texto del Short con narrar.py (Kokoro em_alex) si no existe o si el texto cambió."""
    audio.mkdir(parents=True, exist_ok=True)
    guion = "# Short\n\n## 1. " + s["titulo"] + "\n\n" + "\n\n".join(s["parrafos"]) + "\n"
    previo = audio / "guion.md"
    if previo.exists() and previo.read_text(encoding="utf-8") == guion and (audio / "narracion.wav").exists():
        return
    previo.write_text(guion, encoding="utf-8")
    subprocess.run([str(KOKORO), str(RAIZ / "scripts/narrar.py"), str(previo), str(audio)], check=True)


def main(plan_json, solo=None):
    plan_json = Path(plan_json).resolve()
    pdir = plan_json.parent.parent if re.match(r"\d\d-", plan_json.parent.name) else plan_json.parent
    plan = json.loads(plan_json.read_text(encoding="utf-8"))
    salida = pdir / "render/shorts"
    salida.mkdir(parents=True, exist_ok=True)
    pid = pdir.name
    for s in plan["shorts"]:
        if solo and s["id"] not in solo:
            continue
        audio = pdir / "recursos/audio/shorts" / s["id"]
        narrar(s, audio)
        nombre = f"{pid}-{s['id']}"
        sub = {"formato": "vertical", "entrada": ENTRADA, "cola": COLA, "capitulos": [s["titulo"]], "planos": s["planos"]}
        base, srt, _, durs = montaje.ensamblar(sub, pdir, audio, salida, nombre=f"{nombre}_base", max_c=36, max_linea=22)
        dur = sum(durs)
        if not MIN_S <= dur <= MAX_S:
            raise SystemExit(f"{s['id']}: dura {dur:.1f} s; debe estar entre {MIN_S} y {MAX_S} s.")
        srt_final = salida / f"{nombre}.srt"
        srt.replace(srt_final)
        estilo = ("FontName=Inter SemiBold,FontSize=15,PrimaryColour=&H00F0E6D9,OutlineColour=&H000D0B0B,"
                  "BackColour=&H99000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=14")
        filtro = (
            "drawbox=x=0:y=0:w=iw:h=440:color=0x0B0B0D@0.72:t=fill,"
            f"drawtext=fontfile='{SANS_B}':text='PALIMPSESTO':fontsize=40:fontcolor=0x9E2B25:x=(w-text_w)/2:y=170,"
            f"drawtext=fontfile='{SERIF}':text='{esc(s['titulo'])}':fontsize=82:fontcolor=0xE6DDCB:x=(w-text_w)/2:y=250,"
            f"subtitles='{srt_final}':force_style='{estilo}',"
            f"drawbox=x=0:y=0:w=iw:h=ih:color=0x0B0B0D@0.95:t=fill:enable='gte(t,{dur - COLA + 0.3:.2f})',"
            f"drawtext=fontfile='{SERIF}':text='{esc(s.get('cierre', 'Episodio completo en el canal'))}':"
            f"fontsize=76:fontcolor=0xE6DDCB:x=(w-text_w)/2:y=(h-text_h)/2:enable='gte(t,{dur - COLA + 0.3:.2f})'")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(base), "-vf", filtro, "-c:v", "libx264",
                        "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                        "-movflags", "+faststart", str(salida / f"{nombre}.mp4")], check=True)
        base.unlink()
        print(f"✔ {nombre}: {dur:.1f} s · {s['titulo']}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None)
