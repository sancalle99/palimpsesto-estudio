-- Esquema del estudio. Multicanal: toda fila operativa lleva canal_id.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS canales (
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

-- Presupuesto mensual por canal (permite cambiar topes por mes sin perder historial)
CREATE TABLE IF NOT EXISTS presupuestos (
  canal_id   INTEGER NOT NULL REFERENCES canales(id),
  mes        TEXT NOT NULL,                              -- 'YYYY-MM'
  monto_usd  REAL NOT NULL,
  PRIMARY KEY (canal_id, mes)
);

CREATE TABLE IF NOT EXISTS producciones (
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

CREATE TABLE IF NOT EXISTS tareas (
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

CREATE TABLE IF NOT EXISTS historial_tareas (
  id         INTEGER PRIMARY KEY,
  tarea_id   INTEGER NOT NULL REFERENCES tareas(id),
  de_estado  TEXT,
  a_estado   TEXT NOT NULL,
  actor      TEXT NOT NULL,
  nota       TEXT,
  creado     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS artefactos (
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

-- Cuaderno del Director: el texto literal nunca se modifica
CREATE TABLE IF NOT EXISTS aportes (
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

CREATE TABLE IF NOT EXISTS decisiones (
  id            TEXT PRIMARY KEY,                        -- DEC-0001
  canal_id      INTEGER REFERENCES canales(id),
  produccion_id TEXT REFERENCES producciones(id),
  tipo          TEXT NOT NULL,                           -- tema | enfoque | presupuesto | aprobacion_video | publicacion | estrategia
  descripcion   TEXT NOT NULL,
  decidio       TEXT NOT NULL,                           -- 'director' | agente
  justificacion TEXT,
  creado        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tarifas (
  id            INTEGER PRIMARY KEY,
  proveedor     TEXT NOT NULL,
  producto      TEXT NOT NULL,
  unidad        TEXT NOT NULL,                           -- mtok_in | mtok_out | mtok_cache_w | mtok_cache_r | imagen | segundo | kchar | mes
  precio_usd    REAL NOT NULL,
  vigente_desde TEXT NOT NULL,
  vigente_hasta TEXT,
  fuente        TEXT
);

CREATE TABLE IF NOT EXISTS costos (
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

CREATE TABLE IF NOT EXISTS alertas (
  id            INTEGER PRIMARY KEY,
  canal_id      INTEGER REFERENCES canales(id),
  produccion_id TEXT,
  nivel         TEXT NOT NULL,                           -- info | aviso | bloqueo
  mensaje       TEXT NOT NULL,
  creado        TEXT NOT NULL,
  resuelta      INTEGER NOT NULL DEFAULT 0
);

-- Registro de licencias y procedencia de cada recurso
CREATE TABLE IF NOT EXISTS recursos (
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

CREATE VIEW IF NOT EXISTS v_costos_vigentes AS
  SELECT * FROM costos WHERE anulado = 0;
