"""
Building Skills in Object-Oriented Design V4

Wheel Examples
"""
from typing import List, Any
import random

Bin = Any

class Wheel_RNG:
    def __init__(self, bins: List[Bin], rng: random.Random=None) -> None:
        self.bins = bins
        self.rng = rng or random.Random()

    def choose(self) -> Bin:
        return self.rng.choice(self.bins)


class Wheel:
    def __init__(self, bins: List[Bin]) -> None:
        self.bins = bins
        self.rng = random.Random()

    def choose(self) -> Bin:
        return self.rng.choice(self.bins)
