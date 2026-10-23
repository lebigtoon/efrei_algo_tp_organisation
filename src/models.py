"""Modèle de données central : un colis.

Convention de priorité retenue (voir rapport.md, section "Modélisation") :
plus le nombre de priorité est ÉLEVÉ, plus le colis est important et doit
être favorisé lors du chargement du camion (priorité 5 > priorité 1).
Cette convention suit directement l'énoncé : "favoriser les colis
possédant une priorité importante".
"""

from dataclasses import dataclass

PRIORITE_MIN = 1
PRIORITE_MAX = 5


@dataclass
class Colis:
    id: int
    poids: int
    valeur: float
    priorite: int
    destination: str

    def __post_init__(self) -> None:
        if not isinstance(self.poids, int) or self.poids <= 0:
            raise ValueError(f"poids invalide pour le colis {self.id}: {self.poids!r} (entier > 0 attendu)")
        if self.valeur < 0:
            raise ValueError(f"valeur invalide pour le colis {self.id}: {self.valeur!r} (>= 0 attendu)")
        if not (PRIORITE_MIN <= self.priorite <= PRIORITE_MAX):
            raise ValueError(
                f"priorite invalide pour le colis {self.id}: {self.priorite!r} "
                f"(entre {PRIORITE_MIN} et {PRIORITE_MAX} attendu)"
            )
        if not self.destination:
            raise ValueError(f"destination manquante pour le colis {self.id}")
