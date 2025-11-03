# etl/etl_scraping_cnd.py
from __future__ import annotations
import sqlite3, re, unicodedata
from pathlib import Path
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Chemins des bases de données et du journal
ROOT = Path(__file__).resolve().parents[1]
DB_MAIN = ROOT / "mnemia.db"
LOG     = ROOT / "etl" / "etl_log.txt"
FALLBACK_HTML = ROOT / "etl" / "data" / "web_cnd_sample.html"

URL = "https://www.cnd.fr"  # Exemple fictif; remplacer par l'URL réelle // page à scraper // point d'entrée général; juste pour démontrer l'extraction

# Normalisation simple d'une chaîne de caractères
def norm(s: str) -> str:
    if s is None: return ""
    s = unicodedata.normalize("NFKC", s).strip()
    s = re.sub(r"\s+", " ", s).lower()
    s = s.replace("tres", "très")
    return s

# Journalisation simple
def log(msg: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")

# Extraction simple des mots depuis le HTML
def extract_words_from_html(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    words = []
    # Démo simple: récupérer tous les <li> (ex. biblios, nav, etc.) puis on filtre
    for li in soup.find_all("li"):
        text = (li.get_text() or "").strip()
        if 2 <= len(text) <= 30:
            words.append(text)
    # couper à 10 pour une preuve simple
    return words[:10]

# ETL principal
def main():
    print("=== ETL Webscraping CND → poetic_inspiration ===")
    print(f"DST: {DB_MAIN}")

    html = "" 
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
        html = r.text
        print("→ Scraping en ligne OK (extraction simple)")
    except Exception as e:
        print(f"  ! Scraping en ligne impossible : {e}")
        if FALLBACK_HTML.exists():
            html = FALLBACK_HTML.read_text(encoding="utf-8")
            print(f"→ Fallback local utilisé : {FALLBACK_HTML}")
        else:
            print("  ! Aucun fallback local, arrêt.")
            log("CND ERROR no network and no fallback")
            return

    raw_words = extract_words_from_html(html)
    # EDA
    raw = len(raw_words)
    seen = set()
    keep = 0

    with sqlite3.connect(DB_MAIN) as con:
        con.execute("PRAGMA foreign_keys = ON")
        for w in raw_words:
            w = norm(w)
            if not w or w in seen:
                continue
            seen.add(w)
            con.execute(
                "INSERT OR IGNORE INTO poetic_inspiration(label, source) VALUES (?,?)",
                (w, "webscrap"),
            )
            keep += 1
        con.commit()

    print(f"EDA [poetic] : {raw} → {keep} lignes (dédup / nettoyage).")
    log(f"webscrap raw={raw} kept={keep}")

if __name__ == "__main__":
    main()
