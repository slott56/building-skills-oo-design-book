
..  _`craps.count`:

Roll-Counting Player Class
===========================

A common Craps strategy is to add bets as a kind of "hedge" against
losing the line bet.  This means that a player can have numerous working bets:
the mandatory line bet, the behind the line odds bet, plus any additional hedge
bets.  For example, buying the 6 or 8 is a hedge that will pay out separately
from the game overall.

We'll tackle a particularly complex betting strategy.  In this case,
a player that judges that a game has gone "too long" without a successful
resolution.  This is a common fallacy in probability theory.  A seven is
not "due".  The odds of throwing a seven are always :math:`\tfrac{1}{6}`.

In order to handle this, we'll need to have a larger number of
independent bets, with independent betting strategies. The previous
design will have to be expanded to allow for this.

In `Roll-Counting Analysis`_ we'll examine the essential betting strategy.
This will have large implications. We'll look at them in `Decomposing the Player`_
and `Implementing SevenCounter`_.

This will lead to a round of redesigning a number of classes.
In `BettingStrategy Design`_ we'll disentangle the game-based betting
from the various betting strategies that dictate amounts.

We can then implement each betting strategy in a way that's separate
from each player. We'll look at the details in:

-   `NoChangeBetting Class`_,

-   `MartingaleBetting Class`_, and

-   `Bet1326Betting Class`_.

Once we've separated betting strategies from game playing
strategies, we can then create a number of more advanced players.
These include

-   `CrapsOneBetPlayer class`_,

-   `CrapsTwoBetPlayer class`_, and

-   `CrapsSevenCountPlayer class`_.

We'll enumerate the deliverables in `Roll-Counting Deliverables`_.

Roll-Counting Analysis
-----------------------

There is a distinction between one-roll odds and cumulative odds. The
one roll odds of rolling a 7 are :math:`\tfrac{1}{6}`. This means that a Pass Line bet
will win one time in six on the come out roll. The cumulative odds of
rolling a 7 on a number of rolls depends on not rolling a seven (a :math:`\tfrac{5}{6}`
chance) for some number of rolls, followed by rolling a 7. The odds are
given in the following table.

..  csv-table::

    "Throws","Rule","Odds of 7"
    "1",:math:`\tfrac{1}{6}`,"17%"
    "2",:math:`\tfrac{5}{6} \times \tfrac{1}{6}`,"31%"
    "3",:math:`\left(\tfrac{5}{6}\right)^2 \times \tfrac{1}{6}`,"42%"
    "4",:math:`\left(\tfrac{5}{6}\right)^3 \times \tfrac{1}{6}`,"52%"
    "5",:math:`\left(\tfrac{5}{6}\right)^4 \times \tfrac{1}{6}`,"60%"
    "6",:math:`\left(\tfrac{5}{6}\right)^5 \times \tfrac{1}{6}`,"67%"


This cumulative chance of rolling a 7 suggests the odds of the game
ending with a loss will grow because the cumulative odds of throwing a 7 grow as the game progresses also
grows.

The idea here is the longer a game
runs, the more likely it is to lose the initial Pass Line bet.
Consequently, some players count the throws in the game, and effectively
cancel their bet by betting against themselves with the Seven proposition.

Each game duration has a probability. The sum of all durations weighted by their
probabilities is the expected value of the game duration. With a little coding,
it's apparent the expected duration is six throws. While games longer than
that are possible, they are unexpected.

..  important:: Bad Odds

    Note that the Seven proposition is a :math:`\tfrac{1}{6}` probability that pays "5 for 1", (effectively :math:`4:1`).

While the basic probability analysis of this bet is not encouraging, it
does have an interesting design problem: the player now has multiple
concurrently changing  states:

-   They have Pass Line bet,

-   they can use a Martingale strategy for their Pass Line Odds bet,

-   they are counting throws, and using a
    Martingale strategy for a Seven proposition starting with the seventh
    throw of the game.

Either the class will become quite complex. Or we'll have to decompose
this class into a collection of simpler objects, each modeling the individual state changes.

..  sidebar:: Wrong Bettors

    The simple counting doesn't work for wrong bettors -- those using the
    Don't Pass Line bet. Their concern is the opposite: a short game may
    cause them to lose their Don't Pass bet, but a long game makes it more
    likely that they would win.

Decomposing the Player
~~~~~~~~~~~~~~~~~~~~~~~~

This leads us to consider the :class:`Player` class as a composite object with a number
of states and strategies. It also leads us to design a separate class to
handle Martingale betting.

