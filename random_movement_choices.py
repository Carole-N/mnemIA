import sqlite3
import random

DB_PATH = 'storage/mnemia.sqlite'  # Doit correspondre à la base utilisée par l'ETL CSV

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Supprimer les anciennes associations
cur.execute('DELETE FROM movement_choices;')

# Récupérer tous les mouvements et toutes les catégories
cur.execute('SELECT id_movement FROM movement')
mouvements = [row[0] for row in cur.fetchall()]
cur.execute('SELECT id_category FROM category')
categories = [row[0] for row in cur.fetchall()]

for m in mouvements:
    for cat in categories:
        # Récupérer toutes les contraintes possibles pour cette catégorie
        cur.execute('SELECT id_constraints FROM "constraints" WHERE category_id=?', (cat,))
        contraintes = [row[0] for row in cur.fetchall()]
        # Tirer une contrainte au hasard
        choix = random.choice(contraintes)
        # Insérer l'association
        cur.execute('INSERT INTO movement_choices (movement_id, category_id, constraints_id) VALUES (?, ?, ?)', (m, cat, choix))

conn.commit()
conn.close()
print('Associations aléatoires générées pour chaque mouvement.')
