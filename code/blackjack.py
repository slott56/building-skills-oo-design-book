# -*- coding: utf-8 -*-
"""
Building Skills in Object-Oriented Design V4

Card Definition for unit testing.

Note that Unicode ``\u1f0a1`` (🂡) to ``\u1f0de`` (🃞) has the images
of the cards themselves. There's an interesting wrinkle:
Unicode has 14 ranks; it includes a "knight" rank.
Since we use 13 ranks, we'll skip the knight.

"""
from typing import Any, cast
import sys


class Card:
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
        return self.order <= cast(Card, other).order

    def __lt__(self, other: Any) -> bool:
        return self.order < cast(Card, other).order

    def __ge__(self, other: Any) -> bool:
        return self.order >= cast(Card, other).order

    def __gt__(self, other: Any) -> bool:
        return self.order > cast(Card, other).order

    def __eq__(self, other: Any) -> bool:
        return self.order == cast(Card, other).order

    def __ne__(self, other: Any) -> bool:
        return self.order != cast(Card, other).order

    def __hash__(self) -> int:
        return (hash(self.rank) + hash(self.suit)) % sys.hash_info.width


class AceCard(Card):
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
    def __init__(self, rank: int, suit: str) -> None:
        assert rank in (11, 12, 13)
        self.rank_char = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank, suit)

    def __str__(self) -> str:
        return f" {self.rank_char}{self.suit}"

    @property
    def hardValue(self) -> int:
        return 10

    @property
    def softValue(self) -> int:
        return 10


def card_factory(rank: int, suit: str) -> Card:
    class_ = AceCard if rank == 1 else FaceCard if rank >= 11 else Card
    return class_(rank, suit)
