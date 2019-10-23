..  _`blackjack.game`:


Blackjack Game Class
====================

The game offers a large number of decisions to a player.
This is different from Roulette, where the player's choices are limited to
a list of bets to place.

In `Blackjack Game Analysis`_ we'll look at the game and how the
state of play is going to be managed.

In `Blackjack Collaboration`_ we'll look at the various player interactions.
In `Insurance Collaboration`_ we'll look at the insurance bet.
In `Filling the Hands`_ we'll look at the hit vs. stand decision.
There are some additional decisions -- like splitting -- which require
more interaction. We'll look at this in `Hand-Specific Decisions`_.

We'd like to segregate dealer rules from the rest of the game.
This allows us to alter how a dealer fills their hand without breaking
anything else. We'll look at this in `Dealer Rules`_.

This will require a stub class for a Blackjack Player.
We'll look at this design in `BlackjackPlayer Class`_.

We'll tweak the design for :class:`Card` in order to determine
if insurance should be offered. This covered in `Card Rework`_.

We'll also revisit the fundamental
relationship between Game, Hand and Player. We'll invert our viewpoint
from the Player containing a number of Hands to the Hands sharing a
common Player. This is the subject of `Hand Rework`_.

We'll provide the design for the game in `BlackjackGame Class`_.
In `Blackjack Game Deliverables`_ we'll enumerate all of the deliverables.


Blackjack Game Analysis
-----------------------

The sequence of operations in the game of Blackjack is quite complex. We
can describe the game in either of two modes: as a sequential procedure
or as a series of state changes.

-   A sequential description means that the state is identified by the step that is next in the sequence.

-   The state change description involves a stream of events that change the sateof the game.
    We used this type of approach to describe Craps, see :ref:`craps.details.game.rules`.

Additionally, we need to look at the various collaborations  of the Game.
We also need to address the question of handling the dealer's rules.

**Maintaining State**.
The sequential description of state, where the current state is defined
by the step that is next, is the default description of state in many
programming languages. While it seems obvious beyond repeating, it is
important to note that each statement in a method changes the state of
the application; either by changing state of the object that contains
the method, or invoking methods of other, collaborating objects. In the case
of an *active* class, this description of state as next statement is
adequate. In the case of a *passive* class, this description of state
doesn't work out well because passive classes have their state changed
by collaborating objects. For passive objects, instance variables and state
objects are a useful way to track state changes.


In the case of Roulette, the cycle of betting and the game procedure
were a simple sequence of actions. In the case of Craps, however, the
game was only loosely tied to each the cycle of betting and throwing the
dice. For Craps, the game state a passive part of the cycle of play. In the
case of Blackjack, the cycle of betting and game procedure seem more like Roulette.


Most of a game of Blackjack is sequential in nature: the initial
offers of even money, insurance and splitting the hands are optional
steps that happen in a defined order. When filling the player's :class:`Hand` instances,
there are some minor sub-states and state changes. When all
of the player's :class:`Hand` instances are bust or standing pat, the dealer
fills their hand.  Finally,  the hands are  resolved with no more player
intervention.  There is a sequence to these steps that doesn't seem
to benefit from the :strong:**State** design pattern.

Most of the game appears to be a sequence of offers from the
:class:`Game` instance to the :class:`BlackjackPlayer` instance; these are offers
to place bets, or accept cards, or a combination of the two, for each of
the player's :class:`Hand` instances.

Blackjack Collaboration
-----------------------

In Craps and Roulette, the :class:`Player` object was the primary
collaborator with the game. In Blackjack, however, focus shifts from the :class:`Player` intance
to the individual :class:`Hand` objects. This changes the responsibilities of a :class:`BlackjackPlayer`:
the :class:`Hand` object can delegate certain offers to the :class:`BlackjackPlayer` instance
for a response. The :class:`BlackjackPlayer` object become a plug-in
strategy to the :class:`Hand` instances, providing responses to offers of
insurance, even money, splitting, doubling-down, hitting and standing
pat. The :class:`BlackjackPlayer` object's response will change the states
of the the various :class:`Hand` instances in play. Some state changes involve getting a card,
and others involve placing a bet, and some involve a combination of the two.

