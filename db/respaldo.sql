BEGIN TRANSACTION;
CREATE TABLE alertas (
  id            INTEGER PRIMARY KEY,
  canal_id      INTEGER REFERENCES canales(id),
  produccion_id TEXT,
  nivel         TEXT NOT NULL,                           -- info | aviso | bloqueo
  mensaje       TEXT NOT NULL,
  creado        TEXT NOT NULL,
  resuelta      INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE aportes (
  id            TEXT PRIMARY KEY,                        -- DIR-PAL-2026-001-03 / DIR-GENERAL-07
  canal_id      INTEGER NOT NULL REFERENCES canales(id),
  produccion_id TEXT REFERENCES producciones(id),
  tipo          TEXT NOT NULL CHECK (tipo IN ('pregunta','perspectiva','objecion','idea','decision')),
  texto         TEXT NOT NULL,
  estado        TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente','integrado','descartado')),
  resolucion    TEXT,                                    -- dónde se integró o por qué se descartó
  resuelto_por  TEXT,
  creado        TEXT NOT NULL,
  resuelto      TEXT
);
CREATE TABLE artefactos (
  id            TEXT PRIMARY KEY,                        -- PAL-2026-001-A007
  produccion_id TEXT NOT NULL REFERENCES producciones(id),
  tarea_id      INTEGER REFERENCES tareas(id),
  tipo          TEXT NOT NULL,                           -- expediente | guion | storyboard | ...
  ruta          TEXT NOT NULL,
  version       INTEGER NOT NULL DEFAULT 1,
  sha256        TEXT,
  autor         TEXT NOT NULL,
  creado        TEXT NOT NULL
);
INSERT INTO "artefactos" VALUES('PAL-2026-001-A001','PAL-2026-001',1,'informe_oportunidades','producciones/PAL-2026-001/etapa01_oportunidades.md',1,'8879288cedf9cb6192edcf4785ede46f200dcd8e4d1b5f725fcb619808d6689c','investigador','2026-11-18T00:17:21+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A002','PAL-2026-001',3,'ficha_decision','producciones/PAL-2026-001/decisiones/etapa_3.md',1,'66a009810d3362e91014b346335a65f49abc452e75eb1c33e32ce2f9fc821054','ceo','2026-11-18T00:17:22+00:00');
CREATE TABLE canales (
  id                     INTEGER PRIMARY KEY,
  slug                   TEXT NOT NULL UNIQUE,
  prefijo                TEXT NOT NULL UNIQUE,          -- p. ej. PAL -> PAL-2026-001
  nombre                 TEXT NOT NULL,
  handle                 TEXT,
  youtube_channel_id     TEXT,
  idioma                 TEXT NOT NULL DEFAULT 'es',
  presupuesto_mensual_usd REAL NOT NULL,
  tope_produccion_usd    REAL NOT NULL,
  umbral_alerta          REAL NOT NULL DEFAULT 0.8,
  creado                 TEXT NOT NULL
);
INSERT INTO "canales" VALUES(1,'palimpsesto','PAL','Palimpsesto','@Palimpsestostudio','UCqGznx_OIKoZWTrORoe4xcw','es',150.0,50.0,0.8,'2026-11-18T00:04:49+00:00');
CREATE TABLE costos (
  id               INTEGER PRIMARY KEY,
  canal_id         INTEGER NOT NULL REFERENCES canales(id),
  produccion_id    TEXT NOT NULL,                        -- PAL-2026-001 o GENERAL-PAL-2026-11
  short_id         TEXT,
  agente           TEXT NOT NULL,
  etapa            INTEGER,
  proveedor        TEXT NOT NULL,
  producto         TEXT NOT NULL,
  tokens_in        INTEGER NOT NULL DEFAULT 0,
  tokens_out       INTEGER NOT NULL DEFAULT 0,
  tokens_cache_w   INTEGER NOT NULL DEFAULT 0,
  tokens_cache_r   INTEGER NOT NULL DEFAULT 0,
  unidades         REAL NOT NULL DEFAULT 0,
  unidad           TEXT,
  costo_usd        REAL NOT NULL,
  tipo_costo       TEXT NOT NULL CHECK (tipo_costo IN ('real','estimado','prorrateado','suscripcion')),
  tarifa_ids       TEXT,                                 -- JSON
  id_externo       TEXT NOT NULL,
  hash_dedupe      TEXT NOT NULL UNIQUE,                 -- impide contar dos veces el mismo gasto
  factura_id       TEXT,
  reemplaza_id     INTEGER REFERENCES costos(id),        -- conciliación: el real reemplaza al estimado
  anulado          INTEGER NOT NULL DEFAULT 0,
  creado           TEXT NOT NULL
);
CREATE TABLE decisiones (
  id            TEXT PRIMARY KEY,                        -- DEC-0001
  canal_id      INTEGER REFERENCES canales(id),
  produccion_id TEXT REFERENCES producciones(id),
  tipo          TEXT NOT NULL,                           -- tema | enfoque | presupuesto | aprobacion_video | publicacion | estrategia
  descripcion   TEXT NOT NULL,
  decidio       TEXT NOT NULL,                           -- 'director' | agente
  justificacion TEXT,
  creado        TEXT NOT NULL
);
INSERT INTO "decisiones" VALUES('DEC-0001',1,NULL,'estrategia','Topes aprobados por el Director: 150 USD/mes (meses 1-2), 300 USD/mes desde mes 3, 50 USD por producción','ceo','Mensaje del Director del 18-nov-2026','2026-11-18T00:04:49+00:00');
INSERT INTO "decisiones" VALUES('DEC-0002',1,NULL,'estrategia','Sin dominio web por ahora; foco en YouTube y monetización','ceo','Mensaje del Director del 18-nov-2026','2026-11-18T00:04:49+00:00');
CREATE TABLE historial_tareas (
  id         INTEGER PRIMARY KEY,
  tarea_id   INTEGER NOT NULL REFERENCES tareas(id),
  de_estado  TEXT,
  a_estado   TEXT NOT NULL,
  actor      TEXT NOT NULL,
  nota       TEXT,
  creado     TEXT NOT NULL
);
INSERT INTO "historial_tareas" VALUES(1,1,'pendiente','en_curso','investigador',NULL,'2026-11-18T00:15:51+00:00');
INSERT INTO "historial_tareas" VALUES(2,1,'en_curso','entregado','investigador',NULL,'2026-11-18T00:17:21+00:00');
INSERT INTO "historial_tareas" VALUES(3,1,'entregado','cerrado','investigador','cierre automático (sin puerta)','2026-11-18T00:17:21+00:00');
INSERT INTO "historial_tareas" VALUES(4,2,'pendiente','en_curso','ceo',NULL,'2026-11-18T00:17:21+00:00');
INSERT INTO "historial_tareas" VALUES(5,2,'en_curso','entregado','ceo','Top 3 presentados al Director','2026-11-18T00:17:21+00:00');
INSERT INTO "historial_tareas" VALUES(6,2,'entregado','cerrado','ceo','cierre automático (sin puerta)','2026-11-18T00:17:21+00:00');
INSERT INTO "historial_tareas" VALUES(7,3,'pendiente','en_curso','ceo',NULL,'2026-11-18T00:17:21+00:00');
INSERT INTO "historial_tareas" VALUES(8,3,'en_curso','entregado','ceo',NULL,'2026-11-18T00:17:22+00:00');
INSERT INTO "historial_tareas" VALUES(9,3,'entregado','en_revision','ceo',NULL,'2026-11-18T00:17:22+00:00');
CREATE TABLE presupuestos (
  canal_id   INTEGER NOT NULL REFERENCES canales(id),
  mes        TEXT NOT NULL,                              -- 'YYYY-MM'
  monto_usd  REAL NOT NULL,
  PRIMARY KEY (canal_id, mes)
);
CREATE TABLE producciones (
  id               TEXT PRIMARY KEY,                     -- PAL-2026-001
  canal_id         INTEGER NOT NULL REFERENCES canales(id),
  titulo           TEXT NOT NULL,
  tema             TEXT,
  estado           TEXT NOT NULL DEFAULT 'activa',       -- activa | congelada | publicada | cancelada
  etapa_actual     INTEGER NOT NULL DEFAULT 1,
  presupuesto_usd  REAL NOT NULL,
  ciclos_correccion INTEGER NOT NULL DEFAULT 0,
  duracion_s       INTEGER,
  creado           TEXT NOT NULL,
  actualizado      TEXT NOT NULL
);
INSERT INTO "producciones" VALUES('PAL-2026-001',1,'Episodio piloto 0 (interno)','Por definir en etapa 3','activa',3,50.0,0,NULL,'2026-11-18T00:15:51+00:00','2026-11-18T00:17:22+00:00');
CREATE TABLE recursos (
  id            TEXT PRIMARY KEY,                        -- PAL-2026-001-R0042
  produccion_id TEXT NOT NULL REFERENCES producciones(id),
  tipo          TEXT NOT NULL,                           -- imagen | clip | voz | musica | efecto | documento | mapa
  origen        TEXT NOT NULL CHECK (origen IN ('dominio_publico','ia','licencia','propio')),
  proveedor     TEXT,
  licencia      TEXT NOT NULL,
  url_fuente    TEXT,
  prompt        TEXT,
  es_recreacion INTEGER NOT NULL DEFAULT 0,
  archivo       TEXT,
  creado        TEXT NOT NULL
);
CREATE TABLE tareas (
  id            INTEGER PRIMARY KEY,
  produccion_id TEXT NOT NULL REFERENCES producciones(id),
  etapa         INTEGER NOT NULL,
  nombre        TEXT NOT NULL,
  responsable   TEXT NOT NULL,
  puerta        TEXT NOT NULL DEFAULT 'ninguna',         -- ninguna | humana | auditoria | presupuesto
  estado        TEXT NOT NULL DEFAULT 'pendiente',
  entradas      TEXT NOT NULL DEFAULT '[]',              -- JSON: ids de artefactos
  entregables   TEXT NOT NULL DEFAULT '[]',              -- JSON: ids de artefactos
  fecha_limite  TEXT,
  creado        TEXT NOT NULL,
  iniciado      TEXT,
  entregado     TEXT,
  cerrado       TEXT,
  notas         TEXT,
  UNIQUE (produccion_id, etapa)
);
INSERT INTO "tareas" VALUES(1,'PAL-2026-001',1,'Investigación de oportunidades','investigador','ninguna','cerrado','[]','["PAL-2026-001-A001"]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T00:15:51+00:00','2026-11-18T00:17:21+00:00','2026-11-18T00:17:21+00:00',NULL);
INSERT INTO "tareas" VALUES(2,'PAL-2026-001',2,'Presentación de temas al CEO','ceo','ninguna','cerrado','[]','["PAL-2026-001-A001"]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T00:17:21+00:00','2026-11-18T00:17:21+00:00','2026-11-18T00:17:21+00:00',NULL);
INSERT INTO "tareas" VALUES(3,'PAL-2026-001',3,'Selección del tema','director','humana','en_revision','[]','["PAL-2026-001-A002"]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T00:17:21+00:00','2026-11-18T00:17:22+00:00',NULL,NULL);
INSERT INTO "tareas" VALUES(4,'PAL-2026-001',4,'Propuesta de tres perspectivas narrativas','investigador','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(5,'PAL-2026-001',5,'Observaciones editoriales del Director','director','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(6,'PAL-2026-001',6,'Aprobación de la perspectiva','director','humana','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(7,'PAL-2026-001',7,'Investigación profunda','investigador','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(8,'PAL-2026-001',8,'Expediente de fuentes','investigador','auditoria','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(9,'PAL-2026-001',9,'Escritura del guion','guionista','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(10,'PAL-2026-001',10,'Storyboard','productor','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(11,'PAL-2026-001',11,'Generación de prompts','productor','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(12,'PAL-2026-001',12,'Producción audiovisual','productor','presupuesto','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(13,'PAL-2026-001',13,'Edición','editor','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(14,'PAL-2026-001',14,'Auditoría independiente','auditor','auditoria','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(15,'PAL-2026-001',15,'Correcciones','ceo','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(16,'PAL-2026-001',16,'Aprobación humana del video','director','humana','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(17,'PAL-2026-001',17,'Publicación','director','humana','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(18,'PAL-2026-001',18,'Creación y distribución de Shorts','editor','humana','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(19,'PAL-2026-001',19,'Análisis de métricas','analista','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(20,'PAL-2026-001',20,'Informe financiero','cfo','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
INSERT INTO "tareas" VALUES(21,'PAL-2026-001',21,'Retroalimentación al sistema','ceo','ninguna','pendiente','[]','[]',NULL,'2026-11-18T00:15:51+00:00',NULL,NULL,NULL,NULL);
CREATE TABLE tarifas (
  id            INTEGER PRIMARY KEY,
  proveedor     TEXT NOT NULL,
  producto      TEXT NOT NULL,
  unidad        TEXT NOT NULL,                           -- mtok_in | mtok_out | mtok_cache_w | mtok_cache_r | imagen | segundo | kchar | mes
  precio_usd    REAL NOT NULL,
  vigente_desde TEXT NOT NULL,
  vigente_hasta TEXT,
  fuente        TEXT
);
INSERT INTO "tarifas" VALUES(1,'anthropic','claude-opus-5-5','mtok_in',4.0,'2026-11-01',NULL,'Referencia oficial Anthropic (caché 2026-11-03)');
INSERT INTO "tarifas" VALUES(2,'anthropic','claude-opus-5-5','mtok_out',20.0,'2026-11-01',NULL,'Referencia oficial Anthropic (caché 2026-11-03)');
INSERT INTO "tarifas" VALUES(3,'anthropic','claude-opus-5-5','mtok_cache_r',0.2,'2026-11-01',NULL,'Referencia oficial Anthropic (caché 2026-11-03)');
INSERT INTO "tarifas" VALUES(4,'anthropic','claude-opus-5-5','mtok_cache_w',5.0,'2026-11-01',NULL,'VERIFICAR: supuesto 1.25x entrada (TTL 5 min)');
INSERT INTO "tarifas" VALUES(5,'anthropic','claude-sonnet-5-5','mtok_in',2.0,'2026-11-01',NULL,'Referencia oficial Anthropic (caché 2026-11-03)');
INSERT INTO "tarifas" VALUES(6,'anthropic','claude-sonnet-5-5','mtok_out',10.0,'2026-11-01',NULL,'Referencia oficial Anthropic (caché 2026-11-03)');
INSERT INTO "tarifas" VALUES(7,'anthropic','claude-sonnet-5-5','mtok_cache_r',0.1,'2026-11-01',NULL,'Referencia oficial Anthropic (caché 2026-11-03)');
INSERT INTO "tarifas" VALUES(8,'anthropic','claude-sonnet-5-5','mtok_cache_w',2.5,'2026-11-01',NULL,'VERIFICAR: supuesto 1.25x entrada (TTL 5 min)');
INSERT INTO "tarifas" VALUES(9,'anthropic','claude-haiku-5-5','mtok_in',0.1,'2026-11-01',NULL,'Referencia oficial Anthropic (prompts <=100K)');
INSERT INTO "tarifas" VALUES(10,'anthropic','claude-haiku-5-5','mtok_out',0.5,'2026-11-01',NULL,'Referencia oficial Anthropic (prompts <=100K)');
INSERT INTO "tarifas" VALUES(11,'anthropic','claude-pro','mes',20.0,'2026-11-01',NULL,'VERIFICAR: suscripción Claude Pro (impuestos no incluidos)');
INSERT INTO "tarifas" VALUES(12,'google','gemini-3.1-flash-image','imagen',0.067,'2026-11-01',NULL,'VERIFICAR: fuente secundaria (1K)');
INSERT INTO "tarifas" VALUES(13,'google','veo-3.1-fast','segundo',0.1,'2026-11-01',NULL,'VERIFICAR: fuente secundaria');
INSERT INTO "tarifas" VALUES(14,'elevenlabs','creator','mes',22.0,'2026-11-01',NULL,'VERIFICAR: fuente secundaria');
CREATE VIEW v_costos_vigentes AS
  SELECT * FROM costos WHERE anulado = 0;
COMMIT;
