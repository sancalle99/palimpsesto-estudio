# Auditoría · PAL-2026-001 · Etapa 10 (auditoría integral) · v2 (re-auditoría, ciclo 2 de 2)

**Auditor independiente · 18-nov-2026** · Alcance: solo lo tocado según `correcciones_v1.md`: `09-edicion/metadatos.md`, `shorts.json`; `06-guion/guion.md` §1 y §6 y `recursos/audio/narracion.txt`; `render/master.mp4` (9:23,6), `subtitulos.srt`, `capitulos.txt`; `render/shorts/S1–S4` (.mp4 y .srt); `scripts/montaje.py` (STOMACHION) y `tests/test_montaje.py`.
**Veredicto: APROBADO** · 0 bloqueantes · 0 mayores · 5 menores (no impiden aprobar; se recomienda corregirlos antes de la etapa 11/12).

## Método
- Máster: fotogramas cada 5 s de 6:30 a 8:10 (21), y fotogramas de los planos 17, 18, 21, 50 y 52 (tarjeta final). Shorts: 1 fotograma cada 4 s, más comprobaciones puntuales.
- SRT analizados por script (duración mínima, longitud de línea, solapes, iniciales).
- Geometría del *Stomachion*: `python3 -m unittest tests.test_montaje` (4/4 OK) y rasterizado propio de las 14 piezas en malla 240 × 240: 0 huecos, 0 solapes; áreas {3,3,6,6,6,6,9,12,12,12,12,12,21,24}/144, el perfil clásico de la disección.
- Búsquedas web: 0. No se repite la verificación factual del expediente.

## Estado de los hallazgos de la v1
| v1 | Estado | Evidencia |
|---|---|---|
| HAL-01 (mayor) | Resuelto | Locución y plano 52: "fuentes principales… grado de evidencia… en la descripción". La descripción lista 13 afirmaciones con grado y 19 fuentes numeradas; sin marcador "pendiente". Grados coherentes con el expediente (AF-016b Hp → ○; AF-018/019/020 I → ◐; AF-021/002b L → ✕; fecha de *Contra Diondas* ◐, como en AF-015). Ver HAL-01 nuevo |
| HAL-02 (mayor) | Resuelto | S1–S4 arrancan con frase propia y se entienden solos; el texto nuevo (S2 "En el siglo XX, alguien pintó…"; S3 "¿Cómo descubría Arquímedes…?"; S4 "En el palimpsesto se conserva el *Stomachion*, una obra de Arquímedes…") está respaldado por AF-008, AF-017 y AF-014/020 con el grado correcto en pantalla |
| HAL-03 (mayor) | Resuelto | 6:30–8:10: folio de *El Método* (6:35), tarjetas sobre fondo de folio, diagrama de 14 piezas con rótulo "RECONSTRUCCIÓN MODERNA · INTERPRETACIÓN DE NETZ" (6:55–7:30, con despiece y retícula), folio 110r-105v (7:40). Las tarjetas largas entran línea a línea (plano 48). Ningún tramo de > 10 s sin cambio visual |
| HAL-04 (menor) | Resuelto en lo esencial | "J. L. Heiberg" ya no se parte; ningún cue < 1 s (máster y Shorts). Restos en HAL-03 nuevo |
| HAL-05, 06, 10 | Resueltos | Guion §1 y §6 = `narracion.txt` (cotejo por script: sin diferencias) |
| HAL-07 | Resuelto | Plano 21 "Daños en el pergamino"; plano 50 "Folio de Hipérides (fol. 145r-144v)" |
| HAL-08 | Resuelto | Crédito CC BY con "recortadas, combinadas y con rótulos añadidos por Palimpsesto" en la descripción; en la tarjeta final, versión breve "recortadas y rotuladas" (suficiente con la descripción completa) |
| HAL-09 | Resuelto en lo esencial | Shorts 1080×1920 nativos, imágenes a cuadro completo, tarjetas legibles. Restos en HAL-04 nuevo |
| HAL-11 | Resuelto | Planos 17–18: "Fotografía tomada por Heiberg en 1906" |
| Capítulos | Conforme | Descripción = `capitulos.txt` (0:00, 0:54, 1:55, 3:28, 5:42, 8:06), coherentes con el SRT (cue 36 a 1:55,7) |