Most of the time, there is a one-to-one relationship between the :class:`BlackjackPlayer` instance
and the :class:`Hand` instance in play. This changes where there is a split
and multiple :class:`Hand` instances are shared by a single :class:`BlackjackPlayer` instance.


We'll use the procedure definition in :ref:`blackjack.solution.proc`.
Following this procedure, we see the following methods that a :class:`Hand` object
and a :class:`BlackjackPlayer` object will need to respond to. These are the various
offers from the :class:`BlackjackGame` class. The first portion of the
game involves the :class:`BlackjackPlayer` object responding, the second portion
invovles one or more :class:`Hand` instances responding.

The collaboration is so intensive, it seems helpful to depict it in a swimlane table.
This table shows the operations each object must perform.
This will allow us to expand on the responsibiltiies of the :class:`Hand`
and :class:`BlackjackTable` clases as well as define the interface for :class:`BlackjackPlayer` class.

..  csv-table:: Blackjack Overall Collaboration
    :header-rows: 1
    :file: overall.csv

There are a few common variation in this procedure for play. We'll set
them aside for now, but will visit them in :ref:`blackjack.var`.

Insurance Collaboration
~~~~~~~~~~~~~~~~~~~~~~~~

The insurance procedure involves additional interaction between :class:`Game`
and the the :class:`Player`'s initial :class:`Hand`. The
following is done only if the dealer is showing an ace.


..  csv-table:: Blackjack Insurance Collaboration
    :header-rows: 1
    :file: insurance.csv

Filling the Hands
~~~~~~~~~~~~~~~~~

The procedure for filling each :class:`Hand` involves additional
interaction between :class:`Game` and the the :class:`Player`'s initial
:class:`Hand`. An :class:`Iterator` used for perform the
following procedure for each individual player :class:`Hand`.

..  csv-table:: Blackjack Fill-Hand Collaboration
    :header-rows: 1
    :file: fillhand.csv

There is some variation in this procedure for filling :class:`Hand` instances.
The most common variation only allows a double-down when the :class:`Hand`
has two cards.

Hand-Specific Decisions
~~~~~~~~~~~~~~~~~~~~~~~~

Some of the offers are directly to the :class:`BlackjackPlayer` instance,
while others require informing the :class:`BlackjackPlayer` object which of the
player's :class:`Hand` instances is being referenced.

How do we identify a specific hand?

-   One choice is to have the :class:`BlackjackGame` object
    make the offer to the :class:`Hand` object.  The :class:`Hand` instance
    can pass the offer to the :class:`BlackjackPlayer` object; the :class:`Hand`
    includes a reference to itself.

-   An alternative is to have the :class:`BlackjackGame` object
    make the offer directly to the :class:`BlackjackPlayer` object, including
    a reference to the relevant :class:`Hand` instance.

While the difference is
minor, it seems slightly more sensible for the :class:`BlackjackGame` object
to make offers directly to the :class:`BlackjackPlayer` object, including
a reference to the relevant :class:`Hand` instance.

Dealer Rules
-------------

In a sense, the dealer can be viewed as a special player.  They have a fixed set
of rules for hitting and standing.  They are not actually offered
an insurance bet, nor can they split or double down.

However, the dealer does participate in the hand-filling phase
of the game, deciding to hit or stand pat.

The dealer's rules are quite simple.  Should the Dealer be a
special subclass of the :class:`BlackjackPlayer` class; one that implements
only the dealer's rules?