When we were looking at the design
for the various players in :ref:`craps.refactor`, we glanced at the
possibility of separating the individual betting strategies from the
players, and opted not to. However, we did force each strategy to depend
on a narrowly-defined interface of the :meth:`oddsBet`, :meth:`win`
and :meth:`lose` methods. We can exploit this narrow interface in teasing
apart the various strategies and rebuilding each variation of the :class:`Player` class
with a distinct betting strategy object.


The separation of the :class:`Player` class from the :class:`BettingStrategy` class
involves taking the betting-specific information out of each :class:`Player` subclass,
and replacing the various methods and fields with one or more :class:`BettingStrategy`
objects.

In the case of Roulette players, this is relatively simple. We generally use
just one bet with a variety of strategies.

In the case of Craps players, we often have two bets, one with a
trivial-case betting strategy where the bet never changes. We'll need a special
:class:`NoChange` class to define the strategy for the Pass Line.
We'll need a Martingale (or 1-3-2-6, Cancellation,
or Fibonacci) for the Behind the Line Odds bet.
We can then redefine all Craps player's bets using instances of these :class:`BettingStrategy` objects.

The responsibilities of a :class:`BettingStrategy` object include the following things:

-   Maintain a preferred :class:`Outcome` instance, used to build :class:`Bet` instances.

-   Maintain a bet amount, changing the amount in  response to wins and losses.

The existing :meth:`win` and :meth:`lose`
methods are a significant portion of these responsibilities. The :meth:`oddsBet`
method of the various :class:`CrapsSimplePlayer` classes embodies other
parts of this, however, the name is inappropriate and it has a poorly
thought-out dependency on the :class:`Player` superclass.


The responsibilities of a :class:`Player` instance are to

- keep one or more betting strategies, so as to place bets in a game.

All of the Roulette players will construct a single :class:`BettingStrategy`
object with their preferred :class:`Outcome` instance. This is consistent
with this new design.

The various :class:`CrapsSimplePlayer` classes
will have two :class:`BettingStrategy` instances: one for the line
bet and one for the odds bet. This also fits with the player as a collection
of strategies.

The only difference among the simple
strategies is the actual :class:`BettingStrategy` object,
simplifying the :class:`Player` class hierarchy to a single Roulette
player and two kinds of Craps players: the stub player who makes only
one bet and the other players who make more than one bet and use a
betting strategy for their odds bet.

Implementing SevenCounter
~~~~~~~~~~~~~~~~~~~~~~~~~

Once we have this design in place, our :class:`SevenCounter` class
can then be composed of three, separate betting strategies objects:

-   a Pass Line bet that uses the :class:`NoChange` strategy;

-   a Pass Line Odds bet that uses are more advanced betting strategy;

-   a Seven proposition bet that will only be used after seven rolls have
    passed in a single game.

The Pass Line Odds and Seven proposition bets can use any of the strategies we have
built: Martingale, 1-3-2-6, Cancellation, or Fibonacci.

Currently, there is no method to formally notify the :class:`CrapsPlayer` of
unresolved bets. The player is only told of winners and losers.

The opportunity to place bets indicates that the dice are being rolled.
Additionally, the ability to place a line bet indicates that a game is
beginning. We can use these two methods to count the throws in during
a game, and reset the counter at the start of a game, effectively counting unresolved bets.

BettingStrategy Design
-----------------------

..  class BettingStrategy::

    The :class:`BettingStrategy` class is an abstract superclass for all betting
    strategies. It contains a single :class:`Outcome`, tracks wins and
    losses of :class:`Bet` instances built on this :class:`Outcome`, and
    computes a bet amount based on a specific betting strategy.


Fields
~~~~~~~

..  attribute:: BettingStrategy.outcome

    This is the :class:`Outcome` that will be watched for wins and
    losses, as well as used to create new :class:`Bet` instances.


Constructors
~~~~~~~~~~~~~~


..  method:: BettingStrategy.__init__(self, outcome: Outcome) -> None

    :param outcome: The outcome on which this strategy will create bets
    :type outcome: :class:`Outcome`


    Initializes this betting strategy with the given :class:`Outcome`.


Methods
~~~~~~~


..  method:: BettingStrategy.createBet(self) -> Bet


    Returns a new :class:`Bet` using the :obj:`outcome` :class:`Outcome`
    and any other internal state of this object.



