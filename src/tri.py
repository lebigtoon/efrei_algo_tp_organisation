"""Tris d'affichage des colis.

Implémenté via `sorted()`, qui utilise Timsort en Python : l'entrée est
découpée en "runs" déjà triées (triées par insertion si elles sont trop
courtes), puis ces runs sont fusionnées deux à deux comme dans un tri
fusion (avec un mode "galloping" qui accélère la fusion quand une run est
nettement plus longue que l'autre). Timsort est stable (deux éléments de
même clé gardent leur ordre relatif) et adaptatif (proche de O(n) si les
données sont déjà partiellement triées).

Complexité : O(n log n) dans le pire cas, O(n) dans le meilleur cas.
Espace : O(n) (mémoire temporaire utilisée pendant la fusion).

On réimplémente pas Timsort nous-mêmes (ce n'est pas le cœur algorithmique
de ce TP) mais on l'explique dans le rapport comme demandé par l'énoncé.
"""

from __future__ import annotations

from .models import Colis


def trier_par_poids(colis: list[Colis], decroissant: bool = False) -> list[Colis]:
    return sorted(colis, key=lambda c: c.poids, reverse=decroissant)


def trier_par_valeur(colis: list[Colis], decroissant: bool = True) -> list[Colis]:
    return sorted(colis, key=lambda c: c.valeur, reverse=decroissant)


def trier_par_priorite(colis: list[Colis], decroissant: bool = True) -> list[Colis]:
    """decroissant=True par défaut : priorité 5 (la plus importante,
    cf. convention retenue dans models.py) apparaît en premier."""
    return sorted(colis, key=lambda c: c.priorite, reverse=decroissant)
