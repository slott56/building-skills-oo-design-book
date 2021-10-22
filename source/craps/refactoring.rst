
..  _`craps.refactor`:

Design Cleanup and Refactoring
==============================

We have taken an intentionally casual approach to the names chosen for
our various classes and the relationships among those classes. At this
point, we have a considerable amount of functionality, but it doesn't
reflect our overall purpose, instead it reflects the history of its
evolution. This chapter will review the design from Craps and more
cleanly separate it from the design for Roulette.


We expect two benefits from the rework in this chapter. First,
the design should become "simpler" in the sense that Craps is
separated from Roulette, and this will give us room to insert Blackjack
into the structure with less disruption in the future. Second, and more
important, the class names will more precisely reflect the purpose of
the class, making it easier to understand the application.
This should make it debug, maintain and adapt.

We'll start with a review of the current design in `Design Review`_.
This will include a number of concerns:

-   `Unifying Bin and Throw`_,

-   `Unifying Dice and Wheel`_,

-   `Refactoring Table and CrapsTable`_,

-   `Refactoring Player and CrapsPlayer`_, and

-   `Refactoring Game and CrapsGame`_.

Based on this, we'll need to rework some existing class defintions.
This will involve making small changes to a large number of classes.
The work is organized as follows:

-   `RandomEventFactory Design`_,

-   `Wheel Class Design`_,

-   `Dice Class Design`_,

-   `Table Class Design`_,

-   `Player Class Design`_,

-   `Game Class Design`_,

-   `RouletteGame Class Design`_, and

-   `CrapsGame Class Design`_.

In `Refactoring Deliverables`_ we'll detail all of the deliverables for this chapter.

Design Review
--------------

We can now use our application to generate some more usable results. We
would like the :class:`Simulator` class to be able to use our Craps
game, dice, table and players in the same way that we use our Roulette
game, wheel, table and players. The idea would be to give the :class:`Simulator`
class constructor a bunch of Craps-related objects instead of a bunch of Roulette-related objects
and have everything else work normally. Since we have generally made
Craps a subclass of Roulette, we are reasonably confident that this
should work.


Our :class:`Simulator` class constructor requires :class:`Game`
and :class:`Player` instances. Since the :class:`CrapsGame` class is a subclass of
the :class:`Game` class and the :class:`CrapsPlayer` class is a subclass of
the  :class:`Player` class, we *should* be able
to  construct an instance of :class:`Simulator`.


Looking at this, however, we find a serious problem with the names of
our classes and their relationships. When we designed Roulette, we started
out with generic names like :class:`Table`, :class:`Game` and :class:`Player`
unwisely. Further, there's no reason for Craps to be dependent on
Roulette. We would like them to be siblings, and both children of some
abstract game simulation.


..  sidebar:: Second Soapbox On Refactoring

    ..  _`soapbox.refactoring2`:

    We feel very strongly that design by refactoring
    helps beginning designers produce a more functional design more
    quickly. The alternative approach requires
    defining the game abstraction and player abstraction first and
    then specializing the various games. When defining an abstract
    superclass, some designers will build a :quick and dirty
    design for some of the subclasses, and use this to establish the
    features that belong in the superclass. We find that a more
    successful superclass design comes from having more than one
    working subclasses and a clear understanding of the kinds of
    extensions that are likely to emerge from the problem domain.


    While our approach of refactoring working code seems expensive,
    the total effort is likely to be smaller than trying to do
    **Big Design Up Front**. The largest impediment
    seems to stem from the project management mythology that
    once something passes unit tests it is done for ever and can be
    checked off as completed. We feel that it is very important to
    recognize that nothing is ever truly done. At some point,
    the pace of evolution slows, but it never really stops changing.



    A good sanity test is the designer's ability to explain
    the class structure to someone new to the project. We feel that
    class and package names must make obvious sense in the current
    project context. Any explanation of a class name
    that involves the words "historically" or "originally"
    means there are more serious design deficiencies
    to be repaired.


