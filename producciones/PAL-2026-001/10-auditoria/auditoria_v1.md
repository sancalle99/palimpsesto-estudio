# Auditoría · PAL-2026-001 · Etapa 10 (auditoría integral) · v1

**Auditor independiente · 18-nov-2026** · Entregables: `06-guion/guion.md` v1.1 y `titulos.md`; `05-expediente/expediente.md` v3; `07-storyboard/storyboard.md` v1.2; `09-edicion/montaje.json`, `metadatos.md`, `shorts.json`, `miniaturas.json`; `render/master.mp4` (9:22, 1920×1080, 25 fps), `subtitulos.srt`, `capitulos.txt`, `shorts/S1–S4`, `miniaturas/A–C`; tabla `recursos` (R0001–R0012); aportes DIR-01 a 03.
**Veredicto: CORRECCIONES** · 0 bloqueantes · 3 mayores · 8 menores.

## Alcance y método
- Vídeo: 57 fotogramas (uno cada 10 s) del máster; 1 cada 4 s de cada Short; las 3 miniaturas. Sonoridad medida con ffmpeg `ebur128`.
- Búsquedas web: 3 de 8. Dominios inaccesibles en esta sesión: `support.google.com` (política oficial de contenido sintético, no se pudo leer el texto literal; consulta del 18-nov-2026) y, según las auditorías previas, `en.wikipedia.org`.
- No se repiten las verificaciones de las auditorías del expediente v1–v3 (AF-002, 004, 008, 009, 010, 012, 015, 016, 017, 018, 019, 020/020b, 021).

## Lista de control (resumen)
| Bloque | Estado | Nota |
|---|---|---|
| A. Cifras, fechas y citas | Conforme | 100 % de cifras y fechas del guion cotejadas con el expediente y sus auditorías: 14-abr-1229, siglo X, 90°, 1906, 1910–1915, años veinte, 4 retratos, 1938, 29-oct-1998, 2.000.000 / 2.202.500 USD, 1999–2008, 2008 CC BY 3.0, siglos II–III, prop. 14, 14 piezas, 2003, 536 × 32 = 17.152, "casi un siglo", "casi ocho siglos" (1229→2008). **Nuevo:** el 331 a. C. de Lane Fox (◌ en AF-015) queda verificado: Horváth, *Acta Antiqua* (2025), resume a Lane Fox (*ZPE*) fechando *Contra Diondas* en junio–julio del 331 a. C. No hay citas textuales de fuentes; las frases entre comillas son leyendas rotuladas (L) |
| A. Párrafos ↔ AF y grados | Conforme | Cada párrafo cita AF-…; grados coherentes en narración y rótulos (●, ◐, ○, ✕). Ver HAL-05 y HAL-06 |
| B. Originalidad | Conforme | Elementos ausentes del relato estándar: crítica de *Physics Today*; debate 334/331 a. C.; reserva sobre el recuento del *Stomachion*; matiz del fallo por *laches* ("no decidió si fue robado"); leyenda del limón desmentida. Enfoque distinto al de la competencia (ficha de enfoques). Sin paráfrasis cercana detectada. (No se pudo abrir Wikipedia para el cotejo literal) |
| C. Derechos | Conforme con reserva | R0001–R0011 CC BY 3.0 con URL de origen; R0012 voz Kokoro (Apache-2.0), sin imitar a nadie. Ver HAL-08 |
| D. Contenido sintético | Conforme | 0 imágenes IA (DIR-02); ninguna recreación sin rótulo. No declarar la casilla es defendible (narración sintética que no imita a una persona real; se indica en la descripción). Revisar el texto oficial cuando el dominio sea accesible |
| E. Anunciantes | Conforme | Sin contenido sensible; miniaturas veraces (todo lo que muestran aparece en el vídeo) |
| F. Audio | Conforme | −16,5 LUFS integrados, pico real −1,4 dBTP, LRA 2,9 LU; mono 48 kHz. Sin música (DIR-03) |
| F. Capítulos | Conforme | Coinciden con el SRT (0:53, 1:54, 3:27, 5:41, 8:05) y con la descripción |
| F. Ritmo, subtítulos, Shorts | No conforme | HAL-02, HAL-03, HAL-04, HAL-09 |
| G. Director | Conforme | DIR-01 (piloto ≈ 11 min; el máster dura 9:22, dentro de lo aceptado), DIR-02 (sin IA) y DIR-03 (sin música) integrados; no se atribuye al Director ninguna opinión |

