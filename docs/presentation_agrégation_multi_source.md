# Présentation du projet mnemIA : Agrégation multi-source

---

## Slide 1 : Schéma de flux global

```
flowchart LR
    subgraph Sources de données
        CSV[CSV\n(positions, parties, vitesses...)]
        DATAMUSE[API Datamuse]
        WEBSCRAP[Webscraping CND]
        SQLITE[SQLite source_ref]
        MONGODB[MongoDB Joconde]
    end
    CSV -->|ETL/EDA CSV| REF[Tables de référence\n(category, constraints, movement...)]
    DATAMUSE -->|ETL/EDA| INSP[poetic_inspiration]
    WEBSCRAP -->|ETL/EDA| INSP
    SQLITE -->|ETL/EDA| INSP
    MONGODB -->|ETL/EDA| INSP
```

---

## Slide 2 : Rôle des sources

- **CSV** : structure les mouvements, contraintes, catégories, etc. (tables de référence)
- **API Datamuse, Webscraping, SQLite, MongoDB** : alimentent la table centrale `poetic_inspiration` (inspirations poétiques)
- Chaque source a son propre script ETL/EDA pour nettoyer, normaliser et insérer les données dans la base.

---

## Slide 3 : Exemples de données

**Tables de référence (issues des CSV)**

| id_category | name                |
|-------------|---------------------|
| 1           | positions_dans_l_espace |
| 2           | parties_du_corps    |
| 3           | vitesses_d_execution|

**Table centrale : poetic_inspiration**

| id_poetic_inspiration | label      | source        |
|----------------------|------------|---------------|
| 1                    | brume      | datamuse      |
| 2                    | lumière    | webscrap      |
| 3                    | envol      | sqlite_source |
| 4                    | ...        | mongodb       |

---

## Slide 4 : Récapitulatif ETL multi-source

```
--- Récap par source (poetic_inspiration) ---
API Datamuse     190
CSV              1
SQLite           30
Web scraping     50
MongoDB          1
```

Chaque source a bien alimenté la base, preuve de l’agrégation multi-source.

---

## Slide 5 : Utilisation finale

- Les tables de référence structurent les mouvements et contraintes pour la génération chorégraphique.
- La table `poetic_inspiration` centralise toutes les inspirations poétiques, utilisées pour composer ou analyser des séquences.
- Exemple d’utilisation :
  - Générer une séquence en combinant un mouvement (issu des CSV) et une inspiration (issue de n’importe quelle source).
- **Schéma d’utilisation** :

```
flowchart LR
    REF[Tables de référence] --\nstructure\n--> APP[Application/Analyse]
    INSP[poetic_inspiration] --\ninspiration\n--> APP
```

---

