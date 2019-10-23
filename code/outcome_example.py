"""
Building Skills in Object-Oriented Design V4

Outcome Example
"""

import doctest
from typing import NamedTuple
from dataclasses import dataclass

test_naive = """
>>> class Outcome:
...    def __init__(self, name: str, odds: int) -> None:
...        self.name = name
...        self.odds = odds

>>> oc1 = Outcome("Any Craps", 8)
>>> oc2 = Outcome("Any Craps", 8)

>>> oc1 == oc2
False
>>> id(oc1) == id(oc2)
False
>>> hash(oc1) == hash(oc2)
False
>>> oc1 is oc2
False
"""

test_namedtuple = """
>>> class Outcome(NamedTuple):
...     name: str
...     odds: int
>>> oc1 = Outcome("Any Craps", 8)
>>> oc2 = Outcome("Any Craps", 8)
>>> oc1 == oc2
True
>>> id(oc1) == id(oc2)
False
>>> hash(oc1) == hash(oc2)
True
>>> oc1 is oc2
False

"""

test_dataclass = """
>>> @dataclass(frozen=True)
... class Outcome:
...     name: str
...     odds: int
>>> oc1 = Outcome("Any Craps", 8)
>>> oc2 = Outcome("Any Craps", 8)
>>> oc1 == oc2
True
>>> id(oc1) == id(oc2)
False
>>> hash(oc1) == hash(oc2)
True
>>> oc1
Outcome(name='Any Craps', odds=8)

"""

__test__ = {k: v for k, v in vars().items() if k.startswith("test_")}
