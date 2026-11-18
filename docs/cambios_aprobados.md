# Cambios aprobados pendientes de aplicar

Aprobados por el Director el 18-nov-2026: «Apruebo las 13 etapas, el título y la subida autónoma» (DEC-0014, DEC-0015, DEC-0016).
**Aplicarlos antes de seguir con `/avanzar PAL-2026-001`.** Al terminar, borra este archivo y deja constancia en `docs/decisiones.md`.

## 1. Flujo de 13 etapas (DEC-0014)

| # | Etapa | Antes | Responsable | Puerta | Carpeta |
|---|---|---|---|---|---|
| 1 | Oportunidades y temas | 1+2 | investigador | — | 01-oportunidades |
| 2 | Selección del tema | 3 | director | humana 🔒 | 02-seleccion-tema |
| 3 | Tres enfoques | 4 | investigador | — | 03-enfoques |
| 4 | Aprobación del enfoque y observaciones | 5+6 | director | humana 🔒 | 04-aprobacion-enfoque |
| 5 | Investigación y expediente | 7+8 | investigador | auditoría 🔍 | 05-expediente |
| 6 | Guion y títulos | 9 | guionista | — | 06-guion |
| 7 | Storyboard y prompts | 10+11 | productor | — | 07-storyboard |
| 8 | Producción audiovisual | 12 | productor | presupuesto 💲 | 08-produccion |
| 9 | Edición, Shorts y subida privada | 13+18 | editor | — | 09-edicion |
| 10 | Auditoría y correcciones | 14+15 | auditor | auditoría 🔍 | 10-auditoria |
| 11 | Aprobación del vídeo, Shorts y título final | 16+18 | director | humana 🔒 | 11-aprobacion |
| 12 | Publicación a la hora recomendada | 17 | director (ejecuta editor) | humana 🔒 | 12-publicacion |
| 13 | Cierre: métricas, costos y lecciones | 19+20+21 | analista (con cfo y ceo) | — | 13-cierre |

**Qué hay que cambiar:**

- **`estudio/core.py`:**
  - `ETAPAS`, `CARPETAS` y `ETAPAS_QUE_EXIGEN_APORTES_RESUELTOS`, que pasa a {6, 11}.
  - `ETAPAS_EN_SUBAGENTE`.
  - El cierre automático de la 15 al aprobar la 14 desaparece: las correcciones van dentro de la 10.
  - Revisar los números 9, 14, 15 y 16 que aparezcan en el código.
- **Migración de PAL-2026-001:**
  - Función en `core` y comando de la CLI (`migrar-13`). No se toca la base con sqlite directo.
  - Las tareas se renumeran según la columna «Antes»: las etapas unidas quedan cerradas si todas sus partes lo estaban. La producción queda con las etapas 1–9 cerradas y la 10 pendiente.
  - Se conservan el historial, los artefactos y las decisiones. Los tipos `aprobacion_etapa_N` antiguos se mantienen; en el panel se mapean con la tabla.
  - Las carpetas se renombran con `reorganizar`.
- **Panel:** `docs/organigrama.html` (ETAPA, GATES, `etapas` de cada agente, el «21» del texto y de la cuadrícula) y `estudio/panel.py`.
- **`hook_aprobacion.py`:** su patrón ya acepta 1 o 2 dígitos. Ese archivo no se puede editar por regla; si hiciera falta cambiarlo, se le pide al Director.
- **Documentación y pruebas:**
  - `CLAUDE.md`: puertas 🔒 2, 4, 11, 12; «21 etapas» → 13; regla 2.
  - `.claude/commands/avanzar.md`, `.claude/commands/tablero.md`, skills y agentes: números de etapa.
  - `tests/`.

## 2. Título (DEC-0015)

- **Guionista (etapa 6):** propone 5 títulos en `titulos.md`, con la recomendación y dónde se cumple cada promesa.
- **Editor (etapa 9):** elige el definitivo en coherencia con la miniatura y lo deja en `metadatos.md` con su justificación.
- **Director (etapa 11):** la Ficha de la puerta 11 muestra primero el título y la miniatura.

## 3. Subida autónoma y publicación con orden (DEC-0016)

- **Nueva regla 2 de `CLAUDE.md`:** «El Editor sube siempre en privado. Solo publica o programa un vídeo tras `APRUEBO <ID> 12` del Director, registrado por el hook. Nunca por iniciativa propia.»
- **Etapa 9:** el Editor sube el máster en privado con la API de YouTube (`videos.insert`, `privacyStatus=private`). Registra el ID del vídeo como artefacto.
- **Etapa 12:**
  - El Analista recomienda día y hora. La Ficha lo muestra.
  - Tras la aprobación, el Editor cambia a `public` o fija `publishAt`.
- **Limitación:** un proyecto de API no verificado por Google deja los vídeos bloqueados en privado. Hasta pasar la auditoría gratuita de la API de YouTube, el Director publica subiendo una copia a mano. Esto se indica en la Ficha 12.
- **Configuración (Fase 7), pasos del Director:**
  - Google Cloud: crear el proyecto y activar YouTube Data API v3.
  - Pantalla de consentimiento OAuth y cliente OAuth de escritorio.
  - Solicitud de la auditoría de la API.
- **Secretos:** se guardan con el formulario seguro (request_credential) o en `.env`, nunca en el chat ni en git. Script: `scripts/youtube_subir.py` (subir, publicar y programar).
