# etl/etl_mongodb_joconde.py
from __future__ import annotations
import os, json, sqlite3, re, unicodedata
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

try:
    from pymongo import MongoClient
except Exception:
    MongoClient = None  # au cas où non installé

ROOT = Path(__file__).resolve().parents[1]
DB_MAIN = ROOT / "mnemia.db"
LOG     = ROOT / "etl" / "etl_log.txt"
JSON_FALLBACK = ROOT / "etl" / "data" / "mongo_sample.json"

MONGO_URI = os.getenv("MONGODB_URI", "")
MONGO_DB  = os.getenv("MONGODB_DB", "mnemia")
MONGO_COL = os.getenv("MONGODB_COL", "poetic")

# Normalisation basique
def norm(s: str) -> str:
    if s is None: return ""
    s = unicodedata.normalize("NFKC", s).strip()
    s = re.sub(r"\s+", " ", s).lower()
    s = s.replace("tres", "très")
    return s

# Log dans fichier ETL
def log(msg: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")

# Lecture MongoDB
def read_mongo() -> list[str]:
    if not MONGO_URI or MongoClient is None:
        return []
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        col = client[MONGO_DB][MONGO_COL]
        # on lit 20 docs max, champ 'label'
        docs = list(col.find({}, {"label": 1}).limit(20))
        return [d.get("label", "") for d in docs]
    except Exception as e:
        log(f"mongodb ERROR: {e}")
        return []

# Lecture fallback JSON
def read_fallback() -> list[str]:
    if JSON_FALLBACK.exists():
        try:
            data = json.loads(JSON_FALLBACK.read_text(encoding="utf-8"))
            # data attendu: liste de {'label': '...'}
            return [d.get("label", "") for d in data if isinstance(d, dict)]
        except Exception as e:
            log(f"mongodb_fallback ERROR: {e}")
    return []

# Main ETL
def main():
    print("=== ETL MongoDB → poetic_inspiration ===")
    print(f"DST: {DB_MAIN}")

    words = read_mongo()   
    src = "mongodb"
    if not words:
        print("  ! Mongo indisponible → fallback JSON")
        words = read_fallback()
        src = "mongodb_fallback"

    raw = len(words) 
    keep = 0
    seen = set()

    with sqlite3.connect(DB_MAIN) as con:
        con.execute("PRAGMA foreign_keys = ON")
        for w in words:
            w = norm(w)
            if not w or w in seen:
                continue
            seen.add(w)
            con.execute(
                "INSERT OR IGNORE INTO poetic_inspiration(label, source) VALUES (?,?)",
                (w, src),
            )
            keep += 1
        con.commit()

    print(f"EDA [poetic] : {raw} → {keep} lignes (dédup / nettoyage).")
    log(f"{src} raw={raw} kept={keep}")

if __name__ == "__main__":
    main()
