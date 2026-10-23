"""Préparation et affichage du chargement d'un camion."""

from __future__ import annotations

from dataclasses import dataclass

from .knapsack import ResultatKnapsack, preparer_camion
from .models import Colis


@dataclass
class Camion:
    capacite: int
    resultat: ResultatKnapsack


def preparer(colis: list[Colis], capacite: int, avec_priorite: bool = False, alpha: float = 0.3) -> Camion:
    resultat = preparer_camion(colis, capacite, avec_priorite=avec_priorite, alpha=alpha, methode="auto")
    return Camion(capacite=capacite, resultat=resultat)


def formater_chargement(camion: Camion) -> str:
    resultat = camion.resultat
    lignes = []
    if resultat.avertissement:
        lignes.append(f"⚠ {resultat.avertissement}")

    lignes.append(f"{'ID':>6} {'Poids':>6} {'Valeur':>8} {'Priorité':>9}  Destination")
    for c in resultat.colis_selectionnes:
        lignes.append(f"{c.id:>6} {c.poids:>6} {c.valeur:>8.2f} {c.priorite:>9}  {c.destination}")

    lignes.append("")
    lignes.append(
        f"Poids total  : {resultat.poids_total} / {camion.capacite} kg "
        f"({100 * resultat.poids_total / camion.capacite:.1f} % de la capacité)"
        if camion.capacite > 0
        else f"Poids total  : {resultat.poids_total} / {camion.capacite} kg"
    )
    lignes.append(f"Valeur transportée : {resultat.valeur_totale_reelle:.2f}")
    lignes.append(f"Nombre de colis chargés : {len(resultat.colis_selectionnes)}")
    lignes.append(f"Méthode utilisée : {resultat.methode_utilisee}")
    return "\n".join(lignes)
