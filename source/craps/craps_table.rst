
..  _`craps.table`:

Craps Table Class
=================

In Roulette, the table was a passive repository for :class:`Bet` instances.
In Craps, however, the table and game must collaborate to accept or
reject bets based on the state of the game. This validation includes
rules based on the total amount bet as well as rules for the individual bets.

In :ref:`craps.throw`, we roughed out a stub version of the :class:`CrapsGame` class
to test the :class:`Throw` class. In this section, we will
extend this stub with additional features required by the table.

In `Craps Table Analysis`_ we'll look at two issues related to
how the game works. In `Movable Bets`_ we'll look at how the
Pass Line bet works. In `Game State and Allowed Bets`_ we'll look
at the bet validation issue.

We'll dig into three separate design decisions:

-   `Design Decision -- Table vs. Game Responsibility`_,

-   `Design Decision -- Allowable Outcomes`_, and

-   `Design Decision -- Domain of Allowed Bets`_.

After looking closely at the choices, in `Handling Working Bets`_ we'll
create a final approach to handling the bets on the table.

This will lead to detailed design presentations
in `CrapsGame Stub`_ and `Craps Table Design`_. We'll enumerate the
deliverables for this chapter in `Craps Table Deliverables`_.


..  _`craps.table.ov`:

Craps Table Analysis
---------------------

The :class:`Table` class is a container for  the :class:`Bet` instances. The
money placed on :class:`Bet` instances on the :class:`Table` is
"at risk". There are several outcomes:

-   A bet can win an amount based on the odds,

-   A bet can lose the amount placed by the player,

-   The Don't Come and Don't Pass bets may be returned, an event called a "push", and

-   The Buy and Lay bets include a commission (or vigorish) to place the bet;
    the commission is lost money; the balance of the bet, however, may win or lose.

The responsibility for this new event called
a push is something we can allocate to :class:`CrapsGame`, the commission price belongs to :class:`Bet`.

Movable Bets
~~~~~~~~~~~~

Some :class:`Bet` instances (specifically Pass, Don't Pass, Come and Don't
Come) may have their :class:`Outcome` reference changed.  The use case works like this:

1.  The bet is created by the Player with one :class:`Outcome`, for example, "Pass".
    The :class:`Table` accepts this :class:`Bet` instance.

2.  That bet may be resolved as an immediate winner or loser.  The Game and Throw will
    determine if the Bet is a winner as placed.

    More commonly, the :class:`Bet` may be changed to a new
    :class:`Outcome`, possibly with different odds.

    In a casino, the chips initially placed on Come Line and Don't Come bets are relocated to
    a point number box to show this change. In the case of Pass Line and
    Don't Pass bets, the "On" marker is placed on the table to show
    an implicit movement of all of those line bets.

The change is the
responsibility of the :class:`CrapsGame` object; however, the :class:`Table` instance
must provide an iterator over the line bets that the :class:`CrapsGame` object
will move.

Game State and Allowed Bets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each change to the game state changes the allowed bets as well as the
active bets. When the point is off, most of the bets on the table are not
allowed, and some others are inactive, or not "working".

When a point is established, all bets are allowed, and all bets are active.
We'll examine the rules in detail, below.

The :class:`Table` class must be
able to reject bets which are inappropriate for the current :class:`CrapsGame` object's
state.

Design Decision -- Table vs. Game Responsibility
-------------------------------------------------

We've identified three  responsibilities that are part of handling Craps bets:

-   moving :class:`Bet` instances,

-   inactivating outcomes based on game state, and

-   accepting or rejecting bets based on :class:`CrapsGame` state.

Clearly, these require
additional collaboration between the :class:`CrapsGame` and :class:`Table` classes.
We will have to add methods to the :class:`CrapsGame` class that will allow
or deny some bets, as well as methods that will active or deactive some bets.

We have to choose where in the class hierarchy we will retrofit this
additional collaboration.

**Problem**.
Should we put these new responsibilities at a high-enough level that we'll  add  table and game
collaboriation  to the :class:`Table` class used for Roulette?

**Forces**.
If we do add
this for Roulette, we could simply return :literal:`True` from the
method that validates the allowed bets, since all bets are allowed in
Roulette.

However, our overall application design does not depend on all
subclasses of :class:`CrapsGame` and :class:`Table` being
polymorphic; we will never mix and match different combinations of Craps
Table and Roulette Game.

**Solution**.
Because we don't need polymorphism between Craps and Roulette, we can
create a subclass of :class:`Table` with a more complex interface
and leave Roulette untouched. Perhaps we'll call it :class:`CrapsTable`.

