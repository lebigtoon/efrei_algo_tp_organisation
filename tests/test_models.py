import pytest

from src.models import Colis


def test_creation_colis_valide():
    c = Colis(id=1, poids=10, valeur=20.0, priorite=3, destination="Paris")
    assert c.id == 1
    assert c.poids == 10


def test_poids_invalide_leve_erreur():
    with pytest.raises(ValueError):
        Colis(id=1, poids=0, valeur=20.0, priorite=3, destination="Paris")


def test_priorite_hors_plage_leve_erreur():
    with pytest.raises(ValueError):
        Colis(id=1, poids=10, valeur=20.0, priorite=6, destination="Paris")


def test_destination_manquante_leve_erreur():
    with pytest.raises(ValueError):
        Colis(id=1, poids=10, valeur=20.0, priorite=3, destination="")
