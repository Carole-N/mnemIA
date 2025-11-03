# MnémIA

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)
![Pandas](https://img.shields.io/badge/Pandas-EDA-orange?logo=pandas)
![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-brightgreen?logo=mongodb)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![BeautifulSoup](https://img.shields.io/badge/WebScraping-BeautifulSoup-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative)

> **MnémIA** – un générateur de modules chorégraphiques poétiques.  
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
10. [Captures et preuves](#captures-et-preuves)
11. [Licence](#licence)
12. [Autrice](#autrice)

---

## Description
**MnémIA** automatise la création de *modules créatifs* pour l’enseignement artistique.  
Le pipeline **ETL/EDA** collecte, nettoie et uniformise cinq sources de données :  

| Source | Type | Rôle |
|---|---|---|
| `etl_datamuse.py` | API REST | Mots poétiques |
| `etl_csv_constraints.py` | Fichiers CSV | Contraintes physiques |
| `etl_scraping_cnd.py` | Web scraping | Lexique du CND |
| `etl_sqlite_ref.py` | Base SQLite | Lexique artistique |
| `etl_mongodb_joconde.py` | MongoDB | Données “open data” culturelles |

Toutes les données sont consolidées dans **SQLite (`mnemia.db`)** puis exposées via une **API FastAPI**.

---

## Objectifs du projet
- Collecter et agréger **5 sources hétérogènes**.  
- Nettoyer automatiquement les données : minuscules, accents, espaces, doublons.  
- Charger le tout dans une base relationnelle **SQLite**.  
- Exposer les jeux de données via une **API REST documentée**.  
- Garantir la **traçabilité et la reproductibilité** (logs d’exécution).  

---

## Fonctionnalités principales
- **ETL complet** : extraction, transformation, chargement.  
- **EDA générique** : correction automatique (`tres rapide → très rapide`).  
- **Base Merise complète** : 8 tables (category, constraint, movement…).  
- **API FastAPI** : `/inspirations/random`, `/phrases/generate`, CRUD mouvements.  
- **Conformité RGPD** : aucune donnée personnelle traitée.

---

## Technologies utilisées
| Outil | Usage |
|---|---|
| **Python 3.x** | Langage principal |
| **Pan**
