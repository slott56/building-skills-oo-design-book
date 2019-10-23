
..  _`roul.player`:

Player Class
============

The variations on :class:`Player` class implementations are the heart of this application.
Each subclass can reflect different betting strategies.
In :ref:`roul.game`,
we roughed out a stub class for the :class:`Player` class. In this chapter,
we will complete that design. We will also expand on it to implement the
Martingale betting strategy.

We have now built enough infrastructure that we can begin to add a
variety of players and see how poorly each betting strategy works. Each
player is a betting algorithm that we will evaluate by looking at the
player's stake to see how much they win, and how long they play before
they run out of time or go broke.

We'll look at the player problem in `Roulette Player Analysis`_.

In `Player Design`_ we'll expand on our previous skeleton :class:`Player`
to create a more complete implementation. We'll expand on that again
in `Martingale Player Design`_.

In `Player Deliverables`_ we'll enumerate the deliverables for
this chapter.

Roulette Player Analysis
------------------------

The :class:`Player` class has the responsibility to create :class:`Bet` instances and manage
the amount of their stake. To create :class:`Bet` instances, the player must create legal
bets from known :class:`Outcome` instances and stay within table limits. To
manage their stake, the player must deduct money when creating a bet,
accept winnings or pushes, report on the current value of the stake, and
leave the table when they are out of money.

We'll look at a number of topics:

-   Our overall goal, in `Design Objectives`_.

-   How we manage the budget, in `Tracking the Stake`_.

-   How a player interacts with table limits, in `Table Limits`_.

-   In `Leaving the Table`_ we'll look at a player retiring when they're ahead.
    Or broke.

-   In `Creating Bets from Outcomes`_ we'll look at a technical question of
    transforming an :class:`Outcome` instance into a :class:`Bet` instance.



We roughed out an interface for the player as part of the design of the :class: `Game` class
and the :class:`Table` class. In designing the :class: `Game` class,
we defined a :meth:`Player.placeBets` method to place all bets.
We expected the :class:`Player` instance
to create :class:`Bet` instances and use the :meth:`Table.placeBet` method
to save all of the individual :class:`Bet` instances.


In the :ref:`roul.game.design.passenger57` section we defined a kind of player.
When we finish creating the final superclass, :class:`Player`, we
can then revise our :class:`Passenger57` class to be a subclass of the :class:`Player` class.
We should be able to rerun our unit tests to be sure that this new, more complete design
still handles the original test cases correctly.


Design Objectives
~~~~~~~~~~~~~~~~~

Our objective is to have a new abstract class, :class:`Player`,
with two new concrete subclasses: a revision to the :class:`Passenger57` class
and a new player subclass that follows the Martingale betting system.

We'll defer some of the design required to collect detailed measurements
for statistical analysis. In this first release, we'll simply place bets.

There are four design issues tied up in the :class:`Player` class: tracking
stake, keeping within table limits, leaving the table, and creating
bets. We'll tackle them in separate subsections.

Tracking the Stake
~~~~~~~~~~~~~~~~~~~

One of the more important features we need to add to the
:class:`Player` class are the methods to track the player's stake. The
initial value of the stake is the player's budget. Here is a list of several
significant changes to the stake:

-   Each bet placed will deduct the bet amount from the :class:`Player` object's
    stake. We are stopped from placing bets when our stake is less
    than the table minimum.

-   Each win will credit the stake. The :class:`Outcome` class will
    compute this amount for the :class:`Player` object.

-   Additionally, a "push" outcome will put the original bet amount back
    into the player's stake. This is a kind of win with no odds applied.

We'll have to design an interface that will create :class:`Bet` objects,
reducing the stake. and will be used by :class: `Game` class to notify the :class:`Player`
instance of the amount won.

Additionally, we will need a method to reset the stake to the starting amount. This will be used
as part of data collection for the overall simulation.

Table Limits
~~~~~~~~~~~~

Once we have our superclass, we can then define the :class:`Martingale`
player as a subclass. This player doubles their bet on every loss, and
resets their bet to a base amount on every win. In the event of a long
sequence of losses, this player will have their bets rejected as over
the table limit. This raises the question of how the table limit is
represented and how conformance with the table limit is assured.

We put a preliminary design in place in :ref:`roul.table`.
There are several places where we could isolate this responsibility.


#.  The :class:`Player` class can stop placing bets when they are over the table
    limit. In this case, we will be delegating responsibility to the :class:`Player` class
    hierarchy. In a casino, a sign is posted on the table, and both
    players and casino staff enforce this rule. This can be modeled by
    providing a method in :class:`Table` class to return the
    table limit for use by the :class:`Player` instance to keep bets within
    the limit.


#.  The :class:`Table` class provides a "valid bet" method. This can include
    computing a total of all bets placed, and raise exceptions.


#.  The :class:`Table` class raises an "illegal bet" exception when
    an illegal bet is placed.