Or, should the Dealer be a feature of the :class:BlackjackGame` class?  In this case, the
Game would maintain the dealer's Hand and execute the card-filling
algorithm.

Using an subclass of the :class:`BlackjackPlayer` class is an example
of **Very Large Hammer** design pattern.  We only want a few
features of the :class:`BlackjackPlayer` class, why drive a small nail
with a huge hammer?

**Refactoring**.
To avoid over-engineering these classes, we could refactor the :class:`BlackjackPlayer` class into
two components.  One component is an object that handles hand-filling, and the other component
is an object that handles betting strategies.

The dealer would only use the hand-filling component of a player.

**Mutability**.
We can look at features that are likely to change.  The dealer hand-filling rules seem well-established
throughout the industry.

Further, a change to the hand-filling rules of the dealer would
change the nature of the game enough that we would be hard-pressed
to call in Blackjack.  A different hand-filling rule would constitute
a new kind of game.

We're confident, then, that the dealer's hand can be a feature of the
:class:`BlackjackGame` class.

BlackjackPlayer Class
---------------------

..  class:: BlackjackPlayer

    The :class:`BlackjackPlayer` class is a subclass of :class:`Player` that
    responds to the various queries and interactions with the game of Blackjack.


Fields
~~~~~~~

..  attribute::  BlackjackPlayer.hand

    Some kind of :class:`List` which contains the initial :class:`Hand` and any split hands
    that may be created.


Constructors
~~~~~~~~~~~~~

..  method:: BlackjackPlayer.__init__(self, table: Table) -> None

    :param table: The table on which bets are placed
    :type table: :class:`BlackjackTable`

    Uses the superclass to construct a basic :class:`Player`. Uses the
    :meth:`newGame` to create an empty List fot the hands.


Methods
~~~~~~~~~~

..  method:: BlackjackPlayer.newGame(self) -> None

    Creates a new, empty list in which to keep :class:`Hand` instances.


..  method:: BlackjackPlayer.placeBets(self) -> None

    Creates an empty :class:`Hand`
    and adds it to the List of :class:`Hand` instances.

    Creates a new ante Bet. Updates the :class:`Table` with this :class:`Bet` on
    the initial :class:`Hand`.

..  method:: BlackjackPlayer.getFirstHand(self) -> None

    Returns the initial :class:`Hand`. This is used by the
    pre-split parts of the Blackjack game, where the player only has a single
    :class:`Hand`.


..  method:: BlackjackPlayer.__iter__(self) -> Iterator[Hand]

    Returns an iterator over the List of :class:`Hand` instances this
    player is currently holding.


..  method:: BlackjackPlayer.evenMoney(self, hand: Hand) -> bool

    :param hand: the hand which is offered even money
    :type hand: :class:`Hand`

    Returns :literal:`True` if this Player accepts the even money offer.
    The superclass always rejects this offer.

..  method:: BlackjackPlayer.insurance(self, hand: Hand) -> bool

    :param hand: the hand which is offered insurance
    :type hand: :class:`Hand`

    Returns :literal:`True` if this Player accepts the insurance offer.
    In addition to returning true, the Player must also create the Insurance
    :class:`Bet` and place it on the :class:`BlackjackTable`.
    The superclass always rejects this offer.

..  method:: BlackjackPlayer.split(self, hand: Hand) -> Hand

    :param hand: the hand which is offered an opportunity to split
    :type hand: :class:`Hand`

    If the hand has two cards of the same rank, it can be split.
    Different players will have different rules for determine
    if the hand should be split ot not.

    If the player's rules determine that it wil accepting the split offer for the given :class:`Hand`, :obj:`hand`,
    then the
    player will

    1.  Create a new Ante bet for this hand.

    2.  Create a new one-card :class:`Hand` from the given :obj:`hand` and return that new hand.

    If the player's rules determine that it will not accept the split offer, then :literal:`None`
    is returned.

    If the hand is split, adding cards to each of the resulting hands is the responsibility
    of the Game.  Each hand will be played out independently.


..  method:: BlackjackPlayer.doubleDown(self, hand: Hand) -> bool

    :param hand: the hand which is offered an opportunity to double down
    :type hand: :class:`Hand`


    Returns :literal:`True`
    if this Player accepts the double offer for this :class:`Hand`.
    The Player must also update the :class:`Bet` associated with this
    :class:`Hand`. This superclass always rejects this offer.


..  method:: BlackjackPlayer.hit(self, hand) -> bool

    :param hand: the hand which is offered an opportunity to hit
    :type hand: :class:`Hand`

    Returns :literal:`True`
    if this Player accepts the hit offer for this :class:`Hand`.
    The superclass accepts this offer if the hand is 16 or less, and
    rejects this offer if the hand is 17 more more. This mimics the
    dealer's rules.

    Failing to hit and failing to double down means the player is
    standing pat.


..  method:: BlackjackPlayer.__str__(self) -> str

    Displays the current state of the player, and the various hands.

Card Rework
------------

The :class:`Card` class must provide the :class:BlackjackGame` class some information required to
offer insurance bets.

