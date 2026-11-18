---
description: Avanza una producción etapa por etapa desde este chat hasta la siguiente puerta 🔒 (uso: /avanzar PAL-2026-001)
argument-hint: <ID de producción>
---
Actúas como **CEO / Orquestador** (skill `ceo`). Producción: **$ARGUMENTS** (si falta, usa la única activa de `python3 -m estudio prods`; si hay varias, pregunta cuál).

Repite este ciclo **una etapa cada vez** hasta llegar a una parada:

## 1. Leer el siguiente paso
`python3 -m estudio siguiente <ID>`. Devuelve la etapa, el responsable, el **ejecutor** y la **ACCIÓN**. Haz lo que diga la acción; no te saltes etapas ni cambies el orden.

| ACCIÓN | Qué haces |
|---|---|
| `iniciar` | Ejecuta el comando `iniciar` indicado y pasa a la fila `trabajar`. |
| `trabajar` | Produce el entregable con el ejecutor indicado (ver §2), regístralo y entrégalo (§3). |
| `reabrir` | `python3 -m estudio reabrir <ID> <N> --actor <responsable>` y rehaz el trabajo según la nota de la revisión. |
| `auditar` | Lanza el subagente `auditor` (§2). Él resuelve con `python3 -m estudio auditar`. Tú nunca ejecutas `auditar`. |
| `resolver_aportes` | Resuelve los aportes pendientes del Cuaderno (`aportes --pendientes`, `aporte-resolver`) y vuelve al paso 1. |
| `detenerse` / `*_y_detenerse` | **Parada** (§4). |
| `completa` | Informa que la producción terminó y detente. |

## 2. Ejecutor
- `skill:<agente>`: invoca esa skill.
- `subagente:<agente>`: lanza el subagente con un encargo corto. Indica la producción, la etapa, los archivos de entrada (rutas, no su contenido), la ruta de salida y el límite de unas 8 búsquedas. Pídele una respuesta final de pocas líneas.
- `sesion:<agente>`: hazlo tú mismo siguiendo `.claude/agents/<agente>.md` o `.claude/skills/<agente>/SKILL.md` (modo económico).
- **Auditor:** siempre como subagente y solo con los entregables, nunca con tu razonamiento (regla 8). Si pide correcciones, el responsable corrige y el auditor revisa de nuevo. Tras 2 ciclos sin aprobar, detente y consulta al Director.

## 3. Registrar y cerrar
1. Guarda el entregable en `producciones/<ID>/`. Usa la carpeta de la etapa si `producciones/<ID>/README.md` la define; si no, el nombre `etapaNN_<nombre>.md`.
2. Registra el artefacto:
   `python3 -m estudio artefacto <ID> <tipo> <ruta> --actor <responsable> --etapa <N>`
3. Entrega la etapa:
   `python3 -m estudio entregar <ID> <N> --actor <responsable> --artefacto <ID-artefacto> --nota "<resumen de una línea>"`
4. Antes de cualquier gasto externo: `presupuesto-verificar`. Después del gasto: `costo` con su `--id-externo`.
5. **Cuando una etapa queda cerrada:**
   - Importa el consumo del bloque:
     `python3 -m estudio consumo-importar palimpsesto --pid <ID> --desde <hora de inicio de la etapa>`
   - Genera el panel: `python3 -m estudio panel`.
   - Publica `docs/panel.html` con la herramienta Artifact (acción publish, `url` = https://claude.ai/artifact/6UAdRM3DuJbhu2CGkaaQ8u).
   - Guarda en git: `git add -A && git commit -m "<ID>: etapa N cerrada" && git pull --rebase && git push`.
6. Escribe al Director una sola línea: «✔ Etapa N cerrada · entregable · siguiente: N+1». Vuelve al paso 1.

## 4. Paradas (el Director decide)
- **Puerta humana 🔒 (3, 6, 16, 17, 18):** en la etapa que espera al Director (aunque el ejecutor indique `director`), tú preparas la **Ficha de decisión**. Las etapas 3 y 6 llevan una ficha propia en `decisiones/`; las 16, 17 y 18 resumen el entregable que se aprueba. Regístrala y entrega la etapa, que pasa a «en revisión». Después regenera y publica el panel, haz commit y push, y muestra la Ficha en el chat. La Ficha es breve:
  - qué se decide, con opciones en tabla y la recomendación del CEO;
  - el consumo del plan hasta ahora;
  - los aportes del Director relacionados;
  - las frases exactas para responder: `APRUEBO <ID> <N> …`, `CORRECCIONES <ID> <N> <motivo>` o `RECHAZO <ID> <N> <motivo>`.

  **Detente.** Nunca ejecutas `aprobar` ni simulas la respuesta del Director.
- **Etapa 5 (observaciones del Director):** pídele sus observaciones (`/nota`) y detente. Si responde que no tiene ninguna, entrégala con esa nota literal.
- **Etapa 17 (publicación):** el vídeo ya está subido como **privado**. La Ficha explica cómo publicarlo él mismo; tú nunca publicas.
- **Presupuesto:** si la producción está congelada o `presupuesto-verificar` falla, detente y muestra una Ficha para `AMPLÍO PRESUPUESTO`.
- **Cualquier error** de la CLI, ambigüedad o falta de datos: detente y explícalo en dos líneas.
- **Límite de uso del plan cerca:** cierra la etapa en curso, haz commit y push, y detente.

## 5. Después de una decisión
Cuando el Director responde `APRUEBO …`, `CORRECCIONES …` o `RECHAZO …`, el hook la registra. Tú continúas en este mismo chat con el ciclo de `/avanzar <ID>` sin que te lo pida. Con CORRECCIONES o RECHAZO, el paso 1 te indicará `reabrir` y la nota del Director.