We now know enough to factor out the common features of the :class:`Game`
and :class:`CrapsGame` classes to create three new classes from these two.
To find the common features of these two classes,
we'll see that we have to unify the :class:`Dice` and :class:`Wheel` classes,
as well as the :class:`Table` and :class:`CrapsTable` classes and the
:class:`Player` and :class:`CrapsPlayer` classes.

Looking into :class:`Dice` and :class:`Wheel`,
we see that we'll have to tackle
first. Unifying :class:`Bin` and :class:`Throw` is covered in :ref:`craps.throwbuilder.design.heavy`.

We have several sections on refactoring these various class hierarchies:

-   The :class:`Bin` and :class:`Throw` classes in :ref:`craps.cleanup.ov.unifyBinAndThrow`.

-   The :class:`Wheel` :class:`Dice` classes  in :ref:`craps.cleanup.ov.unifyDiceAndWheel`.

-   The :class:`Table` and :class:`CrapsTable` classes  in :ref:`craps.cleanup.ov.unifyTableAndCrapsTable`.

-   The :class:`Player` and :class:`CrapsPlayer` classes in :ref:`craps.cleanup.ov.unifyPlayerAndCrapsPlayer`.

-   The :class:`Game` and :class:`CrapsGame` classes in :ref:`craps.cleanup.ov.unifyGameAndCrapsGrame`.

This will give us two properly parallel structures with names that reflect
the overall intent.

..  _`craps.cleanup.ov.unifyBinAndThrow`:

Unifying Bin and Throw
~~~~~~~~~~~~~~~~~~~~~~

We need to create a common superclass for the :class:`Bin`
and :class:`Throw` classes, so that we can then create some commonality between
the :class:`Dice` and :class:`Wheel` classes.

The first step, then, is to identify the common features of the :class:`Bin`
and :class:`Throw` classes. The relatively simple :class:`Bin` class and the
more complex :class:`Throw` class can be unified in one of two ways.

#.  Use the :class:`Throw` class as the superclass. A Roulette :class:`Bin` class
    doesn't need a specific list of losing :class:`Outcome` instances.
    Indeed, we don't even need a subclass, since a Roulette :class:`Bin` instance
    can just ignore features of the Craps-centric :class:`Throw` class.

#.  Create a new superclass based on the :class:`Bin` class. We can then
    make a :class:`Bin` subclass that adds no new features.
    We can change the :class:`Throw` class to add features to the new superclass.
    This makes the :class:`Bin` and :class:`Throw` classes  peers with a common parent.

The first design approach is something we call the **Swiss Army Knife**
design pattern: create a structure that has every possible feature, and
then ignore the features in subclasses. This creates a distasteful
disconnect between the use of a :class:`Bin` instance and the declaration of
the :class:`Bin` class:
we only use the set of winning :class:`Outcome` instances, but the
object also has a losing set that isn't used by anything else in the
Roulette game.

We also note that a key feature of OO languages is
inheritance, which :emphasis:`adds` features to a superclass. The
**Swiss Army Knife** design approach, however, works by
subtracting features.
This creates a distance between the OO language and our design intent.

Our first decision, then, is to refactor the :class:`Throw` and :class:`Bin` classes
to make them children of a common superclass, which we'll call the :class:`RandomEvent` class.
See the Craps Throw :ref:`craps.throw.ov` for our initial thoughts on
this, echoed in the :ref:`Soapbox on Refectoring <soapbox.refactoring2>` sidebar.


The responsibilities for the :class:`RandomEvent` class are essentially the
same as the :class:`Bin` class. We can then make a :class:`Bin` subclass
that doesn't add any new features, and a :class:`Throw` subclass
that adds a number of features, including the value of the two dice and
the set of losing :class:`Outcome` instances. See :ref:`soapbox.architecture`
for more information on our preference for this kind of design.


..  _`craps.cleanup.ov.unifyDiceAndWheel`:

Unifying Dice and Wheel
~~~~~~~~~~~~~~~~~~~~~~~

