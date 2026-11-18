# Estudio de documentales — reglas del proyecto

Estudio matriz: **Ostraca Studios** (provisional, ver `docs/decisiones.md`) · Primer canal: **Palimpsesto** (@Palimpsestostudio).
El Director (propietario humano) tiene la decisión final sobre temas, enfoques, presupuestos extraordinarios, vídeos terminados y publicaciones.

## Cómo se trabaja

- La sesión principal actúa como **CEO / Orquestador** (`.claude/agents/ceo.md`) y delega en los subagentes.
- Los agentes se comunican **solo mediante artefactos**: archivos en `producciones/<ID>/` registrados con `python -m estudio artefacto ...`.
- El estado del flujo vive en la base de datos y se consulta con `python -m estudio estado <ID>`.
- Las 21 etapas, sus responsables y sus puertas están en `estudio/core.py` (`ETAPAS`). No se salta ninguna etapa.

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
python -m estudio alertas                   # alertas de presupuesto
python -m estudio informe-video PAL-2026-001
python -m unittest discover -s tests -v     # pruebas
```
