# Correcciones a la auditoría v1 · PAL-2026-001 · etapa 10

**Editor y Guionista · 18-nov-2026** · Elementos tocados (los únicos que se reenvían a auditoría).

| Hallazgo | Qué cambió | Dónde |
|---|---|---|
| HAL-01 | La locución dice ahora "Las fuentes principales de este episodio, y el grado de evidencia de lo que contamos, están en la descripción". La descripción lista cada afirmación con su grado y sus fuentes numeradas (19). El marcador "pendiente" se ha retirado | `06-guion/guion.md` §6 · `09-edicion/metadatos.md` · plano 52 |
| HAL-02 | Shorts v2: cada uno tiene una frase de entrada propia y se narra aparte con la misma voz | `09-edicion/shorts.json` · `render/shorts/` |
| HAL-03 | Tramo de las secciones 5 y 6: diagrama propio del *Stomachion* (14 piezas, rótulo "Reconstrucción moderna"), folios intercalados y tarjetas sobre fondo de folio. Toda tarjeta de más de 8 s entra línea a línea | `09-edicion/montaje.json` (planos 44a–48a) · `scripts/montaje.py` |
| HAL-04 | Subtítulos: no se separan las iniciales, ningún subtítulo dura menos de 1 s y las líneas tienen como máximo 42 caracteres. En los Shorts, como máximo 22 | `render/subtitulos.srt` · `scripts/montaje.py` (pruebas en `tests/test_montaje.py`) |
| HAL-05 | "Y se publicó para que cualquiera pueda leerlo." | guion §6 |
| HAL-06 | "La fecha de *Contra Diondas* se discute…". Lane Fox queda referido vía Horváth 2025 (F22) | guion §6 · `05-expediente/expediente.md` AF-015 |
| HAL-07 | Plano 21: "Daños en el pergamino" · Plano 50: "Folio de Hipérides (fol. 145r-144v)" | `montaje.json` |
| HAL-08 | Crédito: "…CC BY 3.0; recortadas, combinadas y con rótulos añadidos por Palimpsesto" | `metadatos.md` · plano 52 |
| HAL-09 | Shorts compuestos en 9:16 nativo: imágenes a cuadro completo y textos de 48 px o más | `shorts.json` · `scripts/shorts.py` |
| HAL-10 | "En Palimpsesto contamos siempre tres cosas: …" | guion §1 |
| HAL-11 | "Fotografía tomada por Heiberg en 1906" | planos 17–18 |
| Observación | Se retiran del guion las marcas `[RÓTULO: Recreación]` (el vídeo no tiene imágenes IA). Los capítulos de la descripción coinciden con el nuevo máster (9:24) | guion · `metadatos.md` |

**Geometría del Stomachion:** reconstrucción moderna habitual sobre una retícula de 12 × 12, con coordenadas de J. Burkardt, `stomachion.plot` (FSU, 2006). La prueba comprueba que son 14 piezas y que las áreas suman 144.
**No cambia:** la miniatura (la observación de contraste de la A queda para la elección en la etapa 11).
