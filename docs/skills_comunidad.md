# Skills y agentes de la comunidad: evaluación (18-nov-2026)

Estrellas y forks leídos directamente de GitHub el 18-nov-2026. Las estrellas miden popularidad, no calidad ni seguridad: todo código de terceros se revisa antes de instalarlo y se fija a un commit concreto.

## Adoptar (Fase 4)

| Repositorio | ★ / forks | Última actividad | Licencia | Qué tomamos | Para qué agente |
|---|---|---|---|---|---|
| [remotion-dev/skills](https://github.com/remotion-dev/skills) (oficial de Remotion) | 7,4k / 814 | 16-nov-2026 | Ver licencia de Remotion* | `remotion-best-practices`, `remotion-maps`, `remotion-captions`, `remotion-multimedia` | Editor (mapas históricos animados, rótulos, subtítulos) |
| [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) | 2,6k / 454 | 17-nov-2026 | MIT | Skills `ffmpeg`, `elevenlabs`, `video-design`, `youtube-stats`, `moviepy`; script `tools/youtube_upload.py` (adaptado para que solo suba en privado) | Editor, Productor, Analista |
| [anthropics/skills](https://github.com/anthropics/skills) (oficial de Anthropic) | 196,7k / 23,1k | 16-nov-2026 | Ver cada skill | `skill-creator` (para crear nuestras skills propias), `pdf` (leer artículos académicos), `brand-guidelines` | Todos; Investigador |

\* Remotion es gratuito para personas y empresas pequeñas, y exige licencia de pago por encima de cierto tamaño. Hay que confirmar las condiciones vigentes en remotion.dev/docs/license antes de usarlo.

## Usar como referencia (copiar ideas, no instalar)

| Repositorio | ★ | Ideas útiles |
|---|---|---|
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 26,6k | `research-analyst` y `scientific-literature-researcher` (para el Investigador); `content-quality-editor` y `ai-writing-auditor`, que quitan patrones de escritura de IA (para el Guionista y el Auditor). No tiene agentes de fact-checking ni de costos: confirma que los nuestros son necesarios |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 58,2k | Catálogo general de hooks, comandos y orquestadores |

## No recomendados

| Repositorio o servicio | Motivo |
|---|---|
| [elevenlabs/elevenlabs-mcp](https://github.com/elevenlabs/elevenlabs-mcp) (1,6k★) | **Archivado el 20-ago-2026** (solo lectura). Se usará la API directa mediante la skill `elevenlabs` |
| Repos de "faceless YouTube automation" (yt-faceless-automation, faceless-youtube-agents…) | Pocas estrellas. Promueven "clonar el estilo de cualquier canal" y la producción en masa, justo lo que penaliza la política de contenido inauténtico |
| mcp-server-documentary-generation | 0★, sin licencia, investiga solo en Wikipedia: lo contrario a nuestro estándar de rigor |
| Servicios alojados (Cliptude, Faceless MCP) | Producen resultados genéricos con plantilla; no controlamos las fuentes ni las licencias |

## Skills propias a crear (con `skill-creator`)

1. `expediente-historico`: plantilla y método del Expediente con grados H/I/Hp/L.
2. `verificacion-fuentes`: comprobación de citas, DOI y enlaces (Auditor).
3. `fuentes-dominio-publico`: búsqueda de imágenes en Wikimedia, el Met, el Rijksmuseum, el Smithsonian, Europeana y la LoC, con registro de licencia.
4. `estilo-palimpsesto`: bloque de estilo visual, rótulos y transición "palimpsesto" para Remotion.
5. `shorts-arco`: estructura pregunta → giro → revelación para los Shorts.

## Reglas de integración

- Copia fijada (*vendoring*) en `.claude/skills/<nombre>/`, con un archivo `ORIGEN.md` que indique el repositorio, el commit, la licencia y la fecha.
- Revisión completa del código antes de incorporarlo: sin envíos de datos no declarados y sin publicación automática.
- `youtube_upload.py` se modifica para aceptar solo `privacy=private`.
