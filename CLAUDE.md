# Estudio de documentales — reglas del proyecto

Estudio matriz: **Ostraca Studios** (provisional, ver `docs/decisiones.md`) · Primer canal: **Palimpsesto** (@Palimpsestostudio).
El Director (propietario humano) tiene la decisión final sobre temas, enfoques, presupuestos extraordinarios, vídeos terminados y publicaciones.

## Cómo se trabaja

- La sesión principal actúa como **CEO / Orquestador** (skill `ceo`).
- **Roles ligeros como skills** (`.claude/skills/`: `ceo`, `guionista`, `productor`, `editor`, `analista`, `cfo`): la sesión principal carga la skill del rol y trabaja en línea, sin subagente.
- **Subagentes** (`.claude/agents/`): solo `investigador` (etapa 7 y apoyo) y `auditor` (etapas 8 y 14), donde la independencia o la profundidad lo exigen.
- Los agentes se comunican **solo mediante artefactos**: archivos en `producciones/<ID>/NN-etapa/` (p. ej. `09-guion/guion.md`; la carpeta la da `python3 -m estudio carpeta <ID> <N>`) registrados con `python -m estudio artefacto ...`. `producciones/<ID>/README.md` es el índice, generado desde la base; `recursos/` y `render/` quedan en la raíz de la producción.
- Al traer trabajo de otra sesión (`git pull`/merge que cambia `db/respaldo.sql`): `python3 -m estudio restaurar` antes de seguir, o el hook de respaldo sobrescribiría lo traído con la base local.
- El estado del flujo vive en la base de datos y se consulta con `python -m estudio estado <ID>`.
- Las 21 etapas, sus responsables y sus puertas están en `estudio/core.py` (`ETAPAS`). No se salta ninguna etapa.

> **⚠ Pendiente:** hay cambios aprobados por el Director sin aplicar (13 etapas, título, subida autónoma). Léelos en `docs/cambios_aprobados.md` y aplícalos antes de avanzar cualquier producción.

## Flujo desde un solo chat: `/avanzar <ID>`

- `/avanzar PAL-2026-001` ejecuta la siguiente etapa con su responsable, la registra, actualiza el panel y sigue con la próxima. Se detiene en cada puerta 🔒 mostrando la Ficha de decisión (detalle en `.claude/commands/avanzar.md`).
- El siguiente paso lo dice la base de datos: `python3 -m estudio siguiente <ID>`.
- Tras un `APRUEBO / CORRECCIONES / RECHAZO <ID> <N>` registrado por el hook, el CEO retoma `/avanzar <ID>` en el mismo chat.

## Reglas inviolables

1. **Puertas humanas (🔒 etapas 3, 6, 16, 17, 18):** ningún agente ejecuta `python -m estudio aprobar` ni `presupuesto-ampliar`. Se le presenta al Director una Ficha de decisión y se espera. El sistema lo bloquea técnicamente.
2. **Nada se publica.** Las subidas a YouTube son siempre privadas. Solo el Director publica.
3. **Ningún gasto sin verificación previa** (`python -m estudio presupuesto-verificar <ID> <estimado>`) y **ningún gasto sin registro** (`python -m estudio costo ...`) con su `--id-externo` (ID de solicitud del proveedor).
4. **Rigor:** toda afirmación factual tiene una fuente en el expediente y un grado de evidencia: **H** (hecho documentado), **I** (interpretación académica), **Hp** (hipótesis), **L** (leyenda / no verificado). No se inventan controversias, citas, fuentes ni datos.
5. **Aportes del Director:** se registran literalmente (`python -m estudio nota`) y cada uno se resuelve (integrado o descartado con justificación) antes del guion (etapa 9) y de la aprobación final (etapa 16). **Nunca se atribuyen al Director opiniones o experiencias que no constan textualmente en un aporte.**
6. **Recreaciones con IA:** se rotulan "Recreación" en pantalla y nunca se presentan como fotografía o documento de archivo. Cada recurso se registra con su licencia y procedencia (`python -m estudio recurso`).
7. **Secretos:** nunca se piden, se muestran ni se escriben claves, contraseñas o códigos. Viven en `.env` (fuera de git) o en el gestor de secretos del Director.
8. **Independencia del Auditor:** el auditor recibe solo los entregables, no el razonamiento de quien los produjo.

