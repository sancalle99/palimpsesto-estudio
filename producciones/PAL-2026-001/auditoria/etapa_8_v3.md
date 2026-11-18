# Auditoría · PAL-2026-001 · Etapa 8 (expediente de fuentes) · v3

**Auditor independiente · 18-nov-2026 · Entregable:** `expediente.md` v3 (A009) · **Base:** `auditoria/etapa_8_v2.md`.
**Veredicto: APROBADO** (0 bloqueantes · 0 mayores · 3 menores nuevos). Los menores deben cerrarse antes del guion (etapa 9).

## Alcance
- Verificación puntual de AF-020b (HAL-13) y de las filas tocadas por HAL-14 a HAL-16 (AF-009, AF-015, AF-016b, F19 a F24).
- Lecturas web: 2 intentos (Wikipedia "Ostomachion" y la reproducción de F24 en Taipei Times). **Ninguno se pudo hacer:** los dominios en.wikipedia.org y www.taipeitimes.com no resuelven en esta sesión; habría que permitirlos en la configuración de red. F24 no se ha contrastado en línea en esta ronda. Su referencia (Kolata, *NYT*, 14-dic-2003) es coherente con la literatura conocida y la fila no depende solo de ella: las cifras ya se verificaron en F19 (v2).

## Estado de los hallazgos de la v2
| HAL | Sev. | Estado | Comentario |
|---|---|---|---|
| 13 | mayor | **Resuelto en AF-020b** | (a) Se documenta la discrepancia entre F24/Wikipedia y F19 sin dar prioridad a nadie, y el texto para el guion es neutral. (b) Se incluye la reserva sobre el supuesto del cuadrado, los giros y los reflejos, y se dice que el recuento es moderno. (c) F24 se añade con su autora, medio, fecha y la marca ◌ "original no consultado". Queda un resto en la bibliografía: ver HAL-17 |
| 14 | menor | Resuelto | AF-015 indica quién defiende cada fecha (Horváth 334 a. C., F21/F22; Lane Fox 331 a. C., ◌ sin referencia propia), con grado I. F21 sigue ◌ "no consultada directamente": se acepta porque ninguna H depende de ella |
| 15 | menor | Resuelto | F20 se rebaja a [S] y queda ◌ hasta completar la referencia judicial. AF-009 se sostiene (verificado en la v1) |
| 16 | menor | Resuelto | (a) F23 tiene ya las págs. 129–194. (b) Se ha eliminado la valoración "la más reciente y detallada". (c) La atribución a Sharples queda como ◌ "referencia propia", apoyada en F13 y en grado Hp: se acepta como pendiente documentado |
| 08, 12 | menor | Pendientes ◌ aceptados | Según el alcance de esta ronda |

## Hallazgos nuevos

**HAL-17 · menor · Bibliografía, F19 · La entrada repite la atribución que HAL-13 corrigió.**
Evidencia: la F19 dice "Chung, F., 'The Stomachion' (UCSD), que documenta el recuento de Diaconis, Holmes, Graham y Chung (2003) y la confirmación de Cutler" y la clasifica como [S/A]. Según la página (v2), está firmada por Chung **y Graham**, se titula "A tour of Archimedes' stomachion", dice que Cutler "first computed" las 536 y no nombra a Diaconis, a Holmes ni el año 2003. Esto contradice la propia fila AF-020b, y quien redacte el guion podría reintroducir el error.
Corrección: "Chung, F. y Graham, R., 'A tour of Archimedes' stomachion' (UCSD). Atribuye a Bill Cutler el primer cálculo de las 536 teselaciones y da el total de 17.152". Clasificarla como [S] (HAL-13 c).

**HAL-18 · menor · AF-020b · "32 simetrías" es impreciso.**
Evidencia: según F19, el total de 17.152 se obtiene al distinguir **tanto** las simetrías del cuadrado (8) **como** las permutaciones de piezas congruentes. El factor 32 no está formado solo por simetrías.
Corrección: "536 soluciones distintas salvo giros y reflejos; si se cuentan también los giros, los reflejos y el intercambio de piezas iguales, salen 17.152".

**HAL-19 · menor · AF-020b · La reserva sobre el "rectángulo" no tiene fuente concreta.**
Evidencia: "los testimonios antiguos sugieren un rectángulo" no se vincula a ninguna de las fuentes citadas (F19, F24, F16), y esta ronda no ha podido comprobarlo.
Corrección: indicar qué fuente lo dice y en qué testimonio se basa, o rebajarlo a "no sabemos qué forma ni qué objetivo tenía el juego original" (lo que basta para la reserva).

**Observación (sin severidad):** la sección 6 (Pendientes) no recoge los ◌ nuevos de la v3: Lane Fox, Sharples, F20 judicial, F21 y el original de F24. Conviene añadirlos para que la etapa 9 los herede.

## Condición
Aprobado. HAL-17 a HAL-19 se corrigen antes de redactar el guion (etapa 9), sin necesidad de otra auditoría de la etapa 8. Se recomienda volver a intentar la verificación de F24 cuando la red lo permita.
