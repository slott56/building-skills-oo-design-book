
..  _`roul.sevenreds`:

SevenReds Player Class
======================

This section introduces an additional specialization of the Martingale betting
strategy. Adding this new
subclass should be a small change to the main application class.
Additionally, we'll also address some issues in how an overall
application is composed of individual class instances.


We'll also revisit a question in the design of the :class:`Table` class.
Should we really be checking for a minimum? Or was that needless?

In `SevenReds Player Analysis`_ we'll examine the general strategy
this player will follow.

We'll revisit object-oriented design by composition in `Soapbox on Composition`_.

In `SevenReds Design`_ we'll look at the design of this player. We'll
need to revise the overall design for the abstract :class:`Player` class, also,
which we'll look at in `Player Rework`_.

These design changes will lead to other changes. We'll look at these
changes in `Game Rework`_ and `Table Rework`_.

This will lead to `SevenReds Player Deliverables`_, which enumerates all
of the deliverables for this chapter.

SevenReds Player Analysis
---------------------------

The :class:`SevenReds` player subclass waits for seven red wins in a row before betting
black. This is a subclass of the :class:`Player` class. We can create a
subclass of our main :class:`Simulator` class to use this new :class:`SevenReds`
instance.


We note that the :class:`Passenger57` class betting
is stateless: this class places the same bets over and over until they are
cleaned out or their playing session ends.

The :class:`Martingale` player's betting, however, is stateful.  This player changes the
bet based on wins and losses.  The state is a loss counter than resets
to zero on each win, and increments on each loss.

Our :class:`SevenReds`  player will have two states: waiting and betting. In the waiting state, they
are simply counting the number of reds. In the betting state, they have
seen seven reds and are now playing the Martingale system on black. We
will defer serious analysis of this stateful betting until
some of the more sophisticated subclasses of the :class:`Player` class. For
now, we will simply use an integer to count the number of reds.

Game Changer
~~~~~~~~~~~~~

Currently, the :class:`Player` object is not informed of the final outcome unless they
place a bet. We designed the :class: `Game` object to evaluate the :class:`Bet`
instances and notify the :class:`Player` object of just their :class:`Bet` instances
that were wins or losses. We will need to add a method to the :class:`Player` class
to be given the overall list of winning :class:`Outcome` instances even when the
:class:`Player` object has not placed a bet.


Once we have updated the design of :class: `Game` class to notify the :class:`Player` object,
we can add the feature to the new :class:`SevenReds` class. Note that we intend
introduce each new betting strategy via creation of new subclasses. A
relatively straightforward update to our simulation main program allows
us to use these new subclasses. The previously working subclasses are
left in place, allowing graceful evolution by adding features with
minimal rework of existing classes.


In addition to waiting for the wheel to spin seven reds, we will also
follow the Martingale betting system to track our wins and losses,
assuring that a single win will recoup all of our losses. This makes the :class:`SevenReds` class
a further specialization of the :class:`Martingale` class. We will be using
the basic features of the :class:`Martingale` class, but doing additional
processing to determine if we should place a bet or not.

Introducing a new subclass should be done by upgrading the main program. See
:ref:`Soapbox on Composition <soapbox.composition>` for comments on the ideal structure for a
main program. Additionally, see the :ref:`roul.ov.qanda.main` FAQ entry.

Table Changes
~~~~~~~~~~~~~

When we designed the :class:`Table` class, we included a notion of a valid betting state.
We required the sum of all bets placed by a :class:`Player` to be below
some limit. We also required that there be a table minimum present.

A casino has a table minimum for a variety of reasons. Most notably, it
serves to distinguish casual players at low-stakes tables from "high rollers"
who might prefer to play with other people who wager larger amounts.

In the rare event that a player is the only person at a roulette wheel,
the croupier won't spin the wheel until a bet is placed. This is an odd
thing. It's also very rare. Pragmatically, there are almost always other
players, and the wheel is likely to be spun even if a given player is not betting.

Our design for a table really should **not** have any check for a minimum
bet. It's a rule that doesn't make sense for the kind of simulation we're doing.
The simulated results can be scaled by the minimum betting amount, so it's
easiest to think of the bets as multiples of the minimum and use simple integer
bet amounts.


..  _`soapbox.composition`:

Soapbox on Composition
-----------------------

Generally, a solution is composed of a number of objects.
However, the consequences of this can be misunderstood. Since
the solution is a composition of objects, it falls on the main
method to do create the composition and do nothing more.


Our ideal main program creates and composes the working set of
objects, then start the processing.
In some cases, environment variables, command-line arguments and options,
and configuration files may tailor what is built.
For these simple exercises, however, we're omitting the parsing of
command-line parameters, and simply creating the necessary
objects directly.

