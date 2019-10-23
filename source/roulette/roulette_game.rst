
..  _`roul.game`:

Roulette Game Class
===================

Between the :class:`Player` class and the :class:`Game` class, we have a
chicken-and-egg design problem: it's not clear
which we should do first. In this chapter,
we'll describe the design for :class:`Game` in detail. However, in
order to create the deliverables, we have to create a version of :class:`Player`
that we can use to get started.

In the long run, we'll need to create a sophisticated hierarchy of players.
Rather than digress too far, we'll create a simple player, :class:`Passenger57` (they always
bet on black), which will be the basis for further design in later chapters.

The class that implements the game will be examined in `Roulette Game Analysis`_.

Once we've defined the game, we can also define a simple player class
to interact with the game. We'll look at this in `Passenger57 Design`_.

After looking at the player in detail, we can look at the game in detail.
We'll examine the class in `Roulette Game Design`_.

We'll provide some additional details in `Roulette Game Questions and Answers`_.
The `Roulette Game Deliverables`_ section will enumerate the deliverables.

There are a few variations on how Roulette works.
We'll look at how we can include these details in the `Appendix: Roulette Variations`_ section.

Roulette Game Analysis
-----------------------

The :class:`Game`'s responsibility is to cycle through the
various steps of a defined procedure. We'll look at the procedure
in detail. We'll also look at how we match bets in `The Bet Matching Algorithms`_.
This will lead us to define the player interface, which we'll look at in
`Player Interface`_.


This is an :emphasis:`active` class that makes use of the classes we have built so far.
The hallmark of an active class is longer or more complex methods. This is distinct
from most of the classes we have considered so far, which have
relatively trivial methods that are little more than collections of related
instance variables.

The procedure for one round of the game is the following.

..  rubric::  A Single Round of Roulette

1.  **Place Bets**.
    Notify the :class:`Player` object to create :class:`Bet` instances. The real
    work of placing bets is delegated to the :class:`Player` class. Note
    that the money is committed at this point; the player's stake should be
    reduced as part of creating a :class:`Bet` object.

2.  **Spin Wheel**.
    Get the next spin of the :class:`Wheel` instance,
    giving the winning :class:`Bin` object, :emphasis:`w`.
    This is a collection of individual :class:`Outcome` instances.
    Any :class:`Bet` instance with a winning outcome is a winner.
    We can say :math:`w = \{o_0, o_1, o_2, ..., o_n\}`: the winning bin
    is a set of outcomes.

3.  **Resolve All Bets**.

    For each :class:`Bet`, :emphasis:`b`, placed by the :class:`Player`:

    1.  **Winner?**
        If the  :class:`Outcome` object of :class:`Bet`, :emphasis:`b`, is in the winning
        :class:`Bin`, :emphasis:`w`, then notify the :class:`Player` object that
        :class:`Bet` :emphasis:`b` was a winner and update the :class:`Player` object's stake.

    2.  **Loser?**
        If the  :class:`Outcome` object of :class:`Bet`, :emphasis:`b`, is not in the winning
        :class:`Bin`, :emphasis:`w`, then notify the :class:`Player` that
        :class:`Bet` :emphasis:`b` was a loser. This allows the :class:`Player`
        to update the betting amount for the next round.


The Bet Matching Algorithms
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This :class:`Game` class will have the responsibility for matching the
collection of :class:`Outcome` instances in the :class:`Bin` object of the :class:`Wheel` object
with the :class:`Outcome` attributes of the collection of :class:`Bet` instances
on the :class:`Table` object.
We'll need to structure a loop to compare individual elements from these two collections.
There are two common ways to iterate through the bets and outcomes:

-   Driven by :class:`Bin` object contents.
    We can visit each :class:`Outcome` instance in the winning :class:`Bin` object.

-   Driven by :class:`Table` object contents.
    We can to visit each :class:`Bet` instance contained by the :class:`Table` object.

We'll look at each algorithm to select the best choice.

To examine each :class:`Outcome` object in the winning :class:`Bin` object,
we'll use code like the following.

    For each :class:`Outcome` instance in the winning :class:`Bin` object, :math:`o`:

        For each  :class:`Bet` instance contained by the :class:`Table` object, :math:`b`:

            If the :class:`Outcome` instance of the :class:`Bet` instance
            matches the :class:`Outcome` instance in the
            winning :class:`Bin` object (:math:`o = b`),
            this bet, :math:`b`, is  a winner and is paid off.
            The winnings are the amount of the bet multiplied by the odds of the outcome.

