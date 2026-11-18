"""Hook UserPromptSubmit de Claude Code: convierte un mensaje del Director en el chat
en una aprobación formal. Es la vía para abrir puertas humanas desde la app (sin terminal).

Solo se activa con mensajes que EMPIEZAN exactamente con una de estas fórmulas:
    APRUEBO <ID> <etapa> [nota libre]
    CORRECCIONES <ID> <etapa> <motivo>
    RECHAZO <ID> <etapa> <motivo>
    AMPLÍO PRESUPUESTO <ID> <monto_usd> <justificación>

El hook se ejecuta con el texto que escribió el humano (Claude no puede generar ese evento),
registra la decisión con el texto literal y responde con una línea de contexto para la sesión.
"""
from __future__ import annotations

import json
import re
import sys

from . import core

PATRON = re.compile(r"^\s*(APRUEBO|CORRECCIONES|RECHAZO)\s+([A-Z]{2,5}-\d{4}-\d{3})\s+(\d{1,2})\b\s*(.*)$", re.S)
PATRON_PPTO = re.compile(r"^\s*AMPL[IÍ]O\s+PRESUPUESTO\s+([A-Z]{2,5}-\d{4}-\d{3})\s+(\d+(?:[.,]\d+)?)\s*(.*)$", re.S | re.I)
RESULTADO = {"APRUEBO": "aprobado", "CORRECCIONES": "correcciones", "RECHAZO": "rechazado"}


def procesar(texto: str, con=None) -> str | None:
    m, mp = PATRON.match(texto), PATRON_PPTO.match(texto)
    if not (m or mp):
        return None
    con = con or core.conectar()
    try:
        if m:
            accion, pid, etapa, nota = m.group(1), m.group(2), int(m.group(3)), m.group(4).strip()
            if core.ETAPA.get(etapa) is None or core.ETAPA[etapa].puerta != "humana":
                return f"[SISTEMA] La etapa {etapa} no es una puerta humana; no se registró nada."
            if accion != "APRUEBO" and not nota:
                return "[SISTEMA] Indique el motivo después de la etapa. No se registró nada."
            core.revisar(con, pid, etapa, RESULTADO[accion], "director",
                         f"Mensaje literal del Director: «{texto.strip()}»", director=True)
            return (f"[SISTEMA] Decisión del Director registrada: {pid} etapa {etapa} → {RESULTADO[accion]}. "
                    "Continúa el flujo según corresponda.")
        pid, monto, just = mp.group(1), float(mp.group(2).replace(",", ".")), mp.group(3).strip()
        if not just:
            return "[SISTEMA] Indique la justificación de la ampliación. No se registró nada."
        core.ampliar_presupuesto(con, pid, monto, f"Mensaje literal del Director: «{texto.strip()}»", director=True)
        return f"[SISTEMA] Presupuesto de {pid} ampliado a {monto:.2f} USD por el Director."
    except core.ErrorEstudio as e:
        return f"[SISTEMA] No se pudo registrar la decisión: {e}"


def main():
    try:
        datos = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    salida = procesar(datos.get("prompt", ""))
    if salida:
        print(salida)  # en UserPromptSubmit, stdout se añade como contexto de la sesión
    return 0


if __name__ == "__main__":
    sys.exit(main())
