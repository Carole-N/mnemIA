# --- Page d'accueil pédagogique ---
@app.get("/", tags=["Accueil"])
def accueil():
    """
    Page d'accueil de l'API MnémIA pour la démonstration.
    """
    return {
        "message": "Bienvenue sur l'API MnémIA ! Rendez-vous sur /docs pour explorer et tester les fonctionnalités pédagogiques de l'API (création de mouvements, séquences, phrases, inspirations, etc.)."
    }

import os
import sqlite3
import random

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from pydantic import BaseModel

# --- Chargement des variables d'environnement ---
load_dotenv()  # lit .env si présent
DB_PATH = os.getenv("DB_PATH", "mnemia.db")
API_TOKEN = os.getenv("API_TOKEN", "CHANGE_ME_TOKEN")

app = FastAPI(title="MnémIA API", version="1.0.0")

from fastapi.openapi.utils import get_openapi

#    
def custom_openapi():
    """Génère un schéma OpenAPI sans valeurs par défaut."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # ---- suppression des defaults ----
    def remove_defaults(schema_part):
        if isinstance(schema_part, dict):
            schema_part.pop("default", None)
            for v in schema_part.values():
                remove_defaults(v)
        elif isinstance(schema_part, list):
            for v in schema_part:
                remove_defaults(v)

    remove_defaults(openapi_schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# --- Page d'accueil pédagogique ---
@app.get("/", tags=["Accueil"])
def accueil():
    """
    Page d'accueil de l'API MnémIA pour la démonstration.
    """
    return {
        "message": "Bienvenue sur l'API MnémIA ! Rendez-vous sur /docs pour explorer et tester les fonctionnalités pédagogiques de l'API (création de mouvements, séquences, phrases, inspirations, etc.)."
    }


# --- Authentification par Bearer Token (afficher le bouton Authorize dans /docs) ---
security = HTTPBearer(auto_error=True)

def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Authentification par jeton de type Bearer (header HTTP Authorization).
    FastAPI (HTTPBearer) gère automatiquement le préfixe 'Bearer ' dans /docs.
    """
    token = credentials.credentials
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Jeton invalide")
    return True


# --- Fonctions SQLite ---
def fetch_one(query, params=()):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    with con:
        row = con.execute(query, params).fetchone()
    con.close()
    return row

def fetch_all(query, params=()):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    with con:
        rows = con.execute(query, params).fetchall()
    con.close()
    return rows

def execute(query, params=()):
    con = sqlite3.connect(DB_PATH)
    with con:
        cur = con.execute(query, params)
        last_id = cur.lastrowid
    con.close()
    return last_id


# --- Modèles Pydantic ---
class MovementIn(BaseModel):
    label: str

    # 👉 Donne un exemple pour la doc, au lieu de "string"
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"label": "C"}
            ]
        }
    }

class MovementRandomIn(BaseModel):
    label: str


# --- Endpoints ---
@app.get("/health", tags=["Système"])
def health():
    """Vérifie la connexion à la base"""
    try:
        con = sqlite3.connect(DB_PATH)
        con.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/movements", dependencies=[Depends(require_auth)], tags=["Mouvements"])
def create_movement(data: MovementIn):
    """Créer un mouvement"""
    new_id = execute("INSERT INTO movement(label) VALUES (?)", (data.label,))
    return {"id": new_id, "label": data.label}


@app.get("/movements/{id}", dependencies=[Depends(require_auth)], tags=["Mouvements"])
def read_movement(id: int):
    """Lire un mouvement"""
    row = fetch_one("SELECT id_movement, label FROM movement WHERE id_movement = ?", (id,))
    if not row:
        raise HTTPException(status_code=404, detail="Mouvement introuvable")
    return dict(row)


@app.put("/movements/{id}", dependencies=[Depends(require_auth)], tags=["Mouvements"])
def update_movement(id: int, data: MovementIn):
    """Modifier un mouvement"""
    if not fetch_one("SELECT id_movement FROM movement WHERE id_movement = ?", (id,)):
        raise HTTPException(status_code=404, detail="Mouvement introuvable")
    execute("UPDATE movement SET label = ? WHERE id_movement = ?", (data.label, id))
    return {"id": id, "label": data.label}


