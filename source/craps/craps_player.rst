
CrapsPlayer Class
=================

The numerous variations on :class:`CrapsPlayer`, all of which reflect different
betting strategies, are the heart of this application. In :ref:`roul.game`,
we roughed out a stub class for :class:`Player`, and refined it in
:ref:`roul.player`. We will further refine this to create
a definition of the :class:`CrapsPlayer` class for use in simulating
the complex stateful game of Craps.

In `Craps Player Analysis`_ we'll look at the general responsibilities
and collaborators of a player. Since we've already examined many features
of the game, we can focus on the player and revising the roughed-out
version we created earlier.

We'll present the details of the design in three parts:

-   `CrapsPlayer Design`_ covers the superclass features,

-   `CrapsPlayerPass Subclass`_ covers a subclass which only bets the pass line, and

-   `Craps Martingale Subclass`_ covers a player who uses Martingale betting.

In `Craps Player Deliverables`_ we'll detail the deliverables for this chapter.

Craps Player Analysis
----------------------

We have built enough infrastructure that we can begin to add a
variety of players and see how their betting strategies work. Each
player has betting algorithm that we will evaluate by looking at the
player's stake to see how much they win, and when they stop playing
because they've run out of time or gone broke.

As a practical matter, the house edge means players will eventually
go broke. It's mostly a question of how long they can play before
they've run out of money.


The :class:`CrapsPlayer` class has the responsibility to create bets and manage
the amount of their stake. To create bets, the player must create legal
bets from known :class:`Outcome` instances and stay within table limits. To
manage their stake, the player must deduct the price of a bet when it is
created, accept winnings or pushes, report on the current value of the
stake, and leave the table when they are out of money.


We have an interface that was roughed out as part of the design of
the :class:`CrapsGame`
and :class:`CrapsTable` classes. In designing the :class:`CrapsGame` class, we
put a :meth:`placeBets` method in the :class:`CrapsPlayer` class to
place all bets. We expected the :class:`CrapsPlayer` class to create :class:`Bet`
instances and use the :meth:`CrapsTable.placeBet` method
to save the individual :class:`Bet` instances.


In an earlier exercise, we built a stub version of the :class:`CrapsPlayer` class
in order to test the :class:`Game` class. See :ref:`craps.game.playerstub`.
When we finish creating the final superclass, :class:`CrapsPlayer`,
we will also revise our :class:`CrapsPlayerStub` to be more
complete, and rerun our unit tests to be sure the expanded
design still handles the basic test cases correctly.


Our objective is to have a new abstract :class:`CrapsPlayer` class,
with a concrete subclass that follows the Martingale system, using
simple Pass Line bets and behind the line odds bets.


We'll defer some of the design required to collect detailed measurements
for statistical analysis. In this first release, we'll simply place
bets. Most of the :class:`Simulator` class we built for
Roulette should be applicable to Craps without significant modification.

**Some Basic Features**.
Our basic :class:`CrapsPlayer` class will place a Pass Line bet and a Pass
Line Odds bet. This requires the player to interact with the :class:`CrapsTable`
or the :class:`CrapsGame` class to place bets legally. On a come out roll,
only the Pass Line will be legal. After that, a single Pass Line Odds
bet can be placed. This leads to three betting rules:

-   **Come Out Roll**. Condition: No Pass Line Bet is currently placed and
    only the Pass Line bet is legal. Action: Place a Pass Line bet.

-   **First Point Roll**. Condition: No odds bets is currently placed and
    odds bets are legal. Action: Place a Pass Line Odds bet.

-   **Other Point Roll**. Condition: An odds bets is currently placed.
    Action: Do Nothing.


Beyond simply placing Pass Line and Pass Line Odds bets, we can use a
Martingale or a Cancellation betting system to increase the bet on each
loss, and decrease the amount on a win. Since we have two
different bets in play -- a single bet created on the come out roll, a
second odds bet if possible -- the simple Martingale system doesn't work
well. In some casinos, the behind the line odds bet can be double the
pass line bet, or even 10 times the pass line bet, leading to some potentially
complex betting strategies. For example, the :class:`CrapsPlayer` could apply the Martingale
system only to the odds bet, leaving the pass line bet at the table
minimum. We'll set this complexity aside for the moment, build a simple
player first.


CrapsPlayer Design
------------------------------

The :class:`CrapsPlayer` class is a subclass of an abstract :class:`Player` class.
It places bets in Craps. This is also an abstract class, with no actual body for the :meth:`Player.placeBets`
method. However, this subclass does implement the basic :meth:`win` and
:meth:`lose` methods used by all of its subclasses.


Since this is a subclass of a common player definition, we inherit
several useful features. Most of the features of :class:`Player` are
repeated here. The student should refactor the common code out of
the :class:`CrapsPlayer` class into the common superclass shared by
the :class:`CrapsPlayer` and :class:`RoulettePlayer` classes.


Fields
~~~~~~~

..  attribute:: CrapsPlayer.stake

    The player's current stake. Initialized to the player's starting budget.


..  attribute:: CrapsPlayer.roundsToGo

    The number of rounds left to play. Initialized by the overall
    simulation control to the maximum number of rounds to play. In
    Roulette, this is spins. In Craps, this is the number of throws of
    the dice, which may be a large number of quick games or a small
    number of long-running games. In Blackjack, this is the number of cards
    played, which may be large number of hands or small number of
    multi-card hands.

..  attribute:: CrapsPlayer.table
    :noindex:

    The :class:`CrapsTable` used to place individual :class:`Bet` instances.


Constructors
~~~~~~~~~~~~~


