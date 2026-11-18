# Estudio de documentales — sistema multiagente

Sistema de producción de **Palimpsesto** (canal de YouTube de documentales históricos), diseñado para varios canales.

- Reglas del proyecto: `CLAUDE.md`
- Agentes: `.claude/agents/` (ceo, investigador, guionista, productor, editor, auditor, analista, cfo)
- Identidad del canal: `canales/palimpsesto/`
- Núcleo (flujo, Cuaderno del Director, finanzas): `estudio/core.py` · CLI: `python3 -m estudio --help`
- Esquema de datos: `db/schema.sql` · Tarifas versionadas: `finanzas/tarifas.csv`
- Estrategia y decisiones: `docs/`

## Cómo decide el Director desde el chat
Escriba un mensaje que **empiece** exactamente así:

| Acción | Mensaje |
|---|---|
| Aprobar una puerta | `APRUEBO PAL-2026-001 3 comentario opcional` |
| Pedir correcciones | `CORRECCIONES PAL-2026-001 16 el minuto 4 exagera la cifra` |
| Rechazar | `RECHAZO PAL-2026-001 6 ninguna tesis es sostenible` |
| Presupuesto extraordinario | `AMPLÍO PRESUPUESTO PAL-2026-001 70 más planos de vídeo en el acto 3` |
| Aporte editorial | `/nota PAL-2026-001 pregunta ¿y si…?` |
| Ver el estado | `/tablero` |

Un hook de Claude Code (`estudio/hook_aprobacion.py`) registra su texto literal y abre la puerta. Los agentes tienen prohibido ejecutar las aprobaciones (`.claude/settings.json`).

## Pruebas
```
python3 -m unittest discover -s tests -v
```
