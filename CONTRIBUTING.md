# 🤝 Contribuer à Grove
Bienvenue ! Merci d’envisager de contribuer à Grove, le générateur de projets CLI modulaire orienté R&D. Ce document vous explique comment contribuer efficacement et dans le respect des standards élevés que nous avons définis.

## 🧭 Philosophie du projet
Grove est un projet modulaire, évolutif et structuré. Chaque contribution doit respecter :

- Une clarté dans l’objectif
- Une cohérence avec l’architecture existante
- Une testabilité (via pytest)
- Une documentation minimale mais suffisante

## ✅ Prérequis
Avant toute contribution :

- Forkez le projet
- Créez une branche claire (ex. : feat/init-factory, fix/cli-crash)
- Assurez-vous d’avoir Python 3.10+ et poetry ou pip installés
- Installez les dépendances :

```bash
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
```
## 🧪 Tests
Tout nouveau code doit être testé. Utilisez pytest et placez vos tests dans le dossier tests/ en miroir de la structure du projet.

Lancer les tests :

```bash
pytest
```

## 🎯 Types de contributions acceptées
Création de modules CLI ou services dans l’écosystème Grove

- Ajout de templates Jinja2 ou surcharge de structure
- Refactoring propre
- Documentation claire, notamment les README de sous-modules
- Correction de bugs avérés (avec test associé)

## 🚫 Ce que nous ne voulons pas
- Pas de code non typé (mypy doit passer)
- Pas de dépendances inutiles
- Pas de code non testé
- Pas de commit directement sur main

## 📦 Convention de commits (Conventional Commits)
Utilisez la convention suivante :

- `feat`: nouvelle fonctionnalité
- `fix`: correction de bug
- `docs`: modification de la documentation uniquement
- `refactor`: refactorisation sans changement de comportement
- `test`: ajout ou correction de tests
- `chore`: tâches annexes (ex: MAJ dépendances)

Exemple :

```md
feat(cli): add init command with interactive prompt
```

## 🔍 Revue de code
- Chaque PR doit être revu par au moins une personne
- Donnez du contexte dans votre description
- Soyez ouvert aux retours et proposez des alternatives si nécessaire
- Incluez un lien vers une issue quand c’est pertinent

## 📄 Licences et contributions externes
- Toute contribution est placée sous licence du projet (MIT)
- Ne copiez jamais de code sous licence incompatible

## 🙏 Merci
Merci d’avoir lu ce guide. Grove a besoin de vous pour s’améliorer, mais dans le respect de sa vision, de sa rigueur et de sa modularité.

Pour toute question : ouvrez une discussion ou contactez les mainteneurs.
