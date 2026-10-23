"""Sélection optimale des colis à charger dans le camion.

C'est le cœur algorithmique du TP : un problème de sac à dos 0/1 (chaque
colis est pris en entier ou pas du tout, une seule fois). On veut
maximiser la valeur totale transportée sans dépasser la capacité (en kg,
entière) du camion.

Un seul algorithme de programmation dynamique (`knapsack_01_dp`) est
documenté et réutilisé deux fois : une fois avec la valeur brute des
colis, une fois avec une valeur "ajustée" par la priorité
(`calculer_valeur_ajustee_priorite`). Dans les deux cas, la valeur
réellement transportée (`valeur_totale_reelle`) est toujours recalculée à
partir des vraies valeurs des colis sélectionnés, jamais de la valeur
ajustée qui ne sert qu'à guider la sélection.

Voir rapport.md (fiche algorithmique "Sac à dos 0/1") pour la discussion
complète de la complexité et des limites.
"""

from __future__ import annotations

from array import array
from dataclasses import dataclass

from .models import PRIORITE_MAX, PRIORITE_MIN, Colis

# Au-delà de ce produit n * capacite, la table de reconstruction O(n *
# capacite) devient trop coûteuse en temps/mémoire pour un usage
# interactif : on bascule automatiquement sur l'heuristique gloutonne
# (voir preparer_camion). Valeur choisie empiriquement pour rester
# réactif (quelques secondes maximum) même en pur Python.
SEUIL_N_CAPACITE = 3_000_000


@dataclass
class ResultatKnapsack:
    colis_selectionnes: list[Colis]
    valeur_totale_reelle: float
    poids_total: int
    valeur_utilisee_pour_optimisation: float
    methode_utilisee: str  # "dp" ou "glouton"
    avertissement: str | None = None


def knapsack_01_dp(
    colis: list[Colis],
    capacite: int,
    valeurs_entree: list[float] | None = None,
) -> ResultatKnapsack:
    """Sac à dos 0/1 exact par programmation dynamique.

    Principe (sous-structure optimale de Bellman) : soit dp[w] la
    meilleure valeur atteignable avec un budget de poids w, en ayant déjà
    considéré un certain préfixe de colis. Pour un nouveau colis i de
    poids p_i et de valeur v_i :
        dp[w] = max(dp[w],            # on ne prend pas le colis i
                     dp[w - p_i] + v_i)  # on prend le colis i

    On utilise un tableau `dp` 1D "roulant" (une seule dimension, de
    taille capacite + 1) et on le met à jour de w = capacite jusqu'à
    w = p_i en DÉCROISSANT : ainsi dp[w - p_i] contient encore la valeur
    d'AVANT la prise en compte du colis i (puisqu'on écrit les indices
    plus grands avant les plus petits), ce qui garantit que chaque colis
    n'est utilisé qu'une seule fois.

    Reconstruction du sous-ensemble choisi : on ne garde pas une table
    complète des valeurs dp[i][w] (ce qui doublerait l'usage mémoire sans
    raison), mais seulement une matrice compacte de booléens `keep[i][w]`
    (1 octet par cellule via `array('B', ...)`) indiquant si le colis i a
    été inclus pour obtenir la meilleure valeur à l'état w. On retrouve
    ensuite le sous-ensemble en remontant de i = n-1 à 0.

    Complexité temporelle : O(n * capacite).
    Complexité spatiale : O(capacite) pour `dp` + O(n * capacite) pour
    `keep` (1 octet/cellule) -- c'est ce terme qui explose en mémoire pour
    de grandes instances (voir SEUIL_N_CAPACITE et le rapport).

    Optimalité : garantie (preuve par récurrence sur la sous-structure
    optimale du problème).
    """
    n = len(colis)
    if valeurs_entree is None:
        valeurs_entree = [c.valeur for c in colis]

    dp = [0.0] * (capacite + 1)
    keep: list[array] = [array("B", bytes(capacite + 1)) for _ in range(n)]

    for i in range(n):
        poids_i = colis[i].poids
        if poids_i > capacite:
            continue  # ce colis ne peut jamais entrer dans le camion
        valeur_i = valeurs_entree[i]
        ligne_keep = keep[i]
        for w in range(capacite, poids_i - 1, -1):
            candidat = dp[w - poids_i] + valeur_i
            if candidat > dp[w]:
                dp[w] = candidat
                ligne_keep[w] = 1

    selectionnes: list[Colis] = []
    w = capacite
    for i in range(n - 1, -1, -1):
        if keep[i][w]:
            selectionnes.append(colis[i])
            w -= colis[i].poids
    selectionnes.reverse()

    return ResultatKnapsack(
        colis_selectionnes=selectionnes,
        valeur_totale_reelle=sum(c.valeur for c in selectionnes),
        poids_total=sum(c.poids for c in selectionnes),
        valeur_utilisee_pour_optimisation=dp[capacite],
        methode_utilisee="dp",
    )