After this examination, all :class:`Bet` instances which have not been paid off are losers.
This is unpleasantly complex because we can't resolve a :class:`Bet` instance until we've
checked all :class:`Outcome` instances in the winning :class:`Bin` object.


To examine each :class:`Outcome` object in the :class:`Bet` instances within the :class:`Table` object,
we'll use code like the following.

    For each :class:`Bet` instance in the :class:`Table` object, :math:`b`:

        If the :class:`Outcome` attribute of :math:`b` is in
        the :class:`Outcome` instances in the winning :class:`Bin`,
        the bet is a winner.
        The winnings are the amount of the bet multiplied by the odds of the outcome.
        If the :class:`Outcome` is not in the :class:`Bin`, the
        bet is a loser.

This is simpler because the winning :class:`Bin` instance is a frozenset of :class:`Outcome` instances,
we can exploit set membership methods to test for presence or absence
of the :class:`Outcome` instance for a  :class:`Bet` object in the winning :class:`Bin` instance.

Player Interface
~~~~~~~~~~~~~~~~~~

The :class:`Game` class and :class:`Player` class collaboration involves mutual dependencies.
This creates a "chicken and egg" problem in decomposing the
relationship between these classes. The :class:`Player` class depends on
:class:`Game` class features. The :class:`Game` class depends on :class:`Player` class
features.

Which do we design first?

We note that the :class:`Player` class
is really a complete hierarchy of subclasses, each of which provides a
different betting strategy. For the purposes of making the :class:`Game` class
work, we can develop our unit tests with a stub for the :class:`Player` class
that simply places a single kind of bet. We'll call this player
"Passenger57" because it always bets on Black.

Once we have a simplistic player, we can define the :class:`Game` class more
completely.

After we have the :class:`Game` class finished, we can then revisit this design
to make more sophisticated subclasses of :class:`Player` class. In effect,
we'll bounce back and forth between :class:`Player` class and :class:`Game` class, adding
features to each as needed.

For some additional design considerations, see :ref:`roul.game.ov.additional`.
This provides some more advanced game options that our current design
can be made to support. We'll leave this as an exercise for the more
advanced student.

..  _`roul.game.design.passenger57`:

Passenger57 Design
------------------------

..  class::  Passenger57

    :class:`Passenger57` constructs a :class:`Bet` instance
    based on the :class:`Outcome` object named :literal:`"Black"`.
    This is a very persistent player.

    We'll need a source for the Black outcome. We have several choices; we
    looked at these in :ref:`roul.bet`. We will query the :class:`Wheel` object
    for the needed :class:`Outcome` object.

In the long run, we'll have to define a :class:`Player` superclass,
and make :class:`Passenger57` class a proper subclass of :class:`Player` class.
Since our focus is on getting the :class:`Game` class designed and built,
we'll set this consideration aside until later.

Fields
~~~~~~~~

..  attribute:: Passenger57.black

    This is the outcome on which this player focuses their betting.

    This :class:`Player`
    will get this from  the :class:`Wheel` using a well-known bet name.

..  attribute:: Passenger57.table

    The :class:`Table` that is used to place individual :class:`Bet` instances.


Constructors
~~~~~~~~~~~~~


..  method:: Passenger57.__init__(self, table: Table, wheel: Wheel) -> None

    :param table: The :class:`Table` instance on which bets are placed.
    :type table: :class:`Table`

    :param wheel: The :class:`Wheel` instance which defines all :class:`Outcome` instances.
    :type wheel: :class:`Wheel`

    Constructs the :class:`Player` instance with a specific table for placing
    bets. This also creates the "black" :class:`Outcome`.
    This is saved in a variable named :attr:`Passenger57.black`  for use in creating bets.


Methods
~~~~~~~~


..  method:: Passenger57.placeBets(self) -> None


    Updates the :class:`Table` object
    with the various bets. This version creates a :class:`Bet`
    instance from the "Black" :class:`Outcome` instance. It uses
    :meth:`Table.placeBet` to place that bet.


