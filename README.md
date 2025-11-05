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
4. [Technologies utilisées](#technologies-utilisées)
5. [Architecture du pipeline ETL](#architecture-du-pipeline-etl)
6. [Scripts ETL](#scripts-etl)
7. [Installation](#installation)
8. [Lancement du projet](#lancement-du-projet)
9. [Structure du dépôt](#structure-du-dépôt)
10. [Déploiement](#déploiement)
11. [Licence](#licence)
12. [Autrice](#autrice)

---

## Description

MnémIA automatise la création de modules créatifs pour l’enseignement artistique.  
Le pipeline ETL/EDA collecte, nettoie et uniformise cinq sources de données :  

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

- ETL complet : extraction, transformation, chargement.  
- EDA générique : correction automatique (`tres rapide → très rapide`).  
- Base Merise complète : 8 tables (category, constraint, movement, etc.).  
- API FastAPI : `/inspirations/random`, `/phrases/generate`, CRUD mouvements.  
- Conformité RGPD : aucune donnée personnelle traitée.

---

## Technologies utilisées

| Outil | Usage |
|---|---|
| Python 3.x | Langage principal |
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
| `etl_scraping_cnd.py` | Webscraping CND (simulé à partir d'un échantillon html - snippet local : web_cnd_sample.html) | `constraint` |
| `etl_sqlite_ref.py` | Lecture mini-base SQLite | `category` / `constraint` |
| `etl_mongodb_joconde.py` | Lecture MongoDB (connexion simulée via un fallback JSON : mongo_sample.json) | `poetic_inspiration` |

Chaque script écrit un log individuel (`logs/etl_*.log`) et alimente la base principale `mnemia.db`.

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

### Étape 2 : Démarrer l’API FastAPI

```bash
uvicorn main:app --reload --port 8000
```

---

Accès à la documentation interactive Swagger :
http://127.0.0.1:8000/docs

Accès direct à l’API :
http://127.0.0.1:8000/

---

## Structure du dépôt

```text
mnemIA/
├── LICENSE                  # Licence du projet (MIT)
├── README.md                # Documentation principale
├── .env.example             # Exemple de configuration d'environnement
├── .env                     # Variables d'environnement (non suivi par git)
├── .gitignore               # Fichiers à ignorer par git
├── main.py                  # API FastAPI principale
├── mcd_mnemia.py            # Modèle conceptuel de données (MCD)
├── requirements.txt         # Dépendances Python
├── schema.sql               # Schéma de la base SQLite
├── seed.sql                 # Script d'initialisation/données exemples
├── docs/                    # Documentation supplémentaire
├── etl/                     # Scripts ETL (collecte et nettoyage des données)
│   ├── etl_csv_constraints.py      # ETL pour les contraintes depuis CSV
│   ├── etl_datamuse.py            # ETL pour l'API Datamuse (inspirations)
│   ├── etl_log.txt                # Log d'exécution des ETL
│   ├── etl_mongodb_joconde.py     # ETL pour MongoDB (Joconde)
│   ├── etl_scraping_cnd.py        # ETL pour le web scraping (CND)
│   ├── etl_sqlite_ref.py          # ETL pour la mini-base SQLite (lexique)
│   ├── run_etl.py                 # Orchestrateur : lance tous les ETL
│   └── data/                      # Données sources pour les ETL
│       ├── mongo_sample.json          # Exemple de données MongoDB
│       ├── parties_du_corps.csv       # CSV contraintes : parties du corps
│       ├── positions_dans_l_espace.csv# CSV contraintes : positions
│       ├── source_ref.db              # Mini-base SQLite (lexique)
│       ├── vitesses_d_execution.csv   # CSV contraintes : vitesses
│       └── web_cnd_sample.html        # Exemple HTML pour web scraping
├── storage/
│   └── mnemia.sqlite            # Base centrale SQLite (non suivie par git)
├── __pycache__/                 # Cache Python (non suivi par git)
├── .venv/                       # Environnement virtuel Python (non suivi par git)                    
```

---

## Déploiement

1. **Installer les dépendances**  
       ```bash
       python -m venv .venv
       source .venv/bin/activate
       pip install -r requirements.txt
       ```

2. **Configurer l’environnement**  
       Copier `.env.example` en `.env` et adapter si besoin :
       ```bash
       cp .env.example .env
       ```

3. **Lancer l’API**  
       ```bash
       uvicorn main:app --host 0.0.0.0 --port 8000
       ```

- Les logs ETL sont générés dans `etl/logs/`.
- La base SQLite (`mnemia.db`) est créée automatiquement lors de l’exécution des scripts ETL.

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


