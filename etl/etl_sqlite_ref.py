# etl/etl_sqlite_ref.py
from __future__ import annotations
import sqlite3, re, unicodedata
from pathlib import Path
from datetime import datetime

# Chemins des bases de données et du journal
ROOT = Path(__file__).resolve().parents[1]
DB_MAIN = ROOT / "mnemia.db"
DB_SRC  = ROOT / "etl" / "data" / "source_ref.db"
LOG     = ROOT / "etl" / "etl_log.txt"

# Normalisation simple d'une chaîne de caractères
def norm(s: str) -> str:
    if s is None: return ""
    import re, unicodedata
    s = unicodedata.normalize("NFKC", s).strip()
    s = re.sub(r"\s+", " ", s).lower()
    s = s.replace("tres", "très")
    return s

# Journalisation simple
def log(msg: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")

# ETL principal
def main():
    print("=== ETL SQLite source → poetic_inspiration ===")
    print(f"SRC: {DB_SRC}\nDST: {DB_MAIN}")

    with sqlite3.connect(DB_SRC) as con_src, sqlite3.connect(DB_MAIN) as con_dst: 
        con_dst.execute("PRAGMA foreign_keys = ON")
        rows = con_src.execute("SELECT label FROM lexique_artistique").fetchall()
        raw = len(rows)
        keep = 0
        seen = set()
        for (label,) in rows:
            w = norm(label)
            if not w or w in seen: 
                continue
            seen.add(w)
            con_dst.execute(
                "INSERT OR IGNORE INTO poetic_inspiration(label, source) VALUES (?,?)",
                (w, "sqlite_source"),
            )
            keep += 1
        con_dst.commit()
    print(f"EDA [poetic] : {raw} → {keep} lignes (dédup / nettoyage).")
    log(f"sqlite_source raw={raw} kept={keep}")

if __name__ == "__main__":
    main()