## Hallazgos nuevos

**HAL-01 · menor · `metadatos.md`, descripción, línea del *Stomachion* · "17.152 con simetrías" simplifica de más.**
Evidencia: AF-020b: el factor 32 combina las simetrías del cuadrado **y** el intercambio de piezas iguales; la narración lo dice bien.
Corrección: "536 soluciones; 17.152 contando simetrías e intercambio de piezas iguales".

**HAL-02 · menor · `metadatos.md`, cabecera y pie (no se suben) · Datos internos desfasados.**
Evidencia: "publica el Director (etapa 17)", "aprobación del vídeo (etapa 16)" usan la numeración de 21 etapas (hoy 11 y 12, DEC-0014); "Pendientes: la música (DIR-03)" contradice DIR-03 (sin música), ya integrado.
Corrección: actualizar a etapas 11/12 y retirar el pendiente de música.

**HAL-03 · menor · `subtitulos.srt` y SRT de los Shorts · Longitud de línea y cortes.**
Evidencia: máster, cues 15 y 49 con líneas de 43 caracteres (> 42). Shorts: el tope declarado de 22 caracteres no se cumple (líneas de 23–27 en S1, S2, S3 y S4; p. ej. S1 cue 10 "noventa grados. Sobre ellas", 27). Varios cues terminan en preposición o artículo ("dejó al" / "final"; "tratados de" / "Arquímedes"; "Arquímedes sus" / "resultados?").
Corrección: forzar el tope en `partir()` y evitar cortar tras preposición o artículo.

**HAL-04 · menor · Shorts, rótulos verticales.**
Evidencia: S1 ≈ 0:14–0:20, el diagrama "hoja / hoja cruzada" sale como una tira estrecha que invade la cabecera y, sin la leyenda (suprimida en vertical), no se entiende el giro de 90°. Notas partidas con huérfana: "Debajo: Arquímedes, siglo / X" (S1), "Evangelista falsificado, siglo / XX" (S2). S2 ≈ 0:24–0:31: "Rayos X: el texto bajo la pintura" aparece sobre la miniatura pintada antes de que entre la imagen de rayos X (≈ 0:31, visible ~2 s) y tapa el crédito de la imagen. S4: el rótulo "RECONSTRUCCIÓN MODERNA" queda pegado al borde del diagrama (legible).
Corrección: rehacer el diagrama de la hoja en 9:16; acortar las notas ("Debajo: Arquímedes (s. X)"; "Evangelista falso, s. XX"); en S2, mostrar la nota solo con la imagen de rayos X y darle ≥ 3 s; separar nota y crédito.

**HAL-05 · menor · `06-guion/guion.md`, cabecera y recuento · Restos de la versión anterior.**
Evidencia: la línea de marcas aún lista `[RÓTULO: Recreación]`; los encabezados y el recuento siguen en ≈ 11 min/11:15 frente al máster de 9:24 (observación ya hecha en la v1).
Corrección: retirar la marca y ajustar tiempos al montaje si el guion se publica con el expediente.

## Sin errores nuevos introducidos en lo tocado
Narración = guion; grados de la descripción coherentes con el expediente; créditos CC BY presentes; *Stomachion* rotulado como reconstrucción moderna y geométricamente correcto; ninguna imagen IA; el texto nuevo de los Shorts no añade afirmaciones fuera del expediente.

## Condición
Aprobado para pasar a la etapa 11. HAL-01 a HAL-04 son correcciones de una pasada que conviene aplicar antes de la subida pública (etapa 12); no requieren nueva auditoría.