@app.delete("/movements/{id}", dependencies=[Depends(require_auth)], tags=["Mouvements"])
def delete_movement(id: int):
    """Supprimer un mouvement"""
    if not fetch_one("SELECT id_movement FROM movement WHERE id_movement = ?", (id,)):
        raise HTTPException(status_code=404, detail="Mouvement introuvable")
    execute("DELETE FROM movement WHERE id_movement = ?", (id,))
    return {"deleted": id}


@app.get("/inspirations/random", dependencies=[Depends(require_auth)], tags=["Inspirations"])
def get_random_inspiration():
    """Renvoie une consigne poétique aléatoire depuis la table poetic_inspiration."""
    row = fetch_one("SELECT label FROM poetic_inspiration ORDER BY RANDOM() LIMIT 1;")
    if not row:
        raise HTTPException(status_code=404, detail="Aucune inspiration disponible")
    return {"poetic_inspiration": row["label"]}



# Nouvelle route : génère uniquement la séquence mouvements+pauses
@app.get("/sequences/generate", dependencies=[Depends(require_auth)], tags=["Séquences"])
def generate_sequence():
    """
    Génère une séquence chorégraphique :
    - 3 mouvements tirés au hasard (ex. B, B, A)
    - 1 pause aléatoire (courte/longue/aucune)
    """
    rows = fetch_all("SELECT label FROM movement ORDER BY RANDOM() LIMIT 3;")
    if len(rows) == 0:
        raise HTTPException(status_code=400, detail="Aucun mouvement disponible")
    moves = [r["label"] for r in rows]

    p = fetch_one("SELECT label FROM pause ORDER BY RANDOM() LIMIT 1;")
    pause_label = p["label"] if p else "aucune"

    sequence = moves.copy()
    if pause_label and pause_label.lower() != "aucune":
        insert_at = random.randrange(0, len(sequence) + 1)
        sequence.insert(insert_at, "pause")

    return {
        "sequence": sequence,                # ex. ["B", "B", "pause", "A"]
        "pause": pause_label                 # ex. "courte"
    }

# Nouvelle route : assemble séquence + inspiration poétique
@app.get("/phrases/generate", dependencies=[Depends(require_auth)], tags=["Phrases"])
def generate_phrase():
    """
    Génère une phrase chorégraphique complète :
    - Séquence mouvements+pauses
    - Inspiration poétique aléatoire
    """
    # Génère la séquence
    seq = generate_sequence()
    sequence = seq["sequence"]
    pause_label = seq["pause"]

    # Ajoute l'inspiration poétique
    insp = fetch_one("SELECT label FROM poetic_inspiration ORDER BY RANDOM() LIMIT 1;")
    inspiration = insp["label"] if insp else None

    desc = f"Phrase chorégraphique : {', '.join(sequence)}"
    if inspiration:
        desc += f" (inspirée par '{inspiration}')."

    return {
        "sequence": sequence,
        "pause": pause_label,
        "inspiration": inspiration,
        "description": desc
    }

@app.post("/movements/random", dependencies=[Depends(require_auth)], tags=["Mouvements"])
def create_random_movement(data: MovementRandomIn = Body(...)):
    """
    Crée un mouvement avec un label donné et lui associe 3 contraintes aléatoires (une par catégorie).
    Retourne le mouvement et ses contraintes.
    """
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    # 1. Créer le mouvement
    cur = con.execute("INSERT INTO movement(label) VALUES (?)", (data.label,))
    movement_id = cur.lastrowid
    # 2. Tirer 3 contraintes aléatoires (une par catégorie)
    categories = fetch_all("SELECT id_category, name FROM category")
    constraints = []
    for cat in categories:
        row = con.execute(
            "SELECT id_constraints, label FROM constraints WHERE category_id = ? ORDER BY RANDOM() LIMIT 1;",
            (cat["id_category"],)
        ).fetchone()
        if row:
            # Associer la contrainte au mouvement
            con.execute(
                "INSERT INTO movement_choices(movement_id, category_id, constraints_id) VALUES (?, ?, ?)",
                (movement_id, cat["id_category"], row["id_constraints"])
            )
            constraints.append({"categorie": cat["name"], "contrainte": row["label"]})
    con.commit()
    con.close()
    return {"label": data.label, "contraintes": constraints}
