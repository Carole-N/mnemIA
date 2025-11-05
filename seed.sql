/* Permet d’activer les clés étrangères dans SQLite */
PRAGMA foreign_keys = ON;

/* Catégories */
INSERT INTO category (id_category, name) VALUES
  (1,'position_dans_l_espace'),
  (2,'partie_du_corps'),
  (3,'vitesse_d_execution');

/* Contraintes */
INSERT INTO "constraints" (id_constraints, category_id, label) VALUES
  (1,1,'assis'),
  (2,1,'debout'),
  (3,2,'bras'),
  (4,2,'jambes'),
  (5,3,'lent'),
  (6,3,'rapide');

/* Pauses */
INSERT INTO pause (id_pause, label) VALUES
  (1,'aucune'),
  (2,'courte'),
  (3,'longue');

/* Mouvements A et B */
INSERT INTO movement (id_movement, label) VALUES
  (1,'A'),
  (2,'B');

/* Choix des contraintes (1 par catégorie) */
-- A = debout / bras / rapide
INSERT INTO movement_choices (movement_id, category_id, constraints_id) VALUES
  (1,1,2),
  (1,2,3),
  (1,3,6);

-- B = assis / jambes / lent
INSERT INTO movement_choices (movement_id, category_id, constraints_id) VALUES
  (2,1,1),
  (2,2,4),
  (2,3,5);

/* Inspirations poétiques */
INSERT INTO poetic_inspiration (id_poetic_inspiration, label, source, created_at) VALUES
  (1,'brume','datamuse','2025-10-29T10:30:00');

/* Une phrase chorégraphique d'exemple */
INSERT INTO choreographic_phrase (id_choreographic_phrase, label, poetic_inspiration_id) VALUES
  (1,'Séquence 1 – Brume',1);

/* Étapes : B, B, A, pause courte, B */
INSERT INTO choreographic_step (choreographic_phrase_id, order_idx, movement_id, pause_id) VALUES
  (1,1,2,NULL),
  (1,2,2,NULL),
  (1,3,1,NULL),
  (1,4,NULL,2),
  (1,5,2,NULL);
