"""Genera la narración de un guion con la voz del canal (Kokoro em_alex, DEC-0009). Local y gratis.

Uso (con el entorno de Kokoro que instala scripts/instalar_voces.sh):
    /tmp/kenv/bin/python scripts/narrar.py producciones/<ID>/06-guion/guion.md producciones/<ID>/recursos/audio
Genera un WAV por sección (`seccion_N.wav`), `narracion.wav` (todo, con postproceso de la biblia
visual) y `narracion.txt` (el texto exacto locutado, para subtítulos y auditoría) y `tiempos.json`
(inicio y fin de cada párrafo en segundos, para el montaje y los subtítulos).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline

VOZ, VELOCIDAD, SR = "em_alex", 0.95, 24000
PAUSA_PARRAFO, PAUSA_SECCION = 0.6, 1.4

# Solo afecta a la pronunciación; el texto del guion no cambia.
PRONUNCIACION = [
    (r"\bsiglos II o III\b", "siglos segundo o tercero"),
    (r"\bsiglo XIII\b", "siglo trece"), (r"\bsiglo XX\b", "siglo veinte"), (r"\bsiglo X\b", "siglo diez"),
    (r"\bJ\. L\. Heiberg\b", "jota ele Héiberg"), (r"\bHeiberg\b", "Héiberg"),
    (r"\bIoannes Myronas\b", "Ioánes Mirónas"), (r"\bMyronas\b", "Mirónas"),
    (r"\bSLAC\b", "Slac"), (r"\bChristie's\b", "Cristis"), (r"\blaches\b", "láches"),
    (r"\bWalters Art Museum\b", "Wólters Art Miúsiam"), (r"\bWilliam Noel\b", "Wíliam Nóel"),
    (r"\bKimba Wood\b", "Kimba Wud"), (r"\bPhysics Today\b", "Físics Tudéi"),
    (r"\bStomachion\b", "Estomájion"), (r"\bCreative Commons\b", "Criéitiv Cómons"),
    (r"\bSirieix\b", "Sirié"), (r"\bReviel Netz\b", "Reviel Nets"), (r"\bNetz\b", "Nets"),
    (r"\bKen Saito\b", "Ken Saíto"), (r"\bNatalie Tchernetska\b", "Natali Chernetska"),
    (r"\b17\.152\b", "diecisiete mil ciento cincuenta y dos"), (r"\b536\b", "quinientas treinta y seis"),
]


def secciones(guion: str):
    """Devuelve [(título, [párrafos])] con solo el texto que dice el narrador."""
    out = []
    for bloque in re.split(r"^## ", guion, flags=re.M)[1:]:
        titulo, *lineas = bloque.split("\n")
        if not re.match(r"\d+\.", titulo):
            continue  # Aportes, Recuento…
        pars = []
        for l in lineas:
            l = l.strip()
            if not l or l.startswith((">", "|", "---", "#")):
                continue
            l = re.sub(r"`[^`]*`", "", l)          # marcas para el editor
            l = re.sub(r"[*_]", "", l).strip()     # cursivas
            if l:
                pars.append(l)
        out.append((titulo.strip(), pars))
    return out


def locutable(t: str) -> str:
    for a, b in PRONUNCIACION:
        t = re.sub(a, b, t)
    return t


def main(guion_md, salida):
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    pipe = KPipeline(lang_code="e")
    todo, texto, tiempos, t = [], [], [], 0.0
    for i, (titulo, pars) in enumerate(secciones(Path(guion_md).read_text(encoding="utf-8")), 1):
        sec = []
        texto.append(f"## {titulo}")
        for p in pars:
            texto.append(p)
            n = sum(len(x) for x in sec)
            for _, _, audio in pipe(locutable(p), voice=VOZ, speed=VELOCIDAD):
                sec.append(np.asarray(audio))
            fin = sum(len(x) for x in sec)
            tiempos.append({"seccion": i, "texto": p, "ini": round(t + n / SR, 3), "fin": round(t + fin / SR, 3)})
            sec.append(np.zeros(int(SR * PAUSA_PARRAFO)))
        sec = np.concatenate(sec)
        sf.write(salida / f"seccion_{i}.wav", sec, SR)
        todo += [sec, np.zeros(int(SR * PAUSA_SECCION))]
        t += (len(sec) + int(SR * PAUSA_SECCION)) / SR
        print(f"sección {i}: {len(sec) / SR:6.1f} s  {titulo}", flush=True)
    sf.write(salida / "narracion_cruda.wav", np.concatenate(todo), SR)
    (salida / "tiempos.json").write_text(json.dumps(tiempos, ensure_ascii=False, indent=1), encoding="utf-8")
    (salida / "narracion.txt").write_text("\n".join(texto) + "\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(salida / "narracion_cruda.wav"), "-af",
                    "highpass=f=70,acompressor=threshold=-18dB:ratio=2.5,loudnorm=I=-16:TP=-1.5",
                    "-ar", "44100", str(salida / "narracion.wav")], check=True)
    (salida / "narracion_cruda.wav").unlink()
    print("✔", salida / "narracion.wav")


if __name__ == "__main__":
    main(*sys.argv[1:3])
