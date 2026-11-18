"""Motor de montaje del canal (PIL + FFmpeg, sin servicios de pago).

Uso:
    python3 scripts/montaje.py producciones/<ID>/09-edicion/montaje.json
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
ESC = 1.0                    # escala de los rótulos fijos (1,6 en vertical)
TXT = 1.0                    # escala del texto de tarjetas y diagramas (1,4 en vertical: ≥ 48 px en el móvil)
REVELAR_DESDE = 8.0          # tarjetas más largas que esto se revelan por líneas (HAL-03)

# Stomachion: 14 piezas sobre una retícula de 12 × 12 (y hacia arriba). Coordenadas de la reconstrucción
# habitual (Suter), tomadas de J. Burkardt, stomachion.plot (FSU, 2006); las áreas suman 144.
STOMACHION = [
    [(0, 12), (2, 10), (12, 12)], [(2, 10), (4, 8), (12, 12)], [(0, 12), (0, 6), (4, 8)], [(0, 6), (6, 6), (4, 8)],
    [(0, 6), (6, 3), (8, 4), (6, 6)], [(0, 6), (0, 0), (4, 0), (6, 3)], [(4, 0), (6, 0), (6, 3)],
    [(6, 3), (6, 0), (12, 0)], [(6, 3), (12, 0), (8, 4)], [(8, 4), (12, 0), (12, 6)], [(6, 6), (8, 4), (12, 6)],
    [(12, 9), (6, 9), (4, 8), (6, 6), (12, 6)], [(6, 9), (12, 9), (8, 10)], [(8, 10), (12, 9), (12, 12)]]
TONOS = ["#B9A988", "#8C7A5B", "#6E6553", "#D9CBB0", "#A6926E", "#7A6F5C", "#C9B994"]  # sin rojo: el rojo resalta


def formato(vertical):
    """Ajusta las dimensiones globales: 16:9 (máster) o 9:16 (Shorts)."""
    global W, H, BW, BH, ESC, TXT
    if vertical:
        W, H, BW, BH, ESC, TXT = 1080, 1920, 1620, 2880, 1.6, 1.4


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


def fondo(p, plan_dir):
    """Lienzo de una tarjeta: negro o, con `fondo_img`, la imagen de archivo muy oscurecida debajo del texto."""
    if not p.get("fondo_img"):
        return lienzo(p.get("fondo", NEGRO))
    im = ImageOps.fit(cargar(plan_dir / p["fondo_img"]), (BW, BH), centering=tuple(p.get("fondo_centro", (0.5, 0.5))))
    return Image.blend(im.filter(ImageFilter.GaussianBlur(6)), lienzo(), p.get("fondo_velo", 0.86))


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
    if p.get("cubrir"):  # llena todo el cuadro (Shorts verticales): recorte centrado en `centro`
        im = cargar(plan_dir / p["img"])
        if p.get("recorte"):
            x0, y0, x1, y1 = p["recorte"]
            im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
        im = ImageOps.fit(im, (BW, BH), Image.LANCZOS, centering=tuple(p.get("centro", (0.5, 0.5))))
    else:
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


def base_tarjeta(p, plan_dir, hasta=None):
    """Tarjeta tipográfica: líneas [texto, estilo]; estilos: titulo, grande, normal, pequeño, acento, grado.
    `hasta` = número de líneas visibles (revelado progresivo, sin mover las demás)."""
    c = fondo(p, plan_dir)
    d = ImageDraw.Draw(c)
    estilos = {"titulo": (SERIF, 170, 650, PERG), "grande": (SERIF, 130, 600, PERG), "normal": (SERIF, 96, 500, PERG),
               "pequeño": (SANS, 54, None, GRIS), "acento": (SERIF, 110, 650, CINA), "grado": (SIMB, 64, None, CINA),
               "rotulo": (SANS_B, 50, None, CINA)}
    bloques = []
    for i, (texto, est) in enumerate(p["lineas"]):
        ruta, tam, peso, color = estilos[est]
        tam = int(tam * TXT)
        f = fuente(ruta, tam, peso)
        for l in envolver(d, texto, f, BW * 0.78):
            bloques.append((l if hasta is None or i < hasta else None, f, color, int(tam * 1.32)))
        bloques.append((None, None, None, int(tam * 0.35)))
    total = sum(b[3] for b in bloques)
    y = (BH - total) / 2
    for l, f, color, alto in bloques:
        if l:
            d.text((BW / 2, y + alto / 2), l, font=f, fill=color, anchor="mm")
        y += alto
    return c


def base_columnas(p, plan_dir, hasta=None):
    """Dos o tres fichas en paralelo, sin destacar ninguna: [(encabezado, texto)]."""
    c = fondo(p, plan_dir)
    d = ImageDraw.Draw(c)
    if p.get("titulo"):
        d.text((BW / 2, BH * 0.14), p["titulo"], font=fuente(SANS_B, 58), fill=CINA, anchor="mm")
    n = len(p["fichas"])
    cw = BW * 0.86 / n
    for k, (enc, txt) in enumerate(p["fichas"]):
        if hasta is not None and k >= hasta:
            continue
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
    if p.get("pie") and (hasta is None or hasta >= n):
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
        cx, cy, r = BW / 2, BH * 0.50, min(BW, BH) * 0.36
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=PERG, width=8)
        for n, col in ((6, "#6E6553"), (12, GRIS), (24, CINA)):
            pts = [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
            d.line(pts, fill=col, width=5)
    elif tipo in ("stomachion", "stomachion_suelto"):  # diagrama propio, sin IA (HAL-03)
        lado = min(BW * (0.62 if W > H else 0.86), BH * 0.70) * (0.72 if tipo == "stomachion_suelto" else 1)
        x0, y0, u = (BW - lado) / 2, (BH - lado) / 2 - BH * 0.02, lado / 12
        resaltar = set(p.get("resaltar", []))
        for k, pieza in enumerate(STOMACHION):
            cx = sum(x for x, _ in pieza) / len(pieza) - 6
            cy = sum(y for _, y in pieza) / len(pieza) - 6
            sep = p.get("separacion", 0.3) if tipo == "stomachion_suelto" else 0
            pts = [(x0 + (x + cx * sep) * u, y0 + (12 - y - cy * sep) * u) for x, y in pieza]
            col = CINA if k in resaltar else TONOS[k % len(TONOS)]
            d.polygon(pts, fill=col, outline=NEGRO)
            d.line(pts + [pts[0]], fill=NEGRO, width=max(3, int(u / 9)))
        if tipo == "stomachion" and p.get("reticula"):
            for i in range(13):
                d.line((x0 + i * u, y0, x0 + i * u, y0 + lado), fill="#3A3833", width=2)
                d.line((x0, y0 + i * u, x0 + lado, y0 + i * u), fill="#3A3833", width=2)
            for k, pieza in enumerate(STOMACHION):
                d.polygon([(x0 + x * u, y0 + (12 - y) * u) for x, y in pieza], outline=PERG)
    if p.get("leyenda") and W > H:  # en vertical la leyenda chocaría con los subtítulos; la dice la voz
        fl = fuente(SANS_B, int(52 * TXT))
        ys = BH * (0.89 if W > H else 0.80)
        for l in envolver(d, p["leyenda"], fl, BW * 0.9)[::-1]:
            d.text((BW / 2, ys), l, font=fl, fill=CINA, anchor="mm")
            ys -= 80 * TXT
    return c


BASES = {"img": base_imagen, "mosaico": base_mosaico, "tarjeta": base_tarjeta, "columnas": base_columnas,
         "diagrama": base_diagrama}


def superposicion(p):
    """Capa fija (no se mueve con la cámara): rótulos de fuente, grado y recreación."""
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(o)
    abajo = H - (70 if W > H else 420)  # en vertical, por encima de los subtítulos quemados
    if p.get("fuente"):
        f = fuente(SANS, int(24 * ESC))
        lineas = envolver(d, p["fuente"], f, W - 120)
        alto = int(34 * ESC)
        y = abajo - alto * (len(lineas) - 1)
        for l in lineas:
            d.rounded_rectangle((36, y - alto / 2 - 4, 60 + d.textlength(l, font=f), y + alto / 2 + 4), 6, fill=(11, 11, 13, 170))
            d.text((48, y), l, font=f, fill=(217, 203, 176, 230), anchor="lm")
            y += alto
    if p.get("rotulo"):  # p. ej. "RECONSTRUCCIÓN MODERNA", "VERSIÓN POPULAR"
        f = fuente(SANS_B, int(30 * ESC))
        d.text((48, 52 if W > H else 470), p["rotulo"], font=f, fill=(158, 43, 37, 255), anchor="lm")
    if p.get("nota"):  # texto breve en la parte inferior central
        f = fuente(SERIF, int(54 * ESC), 600)
        y = abajo - (95 if W > H else 150)
        for l in envolver(d, p["nota"], f, W - 140)[::-1]:
            wv = d.textlength(l, font=f)
            d.rounded_rectangle((W / 2 - wv / 2 - 28, y - 37 * ESC, W / 2 + wv / 2 + 28, y + 37 * ESC), 8, fill=(11, 11, 13, 200))
            d.text((W / 2, y), l, font=f, fill=(217, 203, 176, 255), anchor="mm")
            y -= int(78 * ESC)
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
    pasos = len(p.get("lineas") or p.get("fichas") or [])
    if p["tipo"] in ("tarjeta", "columnas") and p.get("revelar", dur > REVELAR_DESDE) and pasos > 1:
        # revelado por líneas: cada estado aparece con un fundido; las líneas no se mueven (HAL-03)
        estados = []
        for h in range(1, pasos + 1):
            ruta = tmp / f"p{k:02d}_r{h}.png"
            BASES[p["tipo"]](p, plan_dir, hasta=h).save(ruta)
            estados.append(ruta)
        tramo = min(dur * 0.6, 2.2 * (pasos - 1)) / max(1, pasos - 1)
        ins, cadena, prev = [], "", "[0:v]"
        for i, e in enumerate(estados):
            ins += ["-framerate", str(FPS), "-loop", "1", "-t", f"{dur + 1:.3f}", "-i", str(e)]
        for i in range(1, pasos):
            cadena += f"{prev}[{i}:v]xfade=transition=fade:duration=0.5:offset={0.6 + tramo * i - 0.5:.3f}[x{i}];"
            prev = f"[x{i}]"
        n = max(1, round(dur * FPS))
        z = f"1+{zoom - 1:.4f}*on/{n}"
        cadena += (f"{prev}zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}[a];"
                   f"[a][{pasos}:v]overlay=0:0,{fin},format=yuv420p[v]")
        ins += ["-loop", "1", "-t", f"{dur + 1:.3f}", "-i", str(sup)]
        run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", cadena, "-map", "[v]", "-t", f"{dur:.3f}",
             "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(out)])
        return out
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


def cues(texto, ini, fin, max_c=84, min_s=1.0):
    """Reparte un párrafo en subtítulos (HAL-04): corta en fin de frase solo si el trozo ya es largo, nunca tras
    una inicial ("J. L."), prefiere cortar tras una coma y fusiona los trozos de menos de `min_s` segundos."""
    texto = re.sub(r"(?<!\w)(\w\.) ", "\\1\u00a0", texto)  # "J. L. Heiberg" no se separa
    palabras, trozos, act = texto.split(" "), [], []
    largo = lambda ws: len(" ".join(ws))
    for i, w in enumerate(palabras):
        if act and largo(act + [w]) > max_c:
            comas = [j for j, x in enumerate(act[:-1]) if x.endswith((",", ";", ":", ".", "?")) and largo(act[:j + 1]) >= max_c * 0.3
                     and not re.fullmatch(r"\w\.", x)]
            j = comas[-1] + 1 if comas else len(act)
            trozos.append(act[:j])
            act = act[j:]
        act.append(w)
        inicial = re.fullmatch(r"\w\.", w) is not None
        if w.endswith((".", "?", "!", ":")) and not inicial and largo(act) >= max_c * 0.4 and i < len(palabras) - 1:
            trozos.append(act)
            act = []
    if act:
        trozos.append(act)
    trozos = [" ".join(t) for t in trozos if t]
    total = sum(len(x) for x in trozos)
    durs = [(fin - ini) * len(x) / total for x in trozos]
    k = 0
    while k < len(trozos) and len(trozos) > 1:  # fusiona los demasiado breves con el vecino más corto
        if durs[k] < min_s:
            v = k - 1 if k == len(trozos) - 1 or (k > 0 and len(trozos[k - 1]) < len(trozos[k + 1])) else k + 1
            a, b = min(k, v), max(k, v)
            trozos[a:b + 1] = [trozos[a] + " " + trozos[b]]
            durs[a:b + 1] = [durs[a] + durs[b]]
            k = 0
            continue
        k += 1
    out, t = [], ini
    for x, d in zip(trozos, durs):
        out.append((t, t + d, x.replace("\u00a0", " ")))
        t += d
    return out


def partir(x, max_linea):
    """Divide un subtítulo en dos líneas equilibradas (≤ `max_linea` si es posible), con preferencia por cortar
    tras una coma o un punto y sin separar iniciales ("J. L. Heiberg")."""
    if len(x) <= max_linea:
        return x
    x = re.sub(r"(?<!\w)(\w\.) ", "\\1\u00a0", x)
    w = x.split(" ")
    mejor = min(range(1, len(w)), key=lambda i: max(len(" ".join(w[:i])), len(" ".join(w[i:])))
                - (4 if w[i - 1][-1] in ",.;:?" else 0))
    return (" ".join(w[:mejor]) + "\n" + " ".join(w[mejor:])).replace("\u00a0", " ")


def subtitulos(tiempos, lead, ruta, max_c=76, max_linea=42):
    n, out = 1, []
    for t in tiempos:
        for a, b, x in cues(t["texto"], t["ini"] + lead, t["fin"] + lead, max_c):
            out.append(f"{n}\n{hms(a)} --> {hms(b - 0.04)}\n{partir(x, max_linea)}\n")
            n += 1
    Path(ruta).write_text("\n".join(out), encoding="utf-8")


def ensamblar(plan, pdir, audio_dir, salida, nombre="master", solo=None, max_c=76, max_linea=42):
    """Renderiza los planos de `plan`, los une con la narración de `audio_dir` y escribe <nombre>.mp4 y su .srt."""
    formato(plan.get("formato") == "vertical")
    tiempos = json.loads((audio_dir / "tiempos.json").read_text(encoding="utf-8"))
    total_audio = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        str(audio_dir / "narracion.wav")], capture_output=True, text=True).stdout)
    tmp = salida / ("planos" if nombre == "master" else f"planos_{nombre}")
    tmp.mkdir(parents=True, exist_ok=True)
    durs = calendario(plan, tiempos, total_audio)
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
    video = salida / f"{nombre}.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "video.mp4"), "-i", str(audio_dir / "narracion.wav"),
         "-filter_complex", f"[1:a]adelay={lead_ms}|{lead_ms},apad[a]", "-map", "0:v", "-map", "[a]", "-shortest",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(video)])
    srt = salida / ("subtitulos.srt" if nombre == "master" else f"{nombre}.srt")
    subtitulos(tiempos, plan["entrada"], srt, max_c, max_linea)
    return video, srt, tiempos, durs


def main(plan_json, solo=None):
    plan_json = Path(plan_json).resolve()
    plan = json.loads(plan_json.read_text(encoding="utf-8"))
    pdir = plan_json.parent
    if pdir.name[:2].isdigit() and pdir.name[2:3] == "-":  # producciones/<ID>/09-edicion/montaje.json
        pdir = pdir.parent  # recursos/ y render/ viven en la raíz de la producción
    render = pdir / "render"
    video, _, tiempos, durs = ensamblar(plan, pdir, pdir / "recursos/audio", render, solo=solo)
    caps, vistos = [], set()
    for t in tiempos:
        if t["seccion"] not in vistos:
            vistos.add(t["seccion"])
            ini = 0 if not caps else t["ini"] + plan["entrada"]
            caps.append(f"{hms(ini, srt=False)} {plan['capitulos'][t['seccion'] - 1]}")
    (render / "capitulos.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
    print("✔", video, f"({sum(durs):.1f} s)")


if __name__ == "__main__":
    main(sys.argv[1], set(map(int, sys.argv[2].split(","))) if len(sys.argv) > 2 else None)
