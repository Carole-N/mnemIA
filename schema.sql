/* Permet d’activer les clés étrangères dans SQLite */
PRAGMA foreign_keys = ON;

/* 1) Catégories de contraintes (position_dans_l_espace, partie_du_corps, vitesse_d_execution) */
CREATE TABLE category (
  id_category INTEGER PRIMARY KEY,
  name        TEXT NOT NULL
);

/* 2) Contraintes (valeurs textuelles) rattachées à une catégorie */
CREATE TABLE "constraints" (
  id_constraints INTEGER PRIMARY KEY,
  category_id   INTEGER NOT NULL,
  label         TEXT    NOT NULL,
  FOREIGN KEY (category_id) REFERENCES category(id_category)
);

/* 3) Mouvements (A, B, C, …) */
CREATE TABLE movement (
  id_movement INTEGER PRIMARY KEY,
  label       TEXT NOT NULL
);

/* 4) Choix de contraintes pour un mouvement : 1 contrainte par catégorie */
CREATE TABLE movement_choices (
  id_choice     INTEGER PRIMARY KEY,
  movement_id   INTEGER NOT NULL,
  category_id   INTEGER NOT NULL,
  constraints_id INTEGER NOT NULL,
  UNIQUE (movement_id, category_id),
  FOREIGN KEY (movement_id)  REFERENCES movement(id_movement),
  FOREIGN KEY (category_id)  REFERENCES category(id_category),
  FOREIGN KEY (constraints_id) REFERENCES "constraints"(id_constraints)
);

/* 5) Inspirations poétiques (Datamuse / Web scraping CND / Base Joconde via MongoDB) */
CREATE TABLE poetic_inspiration (
  id_poetic_inspiration INTEGER PRIMARY KEY,
  label                 TEXT NOT NULL,
  source                TEXT,      -- ex. 'datamuse', 'cnd_scrap', 'joconde_mongo'
  created_at            TEXT       -- ISO 8601, ex. '2025-10-29T10:30:00'
);

/* 6) Pauses (aucune, courte, longue) */
CREATE TABLE pause (
  id_pause INTEGER PRIMARY KEY,
  label    TEXT NOT NULL
);

/* 7) Phrases chorégraphiques (titre + inspiration poétique) */
CREATE TABLE choreographic_phrase (
  id_choreographic_phrase INTEGER PRIMARY KEY,
  label                   TEXT NOT NULL,  -- ex. 'Séquence 1 – Brume'
  poetic_inspiration_id   INTEGER NOT NULL,
  FOREIGN KEY (poetic_inspiration_id) REFERENCES poetic_inspiration(id_poetic_inspiration)
);

/* 8) Étapes ordonnées d’une phrase : XOR (mouvement OU pause) */
CREATE TABLE choreographic_step (
  id_step                 INTEGER PRIMARY KEY,
  choreographic_phrase_id INTEGER NOT NULL,
  order_idx               INTEGER NOT NULL,   -- position 1,2,3…
  movement_id             INTEGER,            -- nullable
  pause_id                INTEGER,            -- nullable
  CHECK ( (movement_id IS NULL) <> (pause_id IS NULL) ),
  UNIQUE (choreographic_phrase_id, order_idx),
  FOREIGN KEY (choreographic_phrase_id) REFERENCES choreographic_phrase(id_choreographic_phrase),
  FOREIGN KEY (movement_id) REFERENCES movement(id_movement),
  FOREIGN KEY (pause_id)    REFERENCES pause(id_pause)
);

/* 9) Index utiles (performances et lisibilité des plans d’exécution) */
CREATE INDEX idx_mch_movement   ON movement_choices(movement_id);
CREATE INDEX idx_mch_category   ON movement_choices(category_id);
CREATE INDEX idx_mch_constraints ON movement_choices(constraints_id);

CREATE INDEX idx_step_phrase    ON choreographic_step(choreographic_phrase_id);
CREATE INDEX idx_step_movement  ON choreographic_step(movement_id);
CREATE INDEX idx_step_pause     ON choreographic_step(pause_id);
