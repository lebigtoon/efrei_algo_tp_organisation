# TP Optimisation — Gestion des livraisons

Programme Python pour gérer une collection de colis et préparer le
chargement optimal d'un camion sous contrainte de capacité (problème du
sac à dos 0/1), avec une variante favorisant les colis prioritaires.

Voir `rapport.pdf` (ou `rapport.md`) pour la justification complète des
choix algorithmiques, les complexités et les mesures de performance.

## Installation

```bash
python3 -m venv .venv          # si .venv n'existe pas déjà
.venv/bin/pip install -r requirements.txt
```

`requirements.txt` ne contient que `pytest` (tests) et `markdown` +
`weasyprint` (génération du PDF du rapport) — aucune dépendance externe
n'est utilisée pour résoudre le sac à dos, les tris ou la recherche, qui
sont implémentés et expliqués dans `src/`.

Sur macOS, `weasyprint` nécessite en plus la bibliothèque système
`pango` : `brew install pango` (uniquement nécessaire pour régénérer
`rapport.pdf`, pas pour utiliser le programme).

## Lancer le menu (tout-en-un)

```bash
.venv/bin/python run.py
```

```
===== TP OPTIMISATION — LANCEUR =====
1. Lancer le programme de gestion des livraisons (menu interactif)
2. Lancer les tests (pytest)
3. Lancer les benchmarks (100 / 1 000 / 10 000 / 100 000 colis)
4. Générer le rapport PDF (rapport.md -> rapport.pdf)
0. Quitter
```

Ce lanceur regroupe toutes les fonctionnalités du projet pour éviter de
retenir une commande différente pour chacune. Chaque option peut aussi
être lancée indépendamment (voir sections suivantes).

## Lancer le programme interactif seul

```bash
.venv/bin/python -m src.main
```

Menu disponible :

```
===== GESTION DES LIVRAISONS =====
1. Afficher les colis
2. Ajouter un colis
3. Rechercher un colis
4. Organiser les colis
5. Préparer un camion
6. Afficher le chargement
7. Afficher les statistiques
0. Quitter
```

Les 5 colis d'exemple de l'énoncé (`data/colis_exemple.csv`, IDs 101-105)
sont chargés automatiquement au démarrage.

## Lancer les tests

```bash
.venv/bin/python -m pytest tests/ -v
```

## Lancer les benchmarks (100 / 1 000 / 10 000 / 100 000 colis)

```bash
.venv/bin/python benchmarks/run_benchmarks.py
```

Affiche les temps mesurés en console et écrit
`benchmarks/results/benchmark_results.csv`.

## Régénérer le rapport PDF

```bash
.venv/bin/python scripts/generate_pdf.py
```

Convertit `rapport.md` en `rapport.pdf` (markdown → HTML → PDF via
weasyprint).

## Structure du projet

```
src/            code source (modèle, stockage, tri, sac à dos, CLI...)
data/           colis d'exemple de l'énoncé
benchmarks/      script et résultats de mesure de performance
tests/            tests pytest
scripts/           génération du rapport PDF
rapport.md/.pdf     rapport détaillé (choix algorithmiques, complexités)
```
# efrei_algo_tp_organisation
