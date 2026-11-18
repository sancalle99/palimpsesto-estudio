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
INSERT INTO "aportes" VALUES('DIR-PAL-2026-001-01',1,'PAL-2026-001','decision','Acepto el piloto','integrado','Piloto de ≈11 min sin ampliar la investigación; SOL-04 descartada. Ver guion.md (Aportes del Director) y escaleta.md','guionista','2026-11-18T01:39:11+00:00','2026-11-18T01:39:31+00:00');
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
INSERT INTO "artefactos" VALUES('PAL-2026-001-A003','PAL-2026-001',4,'ficha_enfoques','producciones/PAL-2026-001/etapa04_enfoques.md',1,'9cc1bec1aaf1eb9994870bd9a150134c22632319e98800a80a9ffff3f25317b1','investigador','2026-11-18T00:23:56+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A004','PAL-2026-001',6,'ficha_enfoques','producciones/PAL-2026-001/etapa04_enfoques.md',2,'9cc1bec1aaf1eb9994870bd9a150134c22632319e98800a80a9ffff3f25317b1','ceo','2026-11-18T00:25:47+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A005','PAL-2026-001',7,'expediente','producciones/PAL-2026-001/expediente.md',1,'fc73eb375791c3ce4c29a24bf2b46e38332ecb7cc588070773e1da7426d32be1','investigador','2026-11-18T00:26:45+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A006','PAL-2026-001',8,'auditoria','producciones/PAL-2026-001/auditoria/etapa_8_v1.md',1,'7aea8d0a12f04cfd72d506233317ea6ecb05090744d01771d2546579bf4b7223','auditor','2026-11-18T01:20:16+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A007','PAL-2026-001',8,'expediente','producciones/PAL-2026-001/expediente.md',2,'8bc5d0c72ff391fb440c515d02be889e366f0b7ac18a490fa362b453fabb8d48','investigador','2026-11-18T01:20:16+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A008','PAL-2026-001',8,'auditoria','producciones/PAL-2026-001/auditoria/etapa_8_v2.md',2,'1fa453150b61aacc94e03d79f976e8f2cf846d8407471d31cdedcd3e9f7bbcfe','auditor','2026-11-18T01:23:17+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A009','PAL-2026-001',8,'expediente','producciones/PAL-2026-001/expediente.md',3,'f6421cf5ceb9324ec02a4508679fe238273087b99bbc11a6cb472ed1119f71f7','investigador','2026-11-18T01:23:17+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A010','PAL-2026-001',8,'auditoria','producciones/PAL-2026-001/auditoria/etapa_8_v3.md',3,'65143637f754aac932527bdfc107b5c3f7df15d906fac64e6952e560c44c68bc','auditor','2026-11-18T01:24:45+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A011','PAL-2026-001',8,'expediente','producciones/PAL-2026-001/expediente.md',4,'d7849622d27e4e877a2d6a21565c3629ca692ae2c509290c189e7f072b66c274','investigador','2026-11-18T01:24:45+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A012','PAL-2026-001',9,'escaleta','producciones/PAL-2026-001/escaleta.md',1,'64e1575526a52494d7fa0a86975332436fef33392fd22ba4889b524870074923','guionista','2026-11-18T01:33:57+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A013','PAL-2026-001',9,'guion','producciones/PAL-2026-001/guion.md',1,'de85812d3b68cac02e03c4ad2e69cc2bf9bf2a63f056566c5fb48ee49d162621','guionista','2026-11-18T01:33:57+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A014','PAL-2026-001',9,'titulos','producciones/PAL-2026-001/titulos.md',1,'a27421f6cd4681ce14781c84c2ac47200fe97f0d06a027e43c51eae84664207f','guionista','2026-11-18T01:33:57+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A015','PAL-2026-001',9,'solicitud_investigacion','producciones/PAL-2026-001/solicitudes_investigacion.md',1,'7256b8423eb1c471760a41625dadb5bd024058223580c05e80407662e46b8c76','guionista','2026-11-18T01:33:58+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A016','PAL-2026-001',9,'guion','producciones/PAL-2026-001/guion.md',2,'ddd6cd0f03482ce383dbaca5ecbf909b2404c11404b96f3f772c079b4a8930f7','guionista','2026-11-18T01:39:31+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A017','PAL-2026-001',9,'escaleta','producciones/PAL-2026-001/escaleta.md',2,'522054d6f2f6e883939d4501d45c41798ddb71f50d71c291168b8f86c79a67df','guionista','2026-11-18T01:39:31+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A018','PAL-2026-001',9,'solicitud_investigacion','producciones/PAL-2026-001/solicitudes_investigacion.md',2,'9068853b4df91ff858ab98344a643f276cb0ddc30c75fb2f82cb4cc1fc9978a1','guionista','2026-11-18T01:39:31+00:00');
INSERT INTO "artefactos" VALUES('PAL-2026-001-A019','PAL-2026-001',10,'storyboard','producciones/PAL-2026-001/storyboard.md',1,'102a7abd79521872c98538a5226adedfef10b3db522cffd4d6fcbcd94dc92b7a','productor','2026-11-18T01:41:57+00:00');
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
INSERT INTO "costos" VALUES(1,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2625,27097,61240,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Nkpnr4PXHQvkxo6U3K','b4e6ecaabbb1647001e4edf821232b753ef230c388081b1ae2b409a739191c27',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(2,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,232,57532,88337,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9NoFyUSYfak4MZPzao7','87dad217e58a8173c1db8d7aa6d9236a230b7344dc2dc59f5c1a1888b87cf88f',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(3,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,120,1351,145869,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9NojKXdfoNcKw6byXMJ','cfde5ddf05d51500982329d8e291668694d2743070578970ba390aca57b87410',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(4,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,812,1071,147220,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9NosyRV9j6iN7bZwCnT','afeb4ba7dd4f298fd05637ca8744ac959e9842ed3321aaef281ea928fe9c4096',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(5,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,844,9464,148291,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Npp5ZMRX7Y4JBvZqhM','fb18eedb02a41722b45c10b3ee7c5535379f523ca83d28fdf504ef2d58a57d2d',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(6,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,514,9478,157755,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Nqz8aFptYKNpcv29o4','548d575661218bf0af04fc98c8891e739b872272f6191a9f1999b19316095fad',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(7,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,564,7334,167233,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Ns197dk1rrxnmwx2rd','57c7ffa62695ab6d9b5eb63d24ae1b9d13493bed3a7b990f847c543dc70e1f5c',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(8,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,7887,4021,174567,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Nsk5XPhSnVR7idMgen','39c2b183911882f5835236125f946c593e0b35aac2e41a0fbb185ff539e8566b',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(9,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,10849,7902,178588,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Nz3LH1gaKP7Mt6CD91','369180783f4aa1a02f342bc2080e9d75f88bb4c709f3b4176477b6bf1f274c9d',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(10,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,22201,10902,186490,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9P71QdeBFagf2EqWqCA','8965bfcc3d54d8bc44e2d26543162b2292f352d6d7c421c0faf56d8973e1a412',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(11,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,214,22267,197392,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9PN5BGTGntwj9snYKhc','70abd1efea9800a63b54db7f47eb9e6784d8c5b88f9ee6dc2d1d3921bffa7ecb',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(12,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1743,364,219659,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9PNJuGTXAXBKTR2bub9','2b1311ad5e04a9f18a5d02fb7905633a4d6b3ed5d772caa9a440c42a6b0a199e',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(13,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,983,1020,221766,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Py2EdRq4yrGE3dB4JX','feb0f7278880a11cd68f3d056c3d348bceadab5d82ffc1897e066a4113421cd3',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(14,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,1537,2105,222786,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9PyuaocZ9qWWR5GZjV4','c112641f0871cac7805ba224da717f0e9a7def2fc925fbea5cdee82d2ea3db48',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(15,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2249,1852,224891,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Q19BuGJnf4xAwNe4JD','335b5e4e7a4b6813d446fce6aec9bdcad9c4e436157163adb2795ea40c909a85',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(16,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,334,2424,226743,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Q2cEMdPr8CCm6QVWXq','c346a6b79760aafac83388c02096de63fb494823c53331ccd1bb79ac338cc0f0',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(17,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,278,545,229167,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Q6QGPrTGvALsQNF2N1','02a9eea11fa68cf0a8e2ad65d6867a5455496745e60b4fad6dafd2ec1ee2862c',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(18,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1187,356,229712,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Q79Kzie25Srd3VgKYZ','26d4f5bd5ec94192602712c7c4ee7413733e8c1883b16216b50603df500181bc',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(19,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1133,1719,230068,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Q8k2q4zYNwGr2fqnje','dc7808caccc37a702d76ca67d1d9b027b2bd23f9c8a8be6a4412da4630295e07',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(20,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,1037,1697,231787,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QAifXzKNvNHacJSmoh','4a0c9bd65ecc382e9276049b2c2f169226a2143bd978f11beea8fa3b3259f7ea',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(21,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1900,2322,233484,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QBSYCSfC3nrvbKsHtj','5ddb6d384c5585ba43212bfcb099d5c0fd50b000c2aba3d7bfe37160bbd7915c',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(22,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,3410,158,237706,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QVj19uEhS5FYaJj621','b98763cafa44b272c8659e6b32bfaaa6bc621956ab7bdd268f92f5646669e205',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(23,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,275,3466,237864,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QYKSf1riHotWKfJJrZ','2a35525ff233ce6410936721615e9601e9e6d4801f8065fc3c7babf83ffefe54',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(24,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,3506,314,241330,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QYcHfdCNg7yd8949Ke','5533f931f1ba9f75b9220f38231a6292ce6a9b0d9e4106f0a2fb451d8165bb0a',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(25,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,14159,3551,241644,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QaUasR4GFH7YAsLHiG','29162fabb8882fa7a2f367d63167544211b981df87fc948677cf6259e8998e2d',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(26,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,6443,14204,245195,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QhnVqBx6HYBcogx7AG','e95a56fa4321252262022ac86f2412c9561b3c280c0d1836be41590304166c91',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(27,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,4750,6815,259399,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QmGrkDhYmwYYUR6KMs','8338986d353206b2f1af4b0313f87ef9e1734295711c9619a1973257a1004749',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(28,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,602,4892,266214,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QovbB9cGrqhdUZMuFJ','66c13378afabc1d3b310e9bfbc52f10cd9719347315daed1984022b949c02d0c',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(29,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,9346,1260,271106,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QpY2dq1kZEJAj87hob','689fa0d786bbf14970535154608bc55e1e13e93d3855a20fe2f6ba701acf4b48',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(30,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,3755,10096,272366,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QvdsXydGU1KmU84TVb','5fc509e631552fb323086970ca5645459e6a2fbe0f6775ad4bda46fe674c5709',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(31,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,825,3896,282462,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QyJbkHW8oXQcC1YouV','9af6b38ad1809fd175775270be46901d11d89580545cb283c422597a07145cf1',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(32,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,123,971,286358,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QywJs3uKt7ugHZShiK','04eb6695fdd4a0c8ee8f44be6d5b166b787077c30bc0440a2b17b047999e3ea1',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(33,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,369,492,287329,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QzJhETzYZrEaJaCK4a','df53198308144447d70809b40cf1df189d8ee7dd898419a7cd76fd57689d3ff3',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(34,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,5428,471,287821,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9QzhrGBfWJv97u3FYKj','9f055ddf6ba5ca67c0d6ea9ede152a2bbeb964da7700b568c674da7d975647a2',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(35,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,2116,6185,288292,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9R43GQQeyT4DNAV1pc7','9b5c8c01a59af720dacad7d3ab81e20dddbffb488432e61179a1cdb96e6594b1',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(36,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,572,2297,294477,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9R5RtThsTe1qdPka3K6','94943aa1033c175ec3341e566f843b0831a68307240dcc8d8b77751f5ef0aa8f',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(37,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2040,620,296774,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9R5wq3BPJw167dHfQ5h','669968ccc32b62c7603fb2e798aac26e5a49db50a5f34c4ee398f2d36db5b554',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(38,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,533,126,299434,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RDZYopn7spmWu2xQzm','90ab40e91e7399bab8e63b162a42be98816d9824bd68c11729677128cf49401d',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(39,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,671,5997,299560,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9REZydf7CyA3xo2sTJg','4f0a50745fc40ae0b4fe9d5331136acbc950d982e86266304dca404896e3c0e8',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(40,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,528,2570,305557,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RFQEXMhLK7gkrxAWFY','044031ea22f1529833e83fffe05810f457809ad8e6083ccf9e735703ed5270eb',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(41,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,427,1114,308127,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RG42NPbTm8trjF8FHZ','a4496c6f4cbec7bcf071c4ba92dc70753d6a28a305f0e3ed6ef1e2de25090b8c',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(42,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,353,4784,309241,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RGoL7jyxoqBuGLE5vF','62aec19d4affb645e0c86b22c3785e5a549eaea99d47903c4a22bf2dfeb25573',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(43,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,358,589,314025,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RHaavnvR5n48mrsP7T','2c159a601a6a876885394262cbd0bca9fb6cdc97a5e0900dd7d90c4f2218b476',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(44,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,454,1150,314614,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RHxz4zCyVTZyLK1QL5','d9834b4aea64a254703b8459810e52effb7dac37c4441fcdffb0e38cebd9062d',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(45,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,543,3776,315764,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RJNA6mE6291VVfz5jt','02bcc6f6226e642dc0c2d514e3735908cf5a2c15f16eb38f0d42ba11a8c52ec1',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(46,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,522,1302,319540,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RJtTz2KNxf8rryEJ6h','fb05c0dbb11cffe5766dc10b0dff2fb02f89b4bc8db594817701bec5a32e8112',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(47,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2929,1714,320842,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RKnUMQPgKSqrs2PCK4','545f4b7a3c7d8681c1342c63d5b5019d30f9c4ded6aa8725afeea8ea3dcb3876',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(48,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,262,2979,322556,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RMorWMyP29A2EpQ6wT','94a988fb31737bca9ac117b4ad2cf1b6c81f89bb728a586d7f9e0549e72c144e',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(49,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1632,438,325535,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RN6wfGfxwYygYtNrf4','bbfcbd1250ae20834a8a73d2a14f2fcf49a0cb71538ed1aad5c4d7eb7028d864',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(50,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,474,141,327605,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RVnVsagxcq4VEyrzdr','1d8bb573ae8042c404f078e0bce935c142073683d454ee08ca16def08200c349',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(51,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,88,604,327746,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RWUygxwnBjebe6NVaa','3a569aca9e5ba04090d48a1fa45c2f1fd5f6675d6bd4d710f8cc37ccc562942e',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(52,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,347,530,328350,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RWhJMjiSKAXvbXFNqQ','87522b677de89d295d5e2c29507a429cb533003051f60fef82b7c7a6c47c0ac1',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(53,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,9478,13313,328880,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RX5nTMhpHU9E5p4uid','c476231b45b27e0db99c283ee5262863acdfa433df84f2dad8f2a7937cf34294',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(54,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,469,18787,342193,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RctPXmPqWJwwokoWBS','85092f653ce964dbe6ba7668484d56cb1863e1d9308d4f3c1a7831b198624448',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(55,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,193,704,360980,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RdMYAL2NR3kaaoHE7q','ed15ceea7be0576b895379e7b378f43b0a51b9bbd0b16e67c3394712d74dae66',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(56,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,942,263,361684,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Rdc42r8LK4eP12NFW9','12561212c3dbaf8cee10a3289c3d4d0a8b1b2028211a70ee5f9da0c41a8beb48',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(57,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,137,968,361947,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RebzrGK9ncMTVebXNQ','787a810c585049ef43421824cb6d9df32699d14229eeca24854485cd7cea5564',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(58,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,369,2135,362915,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RexFG3D6rfWshvkry3','b7bc7969fc18a54967d76a0bfca9b0b4b071002113629d7dffee4333507e4763',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(59,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,223,451,365050,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RfPFuWRq8Bhbm7oGz6','cd9b43b1a552fec686c69b478daa0febfd545a64f53e7d7f0c13d800f58bfcb4',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(60,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,174,450,365501,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RfhAv8TkHTwuc1SXWc','4f96605ea8ba0e59fbebb6ad25e2b982b8207f5c56ca90db2419a7da3bc73693',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(61,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1813,340,365951,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RgCuqo8EyeG4Fa7yGF','5d17d5dff0bb45e4c9cfdabe3330034af979381db868abc5aebd07807109f4f8',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(62,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,751,2086,366291,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RhXb2LiBJ7G8obpzJX','76d718a68edce6af9d856a0fbff764cf0dfd9a0ffbd3e5325ad752070498b784',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(63,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,406,875,368377,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RiG1B6dkSvMyVVFoPx','da68cbd7b74026d1baba37764a09ddc9536273ffc73a881a0204c027501ecfb5',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(64,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,134,498,369252,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RivhbgyDqgczxJ5bQX','017c2a16470edd6bbe3b616d1af080a6cf80e4e2aa327c38887b8def8140c5c9',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(65,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,879,376,369750,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RjC1bFDhTqZ9uvUDP9','3e53376050681ccef288e4b256d04158085fc1b0d6040894756eee3d7db53c9a',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(66,1,'GENERAL-PAL-2026-11',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2370,1331,371005,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RtDf4iZtGQq6Cthp6E','c87e14e666c781f7fde4e28fa6a7cb4e8dac1610a9e6341365434ac0d54331d1',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(67,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,547,3633,372336,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RvuwHqvQSeAmELv8yj','6af01f889817039eeecd14b45680f86485281f695a073b321ba9fe443440be17',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(68,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,637,1190,375969,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9RxY7gQ2rHVwNdREfgN','0cf8f1534b92f90fd139ffae9ed692373714d12bd4db991fb21831f7b09ab7a3',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(69,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,3968,1385,377159,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Ryb8n5V9w1Hp8nYibz','c16f92867afdc4b3e21b982c64617f31e8f576aaf98773e3a3d729f5e548f0fe',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(70,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,661,4211,378544,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9S2Krr8SzXpfiuuQCfP','2c58aadb274ab34d075fd941b6913f71eeff57fcb0763124ab9893bca1e5c715',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(71,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1184,910,382755,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9S34wwFWLcnHMssvMjy','fbf0ba639e45299c8c9854258e75b03be378a4748a419c4a0f770a91e1f7c326',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(72,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,184,23,384849,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SLDxA8jQCUwisibpS8','b8c4a1293b0f2d71e1ee8c8624924b8421c4f43a4ed844eca7b08811b4e2a2a1',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(73,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,998,287,384872,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SLYZLScDkYGkwkLoAc','b282bd1d610252094c539e8e4aa992c1213b58ca860c65a80f4c851a6bd1111d',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(74,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,208,154,386157,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9STG56JixVhwMwkcwHH','2be9b3330e716f110e468ec1da3537b05aa7645935f67c284984f73e8d229391',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(75,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1083,253,386311,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9STaDVTWPdKutTfXgLL','0f15df8b0f552e32d0ba828c81ad52ff816034ef4d233920ab6c73c5e636708c',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(76,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,714,1273,386564,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SUbTC8fninvRdWQxrm','8bbd2720c087c892d4eb9515ce04f51ffd0a948e0f95902e9a0652c432ecc4c6',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(77,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,3719,1961,387837,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SVHUUimWQLyb4TZLFJ','5bbae63461dc3d979d30bfe29d3fbffcbe00a9612a3a590730cc5c13af7af2c9',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(78,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1148,3871,389798,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SY83HdhYtC5BeDprtY','0e91003b75b2695fce19d9448cd79279730df4015a9053b9d1118306a843b0df',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(79,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,409,29,394817,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SemvWgi93uiVkSghWt','aaa38afe3c3b02aef66022f5e2285a03bbe96b4d61f6026331fd54e960a922b6',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(80,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,866,484,394846,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SfGn5tBQSL39FSnuU4','666c84058973deac32c5a6e6c2c0abfa6c855ea284f49957a1c17ab65147dbc7',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(81,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,814,1127,395330,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SgDFHjtRT3w6vNajCR','360b617805e87254fff707118ed14fda635ef4dbf6412bce74abeb920de66483',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(82,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,4915,7694,396457,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9ShHnRC6LibN3rTQ4Wp','dd9069d24cff586fa4bf7bc62a97e91b8b705eecc8209c3e9c0ed34ba9b75715',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(83,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1188,5141,404151,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SkceL2E6HrDhnD6SfX','8805883dc5e29c473b2f0d145c838bfde8df062a2983c68c6fddc8290bb63bd2',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(84,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,2338,195,410480,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SsDeA4LSXxwuVjPaEa','96af20781042c34295b4242942237897c6be84e6b70f486419c79cab17bc52c7',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(85,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1373,2354,410675,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9SuKj6A2vChiRz7qFbF','0b8170e5c5a065da6017b88fa16f8afdc0aa919f04bdc75c080e5f809589fc35',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(86,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,1797,190,414402,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9TFXKeMx8Bj97cTLeqf','e2ff98136ad61baf94144c9529c40c08a311a33008457df07871656807149200',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(87,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1295,2030,414592,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9TGwViyXBAscvZ9FD9p','56a2cfffb495481a642cc4131bcbf1962e7f362315e3ec3e1cf65795e826c539',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(88,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,629,1638,416622,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9TKSeiwNm6kVKVZVPDS','de5a31bdf489b5d944d139cca774f6e35c60c7d56091fea553c1a3a1ebfa95aa',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(89,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,799,699,418260,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9TLvxMAsJqkcpMUU9SP','9a4607ba2d1fb65216a196b66f622d08f68ac313766ba67c31f3ed7f8778f5f1',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(90,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,149,1024,418959,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9TbCf474GXVjfoffrs6','84dee617236c1b9a2940e40d582248a93792f17ddcfed70e4beaa02d7d1da7ca',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(91,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,143,633,419983,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9TnAwvAB9s2ZAU2iTNB','fc81e1c629afb562100a918bb672a9172880c1fdab737a59245cfe2df42a2715',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(92,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,853,541,420616,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9TyDifDnx9krEGedY17','441f699bc979cc1676c4c437f0e46078a7575f21c40877c061bc0e2cd5109ede',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(93,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2927,922,421157,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9U4MW7Bh1i8dy8rZWqk','0418c5942e20f6d2bffb8d5ab364822a18d535cfdc77bc486685566fa7eb9a62',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(94,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1592,3197,422079,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9U69a52D6nXcWZqmc3P','6136837a644b30aacc63c6489783f241afd8c2e04ceb72a17360a7a718c08418',NULL,NULL,0,'2026-11-18T00:44:34+00:00');
INSERT INTO "costos" VALUES(95,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2909,1815,425276,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9U7J1MaMMAT2vv5Fikx','ebb2d62c625984203e2a447b29c8e86d122d3c3b0ccca023c6456763e9b2835e',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(96,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,460,3270,427091,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9U9VsnZ9ppcsL5ms8GL','e599e6f08b16352c3f9f4116352adb913caaa0181c71725741fcb0f7da9ab827',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(97,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,1606,1125,430361,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9U9v6KV6zS9R1BeN9rZ','19622edd089a95228ed75a11a89cc855f1f714c13f89f84f36b4f3c591ee9577',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(98,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,863,49,433091,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9UJMBesgWRThuNeQGCa','411c21d1c3380951fe067285d31090241cf29b6a86ce874c778588a343bd7259',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(99,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,502,882,433140,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9UKHTCpR6n2vJ4gh3bY','767ac1d9bea98145787cc6a3220e970aecd3b4af1bacc2b6fe9ed6724452641c',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(100,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,911,3879,434524,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9UrESVPXegdCQagZzw6','adbf06bda8b1d06aa3e861dcb207badca550c02108f6a0a875642030dc025fee',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(101,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2098,441,439314,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Vdr48HWADHi7eazYML','55f8558afc1c251bee36e7c1951912242ca767f8a05fbf834956a3eabc200f73',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(102,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,314,2313,439755,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9VfnikxRGTwd2kBeBbx','2f7f5fe35ffb1553a8052b0b667c823a5083f8e94b715c73071ddcd05983b498',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(103,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,580,4022,442068,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9VgbyPAjdu91apnV7hZ','24458a628a3e8678bcc119ce8bab5f51a0bf9d549a0a0cdf586c892725fa7b59',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(104,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,879,1732,446090,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9VhNdUcnfoNR6CbS6Uk','71f216881c6e8e8c1c049f8c72e130b22a898eda44618188f55b6961e9433ce3',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(105,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,361,4601,447822,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9ViByJW2cKfAeY9dmfJ','e04a8b55e54055c0154964d9892e63b77b1759923b1c0ab9627aaaf3256b367f',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(106,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1116,1342,452423,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9ViXjCHDGxFLXcXNSCN','4363f99c0107b9fbee9a7051d4b1570244f22151d592262bc3aafef1633805c8',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(107,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,418,1383,453765,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9W5SMa5Siv8VVkAZW43','0ef28f9a2fc36369ebb9c1ca8012a923fc3df3e15e932eb3143079a946e8083a',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(108,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,4050,481,455148,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9W5y71HbAdAymj9dRrw','64df3bf0d746b31012c1195e6593345a78497371539e620988ace90c0a5c8c64',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(109,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,2972,4606,455629,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9W8ZSJw3TkUsuuxA85u','ad88593ef7f369521c44ac9c839b5c4df269549ba190eb792a02ef659295a09d',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(110,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,703,3252,460235,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WARMC9evqWAyr4dNjy','73d61556ce70f4d3421dc731c3ed9d86318b0d906903d7e9484f8b06814f8054',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(111,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1922,1442,463487,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WBFsiEkXTcy9VK8U3T','c077ecb13b5f157d692a405b17aa964f10261976e51544b7ba21ce0bbcdbc109',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(112,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,282,2157,464929,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WCtgnxmwKoU2AMxG94','3c60f034e66662010d050e65989569c046319552a62c9c0b43fefbf63dda6ae3',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(113,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,353,448,467086,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WDEKkcHJ3feABzBVdQ','e67a1492da0bab5ece33ae828ad931204647d2e40a83cd6cba533f89fc5e2159',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(114,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1339,619,467534,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WDZ28sCact2obwgGVY','fa0859de4773b6f325a258dd7b210b13185ba72a88f59d8483098c00940e6e9a',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(115,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,560,3408,469492,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WW9XF11gYdgBsetxkU','7a8e1183603c34b702f65242b701c6eb7b4c79c28c5519799a453b42bf692a59',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(116,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,956,729,472900,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WWzMN9iEtj7fY6T3My','202cdc009107c76ee8edb17e54b0bbbed63652f5fa909bad490b983385465465',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(117,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,599,1341,473629,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WgaCanTje1gx5gQyqo','c08f1f0ffb18929906a6b007c01656b8f08ddff0bf2cb8662743129b84bf3f76',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(118,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,1480,2649,475569,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WiknsbamT8Us6nwdik','912ec0867b14cc5c3da71c98748b1e986e16880b00e0bc40b68406212209e034',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(119,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1818,4691,478218,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WkDNJesrfhfpx2tGuC','2af3f973c325a3c0092c5d04fccace6e1d4471a256b5c93a6d4b888d151d01c4',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(120,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,6215,2130,482909,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WmcimuJj3AhZAvDLqm','3e9033bdf5127821a8342740af07d32f93debf727d9268d3f0d20103d8642e59',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(121,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,421,6556,485039,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Wq9n9w41soVM8Uj8JR','42966f013a85b186b09b5fa480e58ccd060bf369c03f0d30ad902922c77390a5',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(122,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,642,427,491595,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Wqt3dk4Rw4if54aPHr','79e2f21d209474177dcde14bc5f6e8aa2bdc2b33b7f3b69f32fa8cb7370a41ad',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(123,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,808,1018,492022,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9WrTEAf2Sn7HgUeaWwW','85b07cec79ee655e72323441936fcf5ade84833f0d09a845c15df41258a73a14',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(124,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,708,1851,493848,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9X1Kfk287qJbupHi7ay','de878dcf95d1ca3ac66c361fd9636657c4dc173b0e7a9641958978e868c2b754',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(125,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,3956,2314,495699,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9X2GiB5X69xtQNGkEeR','eae56fd40f722bc8184517d8020cb08d4571560fb05e9fc93c1a1e70b5dbeb84',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(126,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,668,4702,498013,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9X4iiQr1utxvwQqXXoP','e1eefed45f4146eeacec37d23236b31f9c294c5e9bfb3f3a9d64436f02752a9d',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(127,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,649,1037,502715,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9X5Gjjr4bqYjZjfwuHg','31cd0866436a2acd22335a3c3803252ee867842d2ca7e2b080f66edc5ef44f95',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(128,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,1110,786,503752,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9X64vsTjQQQuuc9ax5Q','7d083b64ceb9dc036e0ee5c37ac435ddf956569b5793f5b55cdb6982a1d6067c',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(129,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1188,1185,504538,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9X739ymuw91eipCJkuR','b8efaa6d54833f536d21b720acd074d141b53839f327146b5612ab0a4d4fb73a',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(130,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,1415,1010,506911,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9X9pfjVEMonheeqVa9N','8dc4322cfd129ad8e728dc4ec11e548c1d47317f4e6c410612c3767a26988d0d',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(131,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,453,2633,507921,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XBKzNERiMB9nEVoFBR','c0cc8282876a2af2ca2625c9adda0b1f371ceb01635cc550e91a7050891358c5',NULL,NULL,0,'2026-11-18T01:24:58+00:00');
INSERT INTO "costos" VALUES(132,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,140,19986,61440,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Xa8xzPZ28VNmQqFaXX','f9ad9e96d5fe71903a6e45570d6a9adb430c84fa6346b7da17dc691f53586770',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(133,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,153,5266,81426,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XaQYN4eeugLAW1pXbd','4a7debd2dc5ec7401209b087188e093a85397a750540f434beb159708002e4e0',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(134,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,148,1630,86692,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XadUyfjVB8dtseLsjr','09e84817592ccb3b4b765e05f066c0248162e32b4ba332dd0c51065c60244271',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(135,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,259,6042,88322,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XaoaCAPAyceGbhZjs7','f17cd6ac692db90b3020430e6d454ab8b217eac5c6948b8ae485d3b8272626f2',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(136,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,165,2599,94364,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Xb5rVPTX3V5xn7wsCD','8777490fb34dfc7da812f1a3d122342eae0714a5adef45b0563926fca2d2da3b',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(137,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,368,1587,96963,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XbLEvFWviWKbsF2HXS','03fbad5c27ad0e43267bfe05e54db3f16a35fe94ccb6b3d6d8de58f8c98794b6',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(138,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,391,2867,98550,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XbnzVq9TWjEzL5ZQYe','53ff3f577f1eabb5dbbbe915ef1ad8b495da5fd3b54187bc2b1b0f8f7bdab337',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(139,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2286,1657,101417,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Xc8u4waFAyikVBpJXi','a5952a1c1e952f97a128c4a456fdcf36fb8a408f77c5d4c25e879d944bd5a165',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(140,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1288,2414,103074,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XdTkRsTDUfBjemNLBm','b60a8283b4246c00969f0c662786d009dcf561f35c27e0414e57e990332fd655',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(141,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,478,1440,105488,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XeJW5hX6vtGvXpGzwp','92129aee68c471c65d9d1335e69d00900f0873bd6a3849677b646e69454def6d',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(142,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1438,3977,106928,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XeoNABL9A8qhjdy5Jf','8ab06c7e85e9db307faa5eaf287c625492b81e62d4f386ce07346a317dbec6c4',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(143,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,853,1982,110905,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XftZyJP4sqWAXpCcCA','e799598a215ab19959851b78622054e0a0878b9d2247e2d674887ad140619fae',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(144,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,508,1035,112887,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XgU6qrQq5g1woY9fNz','f75474fea3b8f6dda34125134d651d34e4b41ea9e20b1ac53a3bff75d1451e2d',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(145,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,155,1391,113922,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XgvJfuRDgnqjfo2U3N','3559fec125de753db9d956587607c310d75f74226bec34e5da22ed6333bd1f68',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(146,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,184,7676,115313,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Xh7vgApbTZi4qdvh2N','24477cea9602c269662e2f5d46dc98e03f40939e404517ccf7b504e5e376b1b3',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(147,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,143,1345,122989,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XhKh6X76cpyfUhxMZu','1d108dd541856b3dda383b1265c435dbdaa9c0973e700fb7ce50a2105e54c10b',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(148,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2336,1400,124334,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XhXjPw97iYScT8HXYo','3655771418a3be59b74f281258ae9fea7836a74de89cb6844059e8c47b652325',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(149,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,875,2504,125734,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XjFgKBCYnLwqTxqWDz','22e45570f340fa699d5084e1d4ac56be6ae04a89094ed81dd975f94d9fed3235',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(150,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,6024,939,128238,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XjsU6jsUqr6m9rFDKE','62e384fa65d505cad67bedba80b36ce5ccb8a47d26d31799f19915f95d60354e',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(151,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,2031,7898,129177,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XoxpBiXskTXKP3RQwn','4c7895d08d1b8037ea0b844f70ab104686b94c533f3af0c7195dcbd76a272be1',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(152,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1699,2226,137075,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XqNaTNUZoZUrvewJTJ','b6676f545fa3c16e580d64ada17ea4cf912e9ccae44b19873f915e7cd362ff9d',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(153,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,802,2713,139301,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XrcX8cpa8Movg8RFJ8','6f7ca62a241fe396a08f729d376c06b68e0ce4c8ae943185d2f217b339edb217',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(154,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,499,995,142014,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XsGqjeNDMeQ6ehaLv1','5694672b1c7d0ab2e5b4998253efa695a301ae01bac31d51c3c5bf2c93b11716',NULL,NULL,0,'2026-11-18T01:33:58+00:00');
INSERT INTO "costos" VALUES(155,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,307,769,143009,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Xsjv9k3msQFG3Cu5G6','da1f97b2eeef63d325035c67c5ffaccaeff3c6de74e356213d32e34172b91d1d',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(156,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,190,2049,143778,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Xt444gsfXJZaYHtR4c','e08aab5b4f93dae47f1b1f8d5a2f26268526b7f73397808db8aa450c880ca57d',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(157,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1102,12310,145827,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XtMTZsEs1KoXzXxxt3','54c2a6da408446aeb75eebafed4867f42e5d316326aad8032f9679f245d2ddca',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(158,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,185,1254,158137,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9Xu7GKdpndYjBEdtyn1','4b3f97d7f0075bb03ff645c2fe380810eebe837878c7ffde20829fa06db5a460',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(159,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,255,653,159391,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XuMjU3w5gc7by9n484','a3bc38752db488b7bd2f19ae3d131c1f9290a4277a761a6ec650a436a568d69f',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(160,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1262,320,160044,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9XumpoNutrmbCa5p1c6','8695fb85d8ccaf777e4f0e8f75a7e319f7b071e0cfa9314a68171f250d920c63',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(161,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,324,85,161626,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YG5aSvGD9EAkLstWtz','2987c2c9fa0426fa28144fa2c924c45339f40796d6911898bdf76d262479d67a',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(162,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,294,619,161711,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YGSgTXRzhJ3kKakayM','813810e3bbbb036cc80a3c7e721782b75634739b8d97afbfb5dad2ca378c6eab',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(163,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,1663,356,162330,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YGpBXNuthKWqWH3MZC','4af1795a5c463fdf786cd64ea097208eb9429419a9161eb8886d9038a39d91d1',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(164,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,586,2126,162686,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YHo8odkJNCj1uJ56ea','3cda44e3f8a093b5e665a2432fb8b504d65fb791bb3bad7e675d30a1964ed5b0',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(165,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,368,866,164812,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YJHfn2TExgNRoxqYp1','cd92ee330ddd9dd21ec20f54233df6ba4d1e81f3978bfe0c0c85833d27e207b6',NULL,NULL,0,'2026-11-18T01:39:36+00:00');
INSERT INTO "costos" VALUES(166,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,180,654,165678,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YJnrDDbJppA56T1eY9','17c989a47bbfc3251a442b36e0e77da84750af9b32ebdd225bf8267a0a43c1a0',NULL,NULL,0,'2026-11-18T01:42:02+00:00');
INSERT INTO "costos" VALUES(167,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,619,612,166332,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YK5f14W1WdaDQm56HX','0dc7d066fa465507597c4d40af698531aa7d0b0c07e1418b36b5c2b44662129d',NULL,NULL,0,'2026-11-18T01:42:02+00:00');
INSERT INTO "costos" VALUES(168,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,137,22,167563,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YQAtfjiJoJFMjKi559','65f794975123a5788726b4e00f0262a7e9dbd08c1be3c279b6e3752e4f25c8f8',NULL,NULL,0,'2026-11-18T01:42:02+00:00');
INSERT INTO "costos" VALUES(169,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',4,166,1105,167585,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YQQ4RmjpjurbqdrTQY','ae9594a4ddb0e77a703c13da08b92b17e603deefadb67dfbfe5e30d93bd14afe',NULL,NULL,0,'2026-11-18T01:42:02+00:00');
INSERT INTO "costos" VALUES(170,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',1,471,4257,168690,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YQcfwxpNQVERSBp9g4','14c49d92a13275adbcc8c385a65fbd69cd9ac37c5066b8cd08798a931ea7f686',NULL,NULL,0,'2026-11-18T01:42:02+00:00');
INSERT INTO "costos" VALUES(171,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,5325,1442,172947,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YR5BtmNusVU7fxu8eD','12bd4f8d192b2352788ef3317a9053042942037c759c460430791eb39ee8cfc3',NULL,NULL,0,'2026-11-18T01:42:02+00:00');
INSERT INTO "costos" VALUES(172,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,205,5389,174389,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YURLBeFmVNE5m5fdqS','a3dc1ac3356ab00229504eb6a03b1d3435682dac146e426f446e4e8e4a44d9a7',NULL,NULL,0,'2026-11-18T01:42:02+00:00');
INSERT INTO "costos" VALUES(173,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,533,289,179778,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YUfXxYAPSnD9vqWH5y','1d0eb33695d0f67153709ccfb086c0ec4e63f4bf9e8eeba9b020da669b53fc57',NULL,NULL,0,'2026-11-18T01:42:02+00:00');
INSERT INTO "costos" VALUES(174,1,'PAL-2026-001',NULL,'claude-code',NULL,'anthropic','claude-opus-5-5',2,321,759,180067,0.0,NULL,0.0,'suscripcion','[]','msg_011Ch9YV5BWgTYrF8ufE7kGi','e75dbff742ed220dcddc1a343e31dc79e0410a149b5dd2a5df3a0cc2e1cb73ad',NULL,NULL,0,'2026-11-18T01:42:02+00:00');
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
INSERT INTO "decisiones" VALUES('DEC-0003',1,'PAL-2026-001','aprobacion_etapa_3','Aprobada etapa 3: Selección del tema','director','Mensaje literal del Director (enviado dos veces): «APRUEBO PAL-2026-001 3 tema 1». Registro MANUAL por excepción: el hook de aprobación no estaba activo en esta sesión (iniciada antes de conectar el repositorio). Tema aprobado: #1 El Palimpsesto de Arquímedes.','2026-11-18T00:23:10+00:00');
INSERT INTO "decisiones" VALUES('DEC-0004',1,'PAL-2026-001','aprobacion_etapa_6','Aprobada etapa 6: Aprobación de la perspectiva','director','Mensaje literal del Director: «APRUEBO PAL-2026-001 6 enfoque A con bloque B». Registro MANUAL: el hook de aprobación sigue inactivo en esta sesión. Enfoque aprobado: A (biografía del objeto) como columna vertebral + bloque B (separar lo demostrado de lo exagerado); mención de Hipérides (C) en el cierre según la recomendación del CEO.','2026-11-18T00:25:47+00:00');
INSERT INTO "decisiones" VALUES('DEC-0005',1,'PAL-2026-001','operativa','Auditoría de fuentes (etapa 8) aplazada a la próxima sesión, abierta con el repositorio seleccionado','ceo','Pedido del Director para repartir el consumo del plan Pro','2026-11-18T00:28:44+00:00');
INSERT INTO "decisiones" VALUES('DEC-0006',1,NULL,'estrategia','Voces: gratuitas y locales (Piper / Kokoro), sin ElevenLabs por ahora','ceo','Pedido del Director: no pagar suscripción de voces','2026-11-18T00:45:02+00:00');
INSERT INTO "decisiones" VALUES('DEC-0007',1,NULL,'estrategia','Métrica de costo principal: consumo del plan Claude Pro por producción (tokens reales + reparto de la cuota)','ceo','Aclaración del Director','2026-11-18T00:45:02+00:00');
INSERT INTO "decisiones" VALUES('DEC-0008',1,NULL,'operativa','Canal verificado por teléfono; Studio configurado con subida privada por defecto','ceo','Confirmado por el Director','2026-11-18T00:45:02+00:00');
INSERT INTO "decisiones" VALUES('DEC-0009',1,NULL,'estrategia','Voz del narrador de Palimpsesto: Kokoro em_alex (voz 1), velocidad 0.95, licencia Apache-2.0','ceo','Elección del Director: «Prefiero la voz 1»','2026-11-18T00:47:15+00:00');
INSERT INTO "decisiones" VALUES('DEC-0010',1,'PAL-2026-001','operativa','Roles ligeros (ceo, guionista, productor, editor, analista, cfo) convertidos en skills que asume la sesión principal; investigador y auditor siguen como subagentes. Importación del consumo ahora incluye los registros de subagentes.','ceo',NULL,'2026-11-18T01:31:31+00:00');
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
INSERT INTO "historial_tareas" VALUES(10,3,'en_revision','aprobado','director','Mensaje literal del Director (enviado dos veces): «APRUEBO PAL-2026-001 3 tema 1». Registro MANUAL por excepción: el hook de aprobación no estaba activo en esta sesión (iniciada antes de conectar el repositorio). Tema aprobado: #1 El Palimpsesto de Arquímedes.','2026-11-18T00:23:10+00:00');
INSERT INTO "historial_tareas" VALUES(11,3,'aprobado','cerrado','director',NULL,'2026-11-18T00:23:10+00:00');
INSERT INTO "historial_tareas" VALUES(12,4,'pendiente','en_curso','investigador',NULL,'2026-11-18T00:23:10+00:00');
INSERT INTO "historial_tareas" VALUES(13,4,'en_curso','entregado','investigador',NULL,'2026-11-18T00:23:56+00:00');
INSERT INTO "historial_tareas" VALUES(14,4,'entregado','cerrado','investigador','cierre automático (sin puerta)','2026-11-18T00:23:56+00:00');
INSERT INTO "historial_tareas" VALUES(15,5,'pendiente','en_curso','ceo',NULL,'2026-11-18T00:23:56+00:00');
INSERT INTO "historial_tareas" VALUES(16,5,'en_curso','entregado','ceo','El Director no aportó observaciones; pasó directamente a aprobar el enfoque','2026-11-18T00:25:47+00:00');
INSERT INTO "historial_tareas" VALUES(17,5,'entregado','cerrado','ceo','cierre automático (sin puerta)','2026-11-18T00:25:47+00:00');
INSERT INTO "historial_tareas" VALUES(18,6,'pendiente','en_curso','ceo',NULL,'2026-11-18T00:25:47+00:00');
INSERT INTO "historial_tareas" VALUES(19,6,'en_curso','entregado','ceo',NULL,'2026-11-18T00:25:47+00:00');
INSERT INTO "historial_tareas" VALUES(20,6,'entregado','en_revision','ceo',NULL,'2026-11-18T00:25:47+00:00');
INSERT INTO "historial_tareas" VALUES(21,6,'en_revision','aprobado','director','Mensaje literal del Director: «APRUEBO PAL-2026-001 6 enfoque A con bloque B». Registro MANUAL: el hook de aprobación sigue inactivo en esta sesión. Enfoque aprobado: A (biografía del objeto) como columna vertebral + bloque B (separar lo demostrado de lo exagerado); mención de Hipérides (C) en el cierre según la recomendación del CEO.','2026-11-18T00:25:47+00:00');
INSERT INTO "historial_tareas" VALUES(22,6,'aprobado','cerrado','director',NULL,'2026-11-18T00:25:47+00:00');
INSERT INTO "historial_tareas" VALUES(23,7,'pendiente','en_curso','investigador',NULL,'2026-11-18T00:25:48+00:00');
INSERT INTO "historial_tareas" VALUES(24,7,'en_curso','entregado','investigador','Investigación en modo económico: 5 búsquedas + Crossref','2026-11-18T00:26:45+00:00');
INSERT INTO "historial_tareas" VALUES(25,7,'entregado','cerrado','investigador','cierre automático (sin puerta)','2026-11-18T00:26:45+00:00');
INSERT INTO "historial_tareas" VALUES(26,8,'pendiente','en_curso','investigador',NULL,'2026-11-18T00:26:45+00:00');
INSERT INTO "historial_tareas" VALUES(27,8,'en_curso','entregado','investigador',NULL,'2026-11-18T00:26:45+00:00');
INSERT INTO "historial_tareas" VALUES(28,8,'entregado','en_revision','investigador',NULL,'2026-11-18T00:26:45+00:00');
INSERT INTO "historial_tareas" VALUES(29,8,'en_revision','correcciones','auditor','Sin bloqueantes; 5 mayores: atribución y grado de la cifra del Stomachion, cita de Netz sin fuente, Hipérides sostenido por Wikipedia, autoría del comentario (falta Porfirio), F7/F13/F16 sin extractos; 7 menores','2026-11-18T01:18:29+00:00');
INSERT INTO "historial_tareas" VALUES(30,8,'correcciones','en_curso','investigador',NULL,'2026-11-18T01:20:16+00:00');
INSERT INTO "historial_tareas" VALUES(31,8,'en_curso','entregado','investigador','v2: corrige HAL-01 a HAL-12','2026-11-18T01:20:16+00:00');
INSERT INTO "historial_tareas" VALUES(32,8,'entregado','en_revision','investigador',NULL,'2026-11-18T01:20:16+00:00');
INSERT INTO "historial_tareas" VALUES(33,8,'en_revision','correcciones','auditor','v2 resuelve HAL-01..12 salvo un error nuevo: HAL-13 (mayor) atribucion invertida del recuento del Stomachion; F19 (Chung-Graham) dice que Cutler calculo primero las 536 y no menciona a Diaconis/Holmes ni 2003. Menores HAL-14..16 (F21 sin verificar, F20 incompleta, F23 paginas/Sharples). F12a, F12b, F17, F18 verificadas.','2026-11-18T01:22:20+00:00');
INSERT INTO "historial_tareas" VALUES(34,8,'correcciones','en_curso','investigador',NULL,'2026-11-18T01:23:17+00:00');
INSERT INTO "historial_tareas" VALUES(35,8,'en_curso','entregado','investigador','v3: corrige HAL-13 a HAL-16','2026-11-18T01:23:18+00:00');
INSERT INTO "historial_tareas" VALUES(36,8,'entregado','en_revision','investigador',NULL,'2026-11-18T01:23:18+00:00');
INSERT INTO "historial_tareas" VALUES(37,8,'en_revision','aprobado','auditor','v3: HAL-13 resuelto en AF-020b (discrepancia F19/F24 sin prioridad, reserva del cuadrado, F24 añadida); HAL-14/15/16 resueltos. Menores antes de etapa 9: HAL-17 entrada F19 de bibliografia aun con atribucion erronea; HAL-18 ''32 simetrias'' impreciso; HAL-19 reserva ''rectangulo'' sin fuente. F24 no verificada en linea (dominio bloqueado).','2026-11-18T01:24:23+00:00');
INSERT INTO "historial_tareas" VALUES(38,8,'aprobado','cerrado','auditor',NULL,'2026-11-18T01:24:23+00:00');
INSERT INTO "historial_tareas" VALUES(39,9,'pendiente','en_curso','guionista',NULL,'2026-11-18T01:32:03+00:00');
INSERT INTO "historial_tareas" VALUES(40,9,'en_curso','entregado','guionista','Guion v1.1 (≈11 min) con escaleta, títulos y solicitudes resueltas; aporte DIR-PAL-2026-001-01 integrado','2026-11-18T01:39:31+00:00');
INSERT INTO "historial_tareas" VALUES(41,9,'entregado','cerrado','guionista','cierre automático (sin puerta)','2026-11-18T01:39:31+00:00');
INSERT INTO "historial_tareas" VALUES(42,10,'pendiente','en_curso','productor',NULL,'2026-11-18T01:40:57+00:00');
INSERT INTO "historial_tareas" VALUES(43,10,'en_curso','entregado','productor','Storyboard v1: 52 planos; 5 recreaciones IA de imagen fija (≈8 %), sin vídeo IA; estimación etapa 12 ≈1,34 USD','2026-11-18T01:41:57+00:00');
INSERT INTO "historial_tareas" VALUES(44,10,'entregado','cerrado','productor','cierre automático (sin puerta)','2026-11-18T01:41:57+00:00');
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
INSERT INTO "producciones" VALUES('PAL-2026-001',1,'El Palimpsesto de Arquímedes (piloto)','El Palimpsesto de Arquímedes','activa',10,50.0,0,NULL,'2026-11-18T00:15:51+00:00','2026-11-18T01:41:57+00:00');
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
INSERT INTO "tareas" VALUES(3,'PAL-2026-001',3,'Selección del tema','director','humana','cerrado','[]','["PAL-2026-001-A002"]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T00:17:21+00:00','2026-11-18T00:17:22+00:00','2026-11-18T00:23:10+00:00',NULL);
INSERT INTO "tareas" VALUES(4,'PAL-2026-001',4,'Propuesta de tres perspectivas narrativas','investigador','ninguna','cerrado','[]','["PAL-2026-001-A003"]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T00:23:10+00:00','2026-11-18T00:23:56+00:00','2026-11-18T00:23:56+00:00',NULL);
INSERT INTO "tareas" VALUES(5,'PAL-2026-001',5,'Observaciones editoriales del Director','director','ninguna','cerrado','[]','[]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T00:23:56+00:00','2026-11-18T00:25:47+00:00','2026-11-18T00:25:47+00:00',NULL);
INSERT INTO "tareas" VALUES(6,'PAL-2026-001',6,'Aprobación de la perspectiva','director','humana','cerrado','[]','["PAL-2026-001-A004"]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T00:25:47+00:00','2026-11-18T00:25:47+00:00','2026-11-18T00:25:47+00:00',NULL);
INSERT INTO "tareas" VALUES(7,'PAL-2026-001',7,'Investigación profunda','investigador','ninguna','cerrado','[]','["PAL-2026-001-A005"]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T00:25:48+00:00','2026-11-18T00:26:45+00:00','2026-11-18T00:26:45+00:00',NULL);
INSERT INTO "tareas" VALUES(8,'PAL-2026-001',8,'Expediente de fuentes','investigador','auditoria','cerrado','[]','["PAL-2026-001-A005", "PAL-2026-001-A007", "PAL-2026-001-A009"]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T01:23:17+00:00','2026-11-18T01:23:18+00:00','2026-11-18T01:24:23+00:00',NULL);
INSERT INTO "tareas" VALUES(9,'PAL-2026-001',9,'Escritura del guion','guionista','ninguna','cerrado','[]','[]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T01:32:03+00:00','2026-11-18T01:39:31+00:00','2026-11-18T01:39:31+00:00',NULL);
INSERT INTO "tareas" VALUES(10,'PAL-2026-001',10,'Storyboard','productor','ninguna','cerrado','[]','[]',NULL,'2026-11-18T00:15:51+00:00','2026-11-18T01:40:57+00:00','2026-11-18T01:41:57+00:00','2026-11-18T01:41:57+00:00',NULL);
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