## Hallazgos

**HAL-01 · mayor · 9:01–9:06 (CTA) y `metadatos.md` (descripción) · El vídeo promete algo que la descripción no cumple.**
Evidencia: la narración dice "Las fuentes de este episodio, con el grado de evidencia de cada afirmación, están en la descripción" (también en el cierre en pantalla). La descripción solo trae 6 fuentes principales y el marcador literal "[enlace al expediente público, pendiente]"; no hay grados por afirmación.
Corrección: antes de la etapa 11, publicar el expediente (o una tabla resumida AF → grado → fuente) y poner el enlace real, o cambiar la locución a "Las fuentes principales están en la descripción". No subir la descripción con el marcador.

**HAL-02 · mayor · Shorts S2, S3 y S4 · No se entienden solos (requisito del plan de Shorts).**
Evidencia: los cortes empiezan con frases que remiten a lo anterior del máster: S2 "Y entonces alguien hizo algo peor" (¿peor que qué?; además no dice de qué libro son "algunas hojas" hasta la última frase); S3 "Esto ya se sabía:" (¿qué?); S4 "El *Stomachion* tiene una historia parecida" (¿a cuál?) y no dice que es de Arquímedes. `shorts.json` declara "narración íntegra del máster, sin texto nuevo", que es la causa.
Corrección: añadir a cada uno una frase de entrada propia (regrabada con la misma voz) que sitúe el tema, p. ej. S2 "En el siglo XX, alguien pintó evangelistas falsos sobre el libro de Arquímedes…"; S3 "¿Cómo descubría Arquímedes sus resultados?"; S4 "Arquímedes dejó un rompecabezas de 14 piezas: el *Stomachion*". Suprimir los arranques anafóricos.

**HAL-03 · mayor · Máster, sobre todo 6:35–8:05 · Ritmo visual: predominio de tarjetas de texto estáticas.**
Evidencia: en el muestreo cada 10 s, ≈ 55 % de los fotogramas son tarjetas de texto sobre fondo negro y ≈ 39 % imágenes de archivo. Entre ≈ 6:35 y 8:05 no aparece ninguna imagen (planos 44–49); tarjetas como "Revisada por pares / Physics Today", "536 × 32 = 17.152" y el resumen H/I/L se mantienen inmóviles 20–30 s. El *Stomachion*, el objeto más visual del bloque B, nunca se muestra (el storyboard preveía las 14 piezas, plano 45). Afecta a la retención y a la diferencia prometida frente a la competencia ("documental cinematográfico"), y una pieza de voz sintética + diapositivas se acerca al perfil que vigila la política de contenido inauténtico de YouTube (vigente desde el 15-jul-2025).
Corrección: (a) gráfico propio de las 14 piezas del *Stomachion* (dibujo vectorial, sin IA; rótulo "Reconstrucción moderna"); (b) intercalar folios ya licenciados (R0004 para la prop. 14, R0002/R0003) bajo las tarjetas del bloque B; (c) limitar cualquier tarjeta fija a ≤ 8 s o animar su entrada por líneas.

**HAL-04 · menor · `subtitulos.srt`, cues 39–41 y otros · Segmentación defectuosa.**
Evidencia: "El filólogo J." / "L." (99 ms) / "Heiberg…": el separador trata las iniciales como fin de frase. 12 de 184 cues duran < 0,8 s ("Lo es.", "importa.", "todo.", "Sidón.", "nosotros?", "fecharlas:") y varias cortan sintagmas ("por" / "fin, leerlo"; "Natalie" / "Tchernetska").
Corrección: no partir tras iniciales; fusionar cues < 1 s con el anterior o el siguiente; mínimo ≈ 1 s y ≤ 42 caracteres por línea. Aplicar lo mismo a los SRT de los Shorts.

**HAL-05 · menor · 8:56, guion §6 · "Y lo publicamos para que cualquiera pueda leerlo."**
Evidencia: la publicación de 2008 la hizo el proyecto del Walters (AF-013). Un "nosotros" en boca del canal puede leerse como que Palimpsesto lo publicó.
Corrección: "Y se publicó para que cualquiera pueda leerlo."

