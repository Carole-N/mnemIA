# MnémIA

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)
![Pandas](https://img.shields.io/badge/Pandas-EDA-orange?logo=pandas)
![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-brightgreen?logo=mongodb)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![BeautifulSoup](https://img.shields.io/badge/WebScraping-BeautifulSoup-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative)

---

> **MnémIA** est un générateur de modules artistiques conçu pour développer la créativité.  
> Destiné en premier lieu aux enseignants du milieu scolaire, cet outil inclusif s’adresse à toutes et à tous, quel que soit l’âge, le niveau et la physicalité. Il ambitionne d'accompagner les enseignants dans la conception de projets artistiques en utilisant la donnée comme déclencheur de créativité.
> Cette première version permet de composer des phrases chorégraphiques à partir d’un processus de création fondé sur les notions de contrainte et d’aléatoire, deux puissants leviers de créativité.  
> La version 2 visera à étendre cette approche à d’autres champs artistiques.
>
> Projet réalisé pour la certification **RNCP37827 – Développeur·se en Intelligence Artificielle (Bloc E1)**.  
> Objectif : illustrer la **chaîne complète de la donnée** – collecte, nettoyage, stockage et exposition via API.

---

## Table des matières
1. [Description](#description)
2. [Objectifs du projet](#objectifs-du-projet)
3. [Fonctionnalités principales](#fonctionnalités-principales)
---

| Source | Type | Rôle |
|---|---|---|
| `etl_datamuse.py` | API REST | Mots poétiques |
| `etl_csv_constraints.py` | Fichiers CSV | Contraintes physiques |
| `etl_scraping_cnd.py` | Web scraping | Lexique du CND |
| `etl_sqlite_ref.py` | Base SQLite | Lexique artistique |
| `etl_mongodb_joconde.py` | MongoDB | Données “open data” culturelles |

Toutes les données sont consolidées dans SQLite (`mnemia.db`) puis exposées via une API FastAPI.

---

## Objectifs du projet

- Collecter et agréger 5 sources hétérogènes.  
- Nettoyer automatiquement les données : mise en minuscules, correction des accents, suppression des espaces et des doublons.  
- Charger le tout dans une base relationnelle SQLite.  
- Exposer les jeux de données via une API REST documentée.  
- Garantir la traçabilité et la reproductibilité (logs d’exécution).  

---

## Fonctionnalités principales

- EDA générique : correction automatique (`tres rapide → très rapide`).  
- Normalisation (EDA) : homogénéisation des textes (mise en casse, normalisation Unicode, suppression d'espaces superflus, standardisation des accents et mappings de corrections).
- Base Merise complète : 8 tables (category, constraint, movement, etc.).  
- API FastAPI : `/inspirations/random`, `/phrases/generate`, CRUD mouvements.  
- Conformité RGPD : aucune donnée personnelle traitée.
---

## Technologies utilisées

| Outil | Usage |
|---|---|
| Pandas | Nettoyage (EDA) |
| SQLite | Base relationnelle |
| MongoDB | Source Big Data |
| BeautifulSoup | Web scraping |
| FastAPI | API REST |
| Uvicorn | Serveur ASGI |
| Git / GitHub | Versionnement |

---

## Architecture du pipeline ETL

         +------------------------------+
         |    etl_datamuse.py (API)     |
         +-------------+----------------+
                       |
         +-------------v----------------+
         | etl_csv_constraints.py (CSV) |
         +-------------+----------------+
                       |
         +-------------v----------------+
         |  etl_scraping_cnd.py (Web)   |
         +-------------+----------------+
                       |
         +-------------v----------------+
         |   etl_sqlite_ref.py (SQLite) |
         +-------------+----------------+
                       |
         +-------------v----------------+
         | etl_mongodb_joconde.py (NoSQL)|
         +-------------+----------------+
                       |
                       v
                EDA (normalize_text)
                       |
                       v
           SQLite — mnemia.db  →  FastAPI (API)

---

## Scripts ETL

| Script | Description | Destination |
|---|---|---|
| `etl_datamuse.py` | Extraction depuis l’API Datamuse | `poetic_inspiration` |
| `etl_csv_constraints.py` | Import CSV (positions, corps, vitesses) | `constraint` |
| `etl_scraping_cnd.py` | Webscraping CND | `constraint` |
| `etl_sqlite_ref.py` | Lecture mini-base SQLite | `category` / `constraint` |
| `etl_mongodb_joconde.py` | Lecture MongoDB | `poetic_inspiration` |

Chaque script écrit un log individuel (`logs/etl_*.log`) et alimente la base principale `mnemia.db`.

### Normalisation (EDA)

Avant le chargement, chaque script applique une étape de normalisation (fonction `normalize_text`) qui :

- met les textes en minuscules et retire les espaces superflus ;
- normalise les caractères Unicode et les accents ;
- applique des mappings/corrections (ex. `tres rapide` → `très rapide`) ;
- supprime les doublons après normalisation.

Exemple simplifié (pseudo-code) :

```python
import re
import unicodedata

def normalize_text(s: str) -> str:
       s = (s or "").strip().lower()
       s = unicodedata.normalize('NFC', s)
       s = re.sub(r'\s+', ' ', s)
       s = s.replace('tres', 'très')
       return s
```

---

## Installation

```bash
git clone https://github.com/Carole-N/mnemIA.git
cd mnemIA
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

---

## Lancement du projet

### Étape 1 : Exécuter les scripts ETL

Chaque script peut être lancé indépendamment afin de prouver la collecte et le chargement des données par source.

```bash
python etl/etl_datamuse.py
python etl/etl_csv_constraints.py
python etl/etl_scraping_cnd.py
python etl/etl_sqlite_ref.py
python etl/etl_mongodb_joconde.py
```

Chaque exécution génère un fichier de log dans etl/logs/, traçant le nombre de lignes importées et nettoyées.

---

## Étape 2 : Démarrer l’API FastAPI

```bash
uvicorn main:app --reload --port 8000
```

---

Accès à la documentation interactive Swagger :
http://127.0.0.1:8000/docs

Accès direct à l’API :
http://127.0.0.1:8000/

---

## Déploiement

Mode d’emploi pour le déploiement en production de MnémIA



- Utiliser un serveur ASGI stable : ex. `uvicorn` en production derrière `gunicorn` (gunicorn + uvicorn workers) ou seulement `uvicorn` avec gestionnaire de processus (systemd, supervisord).
- Fournir les variables sensibles via des variables d'environnement ou un gestionnaire de secrets (ne pas committer `.env`). Utiliser le fichier `.env.example` comme modèle.
- Mettre l'application derrière un reverse proxy (nginx) pour gérer TLS/SSL, compression et mise en cache.
- Prévoir une journalisation structurée et une rotation des logs (logrotate) pour les fichiers dans `etl/logs/`.
- Pour les petites installations, un déploiement simple avec `systemd` est suffisant (exemple ci‑dessous). Pour un déploiement conteneurisé, docker-compose ou Kubernetes conviennent selon l'échelle.

Exemple minimal `systemd` (adapté à votre chemin d'installation) :

```ini
[Unit]
Description=mnemIA API

[Service]
User=youruser
WorkingDirectory=/home/youruser/iadev/mnemIA
EnvironmentFile=/home/youruser/iadev/mnemIA/.env
ExecStart=/home/youruser/iadev/mnemIA/.venv/bin/uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
Restart=always

[Install]
WantedBy=multi-user.target
```

Exemple Docker Compose (très basique) :

```yaml
version: '3.8'
services:
       app:
              build: .
              command: uvicorn main:app --host 0.0.0.0 --port 8000
              ports:
                     - "8000:8000"
              env_file:
                     - .env
              volumes:
                     - ./etl/logs:/app/etl/logs
```

Si tu veux, je peux ajouter un `Dockerfile` minimal et un `docker-compose.yml` en draft dans le repo pour que tu puisses tester le déploiement conteneurisé.

---

## Structure du dépôt

Note : voici une vue simplifiée des fichiers versionnés uniquement. Les artefacts générés localement (environnements virtuels, bases de données, fichiers `.env`, logs temporaires) ne sont pas commités — consultez `.gitignore`.

```text
├── etl/
│   ├── data/
│   ├── etl_csv_constraints.py
│   ├── etl_datamuse.py
│   ├── etl_mongodb_joconde.py
│   ├── etl_scraping_cnd.py
│   ├── etl_sqlite_ref.py
│   └── run_etl.py
├── main.py
├── mcd_mnemia.py
├── requirements.txt
├── README.md
├── schema.sql
├── seed.sql
├── .env.example
├── LICENSE
└── storage/
       └── db_init.py
```

---

## Captures et preuves

Les preuves de bon fonctionnement sont regroupées dans docs/captures_E1/ :

| Capture | Description                                              |
| ------- | -------------------------------------------------------- |
| Cap 1   | Exécution du pipeline Datamuse                           |
| Cap 2   | Import CSV des contraintes                               |
| Cap 3   | EDA : correction automatique “tres rapide → très rapide” |
| Cap 4   | Requête SQLite (contraintes propres)                     |
| Cap 5   | etl_log.txt – récapitulatif par source                   |

---

## Licence

Ce projet est distribué sous la licence MIT.
>
> © 2025 – Carole Novak

---

## Autrice

Carole Novak
>
> Projet réalisé dans le cadre de la certification RNCP 37827 – Bloc E1 “Réaliser la collecte, le stockage et la mise à disposition des données”.
> 
> Dépôt GitHub : https://github.com/Carole-N/mnemIA

---