When we take a step back from the :class:`Dice`
and :class:`Wheel` classes, we see that they are nearly identical. They
differ in the construction of the :class:`Bin` instances or :class:`Throw` instances,
but little else. Looking forward, the deck of cards used for
Blackjack is completely different. Craps dice and a Roulette wheel use
selection with replacement: an event is picked
at random from a pool, and is eligible to be picked again any number of
timers. Cards, on the other hand, are selection
**without** replacement: the cards form a sequence of events of a defined
length that is randomized by a shuffle.

Here's the consequence. If we have a 5-deck shoe, we can
never see more than twenty kings before the shoe is shuffled.
However, we can always roll an indefinite number of 7's on the dice.

We note that there is also a superficial similarity between the rather complex
methods of the :class:`BinBuilder` class and the simpler method in the :class:`ThrowBuilder` class.
Both work from a simple overall :meth:`build` method to create the
collections of :class:`Bin` or :class:`Throw` objects.

Our second design decision, then, is to create a :class:`RandomEventFactory` class
out of the :class:`Dice` and :class:`Wheel` classes.
Each subclass provides an initialization
method that constructs the :class:`RandomEvent` instances.


When we move on to tackle cards, we'll have to create a subclass that
uses a different definition of the random choice method, :meth:`choose`, and adds :meth:`shuffle`.
This will allow a deck of cards to do selection without replacement,
distinct from dice and a wheel which does selection with replacement.


..  _`craps.cleanup.ov.unifyTableAndCrapsTable`:

Refactoring Table and CrapsTable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We see few differences between the :class:`Table`
and :class:`CrapsTable` classes. When we designed :class:`CrapsTable`
we had to add a relationship between the :class:`CrapsTable` and :class:`CrapsGame` objects
so that a table could ask the game to validate individual :class:`Bet` instances
based on the state of the game.


If we elevate the :class:`CrapsTable` to be the superclass, we
eliminate a need to have separate classes for Craps and Roulette. We are
dangerously close to embracing a **Swiss Army Knife** design.
The distinction is a matter of degree: one or two
features can be pushed up to the superclass and then ignored in a
subclass.

In this case, both Craps and Roulette can use the :class:`Game`
as well as the :class:`Table` classes to validate bets. This feature will not be ignored
by one subclass. It happens that the Roulette Game will
permit all bets. The point is to push the responsibility into
the :class:`Game` instead of the :class:`Table` class.

We actually have two sets of rules that must be imposed on bets.
The table rules impose an upper (and lower) limit on the bets.
The game rules specify which outcomes are legal in a given game
state.

The :class:`Game` class provides rules as a set of valid :class:`Outcome` instances.
The :class:`Table` class provides rules via a method that checks the sum of the amount
of the :class:`Bet` instances.


Our third design decision is to merge the :class:`Table` and :class:`CrapsTable` classes
into a new :class:`Table` class and use this for both games. This
will simplify the various Game classes by using a single class of :class:`Table`
for both games.

..  _`craps.cleanup.ov.unifyPlayerAndCrapsPlayer`:

Refactoring Player and CrapsPlayer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before we can finally refactor the :class:`Game` class,
we need to be sure that we have sorted out a proper relationship
between our various players. In this case, we have a large hierarchy,
which we will hope to make even larger as we explore different betting
alternatives. Indeed, the central feature of this simulation is to
expand the hierarchy of players as needed to explore betting strategies.
Therefore, time spent organizing the :class:`Player` class hierarchy is
time well spent.


We'd like to have the following hierarchy.

-   Player.

    -   RoulettePlayer.

        -   RouletteMartingale.

        -   RouletteRandom.

        -   RouletteSevenReds.

        -   Roulette1326.

        -   RouletteCancellation.

        -   RouletteFibonacci.

    -   CrapsPlayer.

        -   CrapsMartingale.


Looking forward to Blackjack, we see that there is much richer player
interaction, because there are player decisions that are not related to
betting. This class hierarchy doesn't seem to enable an expansion
to separate play decisions from betting decisions. In the case of craps,
there seem to be two kinds of betting decisions -- outcome choice vs. amount --
that isn't handled very well.

