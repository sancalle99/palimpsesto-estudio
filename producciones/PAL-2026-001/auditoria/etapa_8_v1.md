# Auditoría · PAL-2026-001 · Etapa 8 (expediente de fuentes) · v1

**Auditor independiente · 18-nov-2026 · Entregable:** `expediente.md` (A005) · **Lista:** secciones A y G.
**Veredicto: CORRECCIONES** (0 bloqueantes · 5 mayores · 7 menores).

## Alcance y límites
- Consultas web: 8 (límite del modo económico). Resolución DNS bloqueada en esta sesión para `archimedespalimpsest.org` (F7, F13, F16), `physicstoday.aip.org` (F15) y `historyofinformation.com` (F5): **no se pudieron abrir directamente**; se contrastaron mediante buscador, Crossref y resultados indexados. Hay que permitir esos dominios para una verificación directa en la v2.
- Verificado (cifras/fechas/nombres): AF-002, AF-004, AF-008, AF-009, AF-010, AF-015, AF-016, AF-020; muestreo de fuentes: F2, F5, F6, F12, F13 (vía literatura), F15, F16 (vía literatura). Muestreo H/I ≥ 20 % (11 de 20 AF H/I).
- Sección G: `python -m estudio aportes PAL-2026-001` no devuelve aportes; el cuaderno está vacío. Conforme: no se atribuye nada al Director.

## Verificaciones conformes
| AF | Resultado |
|---|---|
| AF-002 | Colofón de Ioannes Myronas, 14-abr-1229: conforme con F2 y la literatura estándar |
| AF-004 | Heiberg, 1906, Constantinopla, lupa y fotografías; edición 1910–1915: conforme |
| AF-009 | Subasta Christie's Nueva York **29-oct-1998** (Wikipedia, History of Information, Reuters). Demanda del Patriarcado de Jerusalén; la jueza Kimba Wood falló a favor de Christie's por *laches* (prescripción por demora). El pendiente n.º 2 puede cerrarse con "29 de octubre de 1998" |
| AF-010 | Martillo 2 M USD; 2.202.500 USD con comisión (Reuters): conforme |
| AF-012 | Fluorescencia de rayos X en SLAC (U. Bergmann): conforme |
| AF-015 | Debate de datación de *Contra Diondas* real: Horváth, "in defence of the date January–March 334 BC", *Acta Antiqua* 65 (2026), doi:10.1556/068.2025.00234; Rhodes, *BICS* 52 (2009) 223–228, doi:10.1111/j.2041-5370.2009.tb00757.x |
| AF-019 | La reseña de *Physics Today* existe y critica el "hype" del libro (ver HAL-08) |
| AF-021 | Correctamente rotulada L |

## Hallazgos

**HAL-01 · mayor · AF-020 · Atribución y grado de la cifra del Stomachion.**
Evidencia: la cifra de 17.152 es correcta, pero no la contó "su equipo" (de Netz): la determinaron Persi Diaconis, Susan Holmes, Ronald Graham y Fan Chung (análisis) y la confirmó por ordenador William (Bill) Cutler en 2003 (página de Fan Chung, UCSD; Wikipedia "Ostomachion"; NYT, dic. 2003). Hay además 536 soluciones distintas salvo rotación/reflexión (268 si también se identifican las piezas iguales). Un recuento matemático no es una "I".
Corrección: dividir en (a) "Netz interpreta el Stomachion como problema combinatorio" (I, F16) y (b) "17.152 disposiciones; 536 esencialmente distintas; calculadas por Diaconis, Holmes, Graham, Chung y Cutler" (H, con fuente primaria o NYT). Quitar el "◌" cuando esté verificado.

**HAL-02 · mayor · AF-020 · Cita textual sin fuente.**
Evidencia: "no sé si él lo resolvió correctamente" se presenta como cita de Netz sin fuente concreta, idioma original ni página. Toda cita textual debe verificarse al 100 %.
Corrección: indicar la fuente exacta (artículo, fecha, página) y el texto original en inglés, o reformularla como paráfrasis atribuida; si no se localiza, eliminarla.

**HAL-03 · mayor · AF-015 / F11 / F12 · Un hecho H sostenido de facto solo por Wikipedia.**
Evidencia: la identificación de Tchernetska en 2002 descansa en F11 (Wikipedia, con un dominio no canónico, `wikipedia.com`) y en F12, cuya referencia está marcada como "◌ comprobar" y que en todo caso es de 2008 (edición de *Contra Diondas*), así que no documenta la fecha de 2002. Crossref no devolvió F12 en la consulta realizada. Esto contraviene el criterio de que una fuente secundaria débil no sostenga sola una afirmación H.
Corrección: completar F12 (Carey, Edwards, Farkas, Herrman, Horváth, Mayer, Mészáros, Rhodes, Tchernetska, *ZPE* 165, 2008, págs.) y añadir una fuente primaria para el hallazgo de 2002 (p. ej., la primera publicación de Tchernetska sobre los fragmentos en *ZPE*, a verificar, o F1/F3, que lo narran). Corregir la URL de F11 a `en.wikipedia.org`.

