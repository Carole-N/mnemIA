# MnémIA — Guide de démo rapide

Ce guide synthétise l’ordre des étapes pour présenter l’API devant le jury, avec des phrases pédagogiques à utiliser.

## Ordre de la démo

1. **Accueil**
   - Ouvrir la page d’accueil (`/`) pour présenter le projet et l’API.
2. **Documentation Swagger**
   - Accéder à `/docs` pour explorer les routes et la documentation interactive.
3. **Authentification**
   - Cliquer sur le bouton Authorize et entrer le token (API_TOKEN) pour débloquer les routes protégées.
4. **Création d’un mouvement**
   - Utiliser POST `/movements` pour créer un mouvement simple, ou POST `/movements/random` pour créer un mouvement avec contraintes aléatoires.
5. **Génération d’une séquence**
   - Utiliser GET `/sequences/generate` pour obtenir une séquence de 3 mouvements et une pause.
6. **Génération d’une phrase chorégraphique**
   - Utiliser GET `/phrases/generate` pour générer une phrase complète (5 mouvements + inspiration poétique).
7. **Inspiration poétique**
   - Utiliser GET `/inspirations/random` pour tirer une consigne poétique.

## Phrases pédagogiques pour le jury

- « Chaque étape du processus créatif est accessible via une route dédiée, illustrant la modularité de l’API. »
- « La séquence permet d’explorer la composition chorégraphique étape par étape, tandis que la phrase complète automatise le processus pour un résultat abouti. »
- « L’authentification par token garantit la sécurité et la traçabilité des accès. »
- « La documentation Swagger rend la prise en main de l’API intuitive et pédagogique. »

## Exemples de réponses

```json
POST /movements/random
{
  "label": "A"
}
Réponse :
{
  "label": "A",
  "contraintes": [
    {"categorie": "positions_dans_l_espace", "contrainte": "à genoux"},
    {"categorie": "parties_du_corps", "contrainte": "dos"},
    {"categorie": "vitesses_d_execution", "contrainte": "lent"}
  ]
}
```

```json
GET /sequences/generate
Réponse :
{
  "sequence": ["B", "A", "A"],
  "pause": "aucune"
}
```

```json
GET /phrases/generate
Réponse :
{
  "sequence": ["A", "B", "A", "B", "A"],
  "pause": "courte",
  "inspiration": "lamplit",
  "description": "Phrase chorégraphique : A, B, A, B, A (inspirée par 'lamplit')."
}
```