The first alternative is unpleasant because the responsibility to spread
around: both the :class:`Player` and the :class:`Table` classes must be aware of a feature
of the :class:`Table` class. This means that a change to the :class:`Table` class design will
also require a change to the :class:`Player` class implementation. This is poor object-oriented
design.

The second and third choices reflect two common approaches that are summarized
as:

-   **Ask Permission**. The application has code wrapped in :code:`if permitted:`
    conditional processing.

-   **Ask Forgiveness**. The application assumes that things will work.
    An exception indicates something unexpected happened.

The general advice is this:

    **It's easier to ask forgiveness than to ask permission.**

Most of the time, validation should be handled by raising an exception. This suggests
the :class:`Table` class should raise exceptions for bets which are invalid.
This includes rejecting bets which exceed the table limit.

**Handling Game State**.
The idea of bet validation raises a question about how we handle games where some bets
are not allowed during some game states.

There are two sources of validation for a bet.

-   The :class:`Table` class may reject a bet because it's over (or under) a limit.

-   The :class: `Game` class may reject a bet because it's illegal in the current
    state of the game.

Since these considerations are part of Craps and Blackjack, we'll set them
aside for now. They're side-bar considerations during the design of Roulette.

Leaving the Table
~~~~~~~~~~~~~~~~~

We need to address the issue of the player
leaving the game. We can identify a number of possible reasons for
leaving: out of money, out of time, won enough, and unwilling to place a
legal bet. Since this decision is private to the :class:`Player` class,
we need a way of alerting the :class: `Game` instance that the :class:`Player` object
is finished placing bets.


There are three mechanisms for alerting a :class: `Game` instance that a :class:`Player`
instance is finished placing bets.


#.  Expand the responsibilities of the :meth:`Game.placeBets` to also
    indicate if the player intends to play or is withdrawing from the
    game. While most table games require bets on each round, it is
    possible to step up to a table and watch play before placing a bet.
    This is one classic strategy for winning at blackjack: one player
    sits at the table, placing small bets and counting cards, while a
    confederate places large bets only when the deck is favorable. We
    really have three player conditions: watching, betting, and finished
    playing. It becomes complex trying to bundle all this extra
    responsibility into the :meth:`Game.placeBets` method.


#.  Add another method to the :class:`Player` class, used by the :class: `Game` class
    to determine if the :class:`Player` instance will continue or
    stop playing. This can be used for a player who is placing no bets
    while waiting; for example, a player who is waiting for the Roulette
    wheel to spin red seven times in a row before betting on black.


#.  The :class:`Player` class can raise an exception when they are done
    playing. This is an odd use case for an exception. The situation
    occurs exactly once in each simulation, and it is a well-defined condition:
    it doesn't deserve to be called "exceptional" . It is merely a
    terminating condition for the game.


We recommend adding a method to the :class:`Player` class to indicate when the player
is finished. This gives the most flexibility, and it permits the :class:`Game` class
to cycle until the player withdraws from the game.


A consequence of this decision is to rework the :class: `Game` class
to allow the player to exit. This is relatively small change to
interrogate the :class:`Player` instance to see if they're active
before asking them to place bets.

..  note:: Design Evolution

    This section reveals situations we didn't discover during
    the initial design. It helped to have some experience with the
    classes in order to determine the proper allocation of
    responsibilities. While design walk-throughs are helpful, an
    alternative is to create a "technical spike": a piece of software that is
    incomplete and can be disposed of. The earlier exercise created a
    version of the :class:`Game` class that was incomplete,
    and a version of :class:`Passenger57` that will have to be disposed of.


Creating Bets from Outcomes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generally, a :class:`Player` instance will
have a few :class:`Outcome` instances on which they are betting. Many
systems are similar to the Martingale system, and place bets on only one
of the many :class:`Outcome` instances. These :class:`Outcome` objects are
usually created during player initialization. From these :class:`Outcome` instances,
the :class:`Player` object can create the individual :class:`Bet`
instances based on their betting strategy.

Since we're currently using the :class:`Wheel` class as a repository for all legal
:class:`Outcome` instances, we'll need to provide the :class:`Wheel` class to the
:class:`Player`.

This doesn't generalize well for Craps or Blackjack. We'll need to revisit
this design decision. In the long run, we'll need to find another kind of factory for
creating proper :class:`Outcome` instances.

We'll design the base class of :class:`Player` and a specific subclass,
:class:`Martingale`. This will give us a working player that we can
test with.


Player Design
--------------

..  class:: Player

    :class:`Player` places bets in Roulette. This an abstract class,
    with no actual body for the :meth:`Player.placeBets` method. However,
    this class does implement the basic :meth:`Player.win` method used by all subclasses.

Fields
~~~~~~~

..  attribute:: Player.stake
    :noindex:

    The player's current stake. Initialized to the player's starting budget.

..  attribute:: Player.roundsToGo
    :noindex:

    The number of rounds left to play. Initialized by the overall
    simulation control to the maximum number of rounds to play. In
    Roulette, this is spins. In Craps, this is the number of throws of
    the dice, which may be a large number of quick games or a small
    number of long-running games. In Craps, this is the number of cards
    played, which may be large number of hands or small number of
    multi-card hands.

