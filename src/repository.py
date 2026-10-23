"""Stockage de la collection de colis et recherche par identifiant.

Deux structures redondantes sont maintenues en parallèle :
  - une liste (ordre d'insertion, permet un parcours O(n) pour l'affichage
    et le tri) ;
  - un dictionnaire id -> position dans la liste (permet la recherche en
    O(1) moyen, voir fiche algorithmique n°1 du rapport).
"""

from __future__ import annotations

from .models import Colis


class ColisDejaExistant(Exception):
    pass


class ColisRepository:
    def __init__(self) -> None:
        self._colis: list[Colis] = []
        self._index_par_id: dict[int, int] = {}

    def __len__(self) -> int:
        return len(self._colis)

    def ajouter_colis(self, colis: Colis) -> None:
        """O(1) amorti : append en fin de liste + insertion dans le dict."""
        if colis.id in self._index_par_id:
            raise ColisDejaExistant(f"un colis avec l'id {colis.id} existe déjà")
        self._index_par_id[colis.id] = len(self._colis)
        self._colis.append(colis)

    def rechercher_par_id(self, id_colis: int) -> Colis | None:
        """O(1) moyen : une seule consultation de dict."""
        position = self._index_par_id.get(id_colis)
        if position is None:
            return None
        return self._colis[position]

    def rechercher_lineaire_par_id(self, id_colis: int) -> Colis | None:
        """O(n) : parcours complet de la liste.

        Conservée volontairement pour comparer ses performances à celles
        de `rechercher_par_id` dans le benchmark (fiche algorithmique n°1).
        """
        for colis in self._colis:
            if colis.id == id_colis:
                return colis
        return None

    def supprimer_par_id(self, id_colis: int) -> bool:
        position = self._index_par_id.pop(id_colis, None)
        if position is None:
            return False
        self._colis.pop(position)
        for autre_id, autre_position in self._index_par_id.items():
            if autre_position > position:
                self._index_par_id[autre_id] = autre_position - 1
        return True

    def lister_tous(self) -> list[Colis]:
        """O(n) : copie défensive pour éviter toute mutation externe."""
        return list(self._colis)
