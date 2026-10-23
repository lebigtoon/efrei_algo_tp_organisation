from src.models import Colis
from src.tri import trier_par_poids, trier_par_priorite, trier_par_valeur


def _jeu():
    return [
        Colis(id=1, poids=8, valeur=20.0, priorite=2, destination="Paris"),
        Colis(id=2, poids=3, valeur=10.0, priorite=5, destination="Lille"),
        Colis(id=3, poids=12, valeur=40.0, priorite=1, destination="Lyon"),
    ]


def test_trier_par_poids_croissant():
    resultat = trier_par_poids(_jeu())
    assert [c.poids for c in resultat] == [3, 8, 12]


def test_trier_par_valeur_decroissant():
    resultat = trier_par_valeur(_jeu())
    assert [c.valeur for c in resultat] == [40.0, 20.0, 10.0]


def test_trier_par_priorite_la_plus_importante_en_premier():
    # convention retenue : priorite 5 = la plus importante
    resultat = trier_par_priorite(_jeu())
    assert [c.priorite for c in resultat] == [5, 2, 1]


def test_tri_stable_ne_modifie_pas_ordre_relatif_egalites():
    colis = [
        Colis(id=1, poids=5, valeur=1.0, priorite=1, destination="A"),
        Colis(id=2, poids=5, valeur=2.0, priorite=1, destination="B"),
    ]
    resultat = trier_par_poids(colis)
    assert [c.id for c in resultat] == [1, 2]
