# coding: utf-8
"""
Building Skills in Object-Oriented Design V4

Card Definition for doctest testing -- initial version
"""
from typing import Any
import sys


class Card:
    """
    Superclass for cards.
    >>> c2d = Card(2, Card.Diamonds)
    >>> str(c2d)
    ' 2♢'
    >>> c2d.softValue
    2
    >>> c2d.hardValue
    2
    """

    Clubs = u"\N{BLACK CLUB SUIT}"
    Diamonds = u"\N{WHITE DIAMOND SUIT}"
    Hearts = u"\N{WHITE HEART SUIT}"
    Spades = u"\N{BLACK SPADE SUIT}"
    Jack = 11
    Queen = 12
    King = 13
    Ace = 1

    def __init__(self, rank: int, suit: str) -> None:
        assert suit in (Card.Clubs, Card.Diamonds, Card.Hearts, Card.Spades)
        assert 1 <= rank < 14
        self.rank = rank
        self.suit = suit
        self.order = rank

    @property
    def hardValue(self) -> int:
        return self.rank

    @property
    def softValue(self) -> int:
        return self.rank

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank!r}, suit={self.suit!r})"

    def __str__(self) -> str:
        return f"{self.rank:2d}{self.suit}"

    @property
    def image(self) -> str:
        s = {
            Card.Spades: 0x1F0A0,
            Card.Hearts: 0x1F0B0,
            Card.Diamonds: 0x1F0C0,
            Card.Clubs: 0x1F0D0,
        }[self.suit]
        r = self.rank if self.rank < 12 else self.rank + 1
        return chr(s + r)

    def __le__(self, other: Any) -> bool:
        return self.order <= other.order

    def __lt__(self, other: Any) -> bool:
        return self.order < other.order

    def __ge__(self, other: Any) -> bool:
        return self.order >= other.order

    def __gt__(self, other: Any) -> bool:
        return self.order > other.order

    def __eq__(self, other: Any) -> bool:
        return self.order == other.order

    def __ne__(self, other: Any) -> bool:
        return self.order != other.order

    def __hash__(self) -> int:
        """
        >>> c2d = Card(2, Card.Diamonds)
        >>> c3d = Card(3, Card.Diamonds)
        >>> hash(c2d) == hash(c3d)
        False
        >>> c2d_2 = Card(2, Card.Diamonds)
        >>> hash(c2d) == hash(c2d_2)
        True
        """
        return (hash(self.rank) + hash(self.suit)) % sys.hash_info.width


class AceCard(Card):
    """
    >>> cas = AceCard(Card.Ace, Card.Spades)
    >>> str(cas)
    ' A♠'
    >>> cas.softValue
    11
    """

    def __init__(self, rank: int, suit: str) -> None:
        assert rank == 1
        super().__init__(rank, suit)
        self.order = 14  # above King

    def __str__(self) -> str:
        return f" A{self.suit}"

    @property
    def hardValue(self) -> int:
        return 1

    @property
    def softValue(self) -> int:
        return 11


class FaceCard(Card):
    """
    >>> cjs = FaceCard(Card.Jack, Card.Spades)
    >>> str(cjs)
    ' J♠'
    >>> cjs.softValue
    10
    """

    def __init__(self, rank: int, suit: str) -> None:
        assert rank in (11, 12, 13)
        self.rank_char = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank, suit)

    def __str__(self) -> str:
        return " {rank_char}{suit}".format_map(vars(self))

    @property
    def hardValue(self) -> int:
        return 10

    @property
    def softValue(self) -> int:
        return 10


def card_factory(rank: int, suit: str) -> Card:
    """
    >>> card_factory(Card.Ace, Card.Clubs)
    AceCard(rank=1, suit='♣')
    >>> card_factory(2, Card.Clubs)
    Card(rank=2, suit='♣')
    >>> card_factory(Card.Jack, Card.Clubs)
    FaceCard(rank=11, suit='♣')
    """
    class_ = AceCard if rank == 1 else FaceCard if rank >= 11 else Card
    return class_(rank, suit)
