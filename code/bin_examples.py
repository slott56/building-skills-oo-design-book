"""
Building Skills in Object-Oriented Design V4

"""
from typing import Iterable
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Outcome:
    name: str
    odds: int

class Bin1:
    """
    >>> o1 = Outcome("This", 2)
    >>> o2 = Outcome("That", 1)
    >>> b1 = Bin1([o1, o2])
    >>> len(b1)
    2
    >>> b1
    Bin1([Outcome(name='That', odds=1), Outcome(name='This', odds=2)])

    >>> o3 = Outcome("Third", 3)
    >>> b1.add(o3)
    >>> b1
    Bin1([Outcome(name='That', odds=1), Outcome(name='Third', odds=3), Outcome(name='This', odds=2)])

    """

    def __init__(self, outcomes: Iterable[Outcome]) -> None:
        self.outcomes = frozenset(outcomes)

    def __len__(self) -> int:
        return len(self.outcomes)

    def __repr__(self) -> str:
        """Impose order to make doctest cases work consistently."""
        args = ", ".join(map(repr, sorted(self.outcomes)))
        return f"{self.__class__.__name__}([{args}])"

    def add(self, arg: Outcome) -> None:
        self.outcomes |= frozenset([arg])


class Bin2(frozenset):
    """
    >>> o1 = Outcome("This", 2)
    >>> o2 = Outcome("That", 1)
    >>> b2 = Bin2([o1, o2])
    >>> len(b2)
    2

    We need to impose an ordering on the data.
    >>> list(sorted(b2))
    [Outcome(name='That', odds=1), Outcome(name='This', odds=2)]

    >>> o3 = Outcome("Third", 3)
    >>> b2 |= Bin2([o3])

    We'll force an ordering on the data. here, also.
    >>> list(sorted(b2))
    [Outcome(name='That', odds=1), Outcome(name='Third', odds=3), Outcome(name='This', odds=2)]
    """
    pass
