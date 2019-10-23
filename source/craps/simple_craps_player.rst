
Simple Craps Players
====================

This chapter defines a variety of player strategies. Most of this is
based on strategies already defined in :ref:`roul`, making the
explanations considerably simpler. Rather than cover each individual
design in separate chapters, we'll rely on the experience gained so far,
and cover four variant Craps players in this chapter. We'll mention a
fifth, but leave that as a more advanced exercise.

In `Simple Craps Players Analysis`_ we'll expand on existing definition
of craps players. We'll add a number of betting strategies.
In `Craps 1-3-2-6 Player`_, `Craps Cancellation Player`_, and
`Craps Fibonacci Player`_ we'll look at different betting strategies
and how those can be implemented for a craps player.

In `CrapsPlayer Design`_ we'll look at the general design for these
simple players. We'll look at the superclass in `CrapsSimplePlayer superclass`_.
We'll look at each of the strategies in `Craps Martingale Player`_,
`Player1326 State`_, `Craps1326 Player`_ and `CrapsCancellation Player`_.

In `Simple Craps Players Deliverables`_ we'll detail the deliverables
for this chapter.

Simple Craps Players Analysis
-------------------------------

The :class:`Player` class hierarchy suggests there are a number
of betting strategies for the Pass Line Odds bet. We
use the Martingale strategy for our :class:`CrapsMartingale` player.
We could also use the 1-3-2-6 system, the Cancellation system, or the
Fibonacci system for those odds bets. In each of these cases, we are
applying the betting strategy to one of the two bets the player will use.



An additional design note for this section is the choice of the two
basic bets: the Pass Line and the Pass Line Odds bet. It is interesting
to compare the results of these bets with the results of the Don't Pass
Line and the Don't Pass Odds Bet. In particular, the Don't Pass Odds
Bets involve betting large sums of money for small returns; this will be
compounded by any of these betting systems which accelerate the amount
of the bet to cover losses. This change should be a simple matter of
changing the two base bets used by all these variant players.


