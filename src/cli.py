"""Menu interactif en ligne de commande."""

from __future__ import annotations

from . import camion as camion_module
from . import stats as stats_module
from . import tri
from .data_loader import charger_exemple_enonce
from .models import PRIORITE_MAX, PRIORITE_MIN, Colis
from .repository import ColisDejaExistant, ColisRepository

MENU = """
===== GESTION DES LIVRAISONS =====
1. Afficher les colis
2. Ajouter un colis
3. Rechercher un colis
4. Organiser les colis
5. Préparer un camion
6. Afficher le chargement
7. Afficher les statistiques
0. Quitter
"""


def _afficher_colis(colis: list[Colis]) -> None:
    if not colis:
        print("(aucun colis)")
        return
    print(f"{'ID':>6} {'Poids':>6} {'Valeur':>8} {'Priorité':>9}  Destination")
    for c in colis:
        print(f"{c.id:>6} {c.poids:>6} {c.valeur:>8.2f} {c.priorite:>9}  {c.destination}")


def _lire_int(message: str) -> int:
    while True:
        try:
            return int(input(message).strip())
        except ValueError:
            print("Entrée invalide, un entier est attendu.")


def _lire_int_borne(message: str, minimum: int, maximum: int) -> int:
    while True:
        valeur = _lire_int(message)
        if minimum <= valeur <= maximum:
            return valeur
        print(f"Valeur hors plage, un entier entre {minimum} et {maximum} est attendu.")


def _lire_float(message: str) -> float:
    while True:
        try:
            return float(input(message).strip())
        except ValueError:
            print("Entrée invalide, un nombre est attendu.")


class CLI:
    def __init__(self) -> None:
        self.repo = ColisRepository()
        self.camion_courant: camion_module.Camion | None = None
        for c in charger_exemple_enonce():
            self.repo.ajouter_colis(c)

    def run(self) -> None:
        while True:
            print(MENU)
            choix = input("Choix : ").strip()
            if choix == "0":
                print("Au revoir.")
                break
            self._dispatch(choix)

    def _dispatch(self, choix: str) -> None:
        actions = {
            "1": self._afficher_colis,
            "2": self._ajouter_colis,
            "3": self._rechercher_colis,
            "4": self._organiser_colis,
            "5": self._preparer_camion,
            "6": self._afficher_chargement,
            "7": self._afficher_statistiques,
        }
        action = actions.get(choix)
        if action is None:
            print("Choix invalide.")
            return
        action()

    def _afficher_colis(self) -> None:
        _afficher_colis(self.repo.lister_tous())

    def _ajouter_colis(self) -> None:
        print("-- Ajout d'un colis --")
        id_colis = _lire_int("ID : ")
        if self.repo.rechercher_par_id(id_colis) is not None:
            print(f"Un colis avec l'ID {id_colis} existe déjà.")
            return
        poids = _lire_int("Poids (kg, entier) : ")
        valeur = _lire_float("Valeur : ")
        priorite = _lire_int_borne(
            f"Priorité ({PRIORITE_MIN} à {PRIORITE_MAX}, {PRIORITE_MAX} = la plus importante) : ",
            PRIORITE_MIN,
            PRIORITE_MAX,
        )
        destination = input("Destination : ").strip()
        try:
            colis = Colis(id=id_colis, poids=poids, valeur=valeur, priorite=priorite, destination=destination)
            self.repo.ajouter_colis(colis)
        except (ValueError, ColisDejaExistant) as erreur:
            print(f"Erreur : {erreur}")
            return
        print(f"Colis {id_colis} ajouté.")

    def _rechercher_colis(self) -> None:
        id_colis = _lire_int("ID à rechercher : ")
        colis = self.repo.rechercher_par_id(id_colis)
        if colis is None:
            print("Aucun colis trouvé avec cet ID.")
            return
        _afficher_colis([colis])

    def _organiser_colis(self) -> None:
        print("-- Organiser les colis --")
        print("1. Par poids\n2. Par valeur\n3. Par priorité")
        sous_choix = input("Critère : ").strip()
        tous = self.repo.lister_tous()
        if sous_choix == "1":
            resultat = tri.trier_par_poids(tous)
        elif sous_choix == "2":
            resultat = tri.trier_par_valeur(tous)
        elif sous_choix == "3":
            resultat = tri.trier_par_priorite(tous)
        else:
            print("Critère invalide.")
            return
        _afficher_colis(resultat)

    def _preparer_camion(self) -> None:
        print("-- Préparation du camion --")
        capacite = _lire_int("Capacité du camion (kg, entier) : ")
        reponse = input("Favoriser les colis prioritaires ? (o/n) : ").strip().lower()
        avec_priorite = reponse == "o"
        alpha = 0.3
        if avec_priorite:
            texte_alpha = input("Facteur alpha (défaut 0.3) : ").strip()
            if texte_alpha:
                alpha = float(texte_alpha)
        self.camion_courant = camion_module.preparer(
            self.repo.lister_tous(), capacite, avec_priorite=avec_priorite, alpha=alpha
        )
        print("Camion préparé. Utilisez l'option 6 pour voir le chargement.")

    def _afficher_chargement(self) -> None:
        if self.camion_courant is None:
            print("Aucun camion n'a encore été préparé (option 5).")
            return
        print(camion_module.formater_chargement(self.camion_courant))

    def _afficher_statistiques(self) -> None:
        print("-- Statistiques globales --")
        globales = stats_module.statistiques_globales(self.repo.lister_tous())
        for cle, valeur in globales.items():
            print(f"{cle} : {valeur}")
        if self.camion_courant is not None:
            print("\n-- Statistiques du chargement courant --")
            chargement = stats_module.statistiques_chargement(self.camion_courant)
            for cle, valeur in chargement.items():
                print(f"{cle} : {valeur}")