..  method:: Passenger57.win(self, bet: Bet) -> None

    :param bet: The bet which won.
    :type bet: :class:`Bet`


    Notification from the :class:`Game` object
    that the :class:`Bet` instance was a winner. The amount of money won is
    available via a the :meth:`Bet.winAmount` method.



..  method:: Passenger57.lose(self, bet: Bet) -> None

    :param bet: The bet which won.
    :type bet: :class:`Bet`

    Notification from the :class:`Game` object
    that the :class:`Bet` instance was a loser.


Roulette Game Design
---------------------------

..  class:: Game

    :class:`Game` manages the sequence of actions that defines the game
    of Roulette. This includes notifying the :class:`Player` object to place
    bets, spinning the :class:`Wheel` object and resolving the :class:`Bet` instances
    actually present on the :class:`Table` object.


Fields
~~~~~~

..  attribute:: wheel

    The :class:`Wheel` instance that returns a randomly selected :class:`Bin` object of
    :class:`Outcome` instances.

..  attribute:: table

    The :class:`Table` object which contains the :class:`Bet` instances placed by the :class:`Player` object.

..  attribute:: player

    The :class:`Player` object which creates :class:`Bet` instances at the :class:`Table` object.


Constructors
~~~~~~~~~~~~

We based the Roulette Game constructor on a design that allows any of the
fields to be replaced. This is the **Strategy** design
pattern. Each of these collaborating objects is a replaceable strategy, and can be
changed by the client that uses this game.

Additionally, we specifically do not include the :class:`Player`
instance in the constructor. The :class:`Game` exists
independently of any particular :class:`Player`, and we defer
binding the :class:`Player` and :class:`Game` until we are
gathering statistical samples.


..  method:: Game.__init__(self, wheel: Wheel, table: Table) -> None

    :param wheel: The :class:`Wheel` instance which produces random events
    :type wheel: Wheel

    :param table: The :class:`Table` instance which holds bets to be resolved.
    :type table: Table


Constructs a new :class:`Game`, using a given :class:`Wheel`
and :class:`Table`.


Methods
~~~~~~~~


..  method:: Game.cycle(self, player: Player) -> None
    :noindex:

    :param player: the individual player that places bets, receives winnings and pays losses.
    :type player: :class:`Player`

    This will execute a single cycle of play
    with a given :class:`Player`. It will execute the following steps:

    1.  Call :meth:`Player.placeBets` method to create bets.
    2.  Call :meth:`Wheel.choose` method to get the next winning :class:`Bin` object.
    3.  Call :func:`iter` on the :obj:`table` to get all of the :class:`Bet` instances.
        For each :class:`Bet` instance, if the winning :class:`Bin` contains the
        :class:`Outcome`, call :meth:`Player.win` method,
        otherwise, call the :meth:`Player.lose` method.

Roulette Game Simplification
----------------------------

The essence of the :class:`Game` class includes a large number
of complex methods, but relatively few fields and a very simple constructor.

It may make sense to consider using a ``@dataclass`` definition for this
class. It's not completely clear that all of the various dataclass features
are particularly useful here. The principle benefit seems to be eliminating
the need to write the tiny :meth:`Game.__init__` method.

Roulette Game Questions and Answers
------------------------------------

Why are a :class:`Table` object and :class:`Wheel` object part of the
constructor for :class:`Game` class,
while a :class:`Player` object is given as a parameter for the :meth:`cycle`
method? Why not provide all of the objects as part of the constructor?


    We are making a subtle distinction between the casino table game (a
    Roulette table, wheel, plus casino staff to support it) and having a
    player step up to the table and play the game. The game exists without
    any particular player. By setting up our classes to parallel the
    physical entities, we give ourselves the flexibility to have multiple
    players without a significant rewrite. We allow ourselves to support
    multiple concurrent players or multiple simulations each using a
    different :class:`Player` instance, perhaps with different strategies.


    Also, as we look forward to the structure of the future simulation, we
    note that the game objects are largely fixed, but there will be a parade
    of variations for the players. We would like a main program that
    simplifies inserting a new player subclass with minimal disruption.


