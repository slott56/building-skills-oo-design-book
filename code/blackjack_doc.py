#!/usr/bin/env python3
"""
Building Skills in Object-Oriented Design V4

The blackjack module includes the Suit class and Card class hierarchy.

:author: S. Lott
:license: http://creativecommons.org/licenses/by-nc-nd/3.0/us/
"""
from typing import Any
import enum


class Suit(enum.Enum):
    """Enumerated suit names and values."""

    Clubs = u"\N{BLACK CLUB SUIT}"
    Diamonds = u"\N{WHITE DIAMOND SUIT}"
    Hearts = u"\N{WHITE HEART SUIT}"
    Spades = u"\N{BLACK SPADE SUIT}"


class Card:
    """A single playing card, suitable for Blackjack or
    Poker.  While a suit is retained, it doesn't figure into
    the ordering of cards, as it would in Bridge.

    ..  note:: Aces and Facecards.
        Ace and Facecards are separate subclasses.

    ..  attribute:: rank

        The numeric rank of the card.  2-13,  ace has an effective
        rank of 14 when used in Poker.

    ..  attribute:: suit
    
        The string suit of the card.  This should be from the
        named constants (Clubs, Diamonds, Hearts, Spades).

    At the class level, there are four constants that can
    make code look a little nicer.

    :var: Jack
    :var: Queen
    :var: King
    :var: Ace
    """

    Jack = 11
    Queen = 12
    King = 13
    Ace = 1

    def __init__(self, rank: int, suit: Suit) -> None:
        """Build a card with a given rank and suit.

        :param rank: numeric rank, 2-10.  Aces and FaceCards are separate.
        :type rank: integer in the range 2 to 10 inclusive.

        :param suit:  suit, a value from the Suit enum
        :type suit: Suit
        """
        assert isinstance(suit, Suit)
        self.rank = rank
        self.suit = suit
        self.points = rank

    def hardValue(self) -> int:
        """For blackjack, the hard value of this card.

        :returns: int
        """
        return self.points

    def softValue(self) -> int:
        """For blackjack, the soft value of this card.

        :returns: int
        """
        return self.points

    def __eq__(self, other: Any) -> bool:
        """Compare cards, ignoring suit.

        >>> from blackjack_doc import Card, Suit
        >>> Card(2, Suit.Diamonds) == Card(2, Suit.Spades)
        True
        >>> Card(2, Suit.Diamonds) == Card(10, Suit.Spades)
        False
        """
        return self.rank == other.rank

    def __lt__(self, other: Any) -> bool:
        """Compare cards, ignoring suit.

        >>> from blackjack_doc import Card, Suit
        >>> Card(2, Suit.Diamonds) < Card(3, Suit.Spades)
        True
        >>> Card(10, Suit.Diamonds) < Card(10, Suit.Spades)
        False
        """
        return self.rank < other.rank

    def __le__(self, other: Any) -> bool:
        return self.rank <= other.rank

    def __gt__(self, other: Any) -> bool:
        return self.rank > other.rank

    def __ge__(self, other: Any) -> bool:
        return self.rank >= other.rank

    def __str__(self) -> str:
        """
        >>> from blackjack_doc import Card, Suit
        >>> str(Card(2, Suit.Diamonds))
        ' 2♢'
        """
        return f"{self.rank:2d}{self.suit.value}"

    def __repr__(self) -> str:
        """
        >>> from blackjack_doc import Card, Suit
        >>> repr(Card(2, Suit.Diamonds))
        "Card(rank=2, suit=<Suit.Diamonds: '♢'>)"
        """
        return f"{self.__class__.__name__}(rank={self.rank!r}, suit={self.suit!r})"
