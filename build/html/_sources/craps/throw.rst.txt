
..  _`craps.throw`:

Throw Class
===========

In Craps, a throw of the dice may change the state of the game. This
close relationship between the :class:`Throw` class and :class:`CrapsGame` class
leads us to design the :class:`Throw` class
in detail, along with a rough stub for the :class:`CrapsGame` class.

We'll try to keep the :class:`Throw` class as a parallel with
the :class:`Bin` class in Roulette. It will hold a bunch of
individual :class:`Outcome` instances.

We'll look at the nature of a :class:`Throw` in `Throw Analysis`_.

This will lead us to look -- again -- at `The Wrap vs. Extend Question`_.
This is an important question related to how we'll use a collection class.

In `Throw Design`_ we'll look at the top-level superclass. There are
a number of subclasses:

-   `Natural Throw Design`_,

-   `Craps Throw Design`_,

-   `Eleven Throw Design`_, and

-   `Point Throw Design`_.

Once we have the throw defined, we can examine the outline of the
game in `Craps Game Design`_. This will show how game and throw collaborate.
In `Throw Deliverables`_ we'll enumerate the deliverables for this chapter.

..  _`craps.throw.ov`:

Throw Analysis
--------------

The pair of dice can throw a total of 36 unique combinations. These are
summarized into fifteen distinct outcomes: the eleven numbers from 2 to
12, plus the four hardways variations for 4, 6, 8 and 10.


In Roulette, the randomized positions on the wheel were called :class:`Bin` instances
and each one had a collection of winning :class:`Outcome` instances.
The :class:`Outcome` objects were matched against the :class:`Bet` objects
created by the player.

In Craps, however, the throws of the dice serve three distinct purposes:

-   They resolve any of the one-roll proposition bets.

-   They may also resolve any hardways bets.

-   They may also change the game state. This may also resolve the game
    bets.

We'll look at each of these responsibilities individually.

**One-Throw Propositions**. Each :class:`Throw` object can include a
collection of proposition :class:`Outcome` instances. These are immediate
winners. This collection will be some combination of 2, 3, 7, 11, 12,
Field, Any Craps, or Horn. For completeness, we note that each throw
could also contain one of the 21 hop-bet :class:`Outcome` instances;
however, we'll ignore the hop bets.


**Multi-Throw Propositions**. A :class:`Throw` object may resolve
hardways bets (as well as place bets and buy bets). There are three
possible conditions for a given throw:

-   Some hardways bets may be winners because the number was two equal dice.

-   Some bets may be losers because the number was two non-equal dice or a seven.

-   Some bets may remain unresolved because the dice were neither the target
    number, nor a seven.

This tells us that a :class:`Throw` object may be more than a simple collection of winning
:class:`Outcome` instances.

It seems sensible for a :class:`Throw` object must also contain a list of losing
:class:`Outcome` instances. For example, any of the two easy 8 rolls (6-2 or
5-3) would contain winning :class:`Outcome` instances for the place-8 bet
and buy-8 bet, as well as a losing :class:`Outcome` instances for a hardways-8
bet. The hard 8 roll (4-4), however, would contain winning :class:`Outcome` instances
for the place-8 bet, buy-8 bet, and hardways-8 bet


**Game State Change**. Most importantly, a :class:`Throw` object
can lead to a state change of the game. If the game ends, this will resolve
game-level bets. From the :ref:`craps.details.game.rules`, we see that
the state changes depend on both the :class:`CrapsGame` object's state.
The rules identify the following species of :class:`Throw` instance:

-   **Craps**. These are throws of 2, 3 or 12.
    In the come-out roll state, this is an immediate loss.
    In any other state, this is ignored.
    There are 4 of these throws.

-   **Natural**. This is a throw of 7.
    In the come-out roll state, this is an immediate win.
    In any other state, this is an immediate loss and a change of state back to the start of a game.
    There are 6 of these throws.

-   **Eleven**. This is a throw of 11.
    In the come-out roll state, this is an immediate win.
    In any other state, this is ignored.
    There are 2 of these throws.

-   **Point**. This is a throw of 4, 5, 6, 8, 9, or 10.
    In the come-out roll state, this establishes the point, and changes the game state.
    In any other state, this is is compared against the established point:
    if it matches, this is a win and a change of game state.
    Otherwise, no game state change occurs.
    There are a total of 24 of these throws.