Design Decision -- Allowable Outcomes
---------------------------------------

After deciding to create a :class:`CrapsTable` subclass, we have
several consequent decisions. First, we turn the interesting question of
how best to allocate responsibility for keeping the list of :class:`Outcome` instances
which change with the game state.

**Problem**.
Which class determines the valid and invalid :class:`Outcome` instances?

**Forces**.
We can see two places to place
this responsibility.

#.  :class:`CrapsTable`. This class could have
    methods to return the lists of :class:`Outcome` instances that are
    allowed or not allowed. :class:`CrapsGame` can make a call to
    get the list of :class:`Outcome` instances and make the changes. Making
    each change would involve the :class:`CrapsTable` a second time
    to mark the individual :class:`Outcome` instances. This information is
    then used by the :class:`CrapsTable` to validate individual :class:`Bet` instances.

#.  :class:`CrapsGame`. This class could invoke a
    method of :class:`CrapsTable` that changes a single :class:`Outcome`'s
    state to makt it inactive. This information is then used by the :class:`CrapsTable`
    to validate individual :class:`Bet` instances.

    A feature of this choice is to have the :meth:`validBet`
    method of :class:`CrapsTable` depend on :class:`CrapsGame` to determine which bets are allowed
    or denied. In this case, :class:`CrapsGame` has the
    responsibility to respond to requests from either :class:`CrapsTable`
    or :class:`Player` regarding a specific :class:`Outcome` instances.

**Solution**
We need to place a validation method in the :class:`CrapsTable`; but the Table simply
delegates the details to the :class:`CrapsGame`.  This allows the Player to
deal directly with the Table.  But it centralizes the actual decision-making
on the Game.

This leaves the table as a fairly passive repository for bets. The
bulk of the decision-making for validity is delegated to the game.

**Consequences**.
The game must move :class:`Outcome` instances for certain kinds of bets.
Additionally, the :class:`CrapsTable`'s :meth:`isValid`
method will use the :class:`CrapsGame` to both check the validity of
individual bets as well as the entire set of bets created by a player.
The first check allows or denies individual bets, something :class:`CrapsTable`
must do in collaboration with :class:`CrapsGame`. For the second
check, the :class:`CrapsTable` assures that the total of the bets is
within the table limits; something for which only the table has the
information required.

Design  Decision -- Domain of Allowed Bets
-------------------------------------------

The rule for allowed and non-allowed bets is relatively
simple. When the game state has no point (also known as the come out
roll), only Pass Line and Don't Pass bets are allowed, all other bets
are not allowed. When the point is on, all bets are allowed. We'll have
to add an :meth:`isAllowed` to :class:`CrapsGame`, which :class:`CrapsTable`
will use when the player attempts to place a bet.

We have two ways to implement this:

-   A "validation" function that determines if bets are allowed.

-   A "what's possible" function that returns an enumeration of legal bets.

The idea of one-by-one validation might make sense in a situation where
the player transactions are quite complex. For casino games, the player's
alternatives are narrowly constrained.

It makes considerable sense for the :class:`CrapsGame` to supply the domain of
allowed bets to the :class:`Table` and :class:`Player`. In this way, a :class:`Player`
can simply extract the interesting bets from the available domain of possible
bets.

Handling Working Bets
----------------------

The rule for working and non-working bets adds
a layer of complexity to the game state.

On the come out roll, all odds bets placed behind any
of the six Come Point numbers are not working. This rule only applies to
odds behind Come Point bets; odds behind Don't Come bets are always
working. We'll have to add an :meth:`isWorking` to :class:`CrapsGame`,
which :class:`CrapsTable` will use when iterating through working bets.

The sequence of events that can lead to this condition is as follows.


1.  The player places a Come Line bet, the dice roll is 4, 5, 6, 8, 9
    or 10, and establishes a point. The bet is moved to one of the six come points.

2.  The player creates an additional odds bet placed behind
    this come point bet.

3.  A dice roll makes the main game point is a winner.
    changing the game state so the next roll is a come out roll.
    In this state, any additional odds behind a come point bet will
    be a non-working bets on the subsequent come-out roll.

As with allowed bets, we have a domain of working bets for a given
game state. We can implement this as a function that responds with
state information. We can also implement this as a collection
of bets what are working in a given game state.

The code could look like this:

..  rubric:: Working Bets Method

..  code-block:: python

    if theTable.is_working(some_bet):
        if theTable.winner(some_bet):
            player.win(some_bet)
        else:
            player.lose(some_bet)

