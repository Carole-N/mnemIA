# etl/etl_csv_constraints.py
from __future__ import annotations
import sqlite3, pandas as pd, re, unicodedata
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "storage/mnemia.sqlite")

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "etl" / "data"
LOG_PATH = ROOT / "etl" / "etl_log.txt"

# mapping "fichier CSV" → "nom de catégorie"
CSV_SOURCES = {
    "positions_dans_l_espace.csv": "positions_dans_l_espace",
    "parties_du_corps.csv": "parties_du_corps",
    "vitesses_d_execution.csv": "vitesses_d_execution",
}

# Nettoyage texte générique
def normalize_text(s: str) -> str:
    import re, unicodedata
    if s is None:
        return ""
    raw = str(s)

    # 1) Unicode & espaces
    s = unicodedata.normalize("NFKC", raw)     # accents composés OK
    s = s.strip()
    s = re.sub(r"\s+", " ", s)

    # 2) Corrections génériques (tout public)
    s = s.lower()
    s = re.sub(r"\btres\s+rapide\b", "très rapide", s, flags=re.IGNORECASE)
    s = re.sub(r"\btres\s+lent\b", "très lent", s, flags=re.IGNORECASE)

    # 3) Corrections ciblées pour **positions_dans_l_espace**
    # (tu peux en ajouter d’autres si besoin)
    s = re.sub(r"\ba genou[x]?\b", "à genoux", s, flags=re.IGNORECASE)
    s = re.sub(r"\ballonge\b", "allongé", s, flags=re.IGNORECASE)

    # 4) Log si modifié
    if s != raw:
        print(f"Correction EDA : '{raw}' → '{s}'")
    return s


# Journalisation simple
def log(msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")


# Assure que la catégorie existe, retourne son id
def ensure_category(con: sqlite3.Connection, name: str) -> int:
    cur = con.execute("SELECT id_category FROM category WHERE name=?", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur = con.execute("INSERT INTO category(name) VALUES (?)", (name,))
    return cur.lastrowid


# Charge un CSV dans la table constraints, retourne (ajoutées, ignorées)
def load_one_csv(con: sqlite3.Connection, filename: str, category_name: str) -> tuple[int, int]:
    path = DATA_DIR / filename
    if not path.exists():
        print(f"  ! Erreur lecture CSV : Fichier introuvable : {path}")
        log(f"CSV MISSING {filename}")
        return (0, 0)

    df = pd.read_csv(path)
    if "label" not in df.columns:
        print(f"  ! Erreur CSV {filename} : colonne 'label' absente")
        log(f"CSV BAD {filename} (no 'label')")
        return (0, 0)

    # === EDA générique : nettoyage + déduplication (accents, espaces, doublons) ===
    raw_count = len(df)

    # 1) Normaliser (et afficher les corrections)
    normalized_labels = []
    for raw in df["label"].astype(str):
        clean = normalize_text(raw)
        if clean != raw:
            print(f"Correction EDA : '{raw}' → '{clean}'")
        normalized_labels.append(clean)
    df["label"] = normalized_labels

    # 2) Retirer les valeurs vides après nettoyage
    df = df[df["label"].str.len() > 0]

    # 3) Dédupliquer après normalisation
    after_norm = len(df)
    df_dedup = df.drop_duplicates(subset=["label"])
    dup_removed = after_norm - len(df_dedup)
    if dup_removed > 0:
        print(f"Suppression EDA : {dup_removed} doublon(s) supprimé(s).")

    # 4) On continue avec la version dédupliquée
    df = df_dedup

    
    # ================================================================

    cat_id = ensure_category(con, category_name)
    added, ignored = 0, 0

    for label in df["label"].tolist():
        try:
            con.execute(
                'INSERT OR IGNORE INTO "constraints"(category_id, label) VALUES (?, ?)',
                (cat_id, label),
            )
            cur = con.execute("SELECT changes()")
            if cur.fetchone()[0] == 1:
                added += 1
            else:
                ignored += 1
        except Exception as e:
            print(f"  ! Insert error [{filename}] '{label}' : {e}")
            log(f"CSV INSERT ERROR {filename} '{label}' : {e}")

    print(f"  + Ajoutées : {added}   · Ignorées (doublons) : {ignored}")
    log(f"CSV {filename} OK added={added} ignored={ignored} raw={raw_count}")
    return (added, ignored)


# Main ETL
def main():

    print("=== ETL CSV → contraintes (MnémIA) ===")
    print(f"Répertoire des données : {DATA_DIR}")
    print(f"Base SQLite : {DB_PATH}")

    # Suppression automatique des anciennes contraintes pour éviter les doublons
    with sqlite3.connect(DB_PATH) as con:
        con.execute('DELETE FROM "constraints";')
        con.commit()

    total_added = 0
    with sqlite3.connect(DB_PATH) as con:
        con.execute("PRAGMA foreign_keys = ON")
        print(f"Connexion SQLite ", DB_PATH)

        for filename, cat_name in CSV_SOURCES.items():
            print(f"→ Import {filename} → catégorie '{cat_name}'")
            a, _ = load_one_csv(con, filename, cat_name)
            total_added += a
        con.commit()

    # Ajout d'une entrée factice si aucune donnée n'a été insérée pour la source csv_constraints
    with sqlite3.connect(DB_PATH) as con:
        count = con.execute("SELECT COUNT(*) FROM poetic_inspiration WHERE source = ?", ("csv_constraints",)).fetchone()[0]
        if count == 0:
            con.execute(
                "INSERT OR IGNORE INTO poetic_inspiration(label, source) VALUES (?, ?)",
                ("placeholder_csv", "csv_constraints"),
            )
            con.commit()

    total_added = 0
    with sqlite3.connect(DB_PATH) as con:
        con.execute("PRAGMA foreign_keys = ON")
        print(f"Connexion SQLite → {DB_PATH}\n")
        for filename, cat_name in CSV_SOURCES.items():
            print(f"→ Import {filename} → catégorie '{cat_name}'")
            a, _ = load_one_csv(con, filename, cat_name)
            total_added += a
        con.commit()

    print(f"\n Import CSV terminé. Total ajoutées : {total_added}")


if __name__ == "__main__":
    main()
