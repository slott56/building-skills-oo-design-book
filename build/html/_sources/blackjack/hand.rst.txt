.. |whearts| unicode:: U+02661 .. WHITE HEART SUIT
.. |wdiams|  unicode:: U+02662 .. WHITE DIAMOND SUIT
.. |wclubs|  unicode:: U+02667 .. WHITE CLUB SUIT
.. |wspades| unicode:: U+02664 .. WHITE SPADE SUIT
.. |clubs|  unicode:: U+02663 .. CLUBS SUIT
.. |spades| unicode:: U+02660 .. SPADES SUIT

Hand and Outcome Classes
========================

This chapter introduces the hand of cards used by player and dealer.
It wrestles with the problems of scoring the value
of the hand in the presence of soft and hard values for aces.
It also introduces a subclass of the :class:`Outcome` class that
can handle the more complex evaluation rules for Blackjack.

In `Hand Analysis`_ we'll look at a number of issues related to
Blackjack hands. In `Payout Odds`_ we'll look at how the odds
depend on the cards and the way the hands are resolved.
In `Hard and Soft Totals`_ we'll examine how an Ace leads to a
hand having distinct hard and soft totals. This will cause
us to rexamine the nature of outcomes; this is the subject of
`Blackjack Outcomes`_.

We can then design the overall :class:`Hand` class.
This is described in `Hand Class Design`_. We'll look at all of the
deliverables for this chapter in `Hand Deliverables`_.

Hand Analysis
-------------

The hand of cards is both a container for cards, but is also one
dimension of the current state of the player's playing strategy.
In addition to the player's hand, the other dimension to the
strategy is the dealer's up card.

A player may have multiple hands. The hands are resolved independently.

For each hand, a hand's responsibilities include collecting the cards, producing a
hard and soft point total and determining the appropriate payout odds.

Collecting cards is trivial.  Each hand can be modeled as a bag or multiset of
:class:`Card` instances.  A hand can't be a :class:`Set` because there can easily be duplicate
cards in a multiple deck game.  In an 8-deck game, there are 8 separate instances of A\ |spades|.

Determining the payout odds for a :class:`Hand` object is somewhat more complex.

Payout Odds
~~~~~~~~~~~~

To be compatible with other games, we'll be creating :class:`Bet` objects which
are associated with :class:`Outcome` instances.  In Roulette, there were a profusion
of :class:`Outcome` instances, each with fixed odds.  In Craps, there
were fewer :class:`Outcome` instances, some of which had odds that depended on a
the current :class:`Throw` object.

The player's :class:`Hand` instance must be associated with an :class:`Outcome` object.
The core of the game simulation is matching the :class:`Outcome` object for a :class:`Bet` instance
and the :class:`Outcome` object of a :class:`Hand` instance to determine the payout.

In the case of Roulette, each :class:`Bin` instance was a set of winning :class:`Outcome` objects.
In the case of Craps, both the :class:`Throw` object and the game had a mixtures of winning, losing and
unresolved :class:`Outcome` object.  The :class:`Bet` instances were associated with
:class:`Outcome` instances. The :class:`Wheel`, :class:`Dice`. or :class:`Game`
objects gave us sets of winning (and losing) :class:`Outcome` instances.

In Blackjack, there are relatively few distinct outcomes.  And, it's not clear how each
:class:`Outcome` instance associates with a :class:`Hand` object.

**Survey of Outcomes**.
To figure out how to associate a :class:`Hand` object and a betting :class:`Outcome` object,
we'll start by enumerating all the  individual :class:`Outcome` instances in this game.
Note that the "Ante" bet, placed before any cards are seen, has three distinct outcomes.

#.  **Insurance**. This outcome pays :math:`2:1`.
    This is offered when the up card is an Ace.
    This outcome is a winner when the dealer's hand
    is blackjack. (Also, the "Ante" bet will be a loser.)
    This outcome a loser when the dealer's hand is not blackjack. (The Ante bet is unresolved.)

#.  **Even Money**. This outcome pays :math:`1:1`.
    This is offered in the rare case when the
    player's hand is blackjack and the dealer's up card is an Ace. If
    accepted, it can be looked at as a switch of the Ante bet
    from the original "Ante" outcome to a different
    "Even Money" outcome. After this change, the "Ante" bet is then resolved as a winner.

#.  **Ante** paying :math:`1:1`.
    This variation occurs when the player's hand is
    less than or equal to 21 and the dealer's hand goes over 21. This
    payout also occurs when the player's hand is less than or equal to
    21 and also greater than the dealer's hand.
    All "Ante" outcome variants are a loser as soon as the player's hand
    goes over 21. They are  also a loser when the player's hand is less than
    or equal to 21 and also less than the dealer's hand.
    The odds depend on both player and dealer's hand.

#.  **Ante** paying :math:`3:2`.
    This variation occurs when the player's hand is blackjack.
    The odds depend on the player's hand.

