"""Motor de montaje del canal (PIL + FFmpeg, sin servicios de pago).

Uso:
    python3 scripts/montaje.py producciones/<ID>/montaje.json
El plan JSON define los planos (tipo, recurso, texto) y a qué párrafo de la narración pertenece cada
uno. Los tiempos salen de `recursos/audio/tiempos.json` (scripts/narrar.py). Produce en `render/`:
`master.mp4` (1080p25, H.264 + AAC, -16 LUFS), `subtitulos.srt` y `capitulos.txt`.
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
W, H, FPS = 1920, 1080, 25
BW, BH = 2880, 1620          # lienzo de base (más grande que la salida: movimiento sin saltos)
NEGRO, TINTA, PERG, CINA = "#0B0B0D", "#2B2A33", "#D9CBB0", "#9E2B25"
GRIS = "#8C8576"
SERIF = str(RAIZ / "canales/palimpsesto/fuentes/CormorantGaramond[wght].ttf")
SANS = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
SANS_B = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
SIMB = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"   # ● ◐ ○ ✕
FADE = 0.35


def fuente(ruta, tam, peso=None):
    f = ImageFont.truetype(ruta, tam)
    if peso and "Cormorant" in ruta:
        try:
            f.set_variation_by_axes([peso])
        except Exception:
            pass
    return f


def run(cmd):
    subprocess.run(cmd, check=True)


# ---------------------------------------------------------------- composición de bases (lienzo BW×BH)
def lienzo(color=NEGRO):
    return Image.new("RGB", (BW, BH), color)


def cargar(ruta, realce=True):
    im = Image.open(ruta).convert("RGB")
    if "Sinar" in str(ruta):  # fuera la carta de color de la derecha
        im = im.crop((0, 0, int(im.width * 0.87), im.height))
    caja = im.convert("L").point(lambda v: 255 if v > 40 else 0).getbbox()  # fuera los márgenes negros
    if caja:
        im = im.crop(caja)
    return ImageOps.autocontrast(im, cutoff=0.5) if realce else im


def encajar(im, caja_w, caja_h, recorte=None):
    if recorte:  # fracciones (x0, y0, x1, y1)
        x0, y0, x1, y1 = recorte
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    k = min(caja_w / im.width, caja_h / im.height)
    return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)


def base_imagen(p, plan_dir):
    c = lienzo()
    im = encajar(cargar(plan_dir / p["img"]), BW * 0.92, BH * 0.94, p.get("recorte"))
    if p.get("llenar"):  # fondo desenfocado para planos verticales
        fondo = ImageOps.fit(cargar(plan_dir / p["img"]), (BW, BH)).filter(ImageFilter.GaussianBlur(40))
        c.paste(Image.blend(fondo, lienzo(), 0.75), (0, 0))
    c.paste(im, ((BW - im.width) // 2, (BH - im.height) // 2))
    if p.get("lupa"):
        cx, cy, r, zoom = p["lupa"]  # centro en fracciones del lienzo, radio en px, aumento
        X, Y = int(cx * BW), int(cy * BH)
        zona = c.crop((X - int(r / zoom), Y - int(r / zoom), X + int(r / zoom), Y + int(r / zoom))).resize((2 * r, 2 * r), Image.LANCZOS)
        c = Image.blend(c, lienzo(), 0.45)
        m = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
        c.paste(zona, (X - r, Y - r), m)
        ImageDraw.Draw(c).ellipse((X - r, Y - r, X + r, Y + r), outline=PERG, width=6)
    return c


def base_mosaico(p, plan_dir):
    c = lienzo()
    imgs = [cargar(plan_dir / f) for f in p["imgs"]]
    n = len(imgs)
    cols = p.get("cols", n)
    filas = math.ceil(n / cols)
    cw, ch = BW * 0.94 / cols, BH * (0.80 if p.get("titulo") else 0.92) / filas
    for k, im in enumerate(imgs):
        t = encajar(im, cw - 24, ch - 24)
        x = int(BW * 0.03 + (k % cols) * cw + (cw - t.width) / 2)
        y = int((BH * (0.16 if p.get("titulo") else 0.04)) + (k // cols) * ch + (ch - t.height) / 2)
        c.paste(t, (x, y))
    if p.get("titulo"):
        d = ImageDraw.Draw(c)
        f = fuente(SERIF, 120, 600)
        d.text((BW / 2, BH * 0.08), p["titulo"], font=f, fill=PERG, anchor="mm")
    return c


def envolver(d, texto, f, ancho):
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = (actual + " " + palabra).strip()
        if d.textlength(prueba, font=f) <= ancho:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    return lineas + [actual]


def base_tarjeta(p, _):
    """Tarjeta tipográfica: líneas [texto, estilo]; estilos: titulo, grande, normal, pequeño, acento, grado."""
    c = lienzo(p.get("fondo", NEGRO))
    d = ImageDraw.Draw(c)
    estilos = {"titulo": (SERIF, 170, 650, PERG), "grande": (SERIF, 130, 600, PERG), "normal": (SERIF, 96, 500, PERG),
               "pequeño": (SANS, 54, None, GRIS), "acento": (SERIF, 110, 650, CINA), "grado": (SIMB, 64, None, CINA),
               "rotulo": (SANS_B, 50, None, CINA)}
    bloques = []
    for texto, est in p["lineas"]:
        ruta, tam, peso, color = estilos[est]
        f = fuente(ruta, tam, peso)
        for l in envolver(d, texto, f, BW * 0.78):
            bloques.append((l, f, color, int(tam * 1.32)))
        bloques.append((None, None, None, int(tam * 0.35)))
    total = sum(b[3] for b in bloques)
    y = (BH - total) / 2
    for l, f, color, alto in bloques:
        if l:
            d.text((BW / 2, y + alto / 2), l, font=f, fill=color, anchor="mm")
        y += alto
    return c


def base_columnas(p, _):
    """Dos o tres fichas en paralelo, sin destacar ninguna: [(encabezado, texto)]."""
    c = lienzo()
    d = ImageDraw.Draw(c)
    if p.get("titulo"):
        d.text((BW / 2, BH * 0.14), p["titulo"], font=fuente(SANS_B, 58), fill=CINA, anchor="mm")
    n = len(p["fichas"])
    cw = BW * 0.86 / n
    for k, (enc, txt) in enumerate(p["fichas"]):
        x0 = BW * 0.07 + k * cw + 30
        x1 = x0 + cw - 60
        d.rectangle((x0, BH * 0.26, x1, BH * 0.84), outline=PERG, width=4)
        fe = fuente(SERIF, 104, 650)
        y = BH * 0.34
        for l in envolver(d, enc, fe, x1 - x0 - 80):
            d.text(((x0 + x1) / 2, y), l, font=fe, fill=PERG, anchor="mm")
            y += 120
        ft = fuente(SANS, 52)
        y += 30
        for l in envolver(d, txt, ft, x1 - x0 - 90):
            d.text(((x0 + x1) / 2, y), l, font=ft, fill=GRIS, anchor="mm")
            y += 70
    if p.get("pie"):
        d.text((BW / 2, BH * 0.92), p["pie"], font=fuente(SIMB, 54), fill=CINA, anchor="mm")
    return c


def base_diagrama(p, _):
    c = lienzo()
    d = ImageDraw.Draw(c)
    tipo = p["diagrama"]
    if tipo in ("hoja", "hoja_cruzada"):  # texto antiguo (horizontal) y nuevo (girado 90°)
        x0, y0, x1, y1 = BW * 0.30, BH * 0.10, BW * 0.70, BH * 0.90
        d.rectangle((x0, y0, x1, y1), fill=PERG)
        for k in range(26):
            y = y0 + 60 + k * (y1 - y0 - 120) / 25
            d.line((x0 + 70, y, x1 - 70, y), fill="#B9A988", width=7)
        if tipo == "hoja_cruzada":
            d.line(((x0 + x1) / 2, y0, (x0 + x1) / 2, y1), fill=GRIS, width=4)
            for k in range(24):
                x = x0 + 60 + k * (x1 - x0 - 120) / 23
                d.line((x, y0 + 70, x, y1 - 70), fill=TINTA, width=8)
    elif tipo == "capas":
        capas = p["capas"]
        for k, (txt, est) in enumerate(capas):
            y = BH * 0.16 + k * BH * 0.19
            col = PERG if k == 0 else ("#6E6553" if est != "acento" else CINA)
            d.rectangle((BW * 0.18 + k * 40, y, BW * 0.82 - k * 40, y + BH * 0.15), outline=col, width=6,
                        fill="#1A1A1F" if k else "#2A2620")
            d.text((BW / 2, y + BH * 0.075), txt, font=fuente(SERIF, 92, 600), fill=PERG if k == 0 else col, anchor="mm")
    elif tipo == "rebanadas":  # región bajo una parábola dividida en franjas
        ox, oy, sx, sy = BW * 0.22, BH * 0.82, BW * 0.56, BH * 0.62
        pts = [(ox + sx * t / 100, oy - sy * (t / 100) ** 2) for t in range(101)]
        for k in range(1, 40):
            t = k / 40
            d.line((ox + sx * t, oy, ox + sx * t, oy - sy * t * t), fill="#6E6553", width=4)
        d.line(pts, fill=PERG, width=9)
        d.line((ox, oy, ox + sx, oy), fill=PERG, width=7)
    elif tipo == "exhaucion":  # polígonos inscritos que se acercan al círculo
        cx, cy, r = BW / 2, BH * 0.50, BH * 0.36
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=PERG, width=8)
        for n, col in ((6, "#6E6553"), (12, GRIS), (24, CINA)):
            pts = [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
            d.line(pts, fill=col, width=5)
    if p.get("leyenda"):
        d.text((BW / 2, BH * 0.95), p["leyenda"], font=fuente(SANS_B, 52), fill=CINA, anchor="mm")
    return c


BASES = {"img": base_imagen, "mosaico": base_mosaico, "tarjeta": base_tarjeta, "columnas": base_columnas,
         "diagrama": base_diagrama}


def superposicion(p):
    """Capa fija (no se mueve con la cámara): rótulos de fuente, grado y recreación."""
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(o)
    if p.get("fuente"):
        txt = p["fuente"]
        f = fuente(SANS, 24)
        d.rounded_rectangle((36, H - 70, 60 + d.textlength(txt, font=f), H - 30), 6, fill=(11, 11, 13, 170))
        d.text((48, H - 50), txt, font=f, fill=(217, 203, 176, 230), anchor="lm")
    if p.get("rotulo"):  # p. ej. "RECONSTRUCCIÓN MODERNA", "VERSIÓN POPULAR"
        f = fuente(SANS_B, 30)
        d.text((48, 52), p["rotulo"], font=f, fill=(158, 43, 37, 255), anchor="lm")
    if p.get("nota"):  # texto breve en la parte inferior central
        f = fuente(SERIF, 54, 600)
        wv = d.textlength(p["nota"], font=f)
        d.rounded_rectangle((W / 2 - wv / 2 - 28, H - 170, W / 2 + wv / 2 + 28, H - 96), 8, fill=(11, 11, 13, 200))
        d.text((W / 2, H - 133), p["nota"], font=f, fill=(217, 203, 176, 255), anchor="mm")
    return o


# ---------------------------------------------------------------- render de cada plano
def zoompan(dur, zoom, movimiento):
    n = max(1, round(dur * FPS))
    dz = zoom - 1
    z = f"1+{dz:.4f}*on/{n}" if movimiento != "salir" else f"{zoom:.4f}-{dz:.4f}*on/{n}"
    x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if movimiento == "izq":
        x = f"(iw-iw/zoom)*(1-on/{n})"
    elif movimiento == "der":
        x = f"(iw-iw/zoom)*on/{n}"
    elif movimiento == "arriba":
        y = f"(ih-ih/zoom)*(1-on/{n})"
    elif movimiento == "abajo":
        y = f"(ih-ih/zoom)*on/{n}"
    return f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={W}x{H}:fps={FPS}"


def render_plano(k, p, dur, tmp, plan_dir):
    b1 = tmp / f"p{k:02d}_a.png"
    BASES[p["tipo"]](p, plan_dir).save(b1)
    sup = tmp / f"p{k:02d}_o.png"
    superposicion(p).save(sup)
    zoom = p.get("zoom", 1.07 if p["tipo"] in ("img", "mosaico") else 1.025)
    mov = p.get("mov", "centro")
    out = tmp / f"p{k:02d}.mp4"
    fin = f"fade=t=in:st=0:d={FADE},fade=t=out:st={dur - FADE:.3f}:d={FADE}"
    if p.get("transicion_a"):  # firma "palimpsesto": la imagen A se disuelve en B a mitad del plano
        pb = dict(p, **p["transicion_a"])
        b2 = tmp / f"p{k:02d}_b.png"
        BASES[pb["tipo"]](pb, plan_dir).save(b2)
        t = dur * p.get("corte", 0.5)
        fc = (f"[0:v]{zoompan(dur, zoom, mov)},format=yuv420p[a];[1:v]{zoompan(dur, zoom, mov)},format=yuv420p[b];"
              f"[a][b]xfade=transition=fade:duration=1.6:offset={max(0.1, t - 0.8):.3f},trim=duration={dur:.3f}[ab];"
              f"[ab][2:v]overlay=0:0,{fin},format=yuv420p[v]")
        ins = ["-loop", "1", "-t", f"{dur + 2:.3f}", "-i", str(b1), "-loop", "1", "-t", f"{dur + 2:.3f}", "-i", str(b2),
               "-loop", "1", "-t", f"{dur + 2:.3f}", "-i", str(sup)]
    else:
        fc = f"[0:v]{zoompan(dur, zoom, mov)}[a];[a][1:v]overlay=0:0,{fin},format=yuv420p[v]"
        ins = ["-loop", "1", "-t", f"{dur + 1:.3f}", "-i", str(b1), "-loop", "1", "-t", f"{dur + 1:.3f}", "-i", str(sup)]
    run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", fc, "-map", "[v]", "-t", f"{dur:.3f}",
         "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)])
    return out


# ---------------------------------------------------------------- tiempos, subtítulos y capítulos
def calendario(plan, tiempos, total_audio):
    """Asigna a cada plano su duración: cada párrafo ocupa desde su inicio hasta el inicio del siguiente."""
    lead, cola = plan["entrada"], plan["cola"]
    lim = [0.0] + [t["ini"] + lead for t in tiempos[1:]] + [total_audio + lead + cola]
    por_par = {}
    for k, p in enumerate(plan["planos"]):
        por_par.setdefault(p["par"], []).append(k)
    faltan = set(range(len(tiempos))) - set(por_par)
    if faltan:
        sys.exit(f"Párrafos sin plano: {sorted(faltan)}")
    cortes = {}
    for par, ks in por_par.items():
        a, b = lim[par], lim[par + 1]
        pesos = [plan["planos"][k].get("peso", 1.0) for k in ks]
        acc = a
        for k, w in zip(ks, pesos):
            cortes[k] = (acc, acc + (b - a) * w / sum(pesos))
            acc = cortes[k][1]
    # duraciones en fotogramas enteros, sin deriva acumulada
    marcas = [round(cortes[k][0] * FPS) for k in range(len(plan["planos"]))] + [round(lim[-1] * FPS)]
    return [(marcas[k + 1] - marcas[k]) / FPS for k in range(len(plan["planos"]))]


def hms(t, srt=True):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}" if srt else f"{int(m)}:{int(s):02d}"


def subtitulos(tiempos, lead, ruta, max_c=84):
    n, out = 1, []
    for t in tiempos:
        frases = [f.strip() for f in re.split(r"(?<=[.?!:;])\s+", t["texto"]) if f.strip()]
        trozos = []
        for f in frases:
            palabras, act = f.split(), ""
            for w in palabras:
                if len(act) + len(w) + 1 > max_c and act:
                    trozos.append(act)
                    act = w
                else:
                    act = (act + " " + w).strip()
            trozos.append(act)
        total = sum(len(x) for x in trozos)
        ini = t["ini"] + lead
        for x in trozos:
            dur = (t["fin"] - t["ini"]) * len(x) / total
            if len(x) > 42:  # dos líneas equilibradas
                corte = x.rfind(" ", 0, len(x) // 2 + 6)
                x = x[:corte] + "\n" + x[corte + 1:]
            out.append(f"{n}\n{hms(ini)} --> {hms(ini + dur - 0.04)}\n{x}\n")
            ini += dur
            n += 1
    Path(ruta).write_text("\n".join(out), encoding="utf-8")


def main(plan_json):
    plan_json = Path(plan_json).resolve()
    plan = json.loads(plan_json.read_text(encoding="utf-8"))
    pdir = plan_json.parent
    audio_dir = pdir / "recursos/audio"
    tiempos = json.loads((audio_dir / "tiempos.json").read_text(encoding="utf-8"))
    total_audio = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        str(audio_dir / "narracion.wav")], capture_output=True, text=True).stdout)
    render = pdir / "render"
    tmp = render / "planos"
    tmp.mkdir(parents=True, exist_ok=True)
    durs = calendario(plan, tiempos, total_audio)
    solo = set(map(int, sys.argv[2].split(","))) if len(sys.argv) > 2 else None
    clips = []
    for k, (p, d) in enumerate(zip(plan["planos"], durs)):
        out = tmp / f"p{k:02d}.mp4"
        if solo is None or k in solo or not out.exists():
            render_plano(k, p, d, tmp, pdir)
            print(f"plano {p['id']}: {d:5.2f} s", flush=True)
        clips.append(out)
    (tmp / "lista.txt").write_text("".join(f"file '{c.name}'\n" for c in clips))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "lista.txt"), "-c", "copy",
         str(tmp / "video.mp4")])
    lead_ms = int(plan["entrada"] * 1000)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "video.mp4"), "-i", str(audio_dir / "narracion.wav"),
         "-filter_complex", f"[1:a]adelay={lead_ms}|{lead_ms},apad[a]", "-map", "0:v", "-map", "[a]", "-shortest",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(render / "master.mp4")])
    subtitulos(tiempos, plan["entrada"], render / "subtitulos.srt")
    caps, vistos = [], set()
    for t in tiempos:
        if t["seccion"] not in vistos:
            vistos.add(t["seccion"])
            ini = 0 if not caps else t["ini"] + plan["entrada"]
            caps.append(f"{hms(ini, srt=False)} {plan['capitulos'][t['seccion'] - 1]}")
    (render / "capitulos.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
    print("✔", render / "master.mp4", f"({sum(durs):.1f} s)")


if __name__ == "__main__":
    main(sys.argv[1])