There seem to be at least two "dimensions" to this class hierarchy.
One dimension is the game (Craps or Roulette), the other dimension is a
betting system (Matingale, 1-3-2-6, Cancellation, Fibonacci, etc.) For
Blackjack, there is also a playing system in addition to a betting
system. Sometimes this multi-dimensional aspect of a class hierarchy
indicates that we should be using multiple inheritance to define our classes.

In the case of Python, we have two approaches for implementation:

-   Multiple inheritance is part of the language, and we can pursue this directly.

-   We can also follow the **Strategy** design pattern to add a betting strategy
    object to the basic interface for playing the game.


In Roulette there are no game choices.
However, in Craps, we separated
the Pass Line bet, where the payout doesn't match the actual odds very
well, from the Pass Line Odds bet, where the payout does match the
odds. This means that a Martingale Craps player really has two
betting strategy objects: a flat bet strategy for Pass Line and a
Martingale Bet strategy for the Pass Line Odds.


If we separate the player and the betting system, we could mix
and match betting systems, playing systems and game rules. In the case
of Craps, where we can have many working bets (Pass Line, Come Point
Bets, Hardways Bets, plus Propostions), each player would have a mixture
of betting strategies used for their unique mixture of working bets.



Rather than fully separate the player's game interface and betting
system interface, we can try to adjust the class hierarchy and the class
names to those shown above. We need to make the superclass, :class:`Player`
independent of any game. We can do this by extracting anything
Roulette-specific from the original :class:`Player` class and
renaming our Roulette-focused :class:`Passenger57` to be :class:`RoulettePlayer`,
and fix all the Roulette player subclasses to inherit from :class:`RoulettePlayer`.


We will encounter one design difficulty when doing this. That is the
dependency from the various :class:`Player1326State` classes on a
field of :class:`Player1326`. Currently, we will simply be renaming :class:`Player1326`
to :class:`Roulette1326`. However, as we go forward, we will see
how this small issue will become a larger problem. In Python, we can
easily overlook this, as described in :ref:`Python and Interface Design <tip.interface.python>`.


..  sidebar:: Python and Interface Design

    ..  _`tip.interface.python`:

    Because of the run-time binding done in Python, there is no
    potential problem in having the :class:`Player1326State`
    classes depend on a field defined in :class:`Player1326`.

    Other languages -- like Java -- involve compile-time binding.
    A small change can lead to recompiling the world.
    In some respects this can be helpful for identifying a problem.

    In Python, however, the attributes of an object are
    created dynamically, making it difficult to assure in advance
    that one class properly includes the attributes that will be required by a collaborating
    class. We don't discover problems in Python class dependencies until the
    unit tests raise exceptions because of a missing attribute.

    We can use **mypy** to check for preoper

..  _`craps.cleanup.ov.unifyGameAndCrapsGrame`:

Refactoring Game and CrapsGame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once we have common :class:`RandomEventFactory`,
:class:`Table`, and :class:`Player` classes, we
can separate the :class:`Game` class from the :class:`RouletteGame` and :class:`CrapsGame`
classes to create three new classes:

-   The abstract superclass, :class:`Game`.
    This will contain a :class:`RandomEventFactory` instance,
    a :class:`Table` instance and have the necessary interface to reset the
    game and execute one cycle of play. This class is based on the existing
    :class:`Game` class, with the Roulette-specific :meth:`cycle`
    replaced with an abstract method definition.

-   The concrete :class:`RouletteGame` subclass. This has the :meth:`cycle`
    method appropriate to Roulette that was extracted from the original :class:`Game`
    class.

-   The concrete :class:`CrapsGame` subclass. This has a :meth:`cycle`
    method appropriate to Craps. This is a small change to the parent of the
    :class:`CrapsGame` class.

While this appears to be a tremendous amount of rework, it reflects
lessons learned incrementally through the previous chapters of
exercises. This refactoring is based on considerations that would have
been challenging, perhaps impossible, to explain from the outset. Since
we have working unit tests for each class, this refactoring is easily
validated by rerunning the existing suite of tests.