#.  **Ante** resolved as a push, paying :math:`1:0`.
    This variation occurs when the player's
    hand is less than or equal to 21 and equal to the dealer's hand.
    The odds depend on both player and dealer's hand.

**Problem**. What kind of class is the :class:`Hand` class?
Is it a collection of :class:`Outcome` instances?
Or is it something different?

It appears that the :class:`Hand` class, as a whole, is not simply associated with an :class:`Outcome` object.
It appears that a :class:`Hand` instance must produce an :class:`Outcome` object based on the hand's
total, the dealer's total, and possibly the state of the game.

This is a change from the way the :class:`Dice` class and the collection of :class:`Bin` isntances work.
The :class:`Bin` instances were directly (and immutably) associated with :class:`Outcome` objects.
A Blackjack :class:`Hand`, however, must do a bit of processing
to determine which :class:`Outcome` instance it represents.

-   A two-card hand totalling soft 21 produces a blackjack :class:`Outcome` object that pays
    :math:`3:2`.

-   All other hands produce an :class:`Outcome` object that pays :math:`1:1` and could be resolved
    as a win, a loss, or a push.

Also, changes to the state of the game depend on the values of both
hands, as well as the visible up card in the dealer's hand.  This makes
the state of the hand part of the evolving state of the game, unlike the simple
:class:`RandomEvent` instances we saw in Roulette and Craps.

**Forces**.
We have a few ways we can *deal* with the :class:`Hand` class definition.

-   We can make the :class:`Hand` class a subclass of the :class:`RandomEvent` class, even
    though it's clearly more complex than other events.

-   We can make the :class:`Hand` class unique, unrelated to
    other games.

**Hand is an "Event"**?
While a :class:`Hand` object appears to be a subclass of the :class:`RandomEvent` class,
it jars our sensibilities. A :class:`Hand` object is built up from a
number of :class:`Card` instances. Dealing a :class:`Card` object seems more event-like.

One could rationalize calling a :class:`Hand` instance
an "event" by claiming that the :class:`Shoe` clss is the random event generator.
The  act of shuffling is when the events are created.
The complex event is then revealed to the player and dealer one card at a time.

It seems that we need to define a :class:`Hand` class that shares a common
interface with the :class:`RandomEvent` class, but extends the basic concept
because a hand has an evolving state until it is fully revealed.

**Hand is different**.
While we can object to calling a :class:`Hand` instance a single "event", it's difficult
to locate a compelling reason for making the :class:`Hand` class into something
radically different from the :class:`Bin` or :class:`Dice` classes.

**Hand Features**.
Our first design decision, then, is to define the :class:`Hand` class as a kind of :class:`RandomEvent` subclass.
We'll need to create several :class:`Outcome` instances that can be paired with the event: Insurance, Even Money, Ante and Blackjack.

A :class:`Hand` object will produce an appropriate  :class:`Outcome` object based on the hand's structure,
the game state, and the dealer's hand.  Generally, each :class:`Hand` object will produce a simple Ante outcome
as a winner or loser.  Sometimes a :class:`Hand` object will produce a Blackjack outcome.

Sometimes the Player and Blackjack Game will collaborate to add an Insurance or Even Money :class:`Outcome` object to the :class:`Hand`.

Hard and Soft Totals
~~~~~~~~~~~~~~~~~~~~

Our second design problem is to calculate the
point value of the hand. Because of aces, hands can have two different point totals.
If there are no aces, the total is hard.  When there is an Ace,
there are two totals: the hard total uses an Ace as 1, the soft total
uses an Ace as 11.

We note that only one ace will participate in this
hard total vs. soft total decision-making. If two aces contribute soft
values, the hand is at least 22 points. Therefore, we need to note the presence
of at most one ace to use the soft value of 11, all other cards will
contribute their hard values to the hand's total value.

The presence of an Ace means finding at most one card with a ``card.hardValue != card.sotfValue``.

A :class:`Hand` object has a two internal point totals:

-   **Hard**.  All hands have a hard total. This is the total of the
    hard values of all of the :class:`Card` instances.

-   **Soft**.  When a hand has at least one Ace, the soft total
    is computed as the hard total of all cards *except* the Ace,
    plus the soft value of the Ace.

The final point total for a hand, then, has two options.
When the soft total when is 21 or less, the soft total applies.
WHen the soft total is over 21, the hard total applies.

This leads us to a number of algorithms within the :class:`Hand`
class to locate and isolate one card with different
hard and soft values.

Blackjack Outcomes
~~~~~~~~~~~~~~~~~~~

As a final design decision, we need to consider creating any
subclasses of the :class:`Outcome` class to handle the variable odds for the "Ante"
bet. We don't need a subclass for the "Insurance" or "Even Money" outcomes,
because the base :class:`Outcome` class does everything we need.

The notable complication here is that there are three different odds. If
the player's hand beats the dealer's hand and is blackjack, the odds are
:math:`3:2`. If the player's hand beats the dealer's hand, but is not blackjack,
the odds are :math:`1:1`. If the player's hand equals the dealer's hand, the
result is a push; something like :math:`1:0` odds where you get your money back.