We'll need to add an :meth:`offerInsurance` method on the :class:`Card` class.
The :class:`Card` superclass must respond with :literal:`False`.  This means that
the :class:`FaceCard` subclass can inherit this and also respond with :literal:`False`.

The :class:`AceCard` subclass, however, must respond with :literal:`True` to
this method.

Hand Rework
------------

The :class:`Hand` class should retain some additional hand-specific information.
Since some games allow resplitting of split hands, it's helpful to
record whether or not a player has declined or accepted the offer of a split.

Fields
~~~~~~~

..  attribute:: Hand.player

    Holds a reference to the :class:`Player` who owns this hand.
    Each of the various offers from the :class:`Game` are delegated
    to the :class:`Player`.

..  attribute:: Hand.splitDeclined

    Set to :literal:`True` if split was declined for a splittable hand.
    Also set to :literal:`True` if the hand is not splittable. The split
    procedure will be done when all hands return :literal:`True` for
    split declined.



Methods
~~~~~~~~~~

..  method:: Hand.splittable(self) -> bool

    Returns :literal:`True` if this hand has a size of two and both :class:`Card` instances
    have the same rank. Also sets :attr:`Hand.splitDeclined` to :literal:`True` if
    the hand is not splittable.

..  method:: Hand.getUpCard(self) -> Card

    Returns the first :class:`Card` from the list of cards, the up card.



BlackjackGame Class
--------------------

..  class:: BlackjackGame

    :class:`BlackjackGame` is a subclass of :class:`Game` that
    manages the sequence of actions that define the game of Blackjack.


    Note that a single cycle of play is one complete Blackjack game from the
    initial ante to the final resolution of all bets. Shuffling is implied
    before the first game and performed as needed.


Fields
~~~~~~~~

..  attribute::  BlackjackGame.shoe

    This is the dealer's :class:`Shoe` with the available pool of cards.


..  attribute:: BlackjackGame.dealer

    This is the dealer's :class:`Hand`.

Constructors
~~~~~~~~~~~~~~

..  method:: BlackjackGame.__init__(self, shoe: Shoe, table: BlackjackTable) -> None

    :param shoe: The dealer's shoe, populated with the proper number of decks
    :type shoe: :class:`Shoe`

    :param table: The table on which bets are placed
    :type table: :class:`BlackjackTable`

    Constructs a new :class:`BlackjackGame`, using a given :class:`Shoe`
    for dealing :class:`Card` instances and a :class:`BlackjackTable`
    for recording :class:`Bet` instances that are associated with specific :class:`Hand` instances.


Methods
~~~~~~~~~~


..  method:: BlackjackGame.cycle(self) -> None


    A single game of Blackjack. This steps through the following sequence
    of operations.

    #.  Call :meth:`BlackjackPlayer.newGame` to reset the player. Call :meth:`BlackjackPlayer.getFirstHand`
        to get the initial, empty :class:`Hand`.  Call :meth:`Hand.add` to
        deal two cards into the player's initial hand.

    #.  Reset the dealer's hand and deal two cards.

    #.  Call :meth:`BlackjackGame.hand.getUpCard` to get the dealer's up card. If
        this card returns :literal:`True` for the :meth:`Card.offerInsurance`,
        then use the :meth:`insurance` method.

        Only an instance fo the subclass :class:`AceCard` will return true for
        :meth:`offerInstance`.  All other :class:`Card` classes will return false.

    #.  Iterate through all :class:`Hand` instances, assuring that no hand
        it splittable, or split has been declined for all hands. If a
        hand is splittable and split has not previously been declined, call the :class:`Hand`'s
        :meth:`split` method.

        If the :meth:`split` method returns a new hand, deal an additional Card to the
        original hand and the new split hand.

    #.  Iterate through all :class:`Hand` instances calling the :meth:`fillHand`
        method to check for blackjack, deal cards and check for a bust.
        This loop will finish with the hand either busted or standing pat.

    #.  While the dealer's hand value is 16 or less, deal another card.
        This loop will finish with the dealer either busted or standing pat.

    #.  If the dealer's hand value is bust, resolve all ante bets as
        winners. The :class:`OutcomeAnte` should be able to do this
        evaluation for a given :class:`Hand` compared against the
        dealer's bust.

    #.  Iterate through all hands with unresolved bets, and compare the
        hand total against the dealer's total. The :class:`OutcomeAnte`
        should be able to handle comparing the player's hand and
        dealer's total to determine the correct odds.

    Note that there can be some variations to the steps in this cycle. A single, very long
    method body is a bad design. One of the key places where new functionality
    can be inserted is the final step determining of winning hands after the player and dealer's
    hands have been filled and neither player has gone bust.


