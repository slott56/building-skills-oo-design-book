
..  _`craps.bet`:

Bet Class
=========

This chapter will examine the :class:`Bet` class, and its
suitability for the game of Craps. We'll expand the design to handle
additional complications present in real casino games.

We'll look at details of craps betting in `Bet Analysis`_.

This will lead to some design changes. We'll cover these in `Bet Rework`_.

We can then extend the :class:`Bet` class hierarchy to include an
additional kind of bet that's common in Craps. We'll cover the
details in `CommissionBet Design`_.

We'll detail the deliverables in `Bet Deliverables`_.

..  _`craps.bet.ov`:

Bet Analysis
-------------

A :class:`Bet` instance describes an amount that the player has wagered on a specific
:class:`Outcome` object. This is a simple association of an amount, the :class:`Outcome` object,
and a specific :class:`Player` instance.


When considering the various line bet outcomes (Pass Line, Come Line,
Don't Pass and Don't Come), we noted that when a point was established
the bet was either a winner or a loser, or it was moved from the line to
a particular number based on the throw of the dice. We'll need to add
this responsibility to our existing definition of the :class:`Bet` class.
This responsibility can be implemented as a :meth:`setOutcome`
method that leaves the amount intact, but changes the :class:`Outcome` instance
from the initial Pass Line or Come Line to a specific point outcome.


A complexity of placing bets in Craps is the commission (or vigorish)
required for Buy bets and Lay bets. This is a 5% fee, in addition to the
bet amount. A player puts $21 down, which is a $20 bet and a $1
commission. We'll need to add a a commission or vig responsibility to
our definition of the :class:`Bet` class.


This price to place a bet generalizes nicely to all other bets. For most
bets, the price is simply the amount of the bet. For Buy bets, the price
is 5% higher than the amount of the bet; for Lay bets, the price depends
on the odds. This adds a new method to the  :class:`Bet` class to compute
the price of the bet. This has a ripple effect throughout our :class:`Player` class
hierarchy to reflect this notion of the price of a bet. We will have to
make a series of updates to properly deduct the price from the player's
stake instead of deducting the amount of the bet.

There are two parts to creating a proper Craps bet: a revision of the base
:class:`Bet` class to separate the price from the amount bet, and a new :class:`CommissionBet`
subclass to compute prices properly for the more complex Craps bets.

Bet Rework
-----------

The :class:`Bet` class associates an amount and an :class:`Outcome` instance.
The :class:`Game` class may move a :class:`Bet` instance to a different :class:`Outcome` instance to
reflect a change in the odds used to resolve the bet. In a
future round of design, we can also associate a it with the :class:`Player` instance.

A bet is not a good candidate for :class:`typing.NamedTuple` because, in craps,
it's mutable. If we chose to to use the ``@dataclass(frozen=True)`` decorator,
we'll need to change the decorator to ``@dataclass(frozen=False)``, allowing
the object to be mutable and change state when a pass-line or come bet is moved.


Methods
~~~~~~~~


..  method:: Bet.setOutcome(self, outcome: Outcome) -> None

    :param outcome: The new :class:`Outcome` instance for this bet
    :type outcome: :class:`Outcome`

    Sets the :class:`Outcome` for this
    bet. This has the effect of moving the bet to another :class:`Outcome`.



..  method:: Bet.price(self) -> int


    Computes the price for this bet. For most
    bets, the price is the amount. Subclasses can override this to
    handle buy and lay bets where the price includes a 5% commission on
    the potential winnings.

    For Buy and Lay bets, a $20 bet has a price of $21.


CommissionBet Design
---------------------

..  class:: CommissionBet

    :class:`CommissionBet` extends :class:`Bet` with a commission
    payment (or vigorish) that determines the price for placing the bet.


Fields
~~~~~~~

..  attribute:: CommissionBet.vig

    Holds the amount of the vigorish. This is almost universally 5%.


Methods
~~~~~~~~


..  method:: Bet.price(self) -> int


    Computes the price for this bet. There are
    two variations: Buy bets and Lay bets.

    A Buy bet is a right bet; it has a numerator greater than or equal
    to the denominator (for example, :math:`2:1` odds, which risks 1 to win 2),
    the price is 5% of the amount bet. A $20 Buy bet has a price of $21.

    A Lay bet is a wrong bet; it has a denominator greater than the
    numerator (for example, :math:`2:3` odds, which risks 3 to win 2), the price
    is 5% of :math:`\tfrac{2}{3}` of the amount. A $30 bet Layed at :math:`2:3` odds has a price
    of $31, the $30 bet, plus the vig of 5% of $20 payout.


Bet Deliverables
-----------------

There are three deliverables for this exercise.


-   The revised :class:`Bet` class.

-   The new :class:`CommissionBet` subclass. This computes a price
    that is 5% of the bet amount.

-   A class which performs a unit test of the various :class:`Bet`
    classes. The unit test should create a couple instances of :class:`Outcome`,
    and establish that the :meth:`winAmount` and :meth:`price`
    methods work correctly. It should also reset the :class:`Outcome` object
    associated with a :class:`Bet` instance.


We could rework the entire :class:`Player` class hierarchy for
Roulette to compute the :class:`Bet` object's price in the :meth:`placeBets`,
and deduct that price from the player's stake. For Roulette, however,
this subtlety is at the fringe of over-engineering, as no bet in Roulette has a commission.

Looking Forward
----------------

As with Roulett, once we have the :class:`Dice` and the :class:`Bet` we will
build the :class:`CrapsTable` to make use of these two classes. In the next
chapter we'll build this new class.
