
Random Player Class
===================

This section will introduce a simple subclass of the :class:`Player` class who
bets at random.

In `Random Player Analysis`_ we'll look at what this player does.

We'll turn to how the player works in `Random Player Design`_.

In `Random Player Deliverables`_ we'll enumerate the deliverables for
this player.

An important consideration is to compare this player with the player
who always bets black and the player using the Martingale strategy
to always bet black. Who does better? If they're all about the same,
what does that say about the house edge in this game?

Random Player Analysis
----------------------

One possible betting strategy is to bet completely randomly. This serves
as an interesting benchmark for other betting strategies.


We'll write a subclass of the :class:`Player` class to step through all of
the bets available on the :class:`Wheel` instance, selecting one or more of
the available outcomes at random. This :class:`Player` subclass, like
others, will have a fixed initial stake and a limited amount of time to play.


The :class:`Wheel` class can provide an :class:`Iterator` over
the collection of :class:`Bin` instances. We could revise the :class:`Wheel` class
to provide a :meth:`binIterator` method that we can use to return
all of the :class:`Bin` instances. From each :class:`Bin` object, we will need
an iterator we can use to return all of the :class:`Outcome` instances.
This provides the domain of possible bets.

To collect a list of all possible :class:`Outcome` instances, we would use
the following algorithm:


..  rubric:: Locating All Outcomes

1.  **Empty List of Outcomes**. Create an empty set of all :class:`Outcome` instances, :obj:`all_OC`.

2.  **Get Bin Iterator**. Get the Iterator from the :class:`Wheel` object that
    lists all :class:`Bin` instances.

3.  **For each Bin**.

    **Get Outcome Iterator**. Get the Iterator that lists all :class:`Outcome` instances.

    **For each Outcome**.

        **Save Outcome**. Add each :class:`Outcome` object to the
        set of all known outcomes, :obj:`all_OC`.


To create a random bet, we can use the :meth:`random.choice` function
to pick one of the available :class:`Outcome` instances.


Random Player Design
---------------------

..  class:: PlayerRandom

    :class:`PlayerRandom` is a :class:`Player` who places bets in
    Roulette. This player makes random bets around the layout.

Fields
~~~~~~

..  attribute:: PlayerRandom.rng

    A Random Number Generator which will return the next random number.

    When writing unit tests, we will want to patch this with a mock
    object to return a known sequence of bets.

Constructors
~~~~~~~~~~~~


..  method:: PlayerRandom.__init__(table: Table) -> None

    This uses the :meth:`super` construct to invoke the superclass
    constructor using the :class:`Table` class.

    :param table: The :class:`Table` object which will accept the bets.
    :type table: :class:`Table`

    This will create a :class:`random.Random` random number generator.

    It will also use the wheel associated with the table to get
    the set of bins. The set of bins is then used to create
    the pool of outcomes for creating bets.



Methods
~~~~~~~


..  method:: PlayerRandom.placeBets(self) -> None


    Updates the :class:`Table` object with a randomly placed :class:`Bet` instance.


Random Player Deliverables
---------------------------

There are five deliverables from this exercise. The new classes need Python docstrings.

-   Updates to the class :class:`Bin` to return an iterator over available :class:`Outcome` instances.
    Updates to unittests for the class :class:`Bin`, also.

-   Updates to the :class:`Wheel` to return an iterator over available :class:`Bin` instances.
    Updates to the unittests for the class :class:`Wheel`, also.

-   The :class:`PlayerRandom` class.

-   A unit test of the :class:`PlayerRandom` class. This should use
    the NonRandom number generator to iterate through all possible :class:`Outcome` instances.

-   An update to the overall :class:`Simulator` that uses the :class:`PlayerRandom`.

Looking Forward
---------------

It's time to look at the algorithmically more sophisticated betting strategies.
These all involve player state changes based on the wins and losses at the table.
To an extent, the Martingale betting was stateful. These will involve more
states and more complex rules for state transitions. In the next chapter,
we'll implement the "1-3-2-6" betting strategy.
