"""
Building Skills in Object-Oriented Design V4

Demo of repeatable random tests.
"""

import random
from collections import Counter

def dice():
    return random.randint(1,6), random.randint(1, 6)

def dice_histogram(seed: int=42, samples: int=10_000) -> Counter:
    """
    Generate a lot of random numbers.

    >>> c = dice_histogram()
    >>> c.most_common(5)
    [(7, 1704), (8, 1392), (6, 1359), (9, 1116), (5, 1094)]
    """
    random.seed(seed)
    c = Counter(
        sum(dice()) for _ in range(samples)
    )
    return c

