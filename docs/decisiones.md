# Registro de decisiones y activos digitales

> Inventario de cuentas y servicios. **Aquí nunca se anotan contraseñas, códigos ni claves**: solo *dónde* están guardados.

## Registro de decisiones

| ID | Fecha | Decisión | Decidió | Estado |
|---|---|---|---|---|
| DEC-001 | 17-nov-2026 | Canal principal: **Palimpsesto** | Director | ✅ Aprobada (canal creado) |
| DEC-002 | 17-nov-2026 | Cuenta Google raíz: `astrakastudio@gmail.com` (corregido por el Director el 18-nov) | Director | ✅ Creada, 2FA con llave activa |
| DEC-003 | 18-nov-2026 | Marca matriz: grafía pendiente (el correo usa **Astraka**; el concepto original era *Ostraka*) | Director | ⏳ Pendiente de confirmar |
| DEC-004 | 17-nov-2026 | Plan de Claude actual: **Pro** | Director | ✅ Registrado |
| DEC-005 | 18-nov-2026 | Topes: US$150/mes (meses 1–2), US$300/mes (desde mes 3), US$50 por producción | Director | ✅ Aprobada |
| DEC-006 | 17-nov-2026 | Verificación de disponibilidad automatizada (dominios y YouTube) | Claude | ✅ Hecha |
| DEC-007 | 18-nov-2026 | Sin dominio web por ahora: foco exclusivo en YouTube y su monetización | Director | ✅ Aprobada |
| DEC-008 | 18-nov-2026 | Canal confirmado: Palimpsesto · @Palimpsestostudio · UCqGznx_OIKoZWTrORoe4xcw | Director | ✅ Verificado |
| DEC-009 | 18-nov-2026 | Arquitectura aprobada; inicio de la Fase 2 | Director | ✅ Aprobada |
| DEC-0014 | 18-nov-2026 | Flujo de **13 etapas** (antes 21); puertas 🔒 2, 4, 11 y 12; PAL-2026-001 migrada con `migrar-13` sin perder historial | Director | ✅ Aplicada |
| DEC-0015 | 18-nov-2026 | Título: el Guionista propone 5 (etapa 6), el Editor elige con la miniatura (9) y el Director aprueba (11) | Director | ✅ Aplicada |
| DEC-0016 | 18-nov-2026 | El Editor sube en privado (`scripts/youtube_subir.py`) y solo publica o programa tras `APRUEBO <ID> 12`; el Analista recomienda la hora. Credenciales de la API (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN): en `.env` o gestor de secretos, Fase 7 | Director | ✅ Aplicada · ⏳ credenciales Fase 7 |

## Inventario de activos

| Activo | Identificador | Titular | Creado | Credencial guardada en | Pendientes |
|---|---|---|---|---|---|
| Cuenta Google raíz | astrakastudio@gmail.com | Propietario | nov-2026 | Gestor de contraseñas del propietario | 2FA con llave ✅ · códigos de respaldo impresos (confirmar) |
| Canal de YouTube | Palimpsesto · @Palimpsestostudio · UCqGznx_OIKoZWTrORoe4xcw | Cuenta raíz | nov-2026 | — (acceso vía la cuenta raíz) | Verificar por teléfono; configuración de Studio §13.4 |
| Dominio | — | — | — | — | Aplazado (DEC-007) |
| Proyecto de Google Cloud | — | — | — | — | Semana 6 |

## Presupuesto revisado (DEC-005, propuesta)

Supuestos: Claude Pro, prioridad máxima a imágenes de archivo de dominio público, vídeo IA limitado a 30–60 s por episodio y música de la YouTube Audio Library al inicio.

| Concepto | Meses 1–2 (2 documentales/mes) | Desde el mes 3 (cadencia semanal) |
|---|---|---|
| Claude | Pro, ≈ $20 | Pro ≈ $20 o Max ≈ $100, según los límites de uso reales |
| ElevenLabs | Creator, ≈ $22 | Creator, ≈ $22 (Pro solo si hace falta) |
| Música | $0 (YouTube Audio Library) | ≈ $15 (Epidemic Sound o Artlist) |
| Almacenamiento | ≈ $0–2 | ≈ $5 |
| **Fijos** | **≈ $44** | **≈ $62–142** |
| Variable por documental (imágenes, vídeo, Shorts) | ≈ $15–35 | ≈ $15–35 |
| **Total esperado** | **≈ $75–115/mes** | **≈ $160–280/mes** |
| **Tope mensual propuesto** | **US$150** | **US$300** |
| **Tope por producción** | **US$50** | **US$50** |
| Aviso | Al 80 % | Al 80 % |
| Bloqueo | Al 100 %; solo el Director lo amplía | Al 100 %; solo el Director lo amplía |

**Aviso sobre Claude Pro:** el plan Pro tiene límites de uso más bajos para Claude Code (ventanas de uso que se reinician cada pocas horas y acceso más limitado a los modelos más potentes). Para el desarrollo del sistema y la investigación profunda es probable alcanzar esos límites. No hace falta cambiar ahora: el CFO medirá el uso real durante el piloto y solo se recomendará Max si el límite frena la producción.

## Resultados de la verificación automática (17-nov-2026)

Método: RDAP oficial del registro (.com: Verisign; .studio: Identity Digital) y consulta directa a youtube.com. "Registrado" quiere decir que lo tiene alguien; "libre" quiere decir que el registro no tiene datos, y se confirma al comprarlo.

| Dominio | Estado |
|---|---|
| ostraca.com · ostraka.com · palimpsesto.com · ostraca.studio | 🔴 Registrados |
| ostracastudios.com · ostracastudio.com · ostrakastudio.com | 🟢 Libres |
| palimpsestoestudios.com · palimpsestohistoria.com · palimpsestodocs.com | 🟢 Libres |
| ostraka.studio · palimpsesto.studio | 🟢 Libres |
| Cualquier .co | ⚪ No verificable (el registro .co no ofrece RDAP público; hay que mirarlo en un registrador) |

| Handle de YouTube | Estado |
|---|---|
| @palimpsesto | 🟡 Ocupado por un canal pequeño e inactivo (28 suscriptores, 2 vídeos). No hay conflicto relevante |
| @ostraca | Ocupado (canal religioso, 56 suscriptores) |
| @ostraka | Ocupado (banda de metal escocesa, 25 suscriptores) |
| @PalimpsestoEstudios | ⚠️ No se encuentra públicamente. Hay que confirmar en YouTube Studio que el handle quedó guardado |
| @ostracastudios · @palimpsestohistoria · @palimpsestodocs | 🟢 Libres |

| Red | Estado |
|---|---|
| Instagram / TikTok | ⚪ No verificables automáticamente (Instagram exige iniciar sesión; TikTok responde igual exista o no la cuenta). Comprobación manual |
| SIC (SIPI) / WIPO | ⚪ Comprobación manual: son aplicaciones web con sesión |
