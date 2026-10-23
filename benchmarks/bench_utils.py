"""Utilitaires de chronométrage pour les benchmarks."""

from __future__ import annotations

import time
from contextlib import contextmanager


@contextmanager
def chrono():
    """Context manager qui expose `.secondes` une fois le bloc terminé."""

    class _Resultat:
        secondes: float = 0.0

    resultat = _Resultat()
    depart = time.perf_counter()
    try:
        yield resultat
    finally:
        resultat.secondes = time.perf_counter() - depart
