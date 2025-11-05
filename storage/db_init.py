import sqlite3
import os

def init_db(db_path, schema_path, seed_path=None):
    """
    Initialise la base de données SQLite avec le schéma fourni.
    Optionnellement, exécute un script de seed SQL si fourni.
    """
    # Lire le schéma SQL
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    # Créer la base de données SQLite
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        # Exécuter le schéma
        cursor.executescript(schema_sql)
        print(f"Schéma appliqué avec succès à {db_path}")

        # Exécuter le seed SQL si fourni
        if seed_path:
            with open(seed_path, 'r', encoding='utf-8') as f:
                seed_sql = f.read()
            cursor.executescript(seed_sql)
            print("Données de seed insérées avec succès.")

        conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Chemins par défaut
    db_path = os.path.join(os.path.dirname(__file__), "mnemia.sqlite")
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schema.sql")
    seed_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "seed.sql")

    # Initialiser la base de données
    init_db(db_path, schema_path, seed_path)