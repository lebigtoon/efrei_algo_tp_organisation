"""Chargement des colis d'exemple de l'énoncé et génération de jeux de
données aléatoires pour les benchmarks."""

from __future__ import annotations

import csv
import random
from pathlib import Path

from .models import Colis

CHEMIN_EXEMPLE = Path(__file__).resolve().parent.parent / "data" / "colis_exemple.csv"

DESTINATIONS_PAR_DEFAUT = ("Paris", "Lille", "Lyon", "Marseille", "Nantes")


def charger_depuis_csv(chemin: str | Path) -> list[Colis]:
    colis: list[Colis] = []
    with open(chemin, newline="", encoding="utf-8") as f:
        for ligne in csv.DictReader(f):
            colis.append(
                Colis(
                    id=int(ligne["id"]),
                    poids=int(ligne["poids"]),
                    valeur=float(ligne["valeur"]),
                    priorite=int(ligne["priorite"]),
                    destination=ligne["destination"],
                )
            )
    return colis


def charger_exemple_enonce() -> list[Colis]:
    return charger_depuis_csv(CHEMIN_EXEMPLE)


def generer_colis_aleatoires(
    n: int,
    seed: int | None = None,
    poids_range: tuple[int, int] = (1, 50),
    valeur_range: tuple[int, int] = (1, 100),
    priorite_range: tuple[int, int] = (1, 5),
    destinations: tuple[str, ...] = DESTINATIONS_PAR_DEFAUT,
) -> list[Colis]:
    """Génère n colis aléatoires avec des identifiants séquentiels 1..n
    (unicité garantie en O(1) par construction, sans vérification de
    collision)."""
    rng = random.Random(seed)
    colis = []
    for i in range(1, n + 1):
        colis.append(
            Colis(
                id=i,
                poids=rng.randint(*poids_range),
                valeur=float(rng.randint(*valeur_range)),
                priorite=rng.randint(*priorite_range),
                destination=rng.choice(destinations),
            )
        )
    return colis