..  attribute:: Player.table
    :noindex:

    The :class:`Table` object used to place individual :class:`Bet` instances.
    The :class:`Table` object contains the current :class:`Wheel` object from which
    the player can get :class:`Outcome` objects used to build :class:`Bet` instances.


Constructors
~~~~~~~~~~~~~~


..  method:: Player.__init__(self, table: Table) -> None
    :noindex:

    Constructs the :class:`Player` instance with a specific :class:`Table` object
    for placing :class:`Bet` instances.

    :param table: the table to use
    :type table: :class:`Table`

    Since the table has access to the :class:`Wheel` instance, we can
    use this wheel to extract :class`Outcome` objects.

Methods
~~~~~~~~~


..  method:: Player.playing(self) -> bool
    :noindex:


    Returns :literal:`True`
    while the player is still active.


..  method:: Player.placeBets(self) -> None
    :noindex:


    Updates the :class:`Table` object
    with the various :class:`Bet` objects.

    When designing the :class:`Table` class, we decided that we needed to
    deduct the amount of a bet from the stake when the bet is created.
    See the Table :ref:`roul.table.ov` for more information.


..  method:: Player.win(self, bet: Bet) -> None
    :noindex:

    :param bet: The bet which won
    :type bet: :class:`Bet`


    Notification from the :class: `Game` object
    that the :class:`Bet` instance was a winner. The amount of money won is
    available via the :meth:`Bet.winAmount` method.



..  method:: Player.lose(self, bet: Bet) -> None
    :noindex:

    :param bet: The bet which won
    :type bet: Bet


    Notification from the :class: `Game` object
    that the :class:`Bet` instance was a loser. Note that the amount was
    already deducted from the stake when the bet was created.

..  _`roul.player.martingale`:

Martingale Player Design
--------------------------

..  class:: Martingale

    :class:`Martingale` is a :class:`Player` who places bets in
    Roulette. This player doubles their bet on every loss and resets their
    bet to a base amount on each win.

Fields
~~~~~~

..  attribute:: Martingale.lossCount

    The number of losses. This is the number of times to double the bet.

..  attribute:: Martingale.betMultiple

    The the bet multiplier, based on the number of losses. This starts
    at 1, and is reset to 1 on each win. It is doubled in each loss.
    This is always equal to :math:`2^{lossCount}`.


Methods
~~~~~~~


..  method:: Martingale.placeBets(self) -> None


    Updates the :class:`Table` object
    with a bet on "black". The amount bet is :math:`2^{lossCount}`,
    which is the value of :obj:`betMultiple`.


..  method:: Martingale.win(self, bet: Bet) -> None

    :param bet: The bet which won
    :type bet: :class:`Bet`



    Uses the superclass :meth:`Player.win`
    method to update the stake with an amount won. This method then resets
    :obj:`lossCount` to zero, and resets :obj:`betMultiple` to :literal:`1`.


..  method:: Martingale.lose(self, bet: Bet) -> None

    :param bet: The bet which won
    :type bet: :class:`Bet`


    Uses the superclass :meth:`Player.loss` to do whatever bookkeeping the superclass
    already does.
    Increments :obj:`lossCount` by :literal:`1`
    and doubles :obj:`betMultiple`.


Player Deliverables
-------------------

There are six deliverables for this exercise. The new classes must have
Python docstrings.

-   The :class:`Player` abstract superclass. Since this class
    doesn't have a body for the :meth:`placeBets`, it can't be
    unit tested directly.

-   A revised :class:`Passenger57` class. This version will be a
    proper subclass of :class:`Player`, but still place bets on
    black until the stake is exhausted. The existing unit test for :class:`Passenger57` class
    should continue to work correctly after these changes.

-   The :class:`Martingale` subclass of the :class:`Player` class.

-   A unit test class for the :class:`Martingale` class. This test should
    synthesize a fixed list of :class:`Outcome` instances, :class:`Bin` instances,
    and calls a :class:`Martingale` instance with various
    sequences of reds and blacks to assure that the bet doubles
    appropriately on each loss, and is reset on each win.

-   A revised :class: `Game` class. This will check the player's :meth:`playing`
    method before calling :meth:`placeBets` method, and do nothing if
    the player withdraws. It will also call the player's :meth:`win`
    and :meth:`loss` methods for winning and losing bets.

-   A unit test class for the revised :class: `Game` class. Using a
    non-random generator for :class:`Wheel` instance, this should be able to
    confirm correct operation of the :class: `Game` class for a number of bets.

Looking Forward
---------------

Now that we have working :class:`Table`, :class:`Game`, and :class:`Player` classes, we have
two fundamental choices. One option is to build more subclass of the :class:`Player` class.
The other choice is to put an overall simulation wrapper around the work done so far.

Building the overall simulation control allows us to deliver a small,
working example before investing time in building more sophisticated features.
This is a very helpful next step, so the next chapter will look at overall simulation
control.
