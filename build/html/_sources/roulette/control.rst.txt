
..  _`roul.control`:

Overall Simulation Control
==========================

We can now use our collection of classes to generate some more usable results. We
can perform a number of simulation runs and evaluate the long-term
prospects for the Martingale betting system. We want to know a few
things about the game:


-   How long can we play with a given budget? In other words, how many
    spins before we've lost our stake. The expected value is 38, based
    on an analysis of the payouts for simple outside ("even money") bets.


-   How much we can realistically hope to win? How large a streak can we
    hope for? How far ahead can we hope to get before we should quit?

In the `Simulation Analysis`_ section, we'll look at general features
of simulation.

We'll look at the resulting statistical data in `Statistical Summary`_.

This will lead us to the details in `Simulator Design`_. We'll note that
the details of the simulator require some changes to the definition
of the :class:`Player` class.

We'll enumerate all of this chapter's deliverables in `Simulation Control Deliverables`_.

Simulation Analysis
----------------------------

A :class:`Simulator` class will be allocated a number of responsibilities:


-   Create the :class:`Wheel`, :class:`Table`, and :class: `Game`
    objects.


-   Simulate a number of sessions of play, saving the maximum
    stake and length of each session.


-   For each session: initialize the :class:`Player` and :class: `Game` objects,
    cycle the game a number of times, collect the size of the :class:`Player` object's
    stake after each cycle.


-   Write a final summary of the results.

We'll look at several topics:

-   `Simulation Terms`_ will formalize some definitions.

-   `Simulation Control`_ will look at the overall simulation process.

-   We'll look at how we create a new player in `Player Initialization`_.

-   The most important thing is gather performance data. We'll look
    at this in `Player Interrogation`_.


Simulation Terms
~~~~~~~~~~~~~~~~

We'll try to stick to the following definitions. This will help structure
our data gathering and analysis.

cycle

    A single cycle of betting and bet
    resolution. This depends on a single random event: a spin of the
    wheel or a throw of the dice. Also known as a round of play.

session

    One or more cycles. The session begins
    with a player having their full stake. A session ends when the play
    elects to leave or can no longer participate. A player may elect to
    leave because of elapsed time (typically 250 cycles), or they have
    won a statistically significant amount. A player can no longer
    participate when their stake is too small to make the minimum bet
    for the table.

game

    Some games have intermediate groupings of
    events between an individual cycles and an entire session. As cards
    are dealt in Blackjack, some additional betting opportunities can appear.
    Similarly, a single game of Craps can involve an indefinite number of
    dice rolls, each of which offers new betting opportunities.

Simulation Control
~~~~~~~~~~~~~~~~~~

The sequence of operations for this game simulator looks like this.


..  rubric:: Controlling the Simulation

1.  **Empty List of Maxima**. Create an empty maxima list. This is the maximum
    stake at the end of each session.

2.  **Empty List of Durations**. Create an empty durations list. This is the
    duration of each session, measured in the number of cycles of play
    before the player withdrew or ran out of money.

3.  **For All Sessions**. For each of simulated sessions:

        **Empty List of Stake Details**. Create an empty list to hold the history
        of stake values for this session. This is raw data that we will
        summarize into two metrics for the session: maximum stake and duration.
        We could also have two simple variables to record the maximum stake and
        count the number of spins for the duration. However, the list allows us
        to gather other statistics, like maximum win or maximum loss.

        **While The Player Is Active**.

            **Play One Cycle**. Play one cycle of the game. See the definition in :ref:`roul.game`.

            **Save Outcomes**. Save the player's current stake in the list of stake
            values for this session. An alternative is to update the maximum to be
            the larger of the current stake and the maximum, and increment the duration.

        **Get Maximum**. Get the maximum stake from the list of stake values. Save
        the maximum stake metric in the maxima list.

        **Get Duration**. Get the length of the list of stake values. Save the
        duration metric in the durations list.  Durations less than the maximum
        mean the strategy went bust.

#.  **Statistical Description of Maxima**. Compute the average and standard
    deviation of the values in the maxima list.

#.  **Statistical Description of Durations**. Compute the average and standard
    deviation of values in the durations list.


Both this overall :class:`Simulator` and the :class: `Game` classes
collaborate with the :class:`Player` class. The :class:`Simulator` object's
collaboration, however, initializes the :class:`Player` object and then
monitors the changes to the :class:`Player` object's stake. We have to
design two interfaces for this collaboration.

-   :class:`Player` instance initialization.

-   :class:`Player` instance interrogation.

We'll look at each of these in separate sections.

Player Initialization
~~~~~~~~~~~~~~~~~~~~~~

The :class:`Simulator` class will initialize a :class:`Player` instance
for 250 cycles of play, assuming about one cycle each minute, and about
four hours of patience. We will also initialize the player with a
generous budget of the table limit, 100 betting units. For a $10 table,
this is $1,000 bankroll.

Currently, the :class:`Player` class is designed to play one session
and stop when their duration is reached or their stake is reduced to
zero. We have two alternatives for reinitializing the :class:`Player` object
at the beginning of each session.

#.  The
    overall simulator control will reset the :obj:`stake` and :obj:`roundsToGo`
    values of a :class:`Player` instance. This is a matter
    of setting variables inside the :class:`Player` object, so there's
    nothing to implement here.

#.  Provide a :strong:`Factory` that allows a client class to create
    new, freshly initialized instances of the :class:`Player` class.

While the first solution is quite simple, there are some advantages to
creating a :class:`PlayerFactory` class. If we create an
**Abstract Factory**, we have a single place that creates all :class:`Player` instances.

