import pytest

from src.models import Colis
from src.repository import ColisDejaExistant, ColisRepository


def _colis(id_):
    return Colis(id=id_, poids=5, valeur=10.0, priorite=2, destination="Lyon")


def test_ajouter_et_rechercher_par_id():
    repo = ColisRepository()
    repo.ajouter_colis(_colis(1))
    trouve = repo.rechercher_par_id(1)
    assert trouve is not None
    assert trouve.id == 1


def test_recherche_id_inexistant_retourne_none():
    repo = ColisRepository()
    repo.ajouter_colis(_colis(1))
    assert repo.rechercher_par_id(999) is None


def test_ajout_id_deja_existant_leve_erreur():
    repo = ColisRepository()
    repo.ajouter_colis(_colis(1))
    with pytest.raises(ColisDejaExistant):
        repo.ajouter_colis(_colis(1))


def test_recherche_lineaire_vs_dict_coherentes():
    repo = ColisRepository()
    for i in range(1, 11):
        repo.ajouter_colis(_colis(i))
    for i in range(1, 11):
        assert repo.rechercher_par_id(i) == repo.rechercher_lineaire_par_id(i)
    assert repo.rechercher_par_id(999) == repo.rechercher_lineaire_par_id(999)


def test_supprimer_colis():
    repo = ColisRepository()
    repo.ajouter_colis(_colis(1))
    repo.ajouter_colis(_colis(2))
    assert repo.supprimer_par_id(1) is True
    assert repo.rechercher_par_id(1) is None
    assert repo.rechercher_par_id(2) is not None
    assert repo.supprimer_par_id(999) is False
