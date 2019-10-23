
..  _`blackjack.var`:

Variant Game Rules
==================

There are a number of variations in the sequence of game play offered by
different casinos. In addition to having variations on the player's
strategy, we also need to have variations on the casino rules.

We'll look at just a few of the variants in `Variant Game Examples`_.

In order to support some of the variants, we'll rework our
game class. The details are in `BlackjackGame Rework`_.

We'll define a single-deck game in `OneDeckGame Class`_. We won't delve into
too many other variants. We'll detail the deliverables in `Variant Game Deliverables`_.

Variant Game Examples
----------------------

There are wide variations in the ways people conduct Blackjack games.
We'll list a few of the variations we have heard of.


-   **Additional Win Rule: Charlie**. Informal games may allow a
    "five-card Charlie" or "six-card Charlie" win. If the
    player's hand stretches to five (or six) cards, they are paid at :math:`1:1`.

-   **Additional Offer: Surrender**. This variation allows the player to
    lose only half their bet. The offer is made after insurance and
    before splitting. Surrender against ace and 10 is a good strategy,
    if this offer is part of the game.

-   **No Resplit**. This variation limits the player to a single split. In
    the rare event of another matching card, resplitting is not allowed.

-   **No Double After Split**. This variation prevents the player from a
    double-down after a split.  Ordinarily, splitting Aces is followed
    by double-downs because 4/13 cards will lead to blackjack.

-   **Dealer Hits Soft 17**. This variation forces the dealer to hit soft
    17 instead of standing. This tends in increase the house edge slightly.

-   **Single Deck**. Some casinos offer single-deck blackjack, making
    it easier to count cards. It's common for this variant to offer
    only :math:`6:5` payouts on a "natural" or two-card blackjack.
    Casinos often pair the two variants; it's possible for this simulation
    to treat them separately.

Additional Wins
----------------

Supporting an addition "5-card" win rule is a profound change to the :class:`BlackjackGame` class.
This additional rule means another :class:`Outcome` type must be created. The game rule
must check for this as part of resolving hands that did not go bust.

Currently, the conditions for winning are buried in the :class:`BlackjackGame` class. To
change these rules, we'll need to modify the class design to create a method to test these additional winning conditions.
This will change the implementation of the :meth:`BlackjackGame.cycle` method described in
:ref:`blackjack.game`. Comparing two hands which have not gone bust needs to be extracted
from the :meth:`BlackjackGame.cycle` method and made into a separate method so a subclass
can override it.


No Resplit, No Double After Split
----------------------------------

The restrictions on splitting and doubling down are small changes to the
offers made by a variation on :class:`BlackjackGame`.  This would require
creating a subclass of  :class:`BlackjackGame` to implement the
alternative rules.

To modify the offer, we'll need to modify the class design to create a method to
change the rules for making an offer.
This will change the implementation of the :meth:`BlackjackGame.cycle` method described in
:ref:`blackjack.game`.

Dealer Hits Soft 17
--------------------

The variations in the dealer's rules (hitting a soft 17) is also a small
change best implemented by creating a subclass of  :class:`BlackjackGame`.
A new method for dealer hand-filling needs to be written, pulling some
of one step from the :meth:`BlackjackGame.cycle` method. This new method
can then be over-ridden by a subclass.

Changing the Number of Decks
----------------------------

Reducing the number of decks is a relatively easy change to our application. Since our main application
constructs the :class:`Shoe` before constructing the :class:`Game`,
it can construct a single-deck :class:`Shoe`.

Changing the Payout Odds
------------------------

Handling the variations in
the payout odds is a bit more complex.

1.  The Player creates each Hand, associated with a Bet.  The Bet is associated
    with the simple Ante outcome.

2.  At the end of the Game, the Hand does a comparison between itself
    and the Dealer's Hand to determine the odds for the Ante outcome.

    It's a :math:`1:1` :class:`Outcome` instance if the player does not have blackjack.

    It's a :math:`3:2` :class:`Outcome` instance if the player does have blackjack.

Allocating this responsiblity to the :class:`Hand` class for this was a bad design decision.

We should have allocated responsibility to the :class:`BlackjackGame` class.  We will need
to add a method to the game which compares a player's :class:`Hand`
with the dealer's :class:`Hand`, sets the :class:`Outcome` correctly,
and resolves the bet.

This works out well with other changes like adding additional wins.

BlackjackGame Rework
----------------------

There are a number of methods of the parent :class:`BlackjackGame` class
that need to be reworked to permit some flexibility in the game definitions.

Methods
~~~~~~~

..  method:: BlackjackGame.cycle(self) -> None
    :noindex:

    A single game of Blackjack. This steps through the sequence to play one full game.

..  method:: BlackjackGame.check_winner(self, hand: Hand) -> Outcome

    :param hand: A specific non-bust hand for the current player
    :type hand: :class:`Hand`

    :returns: the final Outcome object for resolving bets.
    :rtype: :class:`Outcome`.

    This checks to see if the winning conditions are met or not for this hand.
    The default implementation compares the player's total to the dealer's total.
    If the player has a two-card twenty-one, called "blackjack" or "a natural",
    a :math:`3:2` Blackjack outcome is provided. If the player has more than
    two cards, and more than the dealer, this is a :math:`1:1` win. If the player
    has a total equal to the dealer, this a push, where the bet value is returned
    with no winnings. Otherwise, the Ante outcome can be left in place, because
    this hand is a  loser.

    There can be alternate definitions for this method, supporting variant games.

FiveCardCharlie Class
---------------------

..  class:: OneDeckGame

    :class:`OneDeckGame` is a subclass of :class:`BlackjackGame`
    that manages the sequence of actions for a one-deck game of Blackjack
    where a player taking five cards without going bust is actually a win,
    irrespective of the dealer's total.

    The :meth:`OneDeckGame.check_winner` method overrides the superclass.
    This method  will set the hand's outcome's odds if the hand is large enough.

OneDeckGame Class
-------------------

..  class:: OneDeckGame

    :class:`OneDeckGame` is a subclass of :class:`BlackjackGame`
    that manages the sequence of actions for a one-deck game of Blackjack
    with a :math:`6:5` blackjack :class:`OutcomeAnteLowOdds`.

    Typically, this is built with a one-deck instance of :class:`Shoe`.

    The :meth:`OneDeckGame.check_winner` method overrides the superclass.
    This method  will set the hand's outcome's odds to 6:5 if the player holds Blackjack.

Variant Game Deliverables
--------------------------

There are three deliverables for this exercise.

-   The revised :class:`BlackjackGame` class.   All of the original unit
    tests should apply to the refactored function that sets the outcome
    odds.

-   The :class:`OneDeckGame` class.

-   A class to perform a unit test of the :class:`OneDeckGame` class.

Looking Forward
---------------

In this chapter, we've built a working simulation of Blackjack, and refactored it so we can accomodate
more game and play variants. Along the way, we've written (and rewritten) a good deal
of Python code.

In the next chapter, we'll summarize the various components built so far.
