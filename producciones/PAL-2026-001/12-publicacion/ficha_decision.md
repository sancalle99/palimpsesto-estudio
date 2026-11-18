# Ficha de decisión 🔒 · PAL-2026-001 · Etapa 12: publicación

**CEO · 18-nov-2026** · Etapa 11 aprobada por el Director (título T1, miniatura A, vídeo y 4 Shorts).

## Cuándo (Analista, confianza baja, sin datos del canal todavía)
- **Documental:** sábado 21-nov-2026, 11:00 hora de Bogotá (17:00 Madrid).
- **Shorts:** S1 ese mismo día, 2 h después. S2 el lunes 23, S3 el miércoles 25 y S4 el viernes 27, a las 18:00 de Bogotá.
- Detalle: `12-publicacion/hora_recomendada.md`.

## Cómo (por ahora, a mano)
No hay credenciales de la API de YouTube (Fase 7), así que el Editor no puede subir ni programar. Usted sube en YouTube Studio:

| Campo | Valor |
|---|---|
| Vídeo | `render/master.mp4` (1080p) |
| Título | El libro que se negó a morir: el palimpsesto de Arquímedes |
| Descripción | `12-publicacion/descripcion.txt` (copiar y pegar, con los capítulos incluidos) |
| Miniatura | `render/miniaturas/miniatura_A.jpg` |
| Subtítulos | `render/subtitulos.srt` (español) |
| Categoría · público | Educación · no es contenido para niños |
| Contenido alterado | No |
| Etiquetas | ver `09-edicion/metadatos.md` |
| Visibilidad | Programado para la fecha y hora de arriba (o la que usted elija) |

## Su decisión
- `APRUEBO PAL-2026-001 12`: autoriza la publicación en la fecha recomendada (la ejecuta usted a mano). Cuando haya API, el Editor programaría con `youtube_subir.py programar`.
- `CORRECCIONES PAL-2026-001 12 <otra fecha u hora>`
- `RECHAZO PAL-2026-001 12 <motivo>`