..  method:: CrapsPlayer.__init__(self, table: CrapsTable) -> None
    :noindex:

    :param table: The table
    :type table: :class:`CrapsTable`


    Constructs the :class:`CrapsPlayer` instance with a specific :class:`CrapsTable` object
    for placing :class:`Bet` instances.


Methods
~~~~~~~~


..  method:: CrapsPlayer.playing(self) -> bool



    Returns :literal:`True`
    while the player is still active. A player with a stake of zero will
    be inactive. Because of the indefinite duration of a craps game, a
    player will only become inactive after their :obj:`roundsToGo`
    is zero and they have no more active bets. This method, then, must
    check the :class:`CrapsTable` instance to see when all the bets are fully
    resolved. Additionally, the player's betting rules should stop
    placing new bets when the :obj:`roundsToGo` is zero.



..  method:: CrapsPlayer.placeBets(self) -> bool


    Updates the :class:`CrapsTable` instance
    with the various :class:`Bet` instances.

    When designing the :class:`CrapsTable` class, we decided that we
    needed to deduct the price of the bet from the stake when the bet is
    created. See the Roulette Table :ref:`roul.table.ov` for more
    information on the timing of this deduction, and the Craps Bet :ref:`craps.bet.ov`
    for more information on the price of a bet.



..  method:: CrapsPlayer.win(self, bet: Bet) -> None

    :param bet: that was a winner
    :type bet: :class:`Bet`


    Notification from the :class:`CrapsGame` object
    that the :class:`Bet` instance was a winner. The amount of money won is
    available via :meth:`Bet.winAmount`.



..  method:: CrapsPlayer.lose(self, bet: Bet) -> None

    :param bet: that was a loser
    :type bet: :class:`Bet`


    Notification from the :class:`CrapsGame`
    that the :class:`Bet` instance was a loser.


CrapsPlayerPass Subclass
------------------------

:class:`CrapsPlayerPass` is a :class:`CrapsPlayer` who places a
Pass Line bet in Craps.


Methods
~~~~~~~



..  method:: CrapsPlayer.placeBets(self) -> bool


    If no Pass Line bet is
    present, this will update the :class:`Table` object with a bet on the
    Pass Line at the base bet amount.

    Otherwise, this method does not place an additional bet.


Craps Martingale Subclass
-------------------------

..  class:: CrapsMartingale
    :noindex:

    The :class:`CrapsMartingale` class is a subclass of :class:`CrapsPlayer` who places
    bets in Craps. This player doubles their Pass Line Odds bet on every
    loss and resets their Pass Line Odds bet to a base amount on each win.


Fields
~~~~~~~

..  attribute:: CrapsPlayer.lossCount

    The number of losses. This is the number of times to double the pass
    line odds bet.

..  attribute:: CrapsPlayer.betMultiple

    The bet multiplier, based on the number of losses. This starts
    at 1, and is reset to 1 on each win. It is doubled in each loss.
    This is always set so that :math:`betMultiple = 2^{lossCount}`.


Methods
~~~~~~~~




..  method:: CrapsPlayer.placeBets(self) -> bool


    If no Pass Line bet is
    present, this will update the :class:`Table` with a bet on the
    Pass Line at the base bet amount.

    If no Pass Line Odds bet is present, this will update the :class:`Table` object
    with a Pass Line Odds bet. The amount is the base amount times the :obj:`betMultiple`.

    Otherwise, this method does not place an additional bet.




..  method:: CrapsPlayer.win(self, bet: Bet) -> None

    :param bet: that was a winner
    :type bet: Bet


    Uses the superclass :meth:`win`
    method to update the stake with an amount won. This method then resets the
    :obj:`lossCount` to zero, and resets the :obj:`betMultiple` to :literal:`1`.



..  method:: CrapsPlayer.lose(self, bet: Bet) -> None

    :param bet: that was a loser
    :type bet: :class:`Bet`


    Increments :obj:`lossCount` by :literal:`1`
    and doubles :obj:`betMultiple`.


Craps Player Deliverables
---------------------------

There are six deliverables for this exercise.


-   The :class:`CrapsPlayer` abstract superclass. Since this class
    doesn't have a body for the :meth:`placeBets` method, it can't
    be unit tested directly.

-   A :class:`CrapsPlayerPass` class that is a proper subclass of the :class:`CrapsPlayer` class,
    but simply places bets on Pass Line until the stake is exhausted.

-   A unit test class for the :class:`CrapsPlayerPass` class. This test
    should synthesize a fixed list of :class:`Outcome` instances, :class:`Throw`
    instances, and calls a :class:`CrapsPlayerPass` instance with various
    sequences of craps, naturals and points to assure that the pass line
    bet is made appropriately.

-   The :class:`CrapsMartingale` subclass of the :class:`CrapsPlayer` class.

-   A unit test class for the :class:`CrapsMartingale` class. This test
    should synthesize a fixed list of :class:`Outcome` instances, :class:`Throw`
    objects, and calls a :class:`CrapsMartingale` instance with various
    sequences of craps, naturals and points to assure that the bet
    doubles appropriately on each loss, and is reset on each win.

-   The unit test class for the :class:`CrapsGame` class should
    still work with the new :class:`CrapsPlayerPass` class. Using a
    non-random generator for the :class:`Dice` instance, this should be able to
    confirm correct operation of the :class:`CrapsGame` class for a number
    of bets.

Looking Forward
---------------

Once we have the basics of a player, we can do some design cleanup and
refactoring of the code. We have a large number of classes, and there are some
areas of overlap and commonality that suggest possible simplifications.
In the next chapter we'll refactor some more of the application class hierarchy.
