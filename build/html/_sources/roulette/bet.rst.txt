
..  _`roul.bet`:

Roulette Bet Class
===================

In addition to the design of the :class:`Bet` class, this chapter
also presents some additional questions and answers on the nature of an
object, identity and state change. This continues some of the ideas from :ref:`roul.outcome.identity`.

In `Roulette Bet Analysis`_ we'll look at the details of a :class:`Bet` instance.
This will raise a question of how to identify the :class:`Outcome` object
associated with a :class:`Bet` instance.

We'll look at object identity in `Design Decision -- Create or Locate an Outcome`_.

We'll provide some additional details in `Roulette Bet Questions and Answers`_.

The `Roulette Bet Design -- Complex`_ section will provide detailed design
for the Bet class. The `Roulette Bet Design -- Simple`_ section will provide
some advice for an alternative design based on ``@dataclass`` definitions.

In `Roulette Bet Deliverables`_ we'll enumerate the deliverables
for this chapter.

..  _`roul.bet.ov`:

Roulette Bet Analysis
----------------------

A :class:`Bet` object is an amount that the player has wagered on a specific
:class:`Outcome` instance. This class has the responsibility for maintaining
an association between an amount, an :class:`Outcome` object, and a specific
:class:`Player` object.

The general scenario is to have the :class:`Player` object construct a number of
:class:`Bet` instances. The :class:`Wheel` object is spun to select a winning :class:`Bin` instance.
Once a winning bin has been chosen, each of the :class:`Bet` objects will be checked to see if the
hoped-for :class:`Outcome` instance is in the actual set of :class:`Outcome` instances
in the winning :class:`Bin` object.

Each winning :class:`Bet` instance must have an :class:`Outcome` instance
that can be found in the winning :class:`Bin` object. The winning bets will adds
money to the :class:`Player` object. All other bets are not in the winning :class:`Bin` object;
they are losers, which removes money from the :class:`Player` object.

We have a design decision to make.  Do we create a fresh  :class:`Outcome` object
with each :class:`Bet` instance or do we locate an existing :class:`Outcome` object?

Design Decision -- Create or Locate an Outcome
-----------------------------------------------

Building a :class:`Bet` object involves two parts: an :class:`Outcome` object
and an amount. The amount is a number. The :class:`Outcome` object, however,
is more complex, and includes two parts: a name and payout odds.

We looked at this issue in :ref:`roul.outcome.factory`. We'll revisit this design
topic in some more depth here.

We don't want to create an :class:`Outcome` object as part of constructing a :class:`Bet` object.
Here's what it might look like to place a $25 bet on Red:

..  rubric:: Bad Idea

..  code-block:: python

    my_bet = Bet(Outcome("red", 1), 25)

The :class:`Bet` object includes an :class:`Outcome` object and an amount.
The :class:`Outcome` object includes a name and the payout odds.
We don't want to repeat payout odds
when creating an :class:`Outcome` object to create a :class:`Bet` object.
This violates the Don't Repeat Yourself (DRY) principle.

We want to get a complete :class:`Outcome` object from the name of the outcome.
The will prevent repeating the odds information.

**Problem**. How do we locate an existing :class:`Outcome` object?

Do we use a collection or a global variable? Or is there some other approach?

**Forces**. There are several parts to this design.

-   We need to identify some global object that can
    maintain the collection of :class:`Outcome` instances for use by the
    :class:`Player` object when building :class:`Bet` instances.

-   We need to create the global object that builds
    the collection of distinct :class:`Outcome` instances. This sounds a lot like the
    :class:`BinBuilder` class.


If the builder and maintainer are the same object, then things would be somewhat simpler
because all the responsibilities would fall into a single place.

We have several choices for the kind of global object we would use.

-   **Variable**. We can define a variable which is a global map from name to :class:`Outcome` instance.
    This could be an instance of the built-in :class:`dict` class to provide
    a mapping from name to complete :class:`Outcome` instance.
    It could be an instance of a class we've designed
    that maps names to :class:`Outcome` instances.

    A truly *variable* global is a dangerous thing. An immutable global
    object, however, is a useful idea.

    We might have this:

    ..  rubric:: Global Mapping

    ..  code-block:: python

        >>> some_map["Red"]
        Outcome('Red', 1)

-   **Function**. An alternative to a collection is a **Factory** function which will produce
    an :class:`Outcome` instance as needed.

    ..  rubric:: Factory Function

    ..  code-block:: python

        >>> some_factory("Red")
        Outcome('Red', 1)


