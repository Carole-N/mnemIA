#!/usr/bin/env python3
import os, subprocess, sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "storage/mnemia.sqlite")

HERE = os.path.dirname(os.path.abspath(__file__))

# Replace DB with DB_PATH
DB = DB_PATH
LOGF = os.path.join(HERE, "etl_log.txt")

# Exécute une commande shell, quitte si échec
def run(cmd):
    print(f"\n$ {cmd}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        raise SystemExit(f"Commande en échec: {cmd}")

# Journalisation simple
def log(line):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGF, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {line}\n")

# Compte les entrées par source dans poetic_inspiration
def count_by_source():
    with sqlite3.connect(DB) as con:
        cur = con.execute("SELECT source, COUNT(*) FROM poetic_inspiration GROUP BY source;")
        return cur.fetchall()

# Main orchestrateur ETL
def main():
    print("=== ETL/EDA MnémIA (orchestrateur) ===")
    print(f"DB  : {DB}")
    print(f"LOG : {LOGF}")

# -- Étapes ETL --
    # 1) API Datamuse → poetic_inspiration
    run(f"python3 {os.path.join(HERE, 'etl_datamuse.py')}") # appel ETL datamuse
    log("datamuse OK")

    # 2) CSV → constraints/category (+ EDA léger intégré)
    run(f"python3 {os.path.join(HERE, 'etl_csv_constraints.py')}") # appel ETL csv_constraints
    log("csv_constraints OK")

    # 3) Webscraping CND (si pb -> exécution ‘webscrap’ avec le snippet)
    run(f"python3 {os.path.join(HERE, 'etl_scraping_cnd.py')}") # appel ETL webscraping
    log("webscrap OK")

    # 4) SQLite source → poetic_inspiration
    run(f"python3 {os.path.join(HERE, 'etl_sqlite_ref.py')}") # appel ETL sqlite_ref
    log("sqlite_source OK")

    # 5) MongoDB Joconde (si pb -> appeler fallback JSON)
    run(f"python3 {os.path.join(HERE, 'etl_mongodb_joconde.py')}") # appel ETL mongodb_joconde
    log("mongodb_fallback OK")

    # Récap rapide à afficher/capturer
    print("\n--- Récap par source (poetic_inspiration) ---")
    # Liste des sources attendues
    expected_sources = [
        ("datamuse", "API Datamuse"),
        ("csv_constraints", "CSV"),
        ("sqlite_source", "SQLite"),
        ("webscrap", "Web scraping"),
        ("mongodb", "MongoDB"),
    ]
    # Récupère les comptes existants
    counts = dict(count_by_source())
    for key, label in expected_sources:
        print(f"{label:16s} {counts.get(key, 0)}")

    print("\n ETL terminé.")

if __name__ == "__main__":
    main()
