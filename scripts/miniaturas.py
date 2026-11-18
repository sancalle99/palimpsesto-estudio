"""Miniaturas A/B/C (1280×720) del canal: una imagen de archivo, un elemento central y máximo 4 palabras.

Uso: python3 scripts/miniaturas.py producciones/<ID>/09-edicion/miniaturas.json
miniaturas.json: {"miniaturas": [{"id": "A", "img": "recursos/archivo/x.jpg", "recorte": [x0,y0,x1,y1], "texto": "…"}]}
Escribe render/miniaturas/miniatura_<id>.jpg. Sin servicios de pago.
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
SERIF = str(RAIZ / "canales/palimpsesto/fuentes/CormorantGaramond[wght].ttf")
W, H = 1280, 720


def main(plan_json):
    plan_json = Path(plan_json).resolve()
    pdir = plan_json.parent.parent if re.match(r"\d\d-", plan_json.parent.name) else plan_json.parent
    salida = pdir / "render/miniaturas"
    salida.mkdir(parents=True, exist_ok=True)
    for m in json.loads(plan_json.read_text(encoding="utf-8"))["miniaturas"]:
        if len(m["texto"].split()) > 4:
            raise SystemExit(f"Miniatura {m['id']}: más de 4 palabras.")
        im = Image.open(pdir / m["img"]).convert("RGB")
        if m.get("recorte"):
            x0, y0, x1, y1 = m["recorte"]
            im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
        im = ImageOps.fit(im, (W, H), Image.LANCZOS)
        im = ImageEnhance.Contrast(im).enhance(1.25)
        # degradado oscuro a la izquierda para el texto
        sombra = Image.new("L", (W, H))
        d = ImageDraw.Draw(sombra)
        for x in range(W):
            d.line([(x, 0), (x, H)], fill=int(215 * max(0, 1 - x / (W * 0.62))))
        im = Image.composite(Image.new("RGB", (W, H), "#0B0B0D"), im, sombra)
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype(SERIF, 112)
        f.set_variation_by_axes([700])
        palabras, lineas = m["texto"].split(), []
        while palabras:
            lineas.append(" ".join(palabras[:2])); palabras = palabras[2:]
        y = (H - len(lineas) * 120) // 2
        for l in lineas:
            d.text((70, y), l, font=f, fill="#E6DDCB", stroke_width=3, stroke_fill="#0B0B0D")
            y += 120
        d.rectangle([70, y + 14, 250, y + 22], fill="#9E2B25")
        im.save(salida / f"miniatura_{m['id']}.jpg", quality=90)
        print(f"✔ miniatura_{m['id']}.jpg · {m['texto']}")


if __name__ == "__main__":
    main(sys.argv[1])