It doesn't seem like new subclasses of the :class:`Outcome` class are necessary.
We simply have some alternative :class:`Outcome` instances that can be produced by a :class:`Hand`.

The player can only create one of four basic :class:`Bet` instances.

-   The "Ante" bet that starts play.  This is assumed to be :math:`1:1` until
    game conditions change this to :math:`3:2` or a push.  This is the essential
    :class:`Outcome` object for the player's primary :class:`Bet` instance.

-   The "Insurance" and "Event Money" bets.
    One of these may also be active after the first cards are dealt.

    For the insurance :class:`Outcome` object to be active,
    the dealer must be showing an Ace and the player's hand is not 21.
    The player is offered and accepts by creating an insurance :class:`Bet` object.

    For even money :class:`Outcome` object to be active,
    the dealer must be showing an Ace and the player's hand is  21.
    The player is offered and accepts by creating an even money :class:`Bet` object.

    These are resolved before further cards are dealt.
    If the dealer does not have 21, these
    bets are lost.  If the dealer has 21, these bets win, but the Ante bet is a loss.

-   The "Double Down" bet.  This is generally offered at any time.  It can be
    looked at as an  an additional amount added to the "ante" bet and a modification
    to game play. The player creates this :class:`Bet` object, changing the course
    of play: only a single card can be dealt when this bet is made.

**Objects**.
It seems simplest to create a few common :class:`Outcome` instances: Ante, Insurance, Even Money
and Double Down.

The Table object will then have to combine a Double-Down :class:`Bet` object's amount
into the Ante :class:`Bet` object's amount.

Hand Class Design
------------------

..  class:: Hand

    :class:`Hand` contains a collection of individual :class:`Card` instances,
    and determines the two point values for the hand.


Fields
~~~~~~~

..  attribute:: Hand.cards

    Holds the collection of individiual :class:`Card` instances of this hand.


Constructors
~~~~~~~~~~~~


..  method:: Hand.__init__(self, *card: Card=None) -> None

    :param card: cards to add
    :type card: :class:`Card`


    Creates an empty hand. The :attr:`Hard.cards` variable is
    initialized to an empty sequence.

    If :obj:`card` values are provided, then use the :meth:`add`
    method to add these cards to the hand.



Methods
~~~~~~~~

..  method:: Hand.hard(self) -> int

    Returns the hard total of all cards in the hand.

..  method:: Hand.soft(self) -> int

    Does the soft-total computation.

    1. Partition the cards into two collections:

        -   **Ace**. This collection has at most one Ace. For this card, ``card.softValue != card.hardValue``.
            If there's no card here, the value is zero.
            If there's a card here, the value is the soft value of the one-and-only :class:`Card` instance.

        -   **Non-Ace**. This collection has all the cards except
            for the card in the **Ace** collection. If there is no Ace, this collection
            is all the cards. The value is the hard total of all cards.

    2. Return the sum of the values for each collection, **Ace** plus **Non-Ace**.


..  method:: Hand.add(self, card: Card) -> None

    :param card: A card to hadd
    :type card: :class:`Card`


    Add this card to the :attr:`Hand.cards` list.


..  method:: Hand.value(self) -> int


    Computes the final total of this hand.

    If there are any aces, and the soft total
    is 21 or less, this will be the soft total.
    If there are no aces, or the soft
    total is over 21, this will be the hard total.


..  method:: Hand.size(self) -> int

    Returns the number of cards in the hand, the size of the :class:`List`.



..  method:: Hand.blackjack(self) -> bool

    Returns true if this hand has a size of two and a value of 21.



..  method:: Hand.busted(self) -> bool

    Returns true if this hand a value over 21.



..  method:: Hand.__iter__(self) -> Iterator[Card]

    Returns an iterator over the cards of the :class:`List`.



..  method:: Hand.__str__(self) -> str

    Displays the content of the hand as a String with all of the card names.


Hand Deliverables
------------------

There are six deliverables for this exercise.

-   The :class:`HandTotal` class hierarchy:  :class:`HandTotal`, :class:`HandHardTotal`, :class:`HandSoftTotal`.

-   A unit test for each of these classes.

-   The :class:`Hand` class.

-   A class which performs a unit tests of the :class:`Hand` class.
    The unit test should create several instances of :class:`Card`, :class:`FaceCard`
    and :class:`AceCard`, and add these to instances of :class:`Hand`,
    to create various point totals.

-   The :class:`Card` and :class:`AceCard` modifications required to set the appropriate values
    in a :class:`Hand`

-   A set of unit tests for assembling a hand and changing the total object in use to correctly
    compute hard or soft totals for the hand.

Looking Forward
----------------

The Cards and Hands are essential elements for the game of Blackjack.
Following the pattern of previous games, the next chapter will look
at the implementation of a table to hold the player's :class:`Bet` objects.
An interesting part of this is the a player's hand can be split,
leading to multiple hands, each of which has multiple active bets.