..  method:: BettingStrategy.win(self, bet: Bet) -> None

    :param bet: The bet which was a winner
    :type bet: :class:`Bet`


    Notification
    from the :class:`Player` that the :class:`Bet` was a winner. The
    :class:`Player` has responsibility for handling money, this
    class has responsibility for tracking bet changes.



..  method:: BettingStrategy.lose(self, bet: Bet) -> None

    :param bet: The bet which was a loser
    :type bet: :class:`Bet`


    Notification
    from the :class:`Player` that the :class:`Bet` was a loser.




..  method:: BettingStrategy.__str__(self) -> str


    Returns a string with the name of the class and appropriate current
    state information. For the superclass, it simply returns the name of
    the class. Subclasses will override this to provide
    subclass-specific information.


NoChangeBetting Class
----------------------

..  class:: NoChangeBetting

    The :class:`NoChangeBetting` is a subclass of :class:`BettingStrategy`
    that uses a single, fixed amount for the bet. This is useful for unit
    testing, for modeling simple-minded players, and for line bets in Craps.


Fields
~~~~~~~

..  attribute:: BettingStrategy.betAmount

    This is the amount that will be bet each time.  A useful default
    value is 1.


Constructors
~~~~~~~~~~~~~


..  method:: NoChangeBetting.__init__(self, outcome: Outcome) -> None

    :param outcome: The outcome on which this strategy will create bets
    :type outcome: :class:`Outcome`


    Uses the superclass initializer with the given :class:`Outcome`.


Methods
~~~~~~~~~~



..  method:: NoChangeBetting.createBet(self) -> Bet


    Returns a new :class:`Bet`
    using the :obj:`outcome` :class:`Outcome` and :obj:`betAmount`.



..  method:: NoChangeBetting.win(self, bet: Bet) -> None

    :param bet: The bet which was a winner
    :type bet: Bet


    Since the bet doesn't change, this does nothing.




..  method:: NoChangeBetting.lose(self, bet: Bet) -> None

    :param bet: The bet which was a loser
    :type bet: Bet


    Since the bet doesn't change, this does nothing.



..  method:: NoChangeBetting.__str__(self) -> str


    Returns a string with the name of the class, :obj:`outcome`, and :obj:`betAmount`.


MartingaleBetting Class
------------------------

..  class:: MartingaleBetting

    The :class:`MartingaleBetting` class is a subclass of :class:`BettingStrategy`
    that doubles the bet on each loss, hoping to recover the entire loss on
    a single win.


Fields
~~~~~~~


..  attribute:: MartingaleBetting.lossCount

    The number of losses. This is the number of times to double the pass
    line odds bet.

..  attribute:: MartingaleBetting.betMultiple

    The the bet multiplier, based on the number of losses. This starts
    at 1, and is reset to 1 on each win. It is doubled in each loss.
    This is always :math:`betMultiple = 2^{lossCount}`.


Constructors
~~~~~~~~~~~~~~


..  method:: MartingaleBetting.__init__(self, outcome: Outcome) -> None

    :param outcome: The outcome on which this strategy will create bets
    :type outcome: :class:`Outcome`



    Uses the superclass initializer with the given :class:`Outcome`.
    Sets the initial lossCount and betMultiplier.



Methods
~~~~~~~~


..  method:: MartingaleBetting.createBet(self) -> Bet


    Returns a new :class:`Bet` using the :obj:`outcome` :class:`Outcome`
    and the :obj:`betMultiple`.



..  method:: MartingaleBetting.win(self, bet: Bet) -> None

    :param bet: The bet which was a winner
    :type bet: :class:`Bet`


    Resets :obj:`lossCount` to zero, and resets
    :obj:`betMultiple` to :literal:`1`.




..  method:: MartingaleBetting.lose(self, bet: Bet) -> None

    :param bet: The bet which was a loser
    :type bet: :class:`Bet`


    Increments :obj:`lossCount` by :literal:`1`
    and doubles :obj:`betMultiple`.



..  method:: NoChangeBetting.__str__(self) -> str


    Returns a string with the name of the class, :obj:`outcome`, the current :obj:`betAmount`
    and :obj:`betMultiple`.


Bet1326Betting Class
---------------------

:class:`Bet1326Betting` is a subclass of :class:`BettingStrategy`
that advances the bet amount through a sequence of multipliers on each
win, and resets the sequence on each loss. The hope is to magnify the
gain on a sequence of wins.


Fields
~~~~~~~

..  attribute:: Bet1326Betting.state

    This is the current state of the 1-3-2-6 betting system. It will be
    an instance of one of the four subclasses of :class:`Player1326State`:
    No Wins, One Win, Two Wins or Three Wins.

