# Prompts de recreación — PAL-2026-001 · v1 · 18-nov-2026

**Etapa 11 · Productor** · **En reserva** desde el 18-nov-2026 (DIR-PAL-2026-001-02): el piloto se monta sin IA; ver storyboard v1.2 · Origen: `storyboard.md` v1 (planos 01, 03, 17, 25, 38) · Modelo previsto: `gemini-3.1-flash-image` (1K, 16:9) · 4 variantes por prompt

## Bloque fijo de estilo (biblia visual v0, se añade al final de cada prompt)
```
cinematic historical reconstruction, chiaroscuro side lighting, muted earth tones, subtle film grain, 35mm, documentary realism, no text, no watermark
```

## Bloque negativo común
```
no faces, no recognizable people, no logos, no readable writing, no modern objects, no plastic skin, no perfect symmetry, no oversaturated colors, no glow, no fantasy elements
```
Si el modelo no admite un campo negativo, se añade al prompt como "Avoid: …".

## Prompts

| ID | Plano | Prompt (en inglés, por rendimiento del modelo) | Controles de plausibilidad |
|---|---|---|---|
| P-01 | 01 | `Close-up of a scribe's hands writing with a quill on a sheet of old parchment, a small oil lamp beside it, worn wooden desk, dark background, only hands and forearms visible in a plain dark wool sleeve` | Sin rostro ni arquitectura. La escritura queda borrosa e ilegible (no se inventa texto griego). Lámpara de aceite en lugar de vela moderna |
| P-02 | 03 | `Extreme close-up of a small metal blade scraping faded ink from a parchment leaf, fine dust caught in a beam of side light, hands partially visible, dark background` | La herramienta es genérica. **No** se muestran limón ni líquidos (AF-002b es leyenda) |
| P-03 | 17 | `Close-up of a brass magnifying glass held over a yellowed parchment page with faint double layers of writing, daylight from a window at the side, early twentieth-century library desk, only a hand in a dark suit sleeve visible` | Sin rostro: no se recrea a Heiberg. Escritorio de principios del s. XX, sin objetos de época posterior |
| P-04 | 25 | `Empty auction room in low light, a wooden lectern with a gavel in the foreground, rows of empty chairs fading into darkness, late twentieth-century interior` | Sin personas, logotipos ni carteles legibles: no se recrea la sala real de Christie's. Se rotula "Recreación" |
| P-05 | 38 | `A closed, worn medieval book with a dark leather binding resting on a wooden lectern, single candle light from the side, deep shadows, stone wall barely visible` | Libro genérico, sin miniaturas ni texto. Pared sin rasgos identificables (el lugar de Myronas no consta) |

## Reglas de uso
- Todo resultado lleva el rótulo **RECREACIÓN** (esquina inferior izquierda, 60 % de opacidad) y se registra con `python -m estudio recurso PAL-2026-001 imagen --origen ia --licencia "<términos del proveedor>" --proveedor google --prompt "<P-xx v1>" --archivo recursos/…`.
- Se descartan las variantes con rostros, manos deformes, texto legible inventado o anacronismos. Si ninguna de las 4 sirve, se ajusta el prompt (v2, en este mismo directorio) antes de regenerar, y cada regeneración cuenta en el presupuesto.
- Lote completo de la etapa 12: 20 imágenes ≈ 1,34 USD (tarifa por verificar). Antes del lote: `python -m estudio presupuesto-verificar PAL-2026-001 1.50`.