The state change can be implemented by defining methods in :class:`CrapsGame` class
that match the varieties of :class:`Throw`. We can imagine that the
design for the :class:`CrapsGame` class will have four methods: :meth:`craps`,
:meth:`natural`, :meth:`eleven`, and :meth:`point`.
Each kind of :class:`Throw` subclass will call the matching method of
the :class:`CrapsGame` class, leading to possible state changes, and possible game bet resolution.


The game state changes lead us to design a hierarchy of :class:`Throw`
subclasses. We can then initialize a :class:`Dice` object with 36 :class:`Throw`
objects, each of the appropriate subclass. When all of the subclasses
have an identical interface, this embodies the principle of
polymorphism. For additional information, see :ref:`soapbox.polymorphism`.


In looking around, we have a potential naming problem: both a wheel's :class:`Bin`
and the dice's :class:`Throw` are somehow instances of a common
abstraction. Looking forward, we may wind up wrestling with a deck of
cards trying to invent a common nomenclature for all of these
randomizers. All three create random events, and this leads us to a possible
superclass for the :class:`Bin` class and :class:`Throw` class: a :class:`RandomEvent` class.

Currently, we can't identify any features that we can refactor up into
the superclass. Rather than over-engineer this, we'll hold off on
complicating the design until we find something else that is common
between our sources of random events.

The Wrap vs. Extend Question
----------------------------

Note that an instance of the :class:`Throw` class is effectively a container for
a set of :class:`Outcome` instances. We have the standard
**Wrap vs. Extend** question that we need to answer here.

-   **Wrap**. Each :class:`Throw` class can have an internal frozenset of
    :class:`Outcome` objects.

-   **Extend**. We base the :class:`Throw` class on the :class:`frozenset` class  directly
    and add methods to add features.

We have a fairly large number of methods that are introduced in this design.

When we look back at Roulette, a :class:`Bin` object had no impact on the state
of the game. In Craps, though, there's a need for each :class:`Throw` object
to update the current state of the game.

Both options seem sensible.
Lacking further information, we'll focus on using a **Wraps** approach,
and define the :class:`Throw` class
so it has a :class:`frozenset` object as an attribute.


Throw Design
------------

..  class:: Throw

    The :class:`Throw` class is the superclass for the various throws of the dice.
    Each subclass is a different grouping of the numbers, based on the rules
    for Craps.

Fields
~~~~~~

..  attribute:: Throw.outcomes

    A :class:`Set` of one-roll :class:`Outcomes` that win with this throw.

    We'll include the two numbers showing on the dice because it makes it easy to produce helpful
    debugging output. In the long run, the numbers don't really matter as much
    as the state changes.

..  attribute:: Throw.d1
    :noindex:

    One of the two die values, from 1 to 6.

..  attribute:: Throw.d2
    :noindex:

    The other of the two die values, from 1 to 6.


Constructors
~~~~~~~~~~~~


..  method:: Throw.__init__(self, d1: int, d2: int, *outcomes: Outcome) -> None
    :noindex:

    Creates this throw, and associates the given :class:`Set` of :class:`Outcome` instances
    that are winning propositions.

    :param d1: The value of one die
    :param d2: The value of the other die
    :param outcomes: The various :class:`Outcome` objects for this throw.
        These are bets immediately resolved as winners.


Methods
~~~~~~~~~


..  method:: Throw.hard(self) -> bool
    :noindex:


    Returns :literal:`True`
    if :obj:`d1` is equal to :obj:`d2`. This helps determine if
    hardways bets have been won or lost.


..  method:: Throw.updateGame(self, game: CrapsGame) -> None
    :noindex:

    :param game: the :class:`CrapsGame` object to be updated based on this throw.
    :type game: :class:`CrapsGame`

    This method calls one of the
    :class:`CrapsGame` state change methods: :meth:`craps`, :meth:`natural`,
    :meth:`eleven`, :meth:`point`. This may change the
    game state and resolve bets.


..  method:: Throw.__str__(self) -> str
    :noindex:


    An easy-to-read string output method is also very handy.
    A form that looks like :literal:`1,2` works nicely.


Natural Throw Design
----------------------

..  class:: NaturalThrow

    :class:`Natural Throw` is a subclass of :class:`Throw` for the
        "natural" number, 7.