RandomEventFactory Design
-------------------------

..  class RandomEventFactory::

    :class:`RandomEventFactory` is a superclass for Dice, Wheel, Cards,
    and other casino random-event generators.


Fields
~~~~~~~~

..  attribute:: RandomEventFactory.rng

    The random number generator, a subclass of :class:`random.Random`.


    Generates the next random number, used to select a :class:`RandomEvent`
    from the :obj:`bins` collection.

..  attribute:: RandomEventFactory.current

    The most recently returned :class:`RandomEvent`.


Constructors
~~~~~~~~~~~~~


..  method:: RandomEventFactory.__init__(self, rng: random.Random) -> None


    Saves the given Random Number Generator. Calls the :meth:`initialize`
    method to create the pool of result instances. These are subclasses
    of the :class:`RandomEvent` class and include the :class:`Bin`, an :class:`Throw`
    classes.


Methods
~~~~~~~


..  method:: RandomEventFactory.initialize(self) -> None


    Create a collection of :class:`RandomEvent` objects with the pool of possible
    results.

    Each subclass must provide a unique implementation for this.



..  method:: RandomEventFactory.choose(self) -> RandomEvent

    Return the next :class:`RandomEvent`.

    Each subclass must provide a unique implementation for this.


Wheel Class Design
-------------------

The :class:`Wheel` class is a subclass of the :class:`RandomEventFactory` class.
It  contains the 38 individual :class:`Bin` instances on a Roulette wheel. As a :class:`RandomEventFactory`,
it contains a random number generator and can select a :class:`Bin` instance
at random, simulating a spin of the Roulette wheel.

Constructors
~~~~~~~~~~~~


..  method:: Wheel.__init__(self, rng: random.Random) -> None
    :noindex:


    Creates a new wheel.  Create a sequence of the :attr:`Wheel.events` with with 38 empty :class:`Bin` instances.

    Use the superclass to save the given random number generator instance and invoke :meth:`initialize`.

Methods
~~~~~~~~



..  method:: Wheel.addOutcome(self, bin: int, outcome: Outcome) -> None


    Adds the given :class:`Outcome` to the
    :class:`Bin` with the given number.



..  method:: Wheel.initialize(self) -> None


    Creates an :obj:`events` collection with the pool of possible events.
    This will create an instance of :class:`BinBuilder`, :obj:`bb`, and delegate the
    construction to the :meth:`BinBuilder.buildBins` method.

Dice Class Design
-----------------

The :class:`Dice` class is a subclass of the :class:`RandomEventFactory` clas.
It contains the 36 individual throws of two dice. As a :class:`RandomEventFactory`,
it contains a random number generator and can select a :class:`Throw` instance
at random, simulating a throw of the Craps dice.

Constructors
~~~~~~~~~~~~



..  method:: Dice.__init__(self, rng: random.Random) -> None
    :noindex:


    Create an empty set of :attr:`Dice.events`.
    Use the superclass to save the given random number generator instance and invoke :meth:`initialize`.


Methods
~~~~~~~~~


..  method:: Wheel.addOutcome(self, faces: Tuple[int, int], outcome: Outcome) -> None


    Adds the given :class:`Outcome` object to the
    :class:`Throw` instance with the given tuple of values. This
    allows us to create a collection of several one-roll :class:`Outcome` instances.
    For example, a throw of 3 includes four one-roll :class:`Outcome` instances:
    Field, 3, any Craps, and Horn.



..  method:: Wheel.initialize(self) -> None



    Creates the 8 one-roll :class:`Outcome`
    instances (2, 3, 7, 11, 12, Field, Horn, Any Craps). It then creates
    the 36 :class:`Throw` objects, each of which has the appropriate
    combination of :class:`Outcome` instances.


Table Class Design
------------------

The :class:`Table` class contains all the :class:`Bet` instances created by the :class:`Player`.
A table has an association with a :class:`Game`, which is
responsible for validating individual bets. A table also has betting
limits, and the sum of all of a player's bets must be within this limits.

Fields
~~~~~~~