Why do we have to include the odds with the :class:`Outcome` class? This
pairing makes it difficult to create an :class:`Outcome` object from scratch.

    The odds are an essential ingredient in the :class:`Outcome` instance.
    It's not clear where else they can possibly go.

    Creating a new :class:`Outcome` instance to create a :class:`Bet` object
    is really a request for a simplified name of each :class:`Outcome` alternative.
    We have three ways to provide a short name:

    -   A variable name. We also need to put the variable in some kind
        of namespace. The :class:`Wheel`
        or the :class:`BinBuilder` make the most sense for owning this variable.

    -   A key in a mapping. We also need to allocate the mapping to
        some object. Again, the :class:`Wheel` or :class:`BinBuilder`
        make the most sense for owning the mapping of name to :class:`Outcome` instance.

    -   A method which returns an :class:`Outcome` object. The method can use
        a fixed variable or can get a value from a mapping.

    The :class:`Wheel` class shows up most often as a place to track
    the :class:`Outcome` instances. A method (or a mapping) in this class
    is an elegant way to track down the :class:`Outcome` instance required to build
    a :class:`Bet` object.


Roulette Game Deliverables
---------------------------

There are three deliverables for this exercise. The stub does not need
documentation, but the other classes do need complete Python docstrings.

-   The :class:`Passenger57` class. We will rework this design
    later. This class always places a bet on Black. Since this is simply
    used to test :class:`Game`, it doesn't deserve a very
    sophisticated unit test of its own. It will be replaced in a future exercise.

-   The :class:`Game` class.

-   A class which performs a demonstration of the :class:`Game`
    class. This demo program creates the :class:`Wheel` object, the stub :class:`Passenger57` object
    and the :class:`Table` object. It creates the :class:`Game` object
    and cycles a few times. Note that the :class:`Wheel` instance returns
    random results, making a formal test rather difficult. We'll address
    this testability issue in the next chapter.


..  _`roul.game.ov.additional`:

Appendix: Roulette Variations
------------------------------------------

In European casinos, the wheel has a single zero. In some
casinos, the zero outcome has a special :emphasis:`en prison`
rule: all losing bets are split and only half the money is lost,
the other half is termed a "push" and is returned to the player. The
following design notes discuss the implementation of this
additional rule.

This is a payout variation that depends on a single :class:`Outcome`.
We will need an additional subclass of :class:`Outcome`
that has a more sophisticated losing amount method: it would
push half of the amount back to the :class:`Player` to be added
to the stake.
We'll call this subclass the the :class:`PrisonOutcome` class.

In this case, we have a kind of hybrid resolution: it is a
partial loss of the bet. In order to handle this, we'll need to
have a :meth:`loss` method in :class:`Bet` as well as a
:meth:`win` method. Generally, the :meth:`loss`
method does nothing (since the money was removed from the :class:`Player`
stake when the bet was created.) However, for the :class:`PrisonOutcome`
class, the :meth:`loss` method returns half the money to the
:class:`Player`.

We can also introduce a subclass of :class:`BinBuilder` that
creates only the single zero, and uses this new :class:`PrisonOutcome`
subclass of :class:`Outcome` for that single zero. We can
call this the :class:`EuroBinBuilder`. The :class:`EuroBinBuilder`
does not create the five-way :class:`Outcome` of 00-0-1-2-3,
either; it creates a four-way for 0-1-2-3.

After introducing these two subclasses, we would then adjust :class:`Game`
to invoke the :meth:`loss` method of each losing :class:`Bet`,
in case it resulted in a push. For an American-style casino, the
:meth:`loss` method does nothing. For a European-style
casino, the :meth:`loss` method for an ordinary :class:`Outcome`
also does nothing, but the :meth:`loss` for a :class:`PrisonOutcome`
would implement the additional rule pushing half the bet back to the
:class:`Player`. The special behavior for zero then emerges
from the collaboration between the various classes.

We haven't designed the :class:`Player` yet, but we would
have to bear this push rule in mind when designing the player.

The uniform interface between :class:`Outcome` and :class:`PrisonOutcome`
is a design pattern called :emphasis:`polymorphism`. We will
return to this principle many times.

Looking Forward
----------------

We've almost got enough software to create detailed simulations of play.
What can be a struggle is creating appropriate unit tests for the
fairly complex collection of classes developed up to this point.

In the next chapter, we'll address the testing considerations required
to be sure the software works correctly. We'll also look at some of
the static analysis considerations that stem from using type hints
and the **mypy** tool.