**HAL-06 · menor · 8:31–8:38, guion §6 · "Incluso su fecha se discute" tras nombrar dos discursos.**
Evidencia: el debate 334/331 a. C. (AF-015) es sobre *Contra Diondas*, no sobre ambos. La referencia de Lane Fox sigue ◌ en el expediente (el dato es correcto, ver bloque A).
Corrección: "La fecha de *Contra Diondas* se discute: …". Añadir al expediente la referencia de Lane Fox (*ZPE*) o citar Horváth 2025 (F22) como fuente de ambas posturas.

**HAL-07 · menor · Rótulos de imagen, planos 21 (≈ 2:50) y 50 (≈ 8:20) · Rótulos que afirman más que la fuente.**
Evidencia: el plano 21 rotula "Agua y moho" sobre el fol. 158r-159v, cuando el propio storyboard (v1.1) indica "en el plano 21 no se afirma qué causó cada mancha". El plano 50 rotula "Hipérides: Contra Timandro · Contra Diondas" sobre un único folio (Hype02r), lo que sugiere que contiene ambos discursos.
Corrección: plano 21, "Daños en el pergamino" o sin rótulo; plano 50, "Folio de Hipérides (fol. 145r-144v)".

**HAL-08 · menor · `metadatos.md`, crédito CC BY · Falta indicar que las imágenes están adaptadas.**
Evidencia: los folios se recortan, se reencuadran, se combinan en mosaicos y en las miniaturas llevan texto encima. La CC BY 3.0 (sección 4 b) pide, en las obras derivadas, un crédito que identifique el uso de la obra original.
Corrección: "Imágenes: The Archimedes Palimpsest Project, Walters Art Museum (https://archimedespalimpsest.net), CC BY 3.0; recortadas y con rótulos añadidos por Palimpsesto".

**HAL-09 · menor · Shorts S1–S4 · Legibilidad en vertical.**
Evidencia: el plano 16:9 ocupa solo la franja central (≈ 1/3 del alto) sobre fondo desenfocado; los rótulos pequeños (grados "◐ interpretación académica", créditos, fichas de S3 y S4) son ilegibles en un móvil.
Corrección: reencuadrar las imágenes a 9:16 (recorte o Ken Burns vertical) y rehacer las tarjetas en formato vertical con texto ≥ 48 px.

**HAL-10 · menor · 0:47, guion §1 · "Como siempre en Palimpsesto".**
Evidencia: es el primer episodio del canal; "como siempre" sugiere episodios previos que no existen.
Corrección: "En Palimpsesto contamos siempre tres cosas: …" o "Aquí haremos lo de siempre en este canal: …" solo cuando haya episodios previos.

**HAL-11 · menor · Planos 17–18 (≈ 1:58–2:24), rótulo de fuente · "Fotografía de Heiberg, 1906" es ambiguo.**
Evidencia: puede leerse como un retrato de Heiberg; es una fotografía tomada por él de un folio.
Corrección: "Fotografía tomada por Heiberg en 1906".

## Observaciones sin severidad
- El guion conserva `[RÓTULO: Recreación]` en el cold open y en el *Stomachion*, y los tiempos del storyboard (≈ 11:15) no corresponden al máster (9:22). Conviene actualizar el guion a la versión montada para que el expediente público coincida con el vídeo.
- Miniatura A: el texto "Debajo, Arquímedes" tiene poco contraste sobre el folio procesado; probar un velo oscuro más intenso.

## Condición
Corregir HAL-01 a HAL-03 (y, en la misma pasada, los menores) y volver a enviar a auditoría solo los elementos tocados: descripción, Shorts, tramo 6:35–8:05 del máster y SRT. No hace falta repetir la verificación factual.

## Fuentes consultadas en esta ronda
- Horváth, L., *Acta Antiqua* (2025), sobre la fecha de *Contra Diondas* y la postura de Lane Fox: https://real.mtak.hu/244185/1/068-article-p235.pdf
- YouTube, "Disclosing use of altered or synthetic content" (no accesible desde la sesión): https://support.google.com/youtube/answer/14328491
- Cobertura de la actualización de la política de contenido inauténtico (2-jul-2025, en vigor el 15-jul-2025): https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/