A main program should, therefore, look something like the following:

..  code-block:: python

    wheel = Wheel()
    table = Table()
    game = Game(wheel, table)
    player = SevenReds(table)
    sim = Simulator(game, player)
    sim.gather()

We created an instance of the :class:`Wheel` class to contain the bins and outcomes.
We created an instance of the :class:`Table` class as a place to put the bets.
We've combined these two objects into an instance of the :class: `Game` object.

When we created the :obj:`player` object, we could have used the :class:`Martingale` class
or the :class:`Passenger57` class.
The player object can use the :class:`Table`  object to get the :class:`Wheel` instance. This
:class:`Wheel` instance provides the outcomes used to build bets.

The real work is done by :meth:`Simulater.gather`. This relies on the game, table,
and player to create the data we can analyze.

In some instances, the construction of objects is not done
directly by the main method. Instead, the main method will
use **Builders** to create the various objects. The idea is
to avoid mentioning the class definitions directly. We can
upgrade or replace a class, and also upgrade the **Builder**
to use that class appropriately. This isolates change to
the class hierarchy and a builder function.

SevenReds Design
-----------------

..  class:: SevenReds

    :class:`SevenReds` is a :class:`Martingale` player who places
    bets in Roulette. This player waits until the wheel has spun red seven
    times in a row before betting black.


Fields
~~~~~~

..  attribute:: SevenReds.redCount

    The number of reds yet to go. This starts at :literal:`7` , is reset to
    :literal:`7` on each non-red outcome, and decrements by :literal:`1`
    on each red outcome.

Note that this class inherits :obj:`betMultiple`. This is initially :literal:`1`,
doubles with each loss and is reset to one on each win.

Methods
~~~~~~~


..  method:: SevenReds.placeBets(self) -> None


    If :obj:`redCount`
    is zero, this places a bet on black, using the bet multiplier.


..  method:: SevenReds.winners(self, outcomes: Set[Outcome]) -> None

    :param outcomes: The :class:`Outcome` set from a :class:`Bin`.
    :type outcomes: Set of :class:`Outcome` instances


    This is notification from the :class: `Game`
    of all the winning outcomes. If this vector includes red, :obj:`redCount`
    is decremented. Otherwise, :obj:`redCount` is reset to :literal:`7`.



Player Rework
--------------

We'll need to revise the :class:`Player` class to add the following method.
The superclass version doesn't do anything with this information.
Some subclasses, however, will process this.


..  method:: Player.winners(self, outcomes: Set[Outcome]) -> None

    :param outcomes: The set of :class:`Outcome` instances that are part of the
        current win.
    :type outcomes: Set of :class:`Outcome` instances


    The game will notify a player of each spin using this method.
    This will be invoked even if the player places no bets.



Game Rework
--------------------

We'll need to revise the :class: `Game` class to extend the cycle method.
This method must provide the winning bin's :class:`Outcome` set.

Table Rework
------------

We'll need to revise the :class:`Table` class to remove any minimum
bet rule. If there are no bets, the game should still proceed.


SevenReds Player Deliverables
------------------------------

There are six deliverables from this exercise. The new classes will
require complete Python docstrings.

-   A revision to the :class:`Player` class to add the :meth:`Player.winners`  method.
    The superclass version doesn't do anything with this information.
    Some subclasses, however, will process this.

-   A revision to the :class:`Player` unit tests.

-   A revision to the :class: `Game` class. This will call the :meth:`winners`
    with the winning :class:`Bin` instance before paying off the bets.

-   A revision to the :class:`Table` class. This will allow
    a table with zero bets to be considered valid for the purposes
    of letting the game continue.

-   The :class:`SevenReds` subclass of :class:`Player` class.

-   A unit test of the :class:`SevenReds` class. This test should
    synthesize a fixed list of :class:`Outcome` instances, :class:`Bin` instances
    and the call a :class:`SevenReds` instance with various
    sequences of reds and blacks. One test cases can assure that no bet
    is placed until 7 reds have been seen. Another test case can assure
    that the bets double (following the Martingale betting strategy) on
    each loss.

-   A main application function that creates the necessary objects, runs the
    :class:`Simulator`'s :meth:`gather` method, and writes
    the available outputs to :obj:`sys.stdout`

For this initial demonstration program, it should simply
print the list of maxima, and the list of session lengths. This raw
data can be redirected to a file, loaded into a spreadsheet and analyzed.

Looking Forward
---------------

We now have a few players to compare. It's time to look at some basic statistics
to compare the performance of the various betting strategies. In the next
section we'll look at some simple statistical processing techniques.