All of these players have a base bet (either Pass Line or Don't Pass)
and an odds bet (either Pass Line Odds or Don't Pass Odds). If we create
a superclass, called :class:`SimpleCraps`, we can assure that all
these simple betting variations will work for Pass Line as well as Don't
Pass Line bets. The responsibility of this superclass is to define a
consistent set of fields and constructor for all of the subclasses.


Craps 1-3-2-6 Player
~~~~~~~~~~~~~~~~~~~~~

This player uses the 1-3-2-6 system for managing their
odds bet. From the Roulette 1-3-2-6 player (see :ref:`roul.player1326.ov`) we can
see that this player will need to use the :class:`Player1326State`
class hierarchy. The craps player will use one of these objects track
the state changes of their odds. The base bet will not change.


However, the current definitions of the :class:`Player1326State`
class hierarchy specifically reference :class:`Roulette1326`.
Presenting us with an interesting design problem. How do we repair our
design so that :class:`Player1326State` can work with :class:`Roulette1326`
and :class:`Craps1326`?

The only dependency is the field :obj:`outcome`,
which both :class:`Roulette1326` and :class:`Craps1326` must
provide to :class:`Player1326State` objects.

**Problem**. Where do store the :class:`Outcome` object
used by both the player and the state?

**Forces**.
We have some common choices:

-   **Create a Mixin Class**.
    We extract the field and make it part of an mixin class that is required by :class:`Player` subclasses
    that use the 1-3-2-6 strategy.

-   **Create a Common Superclass**.
    In this case, we refactor the field up to the superclass.

-   **Delegate to The State Object**.
    This changes the defintion of :class:`Player1326State`
    to make it more self-contained.

**Mixin Class**.

    The relationship between a subclass of the :class:`Player` class
    and the :class:`Player1326State` class can be formalized through an
    mixin class definition. We can define a  :class:`Bet1326_Able` class,
    which contains the :class:`Outcome` attribute and use this for the
    :class:`Roulette1326` and :class:`Craps1326` classes.

    ..  code-block:: python

        class Bet1326_Able:
            def __init__(self) -> None:
                self.outcome = None

        class CrapsPlayer(Bet1326_Able, Player):
            def __init__(self) -> None:
                super().__init__()

    In this case, this appears to be an example of the **Very
    Large Hammer** design pattern. We're using a very large hammer
    to pound a very small nail. The problem seems too small for this
    complex-looknig language feature.

**Common Superclass**.

    We can refactor the single instance variable up to the superclass.
    This is a relatively minor change. However, it places a
    feature in a superclass which all but a few subclasses must
    ignore. This is another example of **Swiss Army Knife**
    design, where we will be subtracting or trying to ignore a feature from a superclass.

**Delegate to the State Class**.

    If we change the :class:`Player1326State` class to
    keep its own copy of the desired :class:`Outcome` instance we cleanly
    remove any dependence on :class:`Player` class. The :class:`Player` class
    is still responsible for keeping track of the :class:`Outcome` instances,
    and has subcontracted or delegated this responsibility to an
    instance of the :class:`Player1326State` class

    The down side of this is
    that we must provide this :class:`Outcome` instance to each state
    constructor as the state changes.

**Solution**. The solution we embrace is changing the definition of the :class:`Player1326State` class
to include the :class:`Outcome` instance. This delegates responsibility to
the state, where it seems to belong. This will change all of the
constructors, and all of the state change methods, but will cleanly
separate the :class:`Player1326State` class hierarchy from the :class:`Player`
class hierarchy.

..  sidebar:: Python Duck-Typing

    In Python, the relationship between a :class:`Player1326State` object
    and the :class:`Craps1326` class is completely casual.  We don't have to
    sweat the details of where -- precisely -- the :class:`Outcome` object
    is kept.

    Python's flexibility is called "duck typing":

        "if it walks like a duck and quacks like a duck, it *is* a duck."

    In this case, **any** class with an :obj:`outcome` attribute is a
    candidate owner for a :class:`Player1326State` object.

Craps Cancellation Player
~~~~~~~~~~~~~~~~~~~~~~~~~

When we examine the Roulette Cancellation :ref:`roul.cancellation.ov` player
we see that this player will need to use a list of individual betting
amounts. Each win for an odds bet will cancel from this list, and each
loss of an odds bet will append to this list.

As with the Craps Martingale player, we will be managing a base Pass
Line bet, as well as an odds bet that uses the Cancellation strategy.
The Cancellation algorithm can be easily transplanted from the original
Roulette version to this new Craps version.

Craps Fibonacci Player
~~~~~~~~~~~~~~~~~~~~~~

We can examine the Roulette Fibonacci :ref:`roul.fib.ov`
and see that this player will need to compute new betting amounts based
on wins and losses. THis will parallel the way the cancellation player
works.

We'll can have a Fibanacci series for some bets (like pass line bets)
but a flat bet for the behind the line odds bet.


CrapsPlayer Design
-------------------

We'll extend the :class:`CrapsPlayer` class to create a :class:`CrapsSimplePlayer` class
to place both Pass Line and Pass Line Odds bets, as well as Don't
Pass Line and Don't Pass Odds bets. This will allow us to drop the :class:`CrapsPlayerPass`
class, and revise the existing :class:`CrapsMartingale` class.

We have to rework the original Roulette-focused :class:`Player1326State` class
hierarchy, and the :class:`Roulette1326` class to use the new
version of the state objects.

Once this rework is complete, we can add the :class:`Craps1326` and :class:`CrapsCancellation`
player subclasses.

For additional exposure, the more advanced student can rework the
Roulette Fibonacci player to create a :class:`CrapsFibonacci` player.



CrapsSimplePlayer superclass
------------------------------

..  class:: CrapsSimplePlayer

    The :class:`CrapsSimplePlayer` is a subclass of :class:`CrapsPlayer` class
    and places two bets in Craps. The simple player has a base bet and an
    odds bet. The base bet is one of the bets available on the come out roll
    (either Pass Line or Don't Pass Line), the odds bet is the corresponding
    odds bet (Pass Line Odds or Don't Pass Odds). This class implements the
    basic procedure for placing the line bet and the behind the line odds
    bet. However, the exact amount of the behind the line odds bet is left
    as an abstract method. This allows subclasses to use any of a variety of
    betting strategies, including Martingale, 1-3-2-6, Cancellation and Fibonacci.


Fields
~~~~~~~

..  attribute:: CrapsSimplePlayer.lineOutcome

    :class:`Outcome` for either Pass Line or Don't Pass Line.
    A right bettor will use a Pass Line bet; a wrong bettor
    will use the Don't Pass Line.


..  attribute:: CrapsSimplePlayer.oddsOutcome

    :class:`Outcome` for the matching odds bet.  This
    is either the Pass Line Odds or Don't Pass Line Odds bet.

    A right bettor will use a Pass Line Odds bet; a wrong bettor
    will use the Don't Pass Line Odds.

Constructors
~~~~~~~~~~~~~~


..  method:: CrapsSimplePlayer.__init__(self, table: Table, line: Outcome, odds: Outcome) -> None

    :param table: The table on which bets are palced
    :type table: :class:`CrapsTable`

    :param line: The line bet outcome
    :type line: :class:`Outcome`

    :param odds: The odds bet outcome
    :type odds: :class:`Outcome`


    Constructs the :class:`CrapsSimplePlayer` instance with a specific :class:`Table` object
    for placing :class:`Bet` instances. Additionally a line bet (Pass Line
    or Don't Pass Line) and odds bet (Pass Line Odds or Don't Pass Odds)
    are provided to this constructor. This allows us to make either Pass
    Line or Don't Pass Line players.


Methods
~~~~~~~~~


..  method:: CrapsSimplePlayer.placeBets(self) -> None



    Updates the :class:`Table` instance
    with the various :class:`Bet` instances. There are two basic betting rules.

    #.  If there is no line bet, create the line :class:`Bet` instance from the
        :obj:`line` :class:`Outcome` object.

    #.  If there is no odds bet, create the behind the line odds :class:`Bet` instance
        from the :obj:`odds` :class:`Outcome` object.

    It's essentual to check the price of the :class:`Bet` instance before placing
    it. Particularly, Don't Pass Odds bets may have a price that exceeds
    the player's stake. This means that the :class:`Bet` object must
    be constructed, then the price tested against the :obj:`stake`
    to see if the player can even afford it. If the :obj:`stake` is
    greater than or equal to the price, subtract the price and place the
    bet. Otherwise, simply ignore it the unafforable :class:`Bet` object.


Craps Martingale Player
------------------------

..  class:: CrapsMartingale


    :class:`CrapsMartingale` is a subclass of :class:`CrapsSimplePlayer`
    who places bets in Craps. This player doubles their Pass Line Odds bet
    on every loss and resets their Pass Line Odds bet to a base amount on
    each win.


Fields
~~~~~~~~~

..  attribute:: CrapsMartingale.lossCount

    The number of losses. This is the number of times to double the pass
    line odds bet.

..  attribute:: CrapsMartingale.betMultiple

    The the bet multiplier, based on the number of losses. This starts
    at 1, and is reset to 1 on each win. It is doubled in each loss.
    This is always :math:`betMultiple = 2^{lossCount}`.


Methods
~~~~~~~~~~


..  method:: CrapsMartingale.placeBets(self) -> None


    Extension to the superclass :meth:`placeBets` method.  This
    version sets the amount based on the value of :attr:`CrapsMartingale.betMultiple`.


..  method:: CrapsMartingale.win(self, bet: Bet) -> None

    :param bet: The bet that was a winner
    :type bet: :class:`Bet`


    Uses the superclass :meth:`win`
    method to update the stake with an amount won. This method then resets
    :obj:`lossCount` to zero, and resets :obj:`betMultiple` to :literal:`1`.




..  method:: CrapsMartingale.lose(self, bet: Bet) -> None

    :param bet: The bet that was a loser
    :type bet: :class:`Bet`


    Increments :obj:`lossCount` by :literal:`1`
    and doubles :obj:`betMultiple`.


Player1326 State
------------------

:class:`Player1326State` is the superclass for all of the states in
the 1-3-2-6 betting system.

Fields
~~~~~~~~~~

..  attribute:: Player1326State.outcome

    The :class:`Outcome` instance on which a :class:`Player`  will bet.

Constructors
~~~~~~~~~~~~~



..  method:: Player1326State.__init__(self, outcome: Outcome) -> None

    :param outcome: The outcome on which to bet
    :type outcome: Outcome


    The constructor for this class saves :class:`Outcome` instance on which a
    :class:`Player`  will bet.


Methods
~~~~~~~~~

Much of the original design for this state hierarchy should remain in place.
See :ref:`roul.player1326` for more information on the original design.



..  method:: Player1326State.nextLost(self) -> Player1326State


    Constructs the new :class:`Player1326State` instance to be used
    when the bet was a loser. This method is the same for each subclass:
    it creates a new instance of :class:`Player1326NoWins` class.

    This method is defined in the superclass to assure that
    it is available for each subclass. This will use the :obj:`outcome`
    to be sure the new state has the :class:`Outcome` object on which the owning
    Player will be  betting.


Craps1326 Player
----------------

..  class:: Craps1326

    :class:`Craps1326` is a subclass of :class:`CrapsSimplePlayer` class
    who places bets in Craps. This player changes their Pass Line Odds bet
    on every loss and resets their Pass Line Odds bet to a base amount on
    each win. The sequence of bet multipliers is given by the current :class:`Player1326State`
    object.


Fields
~~~~~~~~

..  attribute:: Player1326State.state

    This is the current state of the 1-3-2-6 betting system. It will be
    an instance of one of the four states: No Wins, One Win, Two Wins or
    Three Wins.


Constructors
~~~~~~~~~~~~~~~



..  method:: Player1326.__init__(self, table: CrapsTable, line: Outcome, odds: Outcome) -> None

    :param table: The table on which bets are palced
    :type table: :class:`CrapsTable`

    :param line: The line bet outcome
    :type line: :class:`Outcome`

    :param odds: The odds bet outcome
    :type odds: :class:`Outcome`


    Uses the superclass to initialize the :class:`Craps1326` instance with a specific
    :class:`Table` object for placing :class:`Bet` instances, and set the line
    bet (Pass Line or Don't Pass Line) and odds bet (Pass Line Odds or
    Don't Pass Odds).

    Then the initial state is an instance of the  :class:`Player1326NoWins` class, constructed using the odds bet.

Methods
~~~~~~~~


..  method:: Player1326.placeBets(self) -> None


    Updates the :class:`Table` instance
    with a bet created by the current state. This method delegates the
    bet creation to :obj:`state` object's :meth:`currentBet` method.


..  method:: Player1326.win(self, bet: Bet) -> None

    :param bet: The bet that was a winner
    :type bet: :class:`Bet`


    Uses the superclass method to update the
    stake with an amount won. Uses the current state to determine what
    the next state will be by calling :obj:`state`\ 's objects :meth:`nextWon`
    method and saving the new state in :obj:`state`


..  method:: Player1326.lose(self, bet: Bet) -> None

    :param bet: The bet that was a loser
    :type bet: :class:`Bet`


    Uses the current state to determine what the
    next state will be. This method delegates the next state decision to :obj:`state`
    object's :meth:`nextLost` method, saving the result in :obj:`state`.


CrapsCancellation Player
-------------------------

..  class:: CrapsCancellation

    :class:`CrapsCancellation` is a subclass of :class:`CrapsSimplePlayer`
    who places bets in Craps. This player changes their Pass Line Odds bet
    on every win and loss using a budget to which losses are appended and
    winings are cancelled.


Fields
~~~~~~~

..  attribute:: CrapsCancellation.sequence

    This :class:`list` keeps the bet amounts; wins are removed
    from this list and losses are appended to this list. THe current bet
    is the first value plus the last value.


Constructors
~~~~~~~~~~~~~~


..  method:: CrapsCancellation.__init__(self, table: CrapsTable, line: Outcome, odds: Outcome) -> None

    :param table: The table on which bets are palced
    :type table: :class:`CrapsTable`

    :param line: The line bet outcome
    :type line: :class:`Outcome`

    :param odds: The odds bet outcome
    :type odds: :class:`Outcome`



    Invokes the superclass constructor to initialize this instance of :class:`CrapsCancellation`.
    Then calls :meth:`resetSequence` to create the betting budget.


Methods
~~~~~~~

There are few real changes to the original implementation of CancellationPlayer.

See :ref:`roul.cancellation` for more information.


..  method:: CrapsCancellation.placeBets(self) -> None


    Creates a bet from the
    sum of the first and last values of :obj:`sequence` and the preferred
    outcome.

    This uses the essential line bet and odds bet algorithm defined above.
    If no line bet, this is created.

    If there's a line bet and no odds bet, then the odds bet is created.

    If both bets are created, there is no more betting to do.


Simple Craps Players Deliverables
----------------------------------

There are eight deliverables for this exercise.

-   The :class:`CrapsSimplePlayer` abstract superclass. Since this
    class doesn't have a body for the :meth:`oddsBet` method, it
    can't be unit tested directly.

-   A revised :class:`CrapsMartingale` class, that is a proper
    subclass of :class:`CrapsSimplePlayer`. The existing unit test for
    :class:`CrapsMartingale` should continue to work correctly after
    these changes.

-   A revised :class:`Player1326State` class hierarchy. Each
    subclass will use the :obj:`outcome` field instead of getting
    this information from a :class:`Player1326` instance. The unit
    tests will have to be revised slightly to reflect the changed
    constructors for this class.

-   A revised :class:`Roulette1326` class, which reflects the
    changed constructors for this :class:`Player1326State`. The
    unit tests should indicate that this change has no adverse effect.

-   The :class:`Craps1326` subclass of :class:`CrapsSimplePlayer`.
    This will use the revised :class:`Player1326State`.

-   A unit test class for :class:`Craps1326`. This test should
    synthesize a fixed list of :class:`Outcome` instances, :class:`Throw` instances,
    and calls a :class:`Craps1326` instance with various
    sequences of craps, naturals and points to assure that the bet
    changes appropriately.

-   The :class:`CrapsCancellation` subclass of :class:`CrapsSimplePlayer`.

-   A unit test class for :class:`CrapsCancellation`. This test
    should synthesize a fixed list of :class:`Outcome` instances, :class:`Throw` instances,
    and calls a :class:`CrapsCancellation` instance with various
    sequences of craps, naturals and points to assure that the bet
    changes appropriately.

Looking Forward
---------------

This is a large  number of alternative playing strategies. It's important to see how the
betting schemes are their own class hierarchy, separate from the overall players.

In the next chapter we'll at some more stateful player alterives. In this case,
a player that counts rolls and adds "hedge bets" to guard against losses.
