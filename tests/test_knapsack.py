from src.knapsack import (
    calculer_valeur_ajustee_priorite,
    knapsack_01_dp,
    knapsack_glouton_ratio,
    preparer_camion,
)
from src.models import Colis


def _colis_enonce_abcd():
    # Exemple de l'énoncé : A, B, C, D (priorités variées, choisies pour
    # ne pas fausser les tests qui n'utilisent pas la priorité : ces
    # derniers appellent knapsack_01_dp SANS valeurs_entree, la priorité
    # est alors ignorée).
    return [
        Colis(id=1, poids=8, valeur=20.0, priorite=2, destination="X"),  # A
        Colis(id=2, poids=6, valeur=25.0, priorite=4, destination="X"),  # B
        Colis(id=3, poids=5, valeur=18.0, priorite=1, destination="X"),  # C
        Colis(id=4, poids=4, valeur=14.0, priorite=5, destination="X"),  # D
    ]


def test_knapsack_dp_cas_connu_optimal():
    # Calculé à la main : pour capacite=14, la meilleure combinaison est
    # A+B (poids 8+6=14, valeur 20+25=45) ; toute autre combinaison de
    # poids <= 14 donne une valeur strictement inférieure (B+C=43,
    # A+C=38, A+D=34, C+D=32, B seul=25).
    resultat = knapsack_01_dp(_colis_enonce_abcd(), capacite=14)
    assert resultat.poids_total <= 14
    assert resultat.valeur_totale_reelle == 45.0
    assert {c.id for c in resultat.colis_selectionnes} == {1, 2}


def test_knapsack_dp_capacite_nulle_retourne_vide():
    resultat = knapsack_01_dp(_colis_enonce_abcd(), capacite=0)
    assert resultat.colis_selectionnes == []
    assert resultat.valeur_totale_reelle == 0.0


def test_knapsack_dp_tous_colis_tiennent():
    colis = _colis_enonce_abcd()
    resultat = knapsack_01_dp(colis, capacite=100)
    assert len(resultat.colis_selectionnes) == len(colis)
    assert resultat.valeur_totale_reelle == sum(c.valeur for c in colis)


def test_glouton_peut_etre_sous_optimal_vs_dp():
    # Contre-exemple classique : le glouton par ratio valeur/poids choisit
    # les colis 1 et 2 (valeur 160) alors que l'optimum (2+3) vaut 220.
    colis = [
        Colis(id=1, poids=10, valeur=60.0, priorite=1, destination="X"),
        Colis(id=2, poids=20, valeur=100.0, priorite=1, destination="X"),
        Colis(id=3, poids=30, valeur=120.0, priorite=1, destination="X"),
    ]
    resultat_dp = knapsack_01_dp(colis, capacite=50)
    resultat_glouton = knapsack_glouton_ratio(colis, capacite=50)
    assert resultat_dp.valeur_totale_reelle == 220.0
    assert resultat_glouton.valeur_totale_reelle == 160.0
    assert resultat_glouton.valeur_totale_reelle < resultat_dp.valeur_totale_reelle


def test_priorite_peut_changer_la_selection():
    # Deux colis de poids identique et de valeurs proches, mais de
    # priorités opposées. Sans priorité, le colis le plus "riche" est
    # choisi ; avec priorité (alpha assez grand), le colis le plus
    # prioritaire peut l'emporter alors que la capacité ne permet pas de
    # prendre les deux.
    colis = [
        Colis(id=1, poids=10, valeur=100.0, priorite=1, destination="X"),  # peu prioritaire, plus de valeur
        Colis(id=2, poids=10, valeur=90.0, priorite=5, destination="X"),   # très prioritaire, un peu moins de valeur
    ]
    sans_priorite = preparer_camion(colis, capacite=10, avec_priorite=False, methode="dp")
    avec_priorite = preparer_camion(colis, capacite=10, avec_priorite=True, alpha=0.3, methode="dp")

    assert {c.id for c in sans_priorite.colis_selectionnes} == {1}
    assert {c.id for c in avec_priorite.colis_selectionnes} == {2}


def test_valeur_totale_reelle_jamais_la_valeur_ajustee():
    colis = _colis_enonce_abcd()
    valeurs_ajustees = calculer_valeur_ajustee_priorite(colis, alpha=0.3)
    resultat = knapsack_01_dp(colis, capacite=14, valeurs_entree=valeurs_ajustees)
    valeur_reelle_attendue = sum(c.valeur for c in resultat.colis_selectionnes)
    assert resultat.valeur_totale_reelle == valeur_reelle_attendue
    # la valeur réelle ne doit jamais correspondre à la somme des valeurs
    # ajustées (sauf coïncidence numérique improbable avec alpha=0.3 ici)
    assert resultat.valeur_utilisee_pour_optimisation != resultat.valeur_totale_reelle


def test_preparer_camion_bascule_sur_glouton_si_instance_trop_grande():
    colis = [Colis(id=i, poids=1, valeur=float(i), priorite=1, destination="X") for i in range(1, 11)]
    resultat = preparer_camion(colis, capacite=5, methode="auto")
    assert resultat.methode_utilisee == "dp"  # petite instance, DP utilisée

    resultat_force = preparer_camion(colis, capacite=5, methode="glouton")
    assert resultat_force.methode_utilisee == "glouton"
    assert resultat_force.avertissement is not None
