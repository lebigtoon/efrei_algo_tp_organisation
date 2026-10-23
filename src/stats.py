"""Statistiques descriptives sur la collection de colis et sur un
chargement. Calculées en un seul passage O(n) sur la liste (temps O(n),
espace O(1) en plus des structures de comptage dont la taille est bornée
par le nombre de priorités/destinations distinctes, négligeable devant n).
"""

from __future__ import annotations

from .camion import Camion
from .models import Colis


def statistiques_globales(colis: list[Colis]) -> dict:
    if not colis:
        return {"nombre_colis": 0}

    poids = [c.poids for c in colis]
    valeurs = [c.valeur for c in colis]

    repartition_priorite: dict[int, int] = {}
    repartition_destination: dict[str, int] = {}
    for c in colis:
        repartition_priorite[c.priorite] = repartition_priorite.get(c.priorite, 0) + 1
        repartition_destination[c.destination] = repartition_destination.get(c.destination, 0) + 1

    n = len(colis)
    return {
        "nombre_colis": n,
        "poids_total": sum(poids),
        "poids_moyen": sum(poids) / n,
        "poids_min": min(poids),
        "poids_max": max(poids),
        "valeur_totale": sum(valeurs),
        "valeur_moyenne": sum(valeurs) / n,
        "valeur_min": min(valeurs),
        "valeur_max": max(valeurs),
        "repartition_priorite": repartition_priorite,
        "repartition_destination": repartition_destination,
    }


def statistiques_chargement(camion: Camion) -> dict:
    resultat = camion.resultat
    nb_charges = len(resultat.colis_selectionnes)
    taux_remplissage = resultat.poids_total / camion.capacite if camion.capacite > 0 else 0.0
    valeur_moyenne_par_colis = resultat.valeur_totale_reelle / nb_charges if nb_charges > 0 else 0.0
    return {
        "nombre_colis_charges": nb_charges,
        "poids_total": resultat.poids_total,
        "capacite": camion.capacite,
        "taux_remplissage": taux_remplissage,
        "valeur_totale": resultat.valeur_totale_reelle,
        "valeur_moyenne_par_colis": valeur_moyenne_par_colis,
        "methode_utilisee": resultat.methode_utilisee,
    }
