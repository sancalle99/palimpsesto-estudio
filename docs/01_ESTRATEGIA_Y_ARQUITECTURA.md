# PRIMER ENTREGABLE — Estrategia, arquitectura y plan de implementación

**Proyecto:** estudio de documentales históricos operado por agentes de IA
**Nombres internos:** NEBULA STUDIOS → propuesta *Ostraka* · ARCHIVO OCULTO → propuesta *Palimpsesto* (ver `02_INFORME_NAMING.md`)
**Versión:** 1.0 · 17-nov-2026 · **Estado:** para aprobación. No se ha escrito código.

> **Convenciones del documento**
> - Las cifras de precio marcadas con "≈" proceden de fuentes secundarias o de estimaciones, y **deben verificarse en la página oficial antes de contratar**.
> - Los precios de Claude vienen de la referencia oficial de Anthropic (caché del 3-nov-2026).

---

## Índice

1. Estrategia del canal
2. Investigación de competencia
3. Identidad editorial
4. Sistema de diferenciación y originalidad
5. Arquitectura de los ocho agentes
6. Flujo de producción
7. Arquitectura técnica
8. Comparación de proveedores y herramientas
9. Seguimiento de tokens y costos
10. Presupuesto inicial
11. Calendario de 90 días
12. Plan de desarrollo
13. Configuración de cuentas (paso a paso y cuándo)
14. Políticas y cumplimiento de YouTube
15. Información y decisiones que necesito de usted

---

## 1. Estrategia del canal

**Tesis:** el mercado hispanohablante de historia en YouTube está dividido entre:

- (a) divulgadores personales muy populares pero centrados en el presentador;
- (b) canales "faceless" de alto volumen y bajo rigor, muchos generados con IA, que YouTube está desmonetizando de forma activa (política de *contenido inauténtico*, aclarada en julio de 2026);
- (c) pocos canales que producen documentales cinematográficos con fuentes transparentes.

**El hueco a ocupar es (c):** documentales en español con calidad de cine y rigor visible y verificable.

**Propuesta de valor al espectador:** *"Cada episodio te dice qué sabemos, cómo lo sabemos y qué sigue en duda."*

**Pilares temáticos** (para no dispersarse en el primer año):

1. **Versiones que se impusieron:** cómo una interpretación se volvió la oficial (p. ej., la "leyenda negra", la caída de Roma, Colón).
2. **Descubrimientos que reescribieron la historia:** palimpsestos reales, ADN antiguo, lidar maya, Göbekli Tepe.
3. **Personajes borrados:** figuras omitidas por el relato dominante.
4. **Enigmas con evidencia:** misterios reales tratados con método (Voynich, bronce de Antikythera, colonia de Roanoke).
5. **Conexiones improbables:** acontecimientos aparentemente independientes que se relacionan.

**Mercado:** español neutro, con foco en Latinoamérica (México, Colombia, Argentina, Perú) y España. Hay que equilibrar los temas: el público latinoamericano está desatendido en historia precolombina y colonial bien contada.

**Evaluación de la estrategia de publicación pedida** (1 documental semanal de 10–20 min + 3–5 Shorts):

| Aspecto | Evaluación | Propuesta |
|---|---|---|
| 1 documental/semana | **No viable con calidad en los primeros dos meses.** Cada episodio exige investigación profunda, dos aprobaciones suyas y una auditoría. Sin colchón, el primer retraso rompe la cadencia | **Rampa:** 1 cada 2 semanas en los meses 1–2; semanal desde el mes 3 **solo si** hay al menos 2 episodios terminados en reserva |
| Duración de 10–20 min | Correcta. En historia, entre 15 y 25 min suele rendir mejor en tiempo de visualización | **14–22 min** como objetivo; los temas grandes pueden llegar a 30 min |
| 3–5 Shorts | Viable, porque reutilizan investigación y recursos | 3 Shorts por documental al principio, repartidos en los días entre estrenos; subir a 5 si las métricas lo justifican |
| Shorts de 20–60 s | Correcto | 35–60 s, cada uno con mini-arco propio: pregunta → giro → revelación |
| Formato extra | — | Un **"Expediente"** público por episodio (página web o publicación con las fuentes). Genera confianza, posicionamiento en buscadores y es nuestra prueba de autenticidad ante YouTube |

---

## 2. Investigación de competencia

**Limitación:** no fue posible consultar estadísticas en vivo de YouTube desde este entorno. Las cifras de suscriptores no se incluyen, salvo las que citan las fuentes, porque cambian a diario.

### 2.1 Referentes en español