..  attribute:: Table.minimum

    This is the table lower limit. The sum of a :class:`Player`'s
    bets must be greater than or equal to this limit.

..  attribute:: Table.maximum

    This is the table upper limit. The sum of a :class:`Player`'s
    bets must be less than or equal to this limit.

..  attribute:: Table.bets

    This is a :class:`LinkedList` of the :class:`Bet` instances
    currently active. These will result in either wins or losses to the :class:`Player`.
    :noindex:

..  attribute:: Table.game

    The :class:`Game` used to determine if a given bet is allowed in
    a particular game state.


Constructors
~~~~~~~~~~~~~~


..  method:: Table.__init__(self) -> None
    :noindex:


    Creates an empty :class:`list` of bets.


Methods
~~~~~~~~


..  method:: Table.setGame(self, game: Game) -> None


    Saves the given :class:`Game` instance to be
    used to validate bets.


..  method:: Table.isValid(self, bet: Bet) -> bool



    Validates this bet. The first test checks the :class:`Game`
    to see if the bet is valid.




..  method:: Table.allValid(self) -> bool


    Validates the
    sum of all bets within the table limits. Returns false if the
    minimum is not met or the maximum is exceeded.




..  method:: Table.placeBet(self, bet: Bet) -> bool


    Adds this bet to
    the list of working bets. If the sum of all bets is greater than the
    table limit, then an exception should be raised.
    This is a rare circumstance, and indicates a bug in the :class:`Player`
    more than anything else.



..  method:: Table.__iter__(self) -> Iterator[Bet]



    Returns an :class:`Iterator`
    over the list of bets. This gives us the freedom to change the
    representation from :class:`list` to any other :class:`Collection`
    with no impact to other parts of the application.

    We could simply return the list object itself.
    This may, in the long run, prove to be a limitation.
    It's handy to be able to simply iterate over a table
    and example all of the bets.



..  method:: Table.__str__(self) -> str


    Reports on all of the currently placed bets.


Player Class Design
-------------------

The :class:`Player` class places bets in a game. This an
abstract class, with no actual body for the :meth:`placeBets`
method. However, this class does implement the basic :meth:`win` and
:meth:`lose` methods used by all subclasses.


**Roulette Player Hierarchy**. The classes in the Roulette Player
hierarchy need to have their superclass adjusted to conform to the
newly-defined superclass. The former :class:`Passenger57` class is renamed to
:class:`RoulettePlayer`. All of the various Roulette players become
subclasses of the new :class:`RoulettePlayer` class.


In addition to renaming the :class:`Player1326` class to :class:`Roulette1326`,
we will also have to change the references in the various classes of the
:class:`Player1326State` class hierarchy. We suggest leaving the
class names alone, but merely changing the references within those five
classes from :class:`Player1326` to :class:`Roulette1326`.


**Craps Player Hierarchy**. The classes in the Craps Player hierarchy need
to have their superclass adjusted to conform to the newly-defined
superclass. We can rename :class:`CrapsPlayerMartingale` to :class:`CrapsMartingale`,
and make it a subclass of :class:`CrapsPlayer`. Other than names,
there should be no changes to these classes.


Fields
~~~~~~~~

..  attribute:: Player.stake

    The player's current stake. Initialized to the player's starting budget.


..  attribute:: Player.roundsToGo

    The number of rounds left to play. Initialized by the overall
    simulation control to the maximum number of rounds to play. In
    Roulette, this is spins. In Craps, this is the number of throws of
    the dice, which may be a large number of quick games or a small
    number of long-running games. In Craps, this is the number of cards
    played, which may be large number of hands or small number of
    multi-card hands.

..  attribute:: Player.table

    The :class:`Table` object used to place individual :class:`Bet` instances.


Constructors
~~~~~~~~~~~~~


..  method:: Player.__init__(self, table: Table) -> None


    Constructs the :class:`Player` with a specific :class:`Table`
    for placing :class:`Bet` instances.


Methods
~~~~~~~~~