Constructors
~~~~~~~~~~~~~


..  method:: NaturalThrow.__init__(self, d1: int, d2: int) -> None

    :param d1: The value of one die
    :param d2: The value of the other die


    Creates this :class:`Throw` instance. The constraint is that :math:`d1 + d2 = 7`.
    If the constraint is not satisfied, raise an exception.

    This uses the superclass constructor to add appropriate
    :class:`Outcome` instances for a throw of 7.

Methods
~~~~~~~


..  method:: NaturalThrow.hard(self) -> bool


    A natural 7 is odd, and can never be made "the hard way".
    This method always returns :literal:`False`.


..  method:: NaturalThrow.updateGame(self, game: CrapsGame) -> None

    :param game: the CrapsGame to be updated based on this throw.
    :type game: :class:`CrapsGame`


    Calls the :meth:`natural`
    method of a game :class:`CrapsGame`. This may change the game state
    and resolve bets.


Craps Throw Design
-------------------

..  class:: CrapsThrow

    :class:`Craps Throw` is a subclass of :class:`Throw` for the
        "craps" numbers, 2, 3 and 12.


Constructors
~~~~~~~~~~~~


..  method:: CrapsThrow.__init__(self, d1: int, d2: int) -> None

    :param d1: The value of one die
    :param d2: The value of the other die


    Creates this :class:`Throw` instance. The constraint is that :math:`d1 + d2 \in \{2, 3, 12\}`.
    If the constraint is not satisfied, raise an exception.

    This uses the superclass constructor to add appropriate
    :class:`Outcome` instances for a throw of craps.


Methods
~~~~~~~


..  method:: CrapsThrow.hard(self) -> bool


    The craps numbers are never part of "hardways" bets.
    This method always returns :literal:`False`.


..  method:: CrapsThrow.updateGame(self, game: CrapsGame) -> None

    :param game: the :class:`CrapsGame` instance to be updated based on this throw.
    :type game: :class:`CrapsGame`


    Calls the :meth:`craps`
    method of a game :class:`CrapsGame` instance. This may change the game state
    and resolve bets.


Eleven Throw Design
-------------------

..  class:: ElevenThrow

    :class:`ElevenThrow` is a subclass of :class:`Throw` for the
    number, 11.  This is special because 11 has one effect on a come-out
    roll and a different effect on point rolls.


Constructors
~~~~~~~~~~~~


..  method:: ElevenThrow.__init__(self, d1: int, d2: int) -> None

    :param d1: The value of one die
    :param d2: The value of the other die


    Creates this :class:`Throw` instance. The constraint is that :math:`d1 + d2 = 11`.
    If the constraint is not satisfied, raise an exception.

    This uses the superclass constructor to add appropriate
    :class:`Outcome` instances for a throw of 11.


Methods
~~~~~~~~


..  method:: ElevenThrow.hard(self) -> bool


    Eleven is odd and never part of "hardways" bets.
    This method always returns :literal:`False`.


..  method:: ElevenThrow.updateGame(self, game: CrapsGame) -> None

    :param game: the :class:`CrapsGame` instance to be updated based on this throw.
    :type game: :class:`CrapsGame`


    Calls the :meth:`eleven`
    method of a :class:`CrapsGame` instance. This may change the game state
    and resolve bets.


Point Throw Design
------------------

..  class:: PointThrow

    :class:`PointThrow` is a subclass of :class:`Throw` for the
    point numbers 4, 5, 6, 8, 9 or 10.


Constructors
~~~~~~~~~~~~


..  method:: PointThrow.__init__(self, d1: int, d2: int) -> None

    :param d1: The value of one die
    :param d2: The value of the other die


    Creates this :class:`Throw` instance. The constraint is that :math:`d1 + d2 \in \{ 4, 5, 6, 8, 9, 10 \}`.
    If the constraint is not satisfied, raise an exception.

    This uses the superclass constructor to add appropriate
    :class:`Outcome` instances for a throw of craps.


Methods
~~~~~~~


..  method:: PointThrow.hard(self) -> bool

    Returns :literal:`True`
    if :obj:`d1` is equal to :obj:`d2`. This helps determine if
    hardways bets have been won or lost.


