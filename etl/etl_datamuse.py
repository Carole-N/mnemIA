# etl/etl_datamuse.py
from __future__ import annotations
import sqlite3, requests, re, unicodedata
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "storage/mnemia.sqlite")
LOG_PATH = Path(__file__).resolve().parent / "etl_log.txt"

BASE_URL = "https://api.datamuse.com/words"
THEMES = ["mist", "light", "silence", "breath"]  # thèmes simples pour une V1

def normalize_text(s: str) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s).strip()
    s = re.sub(r"\s+", " ", s)
    # minuscule (choix projet) + correction générique 'tres'->'très'
    s = s.lower().replace("tres", "très")
    return s

def log(msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")

def main():
    print("=== ETL Datamuse → poetic_inspiration ===")
    print(f"DB: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as con:
        con.execute("PRAGMA foreign_keys = ON")

        total_raw, total_keep = 0, 0
        seen = set()  # déduplication en mémoire (au cas où l’API renvoie des doublons)

        for theme in THEMES:
            print(f"→ Recherche de mots proches de '{theme}' ...")
            try:
                r = requests.get(BASE_URL, params={"ml": theme, "max": 10}, timeout=10)
                r.raise_for_status()
                words = [normalize_text(w.get("word", "")) for w in r.json()]
            except Exception as e:
                print(f"  ! Erreur Datamuse ({theme}) : {e}")
                log(f"Datamuse ERROR theme={theme} : {e}")
                words = []

            # EDA : filtrage valeurs vides + dédup
            words = [w for w in words if w]
            total_raw += len(words)

            for w in words:
                if w in seen:
                    continue
                seen.add(w)
                con.execute(
                    "INSERT OR IGNORE INTO poetic_inspiration(label, source) VALUES (?, ?)",
                    (w, "datamuse"),
                )
                total_keep += 1

        con.commit()

    print(f"EDA [poetic] : {total_raw} → {total_keep} lignes (dédup / nettoyage).")
    log(f"Datamuse OK raw={total_raw} kept={total_keep}")

if __name__ == "__main__":
    main()
