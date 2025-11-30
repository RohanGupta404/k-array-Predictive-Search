"""
kaps: K-Array Predictive Search implementations.

Exports:
- dd_kaps  → main Different-Distribution KAPS
- lkaps    → L-KAPS (learns distribution)
- base_kaps → simplified 'teaching'/baseline KAPS

Usage:
    from kaps import dd_kaps, lkaps, base_kaps
    result = dd_kaps(arr, target)
"""

from .dd_kaps import kaps as dd_kaps
from .l_kaps import lkaps as lkaps
from .base_kaps import kaps as base_kaps
from .lkaps_to_gchoice import make_G_from_lkaps as lkaps_to_G

from . import generators     # for data generation
from . import baselines      # for binary + interpolation search

__all__ = [
    "dd_kaps",
    "lkaps",
    "base_kaps",
    "generators",
    "baselines",
    "lkaps_to_G",
]
