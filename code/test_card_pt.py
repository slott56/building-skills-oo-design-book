# coding: utf-8
"""
Building Skills in Object-Oriented Design V4

test_card with :mod:`pytest`.
"""
from blackjack import Card, AceCard, FaceCard

def test_card():
    aceClubs = AceCard(Card.Ace, Card.Clubs)
    twoClubs = Card(2, Card.Clubs)
    tenClubs = Card(10, Card.Clubs)
    kingClubs = FaceCard(Card.King, Card.Clubs)
    aceDiamonds = AceCard(Card.Ace, Card.Diamonds)
    
    assert " A♣" == str(aceClubs)
    assert " 2♣" == str(twoClubs)
    assert "10♣" == str(tenClubs)
    assert " K♣" == str(kingClubs)
    assert " A♢" == str(aceDiamonds)

    assert tenClubs < kingClubs
    assert not (tenClubs >= kingClubs)
    assert kingClubs < aceClubs
    assert aceClubs == aceDiamonds

    assert "🃑" == aceClubs.image
    assert "🃒" == twoClubs.image
    assert "🃚" == tenClubs.image
    assert "🃞" == kingClubs.image
    assert "🃁" == aceDiamonds.image