..  method:: BlackjackGame.insurance(self) -> None


    Offers even money or insurance for a single game of blackjack. This
    steps through the following sequence of operations.

    #.  Get the player's :meth:`BlackjackPlayer.getFirstHand`. Is it blackjack?

        If the player holds blackjack, then call :meth:`BlackjackPlayer.evenMoney`.

        If the even money offer is accepted, then
        move the ante bet to even money at 1:1. Resolve the bet as a
        winner. The bet will be removed, and the game will be over.

    #.  Call :meth:`BlackjackPlayer.insurance`. If insurance declined, this
        method is done.

    #.  If insurance was accepted by the player, then check the dealer's hand.  Is it blackjack?

        If the dealer hold blackjack, the insurance bet is resolved as a winner,
        and the ante is a loser; the bets are removed and the game will
        be over.

        If the dealer does not have blackjack, the insurance bet
        is resolved as a loser, and the ante remains.

        If insurance was declined by the player, nothing is done.



..  method:: BlackjackGame.fillHand(self, hand: Hand) -> None

    :param hand: the hand which is being filled
    :type hand: Hand


    Fills one of
    the player's hands in a single game of Blackjack. This steps through
    the following sequence of operations.

    #.  While points are less than 21, call :meth:`BlackjackPlayer.doubleDown` to
        offer doubling down. If accepted, deal one card, filling is
        done.

        If double down is declined, call :meth:`BlackjackPlayer.hit` to
        offer a hit. If accepted, deal one card. If both double down and
        hit are declined, filling is done, the player is standing pat.

    #.  If the points are over 21, the hand is bust, and is immediately resolved as
        a loser.  The game is over.



..  method:: BlackjackGame.__str__(self) -> str


    Displays the current state of the game, including the player, and
    the various hands.


Blackjack Game Deliverables
----------------------------

There are eight deliverables for this exercise.

-   The stub :class:`BlackjackPlayer` class.

-   A class which performs a unit test of the :class:`BlackjackPlayer`
    class. Since this player will mimic the dealer, hitting a 16 and
    standing on a 17, the unit test can provide a variety of :class:`Hand`
    s and confirm which offers are accepted and rejected.

-   The revised :class:`Hand` class.

-   A class which performs a unit tests of the :class:`Hand` class.
    The unit test should create several instances of :class:`Card`, :class:`FaceCard`
    and :class:`AceCard`, and add these to instances of :class:`Hand`,
    to create various point totals. Since this version of :class:`Hand`
    interacts with a :class:`BlackjackPlayer`, additional offers of
    split, double, and hit can be made to the :class:`Hand`.

-   The revised :class:`Card` class.

-   Revised unit tests to exercise the :meth:`Card.offerInsurance` method.

-   The revised :class:`BlackjackGame` class.

-   A class which performs a unit tests of the :class:`BlackjackGame`
    class. The unit test will have to create a :class:`Shoe` instance that
    produces cards in a known sequence, as well as :class:`BlackjackPlayer`.
    The :meth:`cycle` method, as described in the design, is too
    complex for unit testing, and needs to be decomposed into a number
    of simpler procedures.

Looking Forward
----------------

We have all of the components in place to start looking at player strategies.
The player has a number of decisions during the game, plus a betting strategy
decision based on the outcome of each game. We'll set the betting aside
for a moment and focus on the Blackjack rules. In the next chapter, we'll
build a simple player that is able to work with the game and table.