..  method:: Player.playing(self) -> bool


    Returns :literal:`True`
    while the player is still active. There are two reasons why a player
    may be active. Generally, the player has a :obj:`stake` greater
    than the table minimum and has a :obj:`roundsToGo` greater than
    zero. Alternatively, the player has bets on the table; this will
    happen in craps when the game continues past the number of rounds budgeted.



..  method:: Player.placeBets(self) -> Bool


    Updates the :class:`Table`
    with the various :class:`Bet` instances.

    When designing the :class:`Table`, we decided that we needed to
    deduct the amount of a bet from the stake when the bet is created.
    See the Table :ref:`roul.table.ov` for more information.


..  method:: Player.win(self, bet: Bet) -> None


    Notification from the :class:`Game`
    that the :class:`Bet` was a winner. The amount of money won is
    available via :meth:`bet.winAmount`.



..  method:: Player.lose(self, bet: Bet) -> None


    Notification from the :class:`Game`
    that the :class:`Bet` was a loser.


Game Class Design
-----------------

An instance of the :class:`Game` class manages the sequence of actions that defines casino
games, including Roulette, Craps and Blackjack. Individual subclasses
implement the detailed playing cycles of the games. This superclass has
methods for notifying the :class:`Player` instance to place bets, getting a
new :class:`RandomEvent` instance
and resolving the :class:`Bet` objects actually present on the :class:`Table` instance.


Fields
~~~~~~

..  attribute:: Game.eventFactory

    Contains a :class:`Wheel` or :class:`Dice` or other subclass of
    :class:`RandomEventFactory` that returns a randomly selected :class:`RandomEvent`
    with specific :class:`Outcome` s that win or lose.


..  attribute:: Game.table

    Contains a :class:`Table` instance which
    holds all the :class:`Bet` instances placed by the :class:`Player` object.

..  attribute:: Game.player

    Holds  the :class:`Player` object, responsible for placing bets on the :class:`Table`.


Constructors
~~~~~~~~~~~~

We based this constructor on an design that allows any of these
objects to be replaced. This is the **Strategy** (or **Dependency Injection**) design
pattern. Each of these objects is a replaceable strategy, and can be
changed by the client that uses this game.

Additionally, we specifically do not include the :class:`Player`
instance in the constructor. The :class:`Game` instance exists
independently of any particular :class:`Player` object.



..  method:: Game.__init__(self, eventFactory: RandomEventFactory, table: Table) -> None
    :noindex:


    Constructs a new :class:`Game`, using a given :class:`RandomEventFactory`
    and :class:`Table`.


Methods
~~~~~~~~



..  method:: Game.cycle(self, player: Player) -> None



    This will
    execute a single cycle of play with a given :class:`Player`.
    For Roulette it is a single spin of the wheel. For Craps, it is a
    single throw of the dice, which is only one part of a complete game.
    This method will call :meth:`player.placeBets`
    to get bets. It will call :meth:`eventFactory.next`
    to get the next set of :class:`Outcome` instances. It will then call
    :meth:`table.bets` to get an :class:`Iterator` over the :class:`Bet` instances.
    Stepping through this :class:`Iterator` returns the individual
    :class:`Bet` objects. The bets are resolved, calling the :meth:`Player.win`
    or :meth:`Player.lose`.



..  method:: Game.reset(self) -> None


    As a useful default for
    all games, this will tell the table to clear all bets. A subclass
    can override this to reset the game state, also.


RouletteGame Class Design
-------------------------

The :class:`RouletteGame` is a subclass of the :class:`Game` class that
manages the sequence of actions that defines the game of Roulette.


Methods
~~~~~~~~


..  method:: RouletteGame.cycle(self, player: Player) -> None


    This will execute a single cycle of the
    Roulette with a given :class:`Player` instance. It will call
    :meth:`player.placeBets` to get bets. It will call
    :meth:`wheel.next` to get the next winning :class:`Bin`. It
    will then call  :meth:`table.bets` to get an :class:`Iterator`
    over the :class:`Bet` instances. Stepping through this :class:`Iterator`
    returns the individual :class:`Bet` objects. If the winning :class:`Bin`
    contains the :class:`Outcome`, call the :meth:`Player.win`
    otherwise call :meth:`Player.lose`.


