"""Point d'entrée unique du projet : un petit menu pour lancer toutes les
fonctionnalités (programme interactif, tests, benchmarks, rapport PDF)
sans avoir à retenir une commande différente pour chacune."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent

MENU = """
===== TP OPTIMISATION — LANCEUR =====
1. Lancer le programme de gestion des livraisons (menu interactif)
2. Lancer les tests (pytest)
3. Lancer les benchmarks (100 / 1 000 / 10 000 / 100 000 colis)
4. Générer le rapport PDF (rapport.md -> rapport.pdf)
0. Quitter
"""


def lancer_programme() -> None:
    from src.cli import CLI

    CLI().run()


def lancer_tests() -> None:
    subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], cwd=RACINE)


def lancer_benchmarks() -> None:
    subprocess.run([sys.executable, "benchmarks/run_benchmarks.py"], cwd=RACINE)


def generer_rapport_pdf() -> None:
    from scripts.generate_pdf import convertir_md_vers_pdf

    convertir_md_vers_pdf()


def main() -> None:
    actions = {
        "1": lancer_programme,
        "2": lancer_tests,
        "3": lancer_benchmarks,
        "4": generer_rapport_pdf,
    }
    while True:
        print(MENU)
        choix = input("Choix : ").strip()
        if choix == "0":
            print("Au revoir.")
            break
        action = actions.get(choix)
        if action is None:
            print("Choix invalide.")
            continue
        action()


if __name__ == "__main__":
    main()