**HAL-04 · mayor · AF-016 · Controversia de autoría incompleta.**
Evidencia: el expediente solo plantea a Alejandro de Afrodisias como autor. La publicación académica de referencia, Chiaradonna, Rashed y Sedley, "A Rediscovered *Categories* Commentary", *Oxford Studies in Ancient Philosophy* 44 (2013) 129–194, propone a **Porfirio** (posiblemente su *Ad Gedalium*) con fragmentos de Boeto de Sidón. Omitir la atribución principal sesga la controversia.
Corrección: citar ese artículo como fuente y presentar las dos atribuciones (Alejandro / Porfirio), ambas como Hp, atribuidas a sus autores. Revisar la datación "siglos II o III" (sería del III si es de Porfirio).

**HAL-05 · mayor · Alcance de la verificación de fuentes primarias del proyecto (F7, F13, F16).**
Evidencia: tres AF centrales del bloque B (AF-017, AF-018, AF-020) y AF-016 dependen de páginas de `archimedespalimpsest.org` que no se pudieron abrir en esta auditoría, y el propio expediente deja pendiente verificar F16. No hay citas de página ni extractos que permitan comprobar lo que se les atribuye.
Corrección: añadir a cada AF del bloque B un extracto breve (≤ 1 frase) o una referencia de página de la fuente; preferir F1 (edición de Cambridge, 2011) o los artículos de Netz y Saito revisados por pares para AF-018, en lugar de la web divulgativa del proyecto.

**HAL-06 · menor · AF-002 · Grado del "jugo de limón".**
Evidencia: no se cita ninguna fuente que lo proponga como hipótesis académica; circula en divulgación.
Corrección: rotularlo **L** (no verificado), o citar la fuente que lo plantea si se mantiene como Hp.

**HAL-07 · menor · AF-008 · Las dos dataciones no se contradicen.**
Evidencia: "después de 1929" y "después de 1938" son dos *termini post quem* compatibles (el modelo de las falsificaciones y el pigmento, respectivamente); el más restrictivo es 1938. Además, según la literatura, las miniaturas se copiaron de **reproducciones publicadas** de manuscritos de la BnF, no directamente de un manuscrito (a verificar en F8).
Corrección: redactar la nota como "no antes de 1938 (verde ftalocianina)", explicar el origen de 1929 y precisar "copiadas de reproducciones de manuscritos de la BnF" si F8 lo confirma.

**HAL-08 · menor · AF-019 / F15 · Alcance de la crítica de *Physics Today*.**
Evidencia: la reseña existe y critica el "hype" y que el lector pueda atribuir a Arquímedes, por ejemplo, el método de exhaución o la noción de infinito; no se ha podido confirmar que discuta expresamente el "infinito actual" de la proposición 14. No consta autor ni fecha de la reseña en F15.
Corrección: añadir autor y fecha; narrarla como crítica general a la exageración del libro, no como refutación específica de AF-018 (coherente con la nota de prudencia ya incluida).

**HAL-09 · menor · AF-017 · Formulación conceptual imprecisa.**
Evidencia: lo que se sabía desde 1906 es que *El Método* usaba indivisibles y la palanca de forma heurística, mientras que la exhaución usa el infinito potencial en las demostraciones. "Usaba el infinito de forma heurística (la noción de infinito potencial)" mezcla las dos cosas.
Corrección: "Desde Heiberg se sabía que Arquímedes razonaba heurísticamente con indivisibles (*El Método*) y demostraba con el método de exhaución (infinito potencial)".

**HAL-10 · menor · AF-006 · Grado mal aplicado.**
Evidencia: que la familia sostenga una compra en la década de 1920 y que el Patriarcado alegue un robo son **hechos documentados (H)** sobre posiciones enfrentadas (el expediente judicial). No son una interpretación académica (I); la cuestión abierta es cuál de las dos es cierta.
Corrección: H para "cada parte sostiene X", con la cuestión de fondo sin resolver; mantener la obligación de presentar ambas versiones.

**HAL-11 · menor · Sección 4 frente a AF-002 · Nombre y función de Myronas.**
Evidencia: "Ioannes Myronas, sacerdote" (AF-002) frente a "Juan Myronas (escriba)" (sección 4).
Corrección: unificar la grafía (recomendado: Ioannes Myronas) y la función (sacerdote que actuó como copista).

**HAL-12 · menor · AF-009 · Precisión del fallo y fuentes.**
Evidencia: la fecha ya está verificada (29-oct-1998). El fallo fue a favor de Christie's (y de la consignataria) por *laches*, no "a favor de la subasta". F2 y F4 son fuentes secundarias.
Corrección: fijar la fecha, redactar "el tribunal federal falló a favor de Christie's por la demora del demandante en reclamar" y añadir la referencia del caso (*Greek Orthodox Patriarchate of Jerusalem v. Christie's, Inc.*, S.D.N.Y.).

## Pendientes del expediente: estado
1. Cifra del Stomachion: confirmada como 17.152, con la atribución corregida (HAL-01).
2. Fecha de la subasta: 29-oct-1998, cerrable.
3. Licencia de las imágenes (F10): sin verificar en esta etapa; se mantiene para la etapa 12.
4. Equipo de imagen (Easton, Knox, Christens-Barry): coincide con la literatura conocida; sin verificar contra fuente primaria.

## Condiciones para aprobar en la v2
Resolver HAL-01 a HAL-05; los menores pueden resolverse en la misma revisión.
