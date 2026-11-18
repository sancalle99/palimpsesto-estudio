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