| Canal | Modelo | Fortaleza | Debilidad / hueco que deja |
|---|---|---|---|
| Memorias de Pez | Divulgación rápida y comunitaria | Una de las comunidades de historia en español más grandes; formato ágil | Profundidad limitada; poco foco en las fuentes |
| Academia Play | Animación educativa | Claridad y volumen | Orientación escolar; poco suspenso narrativo |
| La Cuna de Halicarnaso | Presentador carismático | Entretenimiento y personalidad | Depende de la persona; no es documental cinematográfico |
| Imineo | Documentales largos | Más de 1,5 M de suscriptores (según la fuente); formato documental | Mucho material licenciado o genérico |
| Historia Incomprendida | Narración de hechos poco conocidos | Buena selección de temas | **Criticado públicamente por falta de rigor** ([análisis](https://recapio.com/digest/historia-incomprendida-el-canal-historico-menos-riguroso-by-brigada-antifraude)), lo que demuestra que el público hispano exige rigor |
| Heródoto, El Cubil de Peter, Pero eso es otra historia | Divulgación temática | Nichos fieles | Producción visual modesta |

### 2.2 Referentes en inglés (estándar de calidad a igualar)

| Canal | Qué aprender |
|---|---|
| Fall of Civilizations | Narración lenta y atmosférica, citas de fuentes primarias leídas en voz alta, duraciones largas |
| LEMMiNO | Misterios tratados con rigor y escepticismo; diseño sonoro excelente; publica poco pero cada vídeo es un evento |
| Kings and Generals / Epic History TV | Mapas animados consistentes; series |
| Timeline / History Hit | Producción con historiadores; autoridad institucional |
| Toldinstone, Voices of the Past | Uso explícito de fuentes primarias |

### 2.3 Canales "faceless" con IA

Proliferan y compiten en volumen. YouTube aclaró en julio de 2026 que el contenido **genérico, basado en plantillas o producido en masa** no es monetizable, aunque **el uso de IA por sí mismo no descalifica** ([eWeek](https://www.eweek.com/news/youtube-responds-to-ai-concerns/), [Metricool](https://metricool.com/youtube-ai-content-rules-monetization/), [TheDesk](https://thedesk.net/2026/07/youtube-clamps-down-low-quality-ai-slop/)). **Para nosotros esto es una oportunidad:** la barrera favorece a quien demuestra aporte original. Toda la arquitectura está pensada para dejar evidencia de ese aporte.

### 2.4 Conclusión competitiva

Nadie en español combina estos cuatro rasgos:

1. Estética cinematográfica sobria.
2. Grado de evidencia visible en pantalla.
3. Expediente de fuentes público.
4. Tesis narrativa propia por episodio.

Esa combinación será nuestra firma.

---

## 3. Identidad editorial

**Manifiesto (borrador):**

> Contamos historias reales. Distinguimos lo que sabemos de lo que creemos y de lo que se ha contado. Buscamos el texto que quedó debajo del texto. Preferimos una pregunta honesta a una respuesta espectacular.

**Reglas editoriales (vinculantes para todos los agentes):**

1. Ninguna afirmación factual sin fuente en el expediente.
2. Toda afirmación lleva un **grado de evidencia**: H (hecho documentado), I (interpretación académica), Hp (hipótesis), L (leyenda o no verificado).
3. Las controversias deben ser reales: hay que identificar quién sostiene cada postura y en qué publicación. No se inventa debate.
4. Las teorías marginales se presentan **como** marginales, explicando por qué el consenso las rechaza.
5. Prohibido el *clickbait* falso: título y miniatura deben poder sostenerse con el contenido.
6. Las recreaciones con IA se rotulan siempre como "Recreación" en pantalla; nunca se presentan como fotografía o documento de archivo.
7. Las citas de fuentes primarias se leen textualmente, con traducción indicada.
8. El suspenso se construye con la secuencia real de los hechos, no con datos ocultos al espectador ni con falsas promesas.
9. Cada episodio termina con una conclusión que aporte conocimiento, no con un "¿y tú qué opinas?" vacío.

**Estructura narrativa estándar** (adaptable):

| Acto | Duración (ep. de 18 min) | Función |
|---|---|---|
| Cold open | 0:00–1:00 | Escena concreta + pregunta central |
| Presentación de la versión conocida | 1:00–3:30 | Lo que "todos saben" |
| Grieta | 3:30–6:00 | Primera evidencia que no encaja |
| Investigación | 6:00–13:00 | Fuentes, contexto, contradicciones, voces olvidadas |
| Revelación | 13:00–16:00 | Lo que la evidencia sugiere, con su grado |
| Cierre | 16:00–18:00 | Qué sigue en duda, por qué importa, siguiente pregunta |

---

## 4. Sistema de diferenciación y originalidad

### 4.1 Tres enfoques por tema (obligatorio)

El Investigador entrega una **Ficha de Enfoques** con tres opciones. Cada una tiene:

- pregunta central;
- tesis narrativa;
- evidencias disponibles, con su grado;
- aspectos poco conocidos;
- contradicciones posibles;
- valor diferencial;
- **riesgo de sostenibilidad** (¿hay fuentes suficientes?).

El CEO puntúa (originalidad, sostenibilidad documental, potencial narrativo, potencial de audiencia) y recomienda una. **La aprobación final es suya.**

### 4.2 Motor de diferenciación

Lista de comprobación que el Investigador aplica a cada tema:

- [ ] ¿Qué dice la versión popular? ¿De dónde salió y quién la difundió?
- [ ] ¿Qué dicen las fuentes primarias?
- [ ] ¿Qué dice la investigación académica de los últimos 20 años?
- [ ] ¿Hay contradicciones entre relato y evidencia?
- [ ] ¿Qué personas o perspectivas quedaron fuera?
- [ ] ¿Se relaciona con otro acontecimiento aparentemente independiente?
- [ ] ¿Qué descubrimiento reciente cambió la comprensión del tema?

### 4.3 Control de originalidad

- **Prueba de duplicado:** antes de aprobar un tema, el Investigador lista los 10 vídeos más vistos sobre él (en español y en inglés) y describe su enfoque. El enfoque elegido debe ser explícitamente distinto.
- **Prueba de "valor añadido":** el Auditor verifica que el guion contiene al menos 3 elementos que no aparecen en la página de Wikipedia del tema (fuente primaria citada, investigación reciente, perspectiva olvidada).
- **Prueba de similitud textual:** el guion se compara con las fuentes para detectar paráfrasis cercana o plagio (umbral automático + revisión).

### 4.4 Mecanismo de aportes del propietario: "Cuaderno del Director"

Diseño sencillo, pensado para el MVP:

1. Cada producción tiene un archivo `producciones/<ID>/cuaderno_director.md`, más una tabla `aportes_editoriales` en la base de datos.
2. Usted escribe en lenguaje natural, o con un comando en Claude Code (`/nota PAL-2026-003 "¿Y si el verdadero protagonista es el escriba?"`).
3. El sistema registra cada aporte con:
   - `ID` (p. ej., `DIR-003-07`);
   - `tipo`: pregunta | perspectiva | objeción | idea | decisión;
   - `fecha`;
   - `texto literal` (nunca se reescribe);
   - `estado`: pendiente | integrado | descartado, **con justificación**.
4. **Regla de trazabilidad:** el expediente y el guion incluyen una tabla "Aportes del Director" que indica dónde se integró cada aporte o por qué se descartó. El Auditor rechaza la entrega si algún aporte queda sin respuesta.
5. **Regla de atribución:** los agentes nunca redactan opiniones ni experiencias en su nombre. Si el guion quiere usar su voz ("el director de este canal se preguntó…"), debe citar textualmente un aporte registrado y usted debe aprobarlo.
6. Más adelante, el dashboard tendrá un formulario y un hilo de comentarios por producción.

---

## 5. Arquitectura de los ocho agentes

### 5.1 Principios

- **Separación de funciones:** quien produce no audita; quien gasta no aprueba su propio presupuesto.
- **Contratos explícitos:** cada agente recibe entradas definidas y entrega artefactos con esquema fijo (Markdown + YAML/JSON), guardados en el repositorio y registrados en la base de datos.
- **El cálculo financiero es código, no IA:** el CFO usa scripts deterministas para sumar costos. El modelo solo interpreta y redacta informes. Así se evitan errores aritméticos y dobles conteos.
- **Mínimo privilegio:** cada agente tiene solo las herramientas que necesita (en Claude Code, mediante la lista `tools` de cada subagente).

### 5.2 Ficha de agentes

| # | Agente | Modelo sugerido | Herramientas | Entradas | Entregables | Límite |
|---|---|---|---|---|---|---|
| 1 | **CEO / Orquestador** | Opus 5.5 | Lectura de todo; escritura en `tareas` y `decisiones`; invocación de subagentes | Informes de todos los agentes, aportes del Director | Plan semanal, priorización, Ficha de decisión, escalamientos | No aprueba temas, enfoques, videos ni gastos extraordinarios: **los propone al Director** |
| 2 | **Investigador Histórico** | Opus 5.5 | Búsqueda y lectura web, APIs académicas (OpenAlex, Crossref, Europeana, Internet Archive, Wikimedia), Zotero | Tema, aportes del Director | Informe de oportunidades, Ficha de 3 enfoques, **Expediente de Investigación**, bibliografía | Toda afirmación con fuente y grado H/I/Hp/L |
| 3 | **Guionista / Director Creativo** | Opus 5.5 | Lectura del expediente; escritura de guiones | Expediente aprobado, enfoque aprobado | Escaleta, guion con marcas de fuente por párrafo, títulos (5 opciones), hooks, CTA | **Prohibido usar información fuera del expediente**; si falta un dato, crea una "solicitud de investigación" |
| 4 | **Productor Audiovisual / Prompt Engineer** | Sonnet 5.5 | APIs de imagen, vídeo y voz; búsqueda en archivos de dominio público; registro de recursos | Guion aprobado, biblia visual del canal | Storyboard, prompts versionados, imágenes, clips, narración, **registro de licencias** | Presupuesto por producción; las recreaciones se marcan como tales |
| 5 | **Editor / Distribuidor** | Sonnet 5.5 (orquesta scripts de FFmpeg y Remotion) | FFmpeg, Remotion, generación de subtítulos, plantillas de miniatura | Recursos + guion + narración | Máster 4K/1080p, subtítulos ES (y EN opcional), 3 miniaturas para pruebas A/B, metadatos, 3–5 Shorts | No publica: sube a YouTube como **privado** |
| 6 | **Auditor / QC** | Opus 5.5 con instrucciones y contexto independientes (no ve el razonamiento de los productores, solo los entregables) | Solo lectura + verificación de fuentes | Todos los entregables | Informe de auditoría: aprobado / con correcciones / rechazado, con hallazgos numerados | Puede bloquear; no corrige por sí mismo |
| 7 | **Analista de Métricas** | Sonnet 5.5 | YouTube Analytics API (solo lectura) | Métricas | Informe semanal, experimentos propuestos, informe postmortem a los 7 y 28 días | Solo lectura |
| 8 | **CFO / Cost Controller** | Haiku 5.5 para redactar; **scripts para calcular** | Lectura del libro de costos, facturas de proveedores | Registros de uso, facturas | Informe por vídeo, informe mensual, alertas | Puede **congelar** una producción que supere su presupuesto |

> **Nota sobre modelos:** la elección de modelo por agente es una decisión de costo y calidad que le corresponde a usted. La tabla es mi recomendación inicial: Opus en las tareas donde el rigor y el criterio importan más, Sonnet/Haiku en tareas operativas. Se medirá y ajustará (Fase 8).

### 5.3 Coordinación

- **MVP:** Claude Code como entorno de ejecución. El CEO es la sesión principal e invoca a los demás como **subagentes** (archivos `.claude/agents/<agente>.md`, cada uno con su prompt, modelo y herramientas permitidas). Se comunican **solo a través de artefactos** (archivos + base de datos), no de memoria compartida. Así todo queda auditable.
- **Fase 8 (operación desatendida):** las tareas programadas, como el informe semanal de métricas o el informe mensual del CFO, pasan a ejecutarse sin que usted abra una sesión, con el *Claude Agent SDK* en un servidor propio o con *Claude Managed Agents* (Anthropic aloja el bucle y el entorno; es beta y cobra tiempo de sesión además de tokens). Lo decidiremos con datos reales de uso.

---

## 6. Flujo de producción

**Estados posibles de cada tarea:** `pendiente → en_curso → entregado → en_revisión → aprobado | correcciones | rechazado → cerrado`.
Cada tarea registra: responsable, estado, fechas (creación, inicio, entrega, límite), entradas (IDs de artefactos), entregables (IDs), costo acumulado y decisión asociada.

| # | Etapa | Responsable | Entradas | Entregable | Puerta |
|---|---|---|---|---|---|
| 1 | Investigación de oportunidades | Investigador | Pilares, métricas, aportes | Informe de 8–10 temas candidatos | — |
| 2 | Presentación de temas | CEO | Informe | Ficha de decisión con 3–5 recomendados | — |
| 3 | Selección del tema | **Director (usted)** | Ficha | Decisión registrada | 🔒 Humana |
| 4 | Tres perspectivas | Investigador | Tema aprobado | Ficha de 3 enfoques | — |
| 5 | Observaciones editoriales | **Director** | Ficha | Aportes en el Cuaderno | — |
| 6 | Aprobación de la perspectiva | **Director** (el CEO recomienda) | Ficha + aportes | Tesis aprobada | 🔒 Humana |
| 7 | Investigación profunda | Investigador | Tesis | Notas de investigación | — |
| 8 | Expediente de fuentes | Investigador → revisión rápida del Auditor | Notas | Expediente v1 | Auditoría de fuentes |
| 9 | Guion | Guionista | Expediente | Escaleta → guion v1 | — |
| 10 | Storyboard | Productor | Guion | Storyboard por plano | — |
| 11 | Prompts | Productor | Storyboard + biblia visual | Prompts versionados | — |
| 12 | Producción audiovisual | Productor | Prompts | Recursos + registro de licencias | Límite de presupuesto (CFO) |
| 13 | Edición | Editor | Recursos | Máster v1 + subtítulos + metadatos | — |
| 14 | Auditoría independiente | Auditor | Todo | Informe de auditoría | 🔒 Auditoría |
| 15 | Correcciones | Responsables señalados | Informe | v2… | Máximo 2 ciclos; después, escala al CEO |
| 16 | Aprobación humana | **Director** | Máster + informe de auditoría + informe de costos | Aprobación | 🔒 Humana |
| 17 | Publicación | Editor sube como privado → **usted programa o publica** | Aprobación | Vídeo publicado | 🔒 Humana |
| 18 | Shorts | Editor | Máster | 3–5 Shorts (auditoría ligera + aprobación en bloque) | 🔒 Humana (en bloque) |
| 19 | Métricas | Analista | Analytics | Informes a 48 h, 7 días y 28 días | — |
| 20 | Informe financiero | CFO | Libro de costos | Informe por vídeo | — |
| 21 | Retroalimentación | CEO | Informes 19–20 | "Lecciones" que actualizan prompts y biblias (cambios versionados) | Cambios relevantes los aprueba el Director |

**Tiempo estimado por episodio** (con la automatización madura): de 5 a 8 días de calendario, más unas **2–3 h de su tiempo** repartidas en las cuatro puertas.

---

## 7. Arquitectura técnica

```
┌──────────────────────────────── Director (usted) ────────────────────────────────┐
│  Claude Code (sesión)  ·  Dashboard (aprobaciones, notas, métricas, costos)      │
└───────────────┬──────────────────────────────────────────────────┬───────────────┘
                │                                                  │
        ┌───────▼────────┐  subagentes   ┌──────────────────────────▼────────────┐
        │ CEO/Orquestador ├─────────────►│ Investigador · Guionista · Productor  │
        └───────┬────────┘               │ Editor · Auditor · Analista · CFO     │
                │                        └───────┬──────────────┬────────────────┘
                │                                │              │
   ┌────────────▼────────────┐   ┌───────────────▼───┐   ┌──────▼──────────────────┐
   │ Base de datos (SQLite →  │   │ Repositorio Git   │   │ Adaptadores de proveedor│
   │ Postgres): producciones, │   │ (prompts, guiones,│   │ (imagen, vídeo, voz,    │
   │ tareas, artefactos,      │   │ expedientes,      │   │ música, YouTube) — cada │
   │ costos, licencias,       │   │ biblias, código)  │   │ llamada se registra en  │
   │ decisiones, aportes      │   └───────────────────┘   │ el libro de costos      │
   └────────────┬────────────┘                            └──────┬──────────────────┘
                │                                                │
        ┌───────▼────────┐                          ┌────────────▼────────────┐
        │ Almacenamiento │◄─────────────────────────┤ Render: FFmpeg, Remotion│
        │ de objetos     │   recursos y másteres    └─────────────────────────┘
        │ (local + R2)   │
        └────────────────┘
```

**Decisiones clave y por qué:**

| Decisión | Por qué |
|---|---|
| Python como lenguaje de pipeline | Mejor ecosistema para FFmpeg, Whisper, APIs de Google y análisis de datos |
| Todo proveedor detrás de un **adaptador** | Cambiar de Veo a Kling (o de ElevenLabs a otro) sin tocar los agentes. Además, el adaptador es el único lugar donde se registra el costo, lo que garantiza que no haya llamadas sin contabilizar |
| SQLite en el MVP → Postgres (Supabase o Neon) al escalar | Cero mantenimiento al inicio; la migración es directa |
| `channel_id` en todas las tablas | Multicanal desde el primer día, sin mezclar métricas, presupuestos ni producciones |
| Carpeta por canal `canales/<slug>/` | Biblia editorial, biblia visual, voz, paleta y prompts base **separados por identidad** |
| Subida a YouTube **siempre como privado** | Garantiza por diseño que ningún agente publique |
| Secretos fuera del repositorio | Ver §13.5 |

**Estructura del repositorio propuesta:**

```
estudio/
├─ .claude/agents/            # 8 definiciones de subagentes
├─ canales/palimpsesto/       # biblia editorial, visual, voz, plantillas
├─ producciones/PAL-2026-001/ # expediente, guion, storyboard, cuaderno_director, auditoría
├─ pipeline/                  # adaptadores de proveedores, render, subida
├─ finanzas/                  # tarifas versionadas, libro de costos, informes
├─ dashboard/
└─ db/                        # esquema y migraciones
```

---

## 8. Comparación de proveedores y herramientas

> Los precios son orientativos (noviembre de 2026). **Ninguna herramienta externa está incluida en Claude Code:** todas se pagan aparte.

### 8.1 Modelos de lenguaje (Claude, precios oficiales por millón de tokens)

| Modelo | Entrada | Salida | Lectura de caché | Uso propuesto |
|---|---|---|---|---|
| Claude Opus 5.5 | $4 | $20 | $0.20 | CEO, Investigador, Guionista, Auditor |
| Claude Sonnet 5.5 | $2 | $10 | $0.10 | Productor, Editor, Analista |
| Claude Haiku 5.5 | $0.10 | $0.50 | — | CFO (redacción), clasificaciones masivas |
| Claude Fable 5.2 | $8 | $40 | $0.20 | No recomendado de entrada (costo) |

**Suscripción frente a API (decisión importante):**

| Opción | Costo | Ventaja | Desventaja |
|---|---|---|---|
| **Claude Max** (suscripción a Claude Code) | ≈ US$100 o US$200/mes (verificar) | Costo fijo predecible; ideal en desarrollo y MVP | Tiene límites de uso; para el CFO es un **costo fijo prorrateado**, no por token |
| **API con clave** (Claude Console) | Pago por token | Costo exacto por producción; necesario para automatizaciones desatendidas | Variable; requiere límites de gasto en la consola |

**Recomendación:** Max durante el desarrollo y el MVP (Fases 1–5). A partir de la Fase 7, API para tareas programadas. El CFO registra ambas modalidades sin mezclarlas (§9).

### 8.2 Investigación

| Herramienta | Costo | Uso |
|---|---|---|
| Búsqueda y lectura web de Claude Code | Incluida en el uso de Claude | Exploración general |
| OpenAlex, Crossref, Semantic Scholar | Gratis (API) | Artículos académicos, DOI, citas |
| Internet Archive, HathiTrust, Gallica (BnF), Biblioteca Digital Hispánica, PARES, Europeana, Library of Congress | Gratis | **Fuentes primarias digitalizadas** |
| Zotero | Gratis (300 MB) / ≈ US$20/año con 2 GB | Bibliografía verificable y exportable |
| JSTOR / Google Scholar | Sin API oficial | Consulta asistida; enlaces en el expediente |

### 8.3 Imágenes

| Opción | Precio ≈ | Calidad para historia | Recomendación |
|---|---|---|---|
| **Archivos de dominio público** (Wikimedia Commons, Met Open Access, Rijksmuseum, Smithsonian Open Access CC0, Library of Congress) | Gratis | Auténtica, la máxima credibilidad | **Prioridad 1**: es nuestro rasgo documental |
| Gemini 3.1 Flash Image ("Nano Banana 2") | ≈ $0.067/imagen 1K, ≈ $0.10 2K; −50 % en batch | Muy buena, edición consistente | **Recomendado para recreaciones** |
| Flux 2 pro (Black Forest Labs) | ≈ $0.03/MP | Muy buena, cinematográfica | Alternativa o complemento |
| Gemini 3.1 Flash-Lite Image | ≈ $0.034/imagen | Buena | Para storyboards y bocetos |

Nota: Imagen 4 de Google está retirado (agosto de 2026); no se recomienda.

### 8.4 Vídeo generado

| Opción | Precio ≈ por segundo | Comentario |
|---|---|---|
| Veo 3.1 Lite / Fast (Google) | $0.03–0.10 | **Recomendado**: buena relación calidad/precio y API estable |
| Kling 3.0 | $0.03–0.11 según proveedor | Alternativa sólida |
| Runway gen4 turbo / gen4.5 | $0.05 / $0.12 | Buen control; más caro |
| Sora 2 API | — | **Se cierra el 24-sep-2026**: descartado |

**Estrategia de costo y estilo:** el vídeo generado **solo para el 10–15 % del metraje** (planos clave). El resto, movimiento sobre imágenes (Ken Burns, parallax 2.5D), mapas animados y documentos de archivo. Así se abarata y además se ve más "documental", menos "IA genérica".

### 8.5 Voz

| Opción | Precio ≈ | Comentario |
|---|---|---|
| **ElevenLabs** Creator / Pro | ≈ $22/mes (unos 100–121 mil caracteres) / ≈ $99/mes (500–600 mil) | Mejor calidad en español; derechos comerciales en planes de pago. **Recomendado: Creator en el MVP y Pro desde la cadencia semanal** |
| Google Cloud TTS / Azure Speech | ≈ $16–30 por millón de caracteres | Más barato, menos expresivo |
| Fish Audio u otras | Variable | Alternativa económica |
| **Narrador humano** (su voz o un locutor contratado) | Locutor: ≈ US$50–200 por episodio | **La señal de autenticidad más fuerte ante la política de contenido inauténtico.** Opción a considerar en serio |

Un episodio de 18 min tiene unas 2.500 palabras, unos 15 mil caracteres. Con tomas repetidas son unos 25–30 mil por episodio, más los Shorts.

### 8.6 Música y efectos

| Opción | Precio ≈ | Comentario |
|---|---|---|
| **Epidemic Sound** o **Artlist** | ≈ US$10–20/mes (plan creador, verificar) | Licencia clara para YouTube, Content ID gestionado. **Recomendado** |
| YouTube Audio Library | Gratis | Útil como complemento |
| Música generada por IA (Suno, Udio, ElevenLabs Music) | ≈ $10–30/mes | **No en el MVP:** licencias y litigios recientes con discográficas hacen que la procedencia sea menos clara |

### 8.7 Edición y render

| Herramienta | Costo | Uso |
|---|---|---|
| **FFmpeg** | Gratis | Ensamblaje, mezcla, codificación, reencuadre vertical para Shorts |
| **Remotion** (vídeo programático con React) | Gratis para individuos y empresas pequeñas (verificar licencia) | Títulos, mapas animados, rótulos de grado de evidencia, plantillas de marca |
| WhisperX / whisper.cpp | Gratis (local) | Alineación de subtítulos con el guion |
| DaVinci Resolve | Gratis | Retoque manual opcional (corrección de color, ajustes finos) |
| Máquina de render | Su computador o un VPS (≈ $10–40/mes) | Un episodio de 18 min se renderiza en minutos u horas según el hardware |

### 8.8 Datos, almacenamiento y panel

| Componente | MVP | Escala |
|---|---|---|
| Base de datos | SQLite (gratis) | Postgres (Supabase o Neon, ≈ $0–25/mes) |
| Almacenamiento | Disco local + **Cloudflare R2** (≈ $0.015/GB-mes, sin costo de salida) | Igual, con política de ciclo de vida |
| Copia de seguridad | Repositorio Git privado (GitHub, gratis) + R2 | Igual |
| Dashboard | **Streamlit** (Python, local, gratis) | Next.js + autenticación, si hay más personas |

### 8.9 YouTube

| API | Costo | Notas |
|---|---|---|
| YouTube Data API v3 | Gratis, cuota diaria por defecto de 10.000 unidades | Subir un vídeo consume mucha cuota (≈ 1.600 unidades, a verificar): unas 6 subidas al día, más que suficiente. **Los proyectos no verificados suben vídeos bloqueados como privados** hasta superar una auditoría de Google. Encaja con nuestro diseño (usted publica manualmente) y la auditoría se puede solicitar más adelante |
| YouTube Analytics API | Gratis | Permiso `yt-analytics.readonly`; ingresos con `yt-analytics-monetary.readonly` |
| YouTube Reporting API | Gratis | Informes masivos diarios (Fase 7) |

---

## 9. Seguimiento de tokens y costos

### 9.1 Modelo de datos (núcleo)

```
canales(id, slug, nombre, presupuesto_mensual, moneda)
producciones(id "PAL-2026-001", canal_id, titulo, estado, presupuesto_autorizado, duracion_final_s)
recursos(id, produccion_id, tipo [imagen|clip|voz|musica|short...], proveedor, licencia, procedencia, archivo)
tarifas(proveedor, producto, unidad, precio_unitario, moneda, vigente_desde, vigente_hasta, fuente_url)
libro_costos(
  id, canal_id, produccion_id, short_id NULL, agente, etapa,
  proveedor, modelo_o_producto,
  tokens_entrada, tokens_salida, tokens_cache_escritura, tokens_cache_lectura,
  unidades, unidad,                         -- p. ej., 15000 caracteres, 8 s de vídeo, 1 imagen
  costo_usd, tipo_costo [real|estimado|prorrateado],
  tarifa_id, id_externo, hash_dedupe UNIQUE, factura_id NULL, timestamp)
facturas(id, proveedor, periodo, total, archivo)
presupuestos(canal_id, mes, monto, umbral_alerta_pct)
alertas(id, nivel, mensaje, produccion_id, timestamp, resuelta)
```

### 9.2 Reglas

1. **Tokens ≠ dólares.** El costo se calcula como `tokens × tarifa vigente del modelo y proveedor` a partir de la tabla `tarifas` versionada. Si cambia un precio, se añade una fila nueva y los registros antiguos conservan la tarifa con la que se calcularon.
2. **Captura en origen:**
   - **API de Claude:** cada respuesta trae `usage` (entrada, salida, escritura y lectura de caché). Se registra por llamada.
   - **Claude Code:** en modo no interactivo (`claude -p --output-format json`) devuelve el uso y un costo estimado por ejecución. En sesiones interactivas se usa la telemetría OpenTelemetry de Claude Code. Con suscripción Max, el token se registra (para medir eficiencia), pero el costo en dólares es **prorrateado**: cuota mensual ÷ producciones del mes, ponderado por los tokens de cada producción.
   - **Otros proveedores:** el adaptador registra unidades (imágenes, segundos, caracteres) y el ID de solicitud del proveedor.
3. **Real, estimado y prorrateado:**
   - *Estimado*: calculado al momento por el adaptador.
   - *Real*: conciliado contra la factura o el panel del proveedor (mensual).
   - *Prorrateado*: suscripciones y costos fijos repartidos.
4. **Anti-doble conteo:** `hash_dedupe = hash(proveedor + id_externo)`, con restricción UNIQUE. Al conciliar, el costo *estimado* se **reemplaza** por el *real*; nunca se suman. Una suscripción se prorratea una sola vez por mes, mediante un trabajo único con marca de periodo.
5. **Asociación obligatoria:** ninguna llamada a un proveedor se ejecuta sin `produccion_id`. Lo que no pertenece a una producción va a `GENERAL-<canal>-<mes>`.
6. **Alertas automáticas:**
   - 80 % del presupuesto de la producción → aviso.
   - 100 % → **bloqueo** de nuevas generaciones; solo usted puede ampliarlo (presupuesto extraordinario).
   - 90 % del mensual → aviso a usted.
7. **Límites también del lado del proveedor:** se configuran topes de gasto en cada consola (Anthropic, Google Cloud, etc.) como segunda barrera.

### 9.3 Informes

- **Por vídeo:** identificador, título, duración, tokens por agente y modelo, costo por agente, por proveedor y por etapa (investigación, guion, audiovisual, edición, auditoría), costo de los Shorts, total, **costo por minuto terminado**, presupuesto frente a real (desviación en % y razón).
- **Mensual:** presupuesto, gasto acumulado, promedio por documental y por Short, proveedor más costoso, consumo por modelo, fijos frente a variables, ingresos (si los hay) y rentabilidad estimada, y recomendaciones (p. ej., "subir la proporción de archivo de dominio público", "mover la redacción de metadatos a Haiku", "aumentar los aciertos de caché").

---

## 10. Presupuesto inicial (estimación, en USD)

### 10.1 Puesta en marcha (única)

| Concepto | Costo ≈ |
|---|---|
| Dominio .com + .co (año 1) | $12 + $25–35 |
| Registro de marca SIC, 2 marcas × clase 41 | ≈ COP 2.4–2.7 M (≈ US$600–680), a verificar |
| Asesoría de propiedad industrial (opcional) | COP 0.5–1.5 M |
| Llave de seguridad física para la cuenta Google (recomendada, 2 unidades) | $50–60 |
| **Total mínimo sin marcas** | **≈ $100** |
| **Total con marcas** | **≈ $700–1.100** |

### 10.2 Mensual: costos fijos

| Concepto | MVP (bisemanal) | Cadencia semanal |
|---|---|---|
| Claude Max | $100 | $200 |
| ElevenLabs | $22 | $99 |
| Música (Epidemic Sound o Artlist) | ≈ $15 | ≈ $15 |
| Almacenamiento R2 + repositorio | ≈ $2 | ≈ $5 |
| Dominio prorrateado | ≈ $4 | ≈ $4 |
| **Subtotal fijo** | **≈ $143** | **≈ $323** |

### 10.3 Variable por documental de unos 18 min

| Concepto | Bajo | Esperado | Alto |
|---|---|---|---|
| Imágenes generadas (60–150 con repeticiones) | $4 | $10 | $20 |
| Vídeo generado (90–180 s útiles × 3 intentos) | $10 | $30 | $70 |
| Tokens de API (si no se usa Max) | $10 | $20 | $40 |
| Shorts (3–5: reencuadre + algunas imágenes nuevas) | $3 | $8 | $15 |
| **Total variable** | **$27** | **$68** | **$145** |

### 10.4 Total mensual estimado

- **Meses 1–2** (2 documentales/mes): ≈ $143 + 2 × $68 ≈ **$280/mes**.
- **Mes 3 en adelante** (4 documentales/mes): ≈ $323 + 4 × $68 ≈ **$600/mes**.

**Límites propuestos:** ~~US$400 / US$700 / US$120~~ → **revisados (DEC-005, ver `03_DECISIONES_Y_ACTIVOS.md`):** tope mensual de **US$150** (meses 1–2) y **US$300** (desde el mes 3). Tope por producción de **US$50**. Cualquier excedente requiere su aprobación.

### 10.5 Realismo sobre ingresos

El Programa de Socios de YouTube exige 1.000 suscriptores y 4.000 horas de visualización en 12 meses (o 10 M de vistas de Shorts en 90 días). **Lo prudente es planificar 6 a 12 meses sin ingresos publicitarios.** El RPM de historia en español suele ser bajo comparado con el inglés; el canal hermano en inglés es la principal palanca de rentabilidad a medio plazo. El CFO calculará el punto de equilibrio con datos reales.

---

## 11. Calendario de lanzamiento de 90 días

| Semana | Hitos |
|---|---|
| **S1** | Aprobación del naming → verificación de disponibilidad → creación de la cuenta Google, seguridad y canal (§13.1–13.4). Reserva de handles y dominios |
| **S2** | Biblia editorial y visual del canal. Identidad visual v1 (logo, banner, plantillas). Fase 2: definiciones de agentes y base de datos |
| **S3** | Fase 3: Investigador y Guionista funcionando. **Episodio piloto 0** (interno, no se publica): tema, enfoques, expediente, guion |
| **S4** | Fase 4: pipeline audiovisual y edición del piloto 0. Calibración de costos reales |
| **S5** | Fase 5: Auditor y CFO operativos. Auditoría completa del piloto 0 → lecciones. Arranque de los episodios 1 y 2 |
| **S6** | Episodios 1 y 2 terminados (colchón). Tráiler del canal. Google Cloud + OAuth (§13.6–13.8) |
| **S7 — Lanzamiento (≈ día 45)** | Publicación del episodio 1 + tráiler + 3 Shorts. Expediente público |
| **S8** | Shorts del episodio 1. Producción del episodio 3 |
| **S9** | Episodio 2 + Shorts. Primer informe a 7 días |
| **S10** | Fase 7: dashboard v1 + métricas automáticas |
| **S11** | Episodio 3. Revisión: ¿hay 2 episodios en reserva? → decidir el paso a cadencia semanal |
| **S12** | Episodio 4 (si se pasa a semanal) |
| **S13 (día 90)** | Informe trimestral: métricas, costos, calidad, decisiones para el siguiente trimestre (incluido el canal en inglés) |

**Meta realista a 90 días:** 4–5 documentales publicados, 12–20 Shorts, sistema completo funcionando y costos medidos con datos reales.

---

## 12. Plan de desarrollo por fases

| Fase | Alcance | Criterio de aceptación | Estimación |
|---|---|---|---|
| **1. Estrategia y arquitectura** | Este documento + naming | Aprobación del Director | ✅ Entregado (pendiente de aprobación) |
| **2. Agentes y coordinación** | 8 definiciones de subagentes, esquema de base de datos, sistema de tareas y estados, Cuaderno del Director, registro de decisiones | Una producción "en seco" recorre los 21 estados con artefactos simulados | 3–5 días |
| **3. Investigación y guiones** | Investigador con APIs académicas, Ficha de 3 enfoques, Expediente, Guionista con trazabilidad de fuentes por párrafo | Expediente y guion del piloto 0 aprobados por usted | 4–6 días |
| **4. Audiovisual y edición** *(MVP termina aquí + Fase 5)* | Adaptadores de imagen, vídeo y voz, búsqueda en archivos de dominio público, registro de licencias, render con FFmpeg y Remotion, subtítulos, miniaturas | Piloto 0 renderizado en 1080p con subtítulos | 6–10 días |
| **5. Auditoría y finanzas** | Auditor con lista de comprobación completa (§14), libro de costos, tarifas, alertas, bloqueo por presupuesto, informe por vídeo | Informe de auditoría + informe financiero del piloto 0 con conciliación | 3–5 días |
| **6. Shorts y distribución** | Generador de Shorts con arco propio, metadatos, subida privada a YouTube | 3 Shorts del piloto 0 + subida privada de prueba | 3–4 días |
| **7. Dashboard y métricas** | Streamlit: producciones, agentes, tareas, costos, alertas, decisiones, métricas; integración con la Analytics API | Panel en uso con datos reales | 4–6 días |
| **8. Optimización y escala** | Pruebas A/B de miniaturas, ajuste de modelo y esfuerzo por agente, caché, ejecución desatendida (Agent SDK o Managed Agents), segundo canal | Costo por minuto −20 % sin pérdida de calidad; segundo canal aislado | Continuo |

Las estimaciones son de trabajo efectivo conmigo e incluyen su tiempo de revisión. Al final de cada fase le presento una demo y pido aprobación antes de pasar a la siguiente.

---

## 13. Configuración de cuentas y activos digitales (paso a paso)

> **Cuándo:** **solo después** de aprobar los nombres (Semana 1). Las secciones 13.6–13.8 (Google Cloud y OAuth) se hacen en la **Semana 6**, cuando el pipeline las necesite.
> **Regla absoluta:** usted crea y controla todas las cuentas. Nunca me comparta contraseñas, códigos 2FA ni códigos de recuperación; tampoco claves API en el chat.

### 13.1 Cuenta Google raíz (≈ 20 min, gratis)

1. En una ventana de incógnito, abra `accounts.google.com/signup` → "Para mí" (o "Para mi trabajo o empresa"; ambas sirven).
2. Nombre: el de la marca (p. ej., "Ostraka Studio"). Use datos reales del titular (usted) para la recuperación.
3. Dirección: la aprobada (p. ej., `ostrakastudio@gmail.com`). Si está ocupada, use la siguiente de la lista del informe de naming.
4. Contraseña: única, de más de 16 caracteres, guardada en un **gestor de contraseñas** (Bitwarden, gratis; o 1Password, ≈ US$3/mes).

### 13.2 Seguridad y recuperación (≈ 20 min)

1. `myaccount.google.com/security`:
   - Verificación en dos pasos → **llaves de acceso (passkeys)** y, si es posible, **dos llaves físicas** (YubiKey o Titan); una se guarda fuera de casa.
   - Como respaldo: app autenticadora.
   - Evite el SMS como único método.
2. Teléfono y correo de recuperación: el suyo personal, no otro de la empresa.
3. Imprima los **códigos de respaldo** y guárdelos físicamente. No los fotografíe ni los suba a la nube.
4. Opcional, pero recomendado para canales que monetizan: inscribirse en el **Programa de Protección Avanzada** de Google.
5. Configure el **Administrador de cuentas inactivas** (designa un heredero de los activos).

### 13.3 Canal de YouTube como cuenta de marca (≈ 15 min)

1. Inicie sesión en YouTube con la cuenta raíz → foto de perfil → "Crear un canal".
2. Si YouTube ofrece crear un canal con **nombre de empresa u otro nombre** (cuenta de marca), elíjalo: permite añadir administradores sin compartir la contraseña y transferir la propiedad en el futuro.
3. Nombre: el aprobado (p. ej., "Palimpsesto"). Handle: el reservado (p. ej., `@palimpsestohistoria`).
4. Verifique el canal por teléfono (`youtube.com/verify`) para habilitar vídeos largos, miniaturas personalizadas y transmisiones en vivo.

### 13.4 YouTube Studio: configuración inicial

- Configuración → Canal: país (Colombia), palabras clave, idioma predeterminado (español).
- Configuración de subida predeterminada: visibilidad **Privado**, categoría "Educación", idioma español, licencia estándar.
- **Contenido alterado o sintético:** se declara por vídeo durante la subida (ver §14).
- Comentarios: retener los potencialmente inapropiados para revisión.
- Permisos (Configuración → Permisos): usted es **Propietario**. Si en el futuro se incorporan personas, rol **Editor** o **Visualizador**, nunca Propietario. **Los agentes no tienen rol en Studio:** actúan solo vía API con permisos limitados (§13.7).

### 13.5 Gestión de secretos (antes de la Fase 4)

| Nivel | Mecanismo |
|---|---|
| MVP | Archivo `.env` **fuera** del repositorio, o en él pero listado en `.gitignore`, con permisos `600`. Se genera desde un `.env.example` sin valores |
| Recomendado | **Gestor de secretos** (1Password CLI o Bitwarden Secrets Manager) que inyecta variables al ejecutar. Las claves no viven en disco |
| Producción | Google Secret Manager / Doppler |

Reglas complementarias:

- Una clave por proveedor y por canal, con **límite de gasto** configurado en cada consola.
- Las instrucciones de los agentes **nunca** contienen claves.
- El repositorio tiene un escáner de secretos (gitleaks) como gancho previo al commit.
- El token OAuth de YouTube se guarda cifrado. Revocarlo desde `myaccount.google.com/permissions` corta el acceso al instante.

### 13.6 Proyecto de Google Cloud (Semana 6, ≈ 15 min, gratis)

1. `console.cloud.google.com` con la cuenta raíz → crear el proyecto `ostraka-produccion`.
2. Facturación: **no hace falta** para las API de YouTube. Si más adelante se usan Gemini o Veo por Google Cloud, se activa con **alertas de presupuesto** (Facturación → Presupuestos y alertas).
3. APIs y servicios → Biblioteca → habilitar **YouTube Data API v3** y **YouTube Analytics API** (más adelante, YouTube Reporting API).

### 13.7 OAuth 2.0 con mínimo privilegio

1. Pantalla de consentimiento OAuth: tipo "Externo", estado "En pruebas". Añada su cuenta raíz como usuario de prueba.
2. Credenciales → crear un ID de cliente OAuth de tipo "App de escritorio". Descargue el JSON y guárdelo **en su gestor de secretos**, no en el chat ni en el repositorio.
3. Permisos solicitados (los mínimos):
   - `youtube.upload`: subir (siempre como privado);
   - `youtube.readonly`: leer el canal;
   - `yt-analytics.readonly`: métricas;
   - `yt-analytics-monetary.readonly`: ingresos, cuando haya monetización.
   - **No** se solicita el permiso completo `youtube`, que permitiría borrar o editar.
4. Usted ejecuta una vez el flujo de autorización en su navegador. El sistema guarda solo el *refresh token* cifrado.
5. Atención: en modo "En pruebas", los tokens caducan cada 7 días. Antes del lanzamiento se pasa la app a "En producción" (sin verificación para uso propio, aunque Google puede pedirla) o se renueva el token semanalmente.

### 13.8 Integración con el sistema multiagente

- Solo el adaptador `pipeline/youtube.py` usa el token. Los agentes piden "subir el borrador X" y el adaptador comprueba que exista una aprobación humana registrada para subidas que no sean privadas. En el MVP **ni siquiera existe código para publicar**.
- **Multicanal:** cada canal tiene su propia cuenta de marca, su propio token OAuth (con una etiqueta `channel_id`) y su propio presupuesto. Para el segundo canal se puede usar el mismo proyecto de Cloud; cuando haya muchos canales, un proyecto por canal aísla las cuotas.
- **Inventario de activos:** el archivo `activos_digitales.md` registra cuentas, handles, dominios, servicios, titular, fecha de creación y dónde se guarda cada credencial (el *dónde*, nunca el valor).

---

## 14. Políticas y cumplimiento de YouTube (lista de control del Auditor)

**Fuente principal a consultar en cada revisión:** páginas oficiales de *Políticas de monetización del Programa de Socios*, *Pautas de la comunidad*, *Divulgación de contenido alterado o sintético* y *Pautas de contenido apto para anunciantes* (la redacción cambia; el Auditor guarda la fecha de la versión consultada).

| Área | Verificación |
|---|---|
| **Contenido inauténtico** | ¿Hay aporte original demostrable (tesis, expediente propio, narrativa)? ¿No es una plantilla repetida? ¿Los episodios difieren entre sí en estructura visual y narrativa? |
| **Contenido reutilizado** | ¿El material de terceros (archivo, citas) está transformado y comentado, no solo expuesto? ¿Proporción razonable? |
| **Derechos de autor** | Cada recurso tiene licencia y procedencia en `recursos`. Dominio público verificado según la jurisdicción (atención: una fotografía de una obra antigua puede tener derechos propios en algunos países). Las citas textuales son breves y atribuidas |
| **Música** | Licencia vigente al momento de publicar; certificado o ID de licencia guardado; canal registrado en la biblioteca de música (Epidemic o Artlist) para evitar reclamos de Content ID |
| **Imágenes** | Origen (archivo / IA / licencia de stock) y prompt guardado si es IA. Sin marcas de agua ajenas. Sin parecido engañoso con personas reales vivas |
| **Voces** | Voz IA con derechos comerciales del plan. **No clonar voces de personas reales** sin consentimiento escrito. La voz IA no imita a personajes históricos con grabaciones existentes |
| **Contenido sintético y declaraciones de IA** | Activar la casilla de *contenido alterado o sintético* cuando haya recreaciones realistas de personas, lugares o eventos que puedan confundirse con material real. Rótulo "Recreación" en pantalla y nota en la descripción ("Este documental contiene recreaciones visuales generadas con IA. Las fuentes están en…") |
| **Apto para anunciantes** | Violencia histórica sin gore gratuito; lenguaje; temas sensibles (genocidios, esclavitud) tratados con contexto educativo y sin imágenes gráficas en la miniatura ni en los primeros 30 s |
| **Miniaturas y títulos** | Sin engaño: lo prometido aparece en el vídeo. Sin imágenes que se presenten como fotografías reales si son IA |
| **Subtítulos** | Sincronía, ortografía y nombres propios verificados contra el expediente |
| **Exactitud histórica** | Muestra de al menos el 20 % de las afirmaciones H/I verificadas contra la fuente original; el 100 % de las cifras, fechas y citas textuales |

---

## 15. Información y decisiones que necesito de usted

**Bloqueantes para avanzar (Semana 1):**

1. **Naming:** ¿aprueba *Ostraka* / *Palimpsesto* (o cuáles otros)? Ver `02_INFORME_NAMING.md` §9.
2. **Verificación de disponibilidad:** ¿la hace usted (unos 30 min, con la lista de comprobación) o habilita en su entorno el acceso de red a YouTube, registradores de dominio, SIPI (SIC) y WIPO para que lo haga yo?
3. **Presupuesto:** ¿acepta los topes propuestos (US$400 al mes en los meses 1–2, US$700 desde el mes 3, US$120 por producción)?
4. **Claude:** ¿qué plan tiene hoy? ¿Acepta Max en el MVP y API más adelante?

**Necesarias antes de la Fase 3:**

5. **Voz del canal:** ¿IA (ElevenLabs), su propia voz o un locutor contratado? *Mi recomendación:* probar IA en el piloto 0 y evaluar un locutor humano antes del lanzamiento.
6. **Mercado y acento:** ¿español neutro latinoamericano? ¿Foco geográfico preferido?
7. **Temas:** ¿tiene una lista de temas que le apasionan o que quiere evitar? ¿Hay límites en temas sensibles (religión, política contemporánea, conflictos recientes)?
8. **Su tiempo:** ¿cuántas horas por semana puede dedicar a las aprobaciones? Esto determina la cadencia real.

**Necesarias antes del lanzamiento:**

9. **Titular legal:** ¿persona natural o una sociedad (SAS)? Afecta al registro de marca, a AdSense y a los impuestos. Le recomiendo consultarlo con un contador.
10. **Registro de marca:** ¿desde el inicio (recomendado, al menos clase 41 para el canal) o tras validar?
11. **Equipo de render:** ¿qué computador usará (sistema operativo, GPU, espacio en disco)? ¿O prefiere un servidor en la nube?
12. **Rostro y presencia:** ¿quiere aparecer alguna vez en cámara o como "el Director" en los créditos? Reforzaría la autenticidad y la marca.

---

### Fuentes principales de este documento

- Precios de Claude: referencia oficial de Anthropic (caché del 3-nov-2026).
- Política de contenido inauténtico: [eWeek](https://www.eweek.com/news/youtube-responds-to-ai-concerns/) · [Metricool](https://metricool.com/youtube-ai-content-rules-monetization/) · [TheDesk](https://thedesk.net/2026/07/youtube-clamps-down-low-quality-ai-slop/) · [OutlierKit](https://outlierkit.com/blog/youtube-updates-july-2026)
- ElevenLabs: [Activepieces](https://www.activepieces.com/blog/elevenlabs-pricing-2026-plans-credits-and-costs) · [BigVU](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/) · [Toolradar](https://toolradar.com/tools/elevenlabs/pricing)
- Vídeo IA: [DevTK](https://devtk.ai/en/blog/ai-video-generation-pricing-2026/) · [Costbench](https://www.costbench.com/compare/kling-api-vs-runway-api/) · [Skila / dev.to](https://dev.to/skilaai/google-just-made-ai-video-50-cheaper-openai-killed-sora-heres-the-new-pricing-math-1ag4)
- Imagen IA: [InVideo – AI image model pricing](https://invideo.io/blog/ai-image-model-pricing/) · [ecorpit](https://ecorpit.com/ai-image-generation-api-cost-comparison-2026/)
- Competencia: [Educación 3.0](https://www.educaciontrespuntocero.com/recursos/canales-youtube-aprender-historia/) · [Pulzo](https://www.pulzo.com/tecnologia/youtube-5-canales-conocer-historia-mundo-PP1442935A) · [Recapio – Brigada Antifraude](https://recapio.com/digest/historia-incomprendida-el-canal-historico-menos-riguroso-by-brigada-antifraude) · [Vidpros](https://vidpros.com/best-history-youtube-channels/)
- SIC y Niza: [Uniandes](https://derecho.uniandes.edu.co/wp-content/uploads/2025/09/Como-Registrar-mi-Marca.pdf) · [Colombia Move](https://colombiamove.com/blog/registrar-marca-colombia-sic-costos-clases-busqueda/) · [Nexo Legal](https://nexo.legal/es/nice-classification-colombia-brand/)