## Modo económico (plan Claude Pro: cuidar el consumo)

Decisión del Director del 18-nov-2026. Mientras el plan sea Pro:
1. Las etapas ligeras (1, 2, 4, 5 y las consultas) las hace la sesión principal sin lanzar subagentes. Los subagentes se usan solo donde la independencia o la profundidad lo exigen: auditoría (8, 14) e investigación profunda (7).
2. Búsquedas: como máximo unas 8 por etapa. Se usan primero las APIs académicas compactas (Crossref; OpenAlex cuando esté disponible) en lugar de leer páginas completas.
3. El análisis de competencia (los 10 vídeos más vistos) se hace solo sobre el tema elegido, no sobre todos los candidatos.
4. Entregables concisos: tablas en lugar de prosa; nada de repetir el contexto ya escrito en otros archivos.
5. Cuando se acerque el límite de uso, se cierra la etapa en curso, se hace commit y se retoma en la siguiente ventana.

## Voces y costo (decisiones del Director, 18-nov-2026)

- **Voces gratis y locales**, sin suscripciones: Piper y Kokoro-82M, ambas con licencia que permite uso comercial. Se instalan con `scripts/instalar_voces.sh`. Ninguna voz imita a una persona real.
- **El "costo del vídeo" que interesa al Director es cuánto del plan Claude Pro consume cada producción.** Al cerrar cada bloque de trabajo de una producción: `python3 -m estudio consumo-importar palimpsesto --pid <ID> --desde <inicio del bloque>`. Informe: `python3 -m estudio consumo-plan palimpsesto <AAAA-MM> --cuota 20`.

## Panel del estudio (anclado en la barra lateral del Director)

- Artefacto: **https://claude.ai/artifact/6UAdRM3DuJbhu2CGkaaQ8u** ("Estudio Documental Histórico").
- **Al cerrar cada bloque de trabajo:** `python3 -m estudio panel` y publicar `docs/panel.html` en ese enlace (herramienta Artifact, acción publish, pasando ese `url`). La plantilla es `docs/organigrama.html`; no se edita `docs/panel.html` a mano.
- El panel muestra el estado al momento de generarse; no es en tiempo real.

## Persistencia (la sesión en la nube es efímera)

- La base `db/estudio.sqlite` no se versiona. Su contenido se guarda como texto en `db/respaldo.sql`: un hook lo regenera al final de cada turno y, en una sesión nueva, la base se reconstruye sola desde ese archivo.
- **Al terminar cada bloque de trabajo:** `git add -A && git commit` y `git push`. Lo que no está en GitHub se pierde al cerrar la máquina.

## Identificadores

- Producción: `PAL-2026-001` · Artefacto: `PAL-2026-001-A007` · Recurso: `PAL-2026-001-R0042`
- Aporte: `DIR-PAL-2026-001-03` · Decisión: `DEC-0001`
- Gastos fuera de una producción: `GENERAL-PAL-2026-11`

## Comandos útiles

```
python -m estudio prods                     # producciones activas
python -m estudio estado PAL-2026-001       # tablero de una producción
python -m estudio siguiente PAL-2026-001    # qué etapa toca y qué acción (lo usa /avanzar)
python -m estudio alertas                   # alertas de presupuesto
python -m estudio informe-video PAL-2026-001
python -m unittest discover -s tests -v     # pruebas
/tmp/kenv/bin/python scripts/narrar.py producciones/<ID>/09-guion/guion.md producciones/<ID>/recursos/audio   # narración + tiempos
python3 scripts/montaje.py producciones/<ID>/13-edicion/montaje.json                                    # máster, SRT y capítulos
```

**Recursos pesados** (`producciones/*/recursos/`, `render/`): no se versionan. En una sesión nueva se regeneran así: las imágenes, descargándolas de las URL registradas con `recurso`; la voz, con `scripts/instalar_voces.sh` y `narrar.py`; el vídeo, con `montaje.py`.