Constructors
~~~~~~~~~~~~~



..  method:: Bet1326Betting.__init__(self, outcome: Outcome) -> None

    :param outcome: The outcome on which this strategy will create bets
    :type outcome: Outcome


    Initializes this betting strategy with the given :class:`Outcome`.
    Creates an initial instance of :class:`Player1326NoWins` using :obj:`outcome`.


Methods
~~~~~~~~


..  method:: Bet1326Betting.createBet(self) -> Bet


    Returns a new :class:`Bet`
    using the :meth:`currentBet` method from the :obj:`state`
    object.



..  method:: Bet1326Betting.win(self, bet: Bet) -> None

    :param bet: The bet which was a winner
    :type bet: :class:`Bet`


    Determines the
    next state when the bet is a winner. Uses :obj:`state`'s :meth:`nextWon`
    method and saves the new state in :obj:`state`.




..  method:: Bet1326Betting.lose(self, bet: Bet) -> None

    :param bet: The bet which was a loser
    :type bet: :class:`Bet`


    Determines the next state when the bet is
    a loser. Uses :obj:`state`'s :meth:`nextLost`, method
    saving the result in :obj:`myState`.




..  method:: Bet1326Betting.__str__(self) -> str


    Returns a string with the name of the class, :obj:`outcome` and :obj:`state`.


CrapsOneBetPlayer class
-------------------------