..  method:: PointThrow.updateGame(self, game: CrapsGame) -> None

    :param game: the :class:`CrapsGame` instance to be updated based on this throw.
    :type game: :class:`CrapsGame`


    Calls the :meth:`point`
    method of a game :class:`CrapsGame`. This may change the game state
    and resolve bets.


Craps Game Design
------------------

This is a stub class definition for :class:`CrapsGame`.
This initial design contains the interface used by the :class:`Throw`
class hierarchy to implement game state changes.  In a later section,
we'll provide a more complete definition.


Fields
~~~~~~~

..  attribute:: GrapsGame.point
    :noindex:

    The current point. This will be replaced by a proper :emphasis:`State`
    design pattern.


Constructors
~~~~~~~~~~~~~~


..  method:: CrapsGame.__init__(self) -> None
    :noindex:


    Creates this game. A later version will use a constructor to include
    the :class:`Dice` instance and the :class:`CrapsTable` instance.


Methods
~~~~~~~~


..  method:: CrapsGame.craps(self) -> None


    Resolves all current 1-roll bets.

    If the point is zero, this was a come out roll: Pass
    Line bets are an immediate loss, Don't Pass Line bets are an
    immediate win.

    If the point is non-zero, Come Line bets are an
    immediate loss; Don't Come Line bets are an immediate win.

    The state doesn't change.

    A future version will delegate responsibility to the :meth:`craps`
    method of a current state object.


..  method:: CrapsGame.natural(self) -> None


    Resolves all current 1-roll bets.

    If the point is :literal:`None`, this was a come out roll: Pass
    Line bets are an immediate win; Don't Pass Line bets are an
    immediate loss.

    If the point is non-:literal:`None`, Come Line bets are an
    immediate win; Don't Come bets are an immediate loss; the point is
    also reset to zero because the game is over.

    Also, hardways bets are all losses.

    A future version will delegate responsibility to the :meth:`natural`
    method of a current state object.


..  method:: CrapsGame.eleven(self) -> None


    Resolves all current 1-roll bets.

    If the point is :literal:`None`, this is a come out roll: Pass
    Line bets are an immediate win; Don't Pass Line bets are an
    immediate loss.

    If the point is non-:literal:`None`, Come Line bets are an
    immediate win; Don't Come bets are an immediate loss.

    The game state doesn't change.

    A future version will delegate responsibility to the :meth:`eleven`
    method of a current state object.


..  method:: CrapsGame.point(self, point: int) -> None

    :param point: The point value to set.
    :type point: integer


    Resolves all current 1-roll bets.

    If the point was :literal:`None`, this is a come out roll, and the value of the dice
    establishes the point.

    If the point was non-:literal:`None` and this throw
    matches the point the game is over: Pass Line bets and associated
    odds bets are winners; Don't Pass bets and associated odds bets are
    losers; the point is reset to zero.

    Finally, if the point is
    non-:literal:`None` and this throw does not match the point, the state doesn't
    change. Come point and Don't come point bets may be
    resolved.  Additionally, hardways bets may be resolved.

    A future
    version will delegate responsibility to the current state's :meth:`point`
    method to advance the game state.




..  method:: Throw.__str__(self) -> str
    :noindex:


    An easy-to-read string output method is also very handy. The
    stub version of this class has no internal state object. This class
    can simply return a string representation of the point; and the string
    :literal:`"Point Off"` when :obj:`point` is :literal:`None`.


Throw Deliverables
-------------------

There are eleven deliverables for this exercise.

-   A stub class for :class:`CrapsGame` with the various methods
    invoked by the throws. The design information includes details on
    bet resolution that doesn't need to be fully implemented at the
    present time. For this stub class, the change to the :obj:`point`
    variable is required for unit testing. The other information should
    be captured as comments and output statements that help confirm the
    correct behavior of the game.

-   The :class:`Throw` superclass, and the four subclasses: :class:`CrapsThrow`,
    :class:`NaturalThrow`, :class:`ElvenThrow`, :class:`PointThrow`.

-   Five classes which perform unit tests on the various classes of the :class:`Throw`
    class hierarchy.

Looking Forward
----------------

Now that we've defined the 36 possible dice throws, we can combine
these into a :class:`Dice` class that selects a throw at random.
The :class:`Dice` class parallels the :class:`Wheel` class in the
Roulette simulation. In the next chapter, we'll look at the design
for the dice and how it emits random values.