Or, it could look like this:

..  rubric:: Working Bets Collection

..  code-block:: python

    if some_bet in theTable.working_bets():
        if some_bet in theTable.winning_bets():
            player.win(some_bet)
        else:
            player.lose(some_bet)

The distinction is minor.

Also note that the examples don't include push outcomes. We'll look at
the details of hanlding that in the :ref:`craps.game` section.

What's important is that we can handle these subtle cases gracefully.
This elegant processing of complex rules is one of the important reasons why
object-oriented programming can be more successful than procedural
programming. In this case, we can isolate this state-specific processing
to the :class:`CrapsGame` class. We can also provide the interface to the :class:`CrapsTable`
class making this responsibility explicit and easy to use.

..  _`craps.game.stub`:

CrapsGame Stub
--------------

The :class:`CrapsGame` class is a preliminary design for the game of Craps. In
addition to features required by the :class:`Throw` class, this version
includes features required by the :class:`CrapsTable` class.


Methods
~~~~~~~


..  method:: CrapsGame.isAllowed(self, outcome: Outcome) -> bool

    :param outcome: An :class:`Outcome` that may be allowed or not allowed,
        depending on the game state.
    :type outcome: :class:`Outcome`


    Determines if the :class:`Outcome` is
    allowed in the current state of the game. When the :obj:`point`
    is zero, it is the come out roll, and only Pass, Don't Pass, Come
    and Don't Come bets are allowed. Otherwise, all bets are allowed.




..  method:: CrapsGame.isWorking(self, outcome: Outcome) -> bool

    :param outcome: An :class:`Outcome` that may be allowed or not allowed,
        depending on the game state.
    :type outcome: :class:`Outcome`


    Determines if the :class:`Outcome` is
    working in the current state of the game. When the :obj:`point`
    is zero, it is the come out roll, odds bets placed behind any of the
    six come point numbers are not working.


Craps Table Design
-------------------

The :class:`CrapsTable` is a subclass of the :class:`Table` class with an
association with a :class:`CrapsGame` object. As a subclass of the :class:`Table` class,
it contains all the :class:`Bet` instances created by the :class:`Player` instance.
It also has a betting limit, and the sum of all of a player's bets
must be less than or equal to this limit. We assume a single :class:`Player` instance
in the simulation.


Fields
~~~~~~~~

..  attribute:: CrapsTable.game

    The :class:`CrapsGame` used to determine if a given bet is
    allowed or working in a particular game state.


Constructors
~~~~~~~~~~~~~~


..  method:: CrapsTable.__init__(self, game: CrapsGame) -> None

    :param game: The CrapsGame instance that controls the state of this table
    :type game: :class:`CrapsGame`


    Uses the superclass for initialization of the empty :class:`LinkedList`
    of bets.


Methods
~~~~~~~~~~


..  method:: CrapsTable.isValid(self, bet: Bet) -> bool

    :param bet: The bet to validate.
    :type bet: :class:`Bet`


    Validates this bet by checking with the :class:`CrapsGame`
    to see if the bet is valid; it returns :literal:`True` if the bet is valid,
    :literal:`False` otherwise.




..  method:: CrapsTable.allValid(self) -> bool


    This uses the
    superclass to see if the sum of all bets is less than or equal to
    the table limit. If the individual bet outcomes are also valid, return :literal:`True`.
    Otherwise, return :literal:`False`.


Craps Table Deliverables
-------------------------

There are three deliverables for this exercise.

-   A revision of the stub :class:`CrapsGame` class to add methods
    for validating bets in different game states. In the stub, the point
    value of 0 means that only the "Pass Line" and "Don't
    Pass Line" bets are valid, where a point value of non-zero means all
    bets are valid.

-   The :class:`CrapsTable` subclass.

-   A class which performs a unit test of the :class:`CrapsTable`
    class. The unit test should create a couple instances of :class:`Bet`,
    and establish that these :class:`Bet` instances are managed by the
    table correctly.

    For testing purposes, it is easiest to have the test method simply
    set the the :obj:`point` variable in the :class:`CrapsGame`
    instance to force a change in the game state. While public instance
    variables are considered by some to be a bad policy, they facilitate
    the creation of unit test classes.

Looking Forward
---------------

We have a table for bets, and a definition of the dice and
throws. The next component is the fairly complex set of state
transition rules for the :class:`CrapsGame` class.
In the next chapter we'll design the state class hierarchy to
run the :class:`CrapsGame` class.
