"""Mesure réelle des temps d'exécution des opérations principales pour
n = 100, 1 000, 10 000, 100 000 colis.

Trois opérations sont chronométrées :
  1. Recherche par ID — dict O(1) moyen vs recherche linéaire O(n).
  2. Tri (Timsort) par poids/valeur/priorité — O(n log n).
  3. Préparation du camion (sac à dos 0/1 DP) — O(n x capacite), avec
     bascule automatique sur le glouton au-delà du seuil mémoire/temps
     (voir src/knapsack.py::SEUIL_N_CAPACITE).

Les résultats sont affichés en tableau et écrits dans
benchmarks/results/benchmark_results.csv pour être repris dans le rapport.
"""

from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from benchmarks.bench_utils import chrono
from src.data_loader import generer_colis_aleatoires
from src.knapsack import SEUIL_N_CAPACITE, preparer_camion
from src.repository import ColisRepository
from src.tri import trier_par_poids

TAILLES = [100, 1_000, 10_000, 100_000]
CAPACITES_TEST = [200, 1_000]
NB_RECHERCHES = 200

CHEMIN_RESULTATS = Path(__file__).resolve().parent / "results" / "benchmark_results.csv"


def bench_recherche_id(repo: ColisRepository, n: int) -> list[dict]:
    rng = random.Random(123)
    ids_existants = rng.sample(range(1, n + 1), k=min(NB_RECHERCHES, n))

    with chrono() as c_dict:
        for id_ in ids_existants:
            repo.rechercher_par_id(id_)
    temps_dict = c_dict.secondes / len(ids_existants)

    with chrono() as c_lineaire:
        for id_ in ids_existants:
            repo.rechercher_lineaire_par_id(id_)
    temps_lineaire = c_lineaire.secondes / len(ids_existants)

    return [
        {"taille_n": n, "operation": "recherche_id_dict", "parametre": "", "temps_s": f"{temps_dict:.9f}", "remarque": "moyenne par recherche, O(1) moyen"},
        {"taille_n": n, "operation": "recherche_id_lineaire", "parametre": "", "temps_s": f"{temps_lineaire:.9f}", "remarque": "moyenne par recherche, O(n)"},
    ]


def bench_tri(colis: list, n: int) -> list[dict]:
    with chrono() as c:
        trier_par_poids(colis)
    return [{"taille_n": n, "operation": "tri_par_poids", "parametre": "", "temps_s": f"{c.secondes:.6f}", "remarque": "Timsort, O(n log n)"}]


def bench_knapsack(colis: list, n: int, capacite: int) -> dict:
    produit = n * capacite
    with chrono() as c:
        resultat = preparer_camion(colis, capacite, methode="auto")
    remarque = "DP exacte, O(n x capacite)" if resultat.methode_utilisee == "dp" else f"bascule glouton (n x capacite = {produit:,} > seuil {SEUIL_N_CAPACITE:,})"
    return {"taille_n": n, "operation": "preparer_camion", "parametre": f"capacite={capacite}", "temps_s": f"{c.secondes:.6f}", "remarque": remarque}


def main() -> None:
    lignes: list[dict] = []

    for n in TAILLES:
        print(f"\n=== n = {n:,} colis ===")
        colis = generer_colis_aleatoires(n, seed=42)

        repo = ColisRepository()
        for c in colis:
            repo.ajouter_colis(c)

        lignes_recherche = bench_recherche_id(repo, n)
        lignes.extend(lignes_recherche)
        for l in lignes_recherche:
            print(f"  {l['operation']:<25} {float(l['temps_s']):.9f} s  ({l['remarque']})")

        lignes_tri = bench_tri(colis, n)
        lignes.extend(lignes_tri)
        for l in lignes_tri:
            print(f"  {l['operation']:<25} {float(l['temps_s']):.6f} s  ({l['remarque']})")

        for capacite in CAPACITES_TEST:
            ligne_knapsack = bench_knapsack(colis, n, capacite)
            lignes.append(ligne_knapsack)
            print(f"  preparer_camion(cap={capacite:<5}) {float(ligne_knapsack['temps_s']):.6f} s  ({ligne_knapsack['remarque']})")

    CHEMIN_RESULTATS.parent.mkdir(parents=True, exist_ok=True)
    with open(CHEMIN_RESULTATS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["taille_n", "operation", "parametre", "temps_s", "remarque"])
        writer.writeheader()
        writer.writerows(lignes)

    print(f"\nRésultats écrits dans {CHEMIN_RESULTATS}")


if __name__ == "__main__":
    main()