-   **Class**. We can define class-level methods for emitting an instance
    of  :class:`Outcome` based on a name. We could, for example, add methods
    to the :class:`Outcome` class which retrieved instances from a class-level
    mapping.

    ..  rubric:: Class Method

    ..  code-block:: python

        >>> Outcome.getInstance("Red")
        Outcome('Red', 1)


After creating the :class:`BinBuilder` class, we can see that this fits the overall
**Factory** design for creating :class:`Outcome` instances.

However, the :class:`BinBuilder` class doesn't -- currently -- have a handy mapping to support looking up
an :class:`Outcome` object based on the name of an outcome.
Is this the right place to do the lookup?

It would look like this:

..  rubric:: BinBuilder as Factory

..  code-block:: python

    >>> theBinBuilder.getOutcome("Red")
    Outcome('Red', 1)

We could also make the case that it would fee in the the :class:`Wheel` class. It would look like this:

..  rubric:: Wheel as Factory

..  code-block:: python

    >>> theWheel.getOutcome("Red")
    Outcome('Red', 1)

**Alternative Solutions**.  We have a number of potential ways to gather all :class:`Outcome` objects
that were created by the :class:`BinBuilder` class.

-   Clearly, the :class:`BinBuilder` class can create the mapping
    from name to each distinct :class:`Outcome` instance.
    To do this, we'd have to do several things.

    First, we expand the :class:`BinBuilder` class to keep a simple Map of the
    various  :class:`Outcome` instances
    that are being assigned via the :meth:`Wheel.add` method.

    Second, we would have to add specific :class:`Outcome` instance
    getters to the :class:`BinBuilder` class. We could, for example, include a :meth:`getOutcome`
    method that returns an :class:`Outcome` object based on its name.

    Here's what it might look like in Python.

    ..  code-block:: python

        class BinBuilder:
            ...
            def save(self, outcome: Outcome, bin: int, wheel: Wheel) -> None:
                self.all_outcomes[outcome.name] = outcome
                wheel.add(bin, outcome)

            def getOutcome(self, name):
                return self.all_outcomes[name]
            ...


-   Access the :class:`Wheel` object.  A better choice is to get :class:`Outcome` objects from the :class:`Wheel`.
    To do this, we'd have to do several things.

    First, we expand the :class:`Wheel` class to keep a simple dict of the various  :class:`Outcome` instances
    created by a :class:`BinBuilder` object.  This dict would be updated by the :meth:`Wheel.add` method.

    Second, we would have to add specific :class:`Outcome`
    getter functions to the :class:`Wheel` class. We could, for example, include a :meth:`getOutcome`
    method that returns an :class:`Outcome` object based on the name string.

    We might write a method function like the following in the :class:`Wheel`.

    ..  code-block:: python

        class Wheel:
            ...
            def add(self, bin: int, outcome: Outcome) -> None:
                self.all_outcomes[outcome.name] = outcome
                self.bins[bin].add(outcome)

            def getOutcome(self, name):
                return self.all_outcomes[name]
            ...

**Solution**.
The allocation of responsibility seems to be a toss-up.  We can see that the amount of programming
is almost identical.  This means that the real question is one of clarity: which allocation
more clearly states our intention?

The :class:`Wheel` class is an essential part of the game of Roulette.  It showed up in our initial noun
analysis.  The :class:`BinBuilder` class was an implementation convenience to separate the one-time
construction of the :class:`Bin` instances from the overall work of the :class:`Wheel` object.

Since the :class:`Wheel` class is part of the problem, as well as part of the solution,
it seems better to augment the :class:`Wheel` class to keep track of our individual
:class:`Outcome` objects by name.

In the next sections, the questions and answers will look at some additional
design considerations. After that, we'll look at two versions of the design.
The complex version will build all of the methods; the simpler version
will rely on ``@dataclass``.

Roulette Bet Questions and Answers
----------------------------------

Why not update each :class:`Outcome` instance with the amount of the bet on that outcome?

    We are isolating the static definition of the :class:`Outcome` objects from
    the presence or absence of an amount wagered. Note that an :class:`Outcome` object
    is shared by the wheel's :class:`Bin` instances, and the available betting
    spaces on a :class:`Table` instance, and possibly even the :class:`Player`
    class. Also, if we have multiple :class:`Player` objects, then we need to
    distinguish bets placed by the individual players.

    Changing a field's value has an implication that the thing has changed
    state. In Roulette, there isn't any state change in an :class:`Outcome` instance.
    Neither the name nor the odds change.

    The odds
    associated with an outcome can't change; this is a fundamental principle of
    casino gambling. An outcome may be disabled by certain game states,
    but the payout must be well known to the players.