..  class:: CrapsOneBetPlayer

    The :class:`CrapsOneBetPlayer` class is a subclass of :class:`CrapsPlayer`
    and places one bet in Craps. The single bet is one of the bets available
    on the come out roll (either Pass Line or Don't Pass Line). This class
    implements the basic procedure for placing the line bet, using an
    instance of :class:`BettingStrategy` to adjust that bet based on
    wins and losses.


Fields
~~~~~~~

..  attribute:: CrapsOneBetPlayer.lineStrategy

    An instance of :class:`BettingStrategy` that applies to the line bet.

    Generally, this is an
    instance of :class:`NoChangeBetting` because we want to make the
    minimum line bet and the maximum odds bet behind the line.

Constructors
~~~~~~~~~~~~~


..  method:: CrapsOneBetPlayer.__init__(self, table: Table, lineStrategy: BettingStrategy) -> None

    Constructs the :class:`CrapsOneBetPlayer` with a specific :class:`Table`
    for placing best. This will save the given :class:`BettingStrategy`
    in :obj:`lineStrategy`.

..  rubric::  Creation of A Player

..  code-block:: python

    passLine = table.dice.get("Pass Line")
    betting = MartingaleBetting(passLine)
    passLineMartin = CrapsOneBetPlayer(betting)

#.  Get the Pass Line :class:`Outcome` instance from the :class:`Dice` object.

#.  Creates a Martingale betting strategy focused on the basic Pass Line outcome.

#.  Creates a one-bet player, who will employ the Martingale betting
    strategy focused on the basic Pass Line outcome.

Methods
~~~~~~~~~~


..  method:: CrapsOneBetPlayer.placeBets(self) -> None


    Updates the :class:`Table`
    with the various :class:`Bet` instances. There is one basic betting rule.

        If there is no line bet, create the line :class:`Bet` instance from the
        :obj:`lineStrategy`.

    Be sure to check the price of the :class:`Bet` before placing
    it. Particularly, Don't Pass Odds bets may have a price that exceeds
    the player's stake. This means that the :class:`Bet` object must
    be constructed, then the price must be tested against the :obj:`stake`
    to see if the player can even afford it. If the :obj:`stake` is
    greater than or equal to the price, subtract the price and place the
    bet. Otherwise, simply ignore it.



..  method:: CrapsOneBetPlayer.win(self, bet: Bet) -> None

    :param bet: The bet which was a winner
    :type bet: :class:`Bet`


    Notification from the :class:`Game`
    that the :class:`Bet` was a winner. The amount of money won is
    available via :obj:`theBet` :meth:`winAmount`. If the bet's
    :class:`Outcome` matches the :obj:`lineStrategy` 's :class:`Outcome`,
    notify the strategy, by calling the :obj:`lineStrategy` 's :meth:`win`
    method.



..  method:: CrapsOneBetPlayer.lose(self, bet: Bet) -> None

    :param bet: The bet which was a loser
    :type bet: :class:`Bet`


    Notification from the :class:`Game`
    that the :class:`Bet` was a loser. If the bet's :class:`Outcome`
    matches the :obj:`lineStrategy` 's :class:`Outcome`, notify
    the strategy, by calling the :obj:`lineStrategy` 's :meth:`lose`
    method.


CrapsTwoBetPlayer class
------------------------

..  class:: CrapsTwoBetPlayer

    The :class:`CrapsTwoBetPlayer` ckass is a subclass of :class:`CrapsOneBetPlayer`
    and places one or two bets in Craps. The base bet is one of the bets
    available on the come out roll (either Pass Line or Don't Pass Line). In
    addition to that, an odds bet (either Pass Line Odds or Don't Pass Odds)
    can also be placed. This class implements the basic procedure for
    placing the line and odds bets, using two instances of :class:`BettingStrategy`
    to adjust the bets based on wins and losses.

    Typically, the line bet uses an instance of :class:`NoChangeBetting`.

    The odds bets, however, are where we want to put more money in play.


Fields
~~~~~~~


..  attribute:: CrapsTwoBetPlayer.oddsStrategy

    An instance of :class:`BettingStrategy` that applies to the line bet.


Constructors
~~~~~~~~~~~~~

..  method:: CrapsTwoBetPlayer.__init__(self, table: Table, lineStrategy: BettingStrategy, oddStragtegy: BettingStrategy) -> None

    Constructs the :class:`CrapsTwoBetPlayer` with a specific :class:`Table`
    for placing bets. This will save the two given :class:`BettingStrategy` instances
    in :obj:`lineStrategy` and :obj:`oddsStrategy`.

    The superclass handles the :obj:`lineStrategy`. This subclass extends that definition
    with the :obj:`oddsStrategy`.

Methods
~~~~~~~~~


..  method:: CrapsTwoBetPlayer.placeBets(self) -> None


    Updates the :class:`Table`
    with the various :class:`Bet` objects. There are two basic betting rules.

    #.  If there is no line bet, create the line :class:`Bet` instance from the
        :obj:`lineStrategy`.

    #.  If there is no odds bet, create the odds :class:`Bet` instance from the
        :obj:`oddsStrategy`.


..  method:: CrapsTwoBetPlayer.win(self, bet: Bet) -> None

    :param bet: The bet which was a winner
    :type bet: Bet


    Notification from the :class:`Game`
    that the :class:`Bet` was a winner. The superclass handles the
    money won and the line bet notification. This subclass adds a
    comparison between the bet's :class:`Outcome` and the :obj:`oddsStrategy` object's
    :class:`Outcome`; if they match, it will notify the
    strategy, by calling the :obj:`oddsStrategy` object's :meth:`win`
    method.



..  method:: CrapsTwoBetPlayer.lose(self, bet: Bet) -> None

    :param bet: The bet which was a loser
    :type bet: Bet


    Notification from the :class:`Game`
    that the :class:`Bet` was a loser. The superclass handles the
    line bet notification. If the bet's :class:`Outcome` matches the :obj:`oddsStrategy` object's
    :class:`Outcome`, notify the strategy, by calling the :obj:`oddsStrategy` object's
    :meth:`lose` method.


CrapsSevenCountPlayer class
----------------------------

..  class:: CrapsSevenCountPlayer

    The :class:`CrapsSevenCountPlayer` class is a subclass of :class:`CrapsTwoBetPlayer`
    and places up to three bets in Craps. The base bet is a Pass Line bet.
    In addition to that, a Pass Line Odds bet can also be placed. If the
    game runs to more than seven throws, then the "7" proposition bet
    (at 4:1) is placed, using the Martingale strategy.


    The Pass Line bet uses an instance of :class:`NoChangeBetting`. The
    Pass Line Odds bet uses an instance of :class:`Bet1326Betting`.


Fields
~~~~~~~

..  attribute:: CrapsSevenCountPlayer.sevenStrategy

    The :class:`BettingStrategy` for the seven bet. Some argue that this should be
    a no-change strategy.  The bet is rare, and -- if effect --
    the player bets against them self with this.  One could also argue that it
    should be a Martingale because each throw after the seventh are less and
    less likely to win.

..  attribute:: CrapsSevenCountPlayer.throwCount

    The number of throws in this game. This is set to zero when we place
    a line bet, and incremented each time we are allowed to place bets.


Constructors
~~~~~~~~~~~~~


..  method:: CrapsSevenCountPlayer.__init__(self, table: Table) -> None


    This will create a :class:`NoChangeBetting` strategy based on
    the Pass Line :class:`Outcome`. It will also create a :class:`MartingaleBetting`
    strategy based on the Pass Line Odds :class:`Outcome`. These
    will be given to the superclass constructor to save the game, the
    line bet and the odds bet. Then this constructor creates a :class:`Bet1326Betting`
    strategy for the Seven Proposition :class:`Outcome`.


Methods
~~~~~~~~


..  method:: CrapsSevenCountPlayer.placeBets(self) -> None


    Updates the :class:`Table`
    with the various :class:`Bet` instances. There are three basic betting rules.

    #.  If there is no line bet, create the line :class:`Bet` from the
        :obj:`lineStrategy`. Set the :obj:`throwCount` to zero.

    #.  If there is no odds bet, create the odds :class:`Bet` from the
        :obj:`oddsStrategy`.

    #.  If the game is over seven throws and there is no seven
        proposition bet, create the proposition :class:`Bet` from the
        :obj:`sevenStrategy`.


    Each opportunity to place bets will also increment the :obj:`throwCount`
    by one.


..  method:: CrapsSevenCountPlayer.win(self, bet: Bet) -> None

    :param bet: The bet which was a winner
    :type bet: :class:`Bet`


    Notification from the :class:`Game`
    that the :class:`Bet` was a winner. The superclass handles the
    money won and the line and odds bet notification.



..  method:: CrapsSevenCountPlayer.lose(self, bet: Bet) -> None

    :param bet: The bet which was a loser
    :type bet: :class:`Bet`


    Notification from the :class:`Game`
    that the :class:`Bet` was a loser. The superclass handles the
    line and odds bet notification.


Roll-Counting Deliverables
--------------------------

There are two groups of deliverables for this exercise. The first batch
of deliverables are the new Betting Strategy class hierarchy and unit
tests. The second batch of deliverables are the two revised Craps Player
classes, the final Roll Counter Player, and the respective unit tests.

Also, note that these new classes make the previous :class:`CrapsSimplePlayer`,
:class:`CrapsMartingale`, :class:`Craps1326` and :class:`CrapsCancellation`
classes obsolete. There are two choices for how to deal with this
change: remove and re-implement. The old classes can be removed, and the
Simulator reworked to use the new versions. The alternative is to
re-implement the original classes as :emphasis:`Facade` over the new classes.

**Betting Strategy class hierarchy**. There are four classes, with
associated unit tests in this group of deliverables.

-   The :class:`BettingStrategy` superclass. This class is abstract;
    there is no unit test.

-   The :class:`NoChangeBetting` class.

-   A unit test for the :class:`NoChangeBetting` class. This will
    simply confirm that the :meth:`win` and :meth:`lose`
    methods do not change the bet amount.

-   The :class:`MartingaleBetting` class.

-   A unit test for the :class:`MartingaleBetting` class. This will
    confirm that the :meth:`win` method resets the bet amount and :meth:`lose`
    method doubles the bet amount.

-   The :class:`Bet1326Betting` class.

-   A unit test for the :class:`Bet1326Betting` class. This will
    confirm that the :meth:`win` method steps through the various
    states, and the :meth:`lose` method resets the state.


**CrapsPlayer class hierarchy**. There are three classes, each with an
associated unit test in this group of deliverables.

-   The :class:`CrapsOneBetPlayer` class.

-   A unit test for the :class:`CrapsOneBetPlayer` class. One test
    can provide a No Change strategy for a Pass Line bet to verify that
    the player correctly places Line bets. Another test can provide a
    Martingale strategy for a Pass Line bet to verify that the player
    correctly changes bets on wins and losses.

-   The :class:`CrapsTwoBetPlayer` class.

-   A unit test for the :class:`CrapsTwoBetPlayer` class. One test
    can provide a No Change strategy for a Pass Line bet and a
    Martingale strategy for a Pass Line Odds bet to verify that the
    player correctly places Line bets and correctly changes bets on wins
    and losses.

-   The :class:`CrapsSevenCountPlayer` class.

-   A unit test for the :class:`CrapsSevenCountPlayer` class. This
    will require a lengthy test procedure to assure that the player
    correctly places a Seven proposition bet when the game is over seven
    throws long.

Looking Forward
---------------

We've build a detailed, and reasonably complete simulation of craps.
We've also refactored the players and the betting strategies to allow
us to compose a player with a variety of complex betting behaviors.
This allows us to evaluate the various strategies to see which one
loses money the slowest.

In the long run, they all lose.

In the next chapter, we'll summarize the various components built so far.