Further, when we add new player subclasses, we introduce these new
subclasses by creating a new subclass of the factory. In this case,
however, only the main program creates instances of the :class:`Player` class,
reducing the value of the factory. While design of a **Factory** is a
good exercise, we can scrape by setting attribute values of a :class:`Player`
instance.


Player Interrogation
~~~~~~~~~~~~~~~~~~~~~

The :class:`Simulator` object will interrogate the :class:`Player` object
after each cycle and capture the current stake. An easy way to manage
this detailed data is to create a :class:`list` that contains
the stake at the end of each cycle. The length of this list and the
maximum value in this list are the two metrics the :class:`Simulator`
gathers for each session.

Our list of maxima and durations are created sequentially during the
session and summarized at the end of the session. A :class:`list`
will do everything we need. For a deeper discussion on the alternatives
available in the collections framework, see :ref:`roul.bin.collections`.


Statistical Summary
--------------------

While the :class:`Simulator` class can interrogate the :class:`Player` object
after each cycle to capture the current stake, we don't want the
sequence of values for each cycle. We want a summary of all the
cycles in the session. We can save the length of the sequence as well as
the maximum of the sequence. We can then calculate aggregate performance
parameters for each session.

Our objective is to run several session
simulations to get averages and a standard deviations for duration and
maximum stake. This means that the :class:`Simulator` class needs to
retain these statistical samples. We will defer the detailed design of
the statistical processing, and simply keep the duration and maximum
values in lists for this first round of design.


Simulator Design
-----------------

..  class:: Simulator

    :class:`Simulator` exercises the Roulette simulation with a given :class:`Player`
    placing bets. It reports raw statistics on a number of sessions of play.

Fields
~~~~~~

..  attribute:: Simulator.initDuration

    The duration value to use when initializing a :class:`Player` instance
    for a session.  A default value of 250 is a good choice here.

..  attribute:: Simulator.initStake

    The stake value to use when initializing a :class:`Player` instance for a session.
    This is a count of the number of bets placed; i.e., 100 $10 bets is $1000 stake.
    A default value of 100 is sensible.

..  attribute:: Simulator.samples

    The number of game cycles to simulate. A default value of 50 makes sense.

..  attribute:: Simulator.durations

    A :class:`list` of lengths of time the :class:`Player` object remained in the
    game. Each session of play produces a duration metric, which are
    collected into this list.

..  attribute:: Simulator.maxima

    A :class:`list` of maximum stakes for the :class:`Player` object. Each session
    of play produces a maximum stake metric, which are collected into
    this list.

..  attribute:: Simulator.player

    The :class:`Player` instance; essentially, the betting strategy we are simulating.

..  attribute:: Simulator.game

    The casino game we are simulating.  This is an instance
    of the :class:`Game` class, which
    embodies the various rules, the :class:`Table` object and the :class:`Wheel` instance.

Constructors
~~~~~~~~~~~~


..  method:: Simulator.__init__(self, game: Game, player: Player) -> None

    Saves the :class:`Player` and :class: `Game` instances so we
    can gather statistics on the performance of the player's betting strategy.

    :param game: The game we're simulating.  This includes the :class:`Table` and :class:`Wheel`.
    :type game: :class:`Game`

    :param player: The player.  This encapsulates the betting strategy.
    :type player: :class:`Player`


Methods
~~~~~~~


..  method:: Simulator.session(self) -> List[int]

    :return: :class:`list` of stake values.
    :rtype: list


    Executes a single
    game session. The :class:`Player` instance is initialized with their
    initial stake and initial cycles to go. An empty :class:`list`
    of stake values is created. The session loop executes until the
    :meth:`Player.playing` method returns false. This loop executes the
    :meth:`Game.cycle` method; then it gets the stake from the :class:`Player`
    and appends this amount to the :class:`list` of stake
    values. The :class:`list` of individual stake values is
    returned as the result of the session of play.



..  method:: Simulator.gather(self) -> None


    Executes the number of games
    sessions in :obj:`samples`. Each game session returns a :class:`list`
    of stake values. When the session is over (either the play reached
    their time limit or their stake was spent), then the length of the session
    :class:`;ist` and the maximum value in the session :class:`list`
    are the resulting duration and maximum metrics. These two metrics
    are appended to the :obj:`durations` list and the
    :obj:`maxima` list.

    A client class will either display the durations and maxima raw
    metrics or produce statistical summaries.

Simulation Control Deliverables
--------------------------------

There are five deliverables for this exercise. Each of these classes
needs complete Python docstring comments.


-   Revision to the :class:`Player` class.  Don't forget to update unit tests.

-   The :class:`Simulator` class.

-   The expected outcomes from the non-random wheel can be rather
    complex to predict. Because of this, one of the deliverables is a
    demonstration program that enumerates the actual sequence of
    non-random spins. From this we can derive the sequence of wins and
    losses, and the sequence of :class:`Player` bets. This will
    allow us to predict the final outcome from a single session.

-   A unit test of the :class:`Simulator` class that uses the
    non-random generator to produce the predictable sequence of spins
    and bets.


-   A main application function that creates the necessary objects, runs the
    :class:`Simulator`'s :meth:`gather` method, and writes
    the available outputs to :obj:`sys.stdout`

For this initial demonstration program, it should simply
print the list of maxima, and the list of session lengths. This raw
data can be redirected to a file, loaded into a spreadsheet and analyzed.

Looking Forward
---------------

We can now, comfortably, add subclasses to the :class:`Player` superclass.
We'll start with a player betting on a fallacious notion of a color being
"due". This player waits for seven reds in a row, then bets black.