Does an individual bet really have unique identity? Isn't it just
anonymous money?

    Yes, the money is anonymous. In a casino, the chips all look alike.
    A :class:`Bet` is owned by a particular player, it lasts for a specific duration, it
    has a final outcome of won or lost. When we want to create summary
    statistics, we could do this by saving the individual :class:`Bet`
    objects.

    This points up another reason why we know a :class:`Bet` instance
    is distinct from the associated :class:`Outcome` object.
    A :class:`Bet` instance changes state; initially a bet is active,
    in some games they can be deactivated, eventually they are
    winners or losers.

    We don't need all of this state-change machinery for simulating
    Roulette. We will, however, see more complex bets when simulating
    Craps.


Roulette Bet Design -- Complex
------------------------------

..  class:: Bet

    :class:`Bet` associates an amount and an :class:`Outcome`. In a
    future round of design, we can also associate a :class:`Bet` with a :class:`Player`.

Fields
~~~~~~

..  attribute:: Bet.amountBet

    The amount of the bet.

..  attribute:: Bet.outcome

    The :class:`Outcome` on which the bet is placed.



Constructors
~~~~~~~~~~~~


..  method:: Bet.__init__(self, amount: int, outcome: Outcome) -> None
    :noindex:

    :param amount: The amount of the bet.
    :type amount: int

    :param outcome: The :class:`Outcome` we're betting on.
    :type outcome: :class:`Outcome`


    Create a new Bet of a specific amount on a specific outcome.

    For these first exercises, we'll omit the :class:`Player`. We'll come back to
    this class when necessary, and add that capability back in to this class.


Methods
~~~~~~~


..  method:: Bet.winAmount(self) -> int

    :returns: amount won
    :rtype: int


    Uses the :class:`Outcome`'s :class:`winAmount` to compute the amount won, given the
    amount of this bet. Note that the amount bet must also be added in.
    A 1:1 outcome (e.g. a bet on Red) pays the amount bet plus the
    amount won.



..  method:: Bet.loseAmount(self) -> int

    :returns: amount lost
    :rtype: int


    Returns the amount
    bet as the amount lost. This is the cost of placing the bet.



..  method:: Bet.__str__(self) -> str

    :returns: string representation of this bet with the form :samp:`"{amount} on {outcome}"`
    :rtype: str


    Returns a string representation of this bet. Note that this method
    will delegate the much of the work to the :meth:`__str__` method of the :class:`Outcome`.

..  method:: Bet.__repr__(self) -> str

    :returns: string representation of this bet with the form :samp:`"Bet(amount={amount}, outcome={outcome})"`
    :rtype: str

Roulette Bet Design -- Simple
-----------------------------

A simpler variation on the :class:`Bet` class can be
based on ``@dataclass``.

See above, in the  `fields`_ section, the two fields required.

The default methods created by the ``@dataclass`` decorator should work perfectly.

The :meth:`__str__` method will have to be written based on the description above,
under `methods`_.

This should pass all of the unit tests described in the `Roulette Bet Deliverables`_ section.


Wheel Redesign
---------------

We'll need to update the :class:`Wheel` class to have the following method.
This will return an :class:`Outcome` instance given the string name of
the outcome. This works by maintaining a dict of :class:`Outcome` objects using
the name attribute as a key. This is built incrementally
as each :class:`Bin` added to the :class:`Wheel` instance.

..  method:: Wheel.getOutcome(str: name) -> Outcome

    :param name: the name of an :class:`Outcome`
    :type name: str

    :returns: the :class:`Outcome` object
    :rtype: :class:`Outcome`

This should raise an exception if the string isn't the name of a known :class:`Outcome`.

Roulette Bet Deliverables
--------------------------

There are four deliverables for this exercise. The new classes will have
Python docstrings.

-   The expanded :class:`Wheel` class which creates a mapping of string name to :class:`Outcome`.

-   Expanded unit tests of :class:`Wheel` that confirm that the mapping is being built
    correctly.

-   The :class:`Bet` class.

-   A class which performs a unit test of the :class:`Bet` class.
    The unit test should create a couple instances of :class:`Outcome`,
    and establish that the :meth:`winAmount` and :meth:`loseAmount`
    methods work correctly.

Looking Forward
----------------

Once we have a useful definition of bets we have to work out how
to place them, and decide if they are winners or losers.
In the next chapter, we'll look at the :class:`Table` class as a container
for active :class:`Bet` instances.