def knapsack_glouton_ratio(colis: list[Colis], capacite: int) -> ResultatKnapsack:
    """Heuristique gloutonne : trie les colis par ratio valeur/poids
    décroissant (Timsort, O(n log n)) puis les ajoute tant que la
    capacité restante le permet.

    Rapide (O(n log n) temps, O(n) espace pour la copie triée) mais PAS
    garantie optimale pour le sac à dos 0/1 (contrairement au cas
    fractionnaire, où ce glouton est optimal). Contre-exemple classique :
    poids [10, 20, 30], valeurs [60, 100, 120], capacité 50 -- le glouton
    choisit les colis 1 et 2 (valeur 160) alors que l'optimum est 2 et 3
    (valeur 220). Utilisée ici comme solution de repli rapide quand la DP
    exacte devient trop coûteuse (voir SEUIL_N_CAPACITE).
    """
    colis_tries = sorted(colis, key=lambda c: c.valeur / c.poids, reverse=True)
    selectionnes: list[Colis] = []
    poids_restant = capacite
    for c in colis_tries:
        if c.poids <= poids_restant:
            selectionnes.append(c)
            poids_restant -= c.poids

    valeur_totale = sum(c.valeur for c in selectionnes)
    return ResultatKnapsack(
        colis_selectionnes=selectionnes,
        valeur_totale_reelle=valeur_totale,
        poids_total=capacite - poids_restant,
        valeur_utilisee_pour_optimisation=valeur_totale,
        methode_utilisee="glouton",
    )


def calculer_valeur_ajustee_priorite(colis: list[Colis], alpha: float = 0.3) -> list[float]:
    """Valeur "vue" par l'algorithme de sélection quand on veut favoriser
    les colis prioritaires, sans changer d'algorithme.

        score_normalise = (priorite - PRIORITE_MIN) / (PRIORITE_MAX - PRIORITE_MIN)
        valeur_ajustee   = valeur * (1 + alpha * score_normalise)

    Avec la convention retenue (priorite 5 = la plus importante), un
    colis de priorité maximale voit sa valeur d'entrée augmentée de
    `alpha * 100` % au maximum (alpha = 0.3 par défaut : +30 % max),
    tandis qu'un colis de priorité minimale (1) n'est pas boosté du tout.
    Ce facteur suffit à faire basculer des choix proches en ratio
    valeur/poids sans écraser complètement la logique de maximisation de
    la valeur brute (voir rapport.md, section "Variante priorité").
    """
    etendue = PRIORITE_MAX - PRIORITE_MIN
    valeurs_ajustees = []
    for c in colis:
        score_normalise = (c.priorite - PRIORITE_MIN) / etendue
        valeurs_ajustees.append(c.valeur * (1 + alpha * score_normalise))
    return valeurs_ajustees


def preparer_camion(
    colis: list[Colis],
    capacite: int,
    avec_priorite: bool = False,
    alpha: float = 0.3,
    methode: str = "auto",
) -> ResultatKnapsack:
    """Point d'entrée unique utilisé par la CLI et les benchmarks.

    methode: "auto" (choisit dp ou glouton selon SEUIL_N_CAPACITE),
             "dp" (force la DP exacte), "glouton" (force l'heuristique).
    """
    valeurs_entree = calculer_valeur_ajustee_priorite(colis, alpha) if avec_priorite else None

    bascule_automatique = False
    if methode == "auto":
        produit = len(colis) * max(capacite, 1)
        methode = "dp" if produit <= SEUIL_N_CAPACITE else "glouton"
        bascule_automatique = methode == "glouton"

    if methode == "dp":
        resultat = knapsack_01_dp(colis, capacite, valeurs_entree)
    elif methode == "glouton":
        if avec_priorite:
            # Le glouton trie par ratio valeur/poids : on lui fournit des
            # colis "virtuels" dont la valeur est la valeur ajustée, pour
            # que le tri reflète aussi la priorité, puis on recalcule la
            # vraie valeur transportée à partir des colis réels choisis.
            colis_virtuels = [
                Colis(c.id, c.poids, v, c.priorite, c.destination)
                for c, v in zip(colis, valeurs_entree)
            ]
            resultat_virtuel = knapsack_glouton_ratio(colis_virtuels, capacite)
            ids_choisis = {c.id for c in resultat_virtuel.colis_selectionnes}
            selectionnes = [c for c in colis if c.id in ids_choisis]
            resultat = ResultatKnapsack(
                colis_selectionnes=selectionnes,
                valeur_totale_reelle=sum(c.valeur for c in selectionnes),
                poids_total=sum(c.poids for c in selectionnes),
                valeur_utilisee_pour_optimisation=resultat_virtuel.valeur_utilisee_pour_optimisation,
                methode_utilisee="glouton",
            )
        else:
            resultat = knapsack_glouton_ratio(colis, capacite)
    else:
        raise ValueError(f"méthode inconnue : {methode!r}")

    if methode == "glouton":
        if bascule_automatique:
            resultat.avertissement = (
                "Instance trop grande pour la programmation dynamique exacte "
                f"(n x capacite = {len(colis) * capacite:,} > {SEUIL_N_CAPACITE:,}) : "
                "bascule automatique sur la solution gloutonne, non garantie optimale."
            )
        else:
            resultat.avertissement = "Méthode gloutonne demandée explicitement : non garantie optimale."

    return resultat