CrapsGame Class Design
----------------------

The :class:`CrapsGame` is a subclass of the :class:`Game` class that manages
the sequence of actions that defines the game of Craps.

Note that a single cycle of play is one throw of the dice, not a
complete craps game. The state of the game may or may not change.


Methods
~~~~~~~~



..  method:: RouletteGame.cycle(self, player: Player) -> None


    This will execute a single cycle of play
    with a given :class:`Player`.

    #.  It will call :meth:`Player.placeBets` to get
        bets. It will validate the bets, both individually, based on the
        game state, and collectively to see that the table limits are met.

    #.  It will call :meth:`Dice.next` to get the
        next winning :class:`Throw`.

    #.  It will use the :meth:`Throw.updateGame`
        to advance the game state.

    #.  It will then call :meth:`Table.bets` to get an
        :class:`Iterator`; stepping through this :class:`Iterator`
        returns the individual :class:`Bet` objects.

        -   It will use the :class:`Throw` object's :meth:`resolveOneRoll`
            method to check one-roll propositions. If the method returns
            true, the :class:`Bet` is resolved and should be deleted.

        -   It will use the :class:`Throw` object's :meth:`resolveHardways`
            method to check the hardways bets. If the method returns
            true, the :class:`Bet` is resolved and should be deleted.



..  method:: CrapsGame.pointOutcome(self) -> Outcome
    :noindex:


    Returns an :class:`Outcome` instance
    based on the current point. This is used to create Pass Line Odds or
    Don't Pass Odds bets. This delegates the real work to the current :class:`CrapsGameState`
    object.




..  method:: CrapsGame.moveToThrow(self, bet: Bet, throw: Throw) -> None
    :noindex:


    Moves a Come Line or Don't Come Line bet
    to a new :class:`Outcome` based on the current throw. This delegates
    the move to the current :class:`CrapsGameState` object.

    This method should -- just as a precaution -- assert that the
    value of :obj:`theThrow` is 4, 5, 6, 8, 9 or 10.  These
    point values indicate that a Line bet can be moved.
    For other values of :obj:`theThrow`, this method should raise an
    exception, since there's no reason for attempting to move a line bet
    on anything but a point throw.



..  method:: CrapsGame.reset(self) -> None
    :noindex:


    This will reset the game
    by setting the state to a new instance of the :class:`GamePointOff` class.
    It will also tell the table to clear all bets.



Refactoring Deliverables
-------------------------

There are six deliverables for this exercise.

-   If necessary, create :class:`RandomEvent`, and revisions to :class:`Throw`
    and :class:`Bin`. See :ref:`craps.throwbuilder.design.heavy` .

-   Create :class:`RandomEventFactory`, and associated changes to :class:`Wheel`
    and :class:`Dice`. The existing unit tests will confirm that
    this change has no adverse effect.

-   Refactor :class:`Table` and :class:`CrapsTable` to make a
    single class of these two. The unit tests for the original :class:`CrapsTable`
    should be merged with the unit tests for the original :class:`Table`.

-   Refactor :class:`Player` and :class:`CrapsPlayer` to create
    a better class hierarchy with :class:`CrapsPlayer` and :class:`RoulettePlayer`
    both sibling subclasses of :class:`Player` . The unit tests
    should confirm that this change has no adverse effect.

-   Refactor :class:`Game` and :class:`CrapsGame` to create
    three classes: :class:`Game`, :class:`RouletteGame` and :class:`CrapsGame`.
    The unit tests should confirm that this change has no adverse effect.

-   Create a new main program class that uses the existing :class:`Simulator`
    with the :class:`CrapsGame` and :class:`CrapsPlayer` classes.

Looking Forward
-----------------

Now that we have a more organized and symmetric class hierarchy, we can
look again again at the variety of play options available in Craps.
In the next chapter, we'll implement a number of simple Craps players with
different strategies.
