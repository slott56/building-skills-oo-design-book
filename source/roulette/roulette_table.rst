
..  _`roul.table`:

Roulette Table Class
====================

This section provides the design for the :class:`Table` class to hold the
bets.  In the section `Roulette Table Analysis`_ we'll look at the
table as a whole.

One of the table's responsibilities seems to be to validate
bets. In `InvalidBet Exception Design`_ we'll look at how we can
design an appropriate exception.

In `Roulette Table Design`_ we'll look at the details of creating
the table class. Then, in `Roulette Table Deliverables`_ we'll enumerate
the deliverables for this chapter.

..  _`roul.table.ov`:

Roulette Table Analysis
------------------------

We'll look at several topics in detail as part of the analysis
of the table.

-   `Winning vs. Losing`_ explores how we handle the payment
    of a bet and the receipt of the winnings.

-   In `Container Implementation`_ we'll look at how we store
    bets.

-   We'll look at casino betting limits in `Table Limits`_.

-   The `Adding and Removing Bets`_ section discusses some
    additional details of how the bet container must work.


The :class:`Table` object has the responsibility to keep the :class:`Bet` instances
created by the :class:`Player` object. Additionally, the house imposes
table limits on the minimum amount that must be bet and the
maximum that can be bet. A :class:`Table` object has all the
information required to evaluation these conditions.


..  note:: Betting Constraints

    Casinos prevent the :emphasis:`Martingale` betting system from
    working by imposing a table limit on each game. To cover the cost of
    operating the table game, the casino also imposes a minimum bet.
    Typically, the maximum is a multiplier of the minimum bet, often in
    the range of 10 to 50; a table with a $5 minimum might have a $200
    limit, a $10 minimum may have only a $300 limit.


It isn't clear where the responsibility lies for determining winning and
losing bets. The money placed on :class:`Bet` instances on the :class:`Table` instance
is "at risk" of being lost. If the bet is a winner, the house
pays the :class:`Player` object an amount based on the :class:`Outcome` object's
odds and the :class:`Bet` object's amount. If the bet is a loser, the
amount of the :class:`Bet` amount is forfeit by the :class:`Player` object.

It's important to see how the behavior of the simulation as a whole
emerges from the interaction of the various objects. This question
of responsibility is central to all OO design. Indeed, the rich
complexity of this simulation stems directly from the complexity
of human interactions over wagering.

Looking forward to stateful games like Craps, we'll place the
responsibility for determining winners and losers with a yet-to-be-defined :class:`Game` class,
and not with the :class:`Table` object. The :class:`Table` class is a passive container
for :class:`Bet` instances. The :class:`Game` will handle the details of winning
and losing.

We'll wait, then, until we write the :class:`Game` class to finalize paying winning
bets and collecting losing bets.

Winning vs. Losing
~~~~~~~~~~~~~~~~~~

Another open question is the timing of the payment for the bet from
the player's stake. In a casino, the payment to the casino -- effectively --
happens when the bet is
placed on the table. In our Roulette simulation, this is a subtlety that
doesn't have any practical consequences. We could deduct the money as
part of :class:`Bet` object creation, or we could deduct the money as part of resolving
the spin of the wheel.

In other games, however, there may several events
and several opportunities for placing additional bets. For example, splitting a
hand in Blackjack, or placing additional odds bets in Craps.
We can't allow a player to bet more than their stake; therefore,
we should deduct the payment as the :class:`Bet` instance is created.


A consequence of this is a change to our definition of the :class:`Bet`
class. We don't need to compute the amount that is lost. We're not going
to deduct the money when the bet resolved, we're going to deduct  the money
from the :class:`Player` object's stake as part of creating the :class:`Bet` instance.
This will become part of the design of the :class:`Player` class and :class:`Bet` class.

Looking forward a little, a stateful game like Craps will introduce a
subtle distinction that may be appropriate for a future subclass of :class:`Table`.
In Craps, some bets are "not working" or "working" depending on the game
state. Additionally, some :class:`Outcome` instances are permitted only
in certain game states. None of this subtlety applies to Roulette, however.

Container Implementation
~~~~~~~~~~~~~~~~~~~~~~~~

A :class:`Table` object holds a collection of :class:`Bet` instances.
We need to choose a concrete class for the collection of the bets. We
can review the survey of collections in :ref:`roul.bin.collections` for
some guidance.

In this case, the bets are placed in no particular
order, and are simply visited in an arbitrary order for resolution.  Bets don't
have specific names.


Since the number of
bets varies, we can't use a Python :class:`tuple`; a :class:`list`
will have to do. We could also use a :class:`set` because duplicate bets
don't make any sense; the amounts should be combined.


Table Limits
~~~~~~~~~~~~

Table limits can be checked by providing a public method :meth:`isValid`
that compares the total of all existing :class:`Bet` instances
against the table limit. This should be used by the :class:`Game` class
and the :class:`Player` class to confirm that bets are legal before proceeding.


In the unlikely event of the :class:`Player` object creating an illegal
:class:`Bet` instance, this will raise an exception to indicate
that we have a design error that was not detected via unit testing. This
exception should be a subclass of :class:`Exception` that has enough
information to debug the problem with the :class:`Player` object's state that
lead to placing an illegal bet.

Each individual :class:`Bet` instance must meet the :class:`Table` instance minimum.
This is a separate rule that can be checked each time a bet is placed.

Adding and Removing Bets
~~~~~~~~~~~~~~~~~~~~~~~~~

A :class:`Table` object contains :class:`Bet` instances;
the bets are added by the :class:`Player` class. Later,
:class:`Bet` instances will be removed from the :class:`Table` object by the :class:`Game` class.
When a bet is resolved, it must be deleted. Some games, like Roulette
resolve all bets with each spin. Other games, like Craps, involve
multiple rounds of placing and resolving some bets, and leaving other
bets in play.

For bet deletion to work, we have to provide a method to remove a :class:`Bet` instance.
When we look at game and bet resolution we'll return to bet deletion.
It's import not to over-design this class at this time; we will often
add features as we develop designs for additional use cases.


InvalidBet Exception Design
-----------------------------

We'll raise an exception for an invalid bet. This is, in general,
better than having a method which returns :literal:`True` for a valid bet
and :literal:`False` for an invalid bet.

Exceptions are better because we can simply place the bet, assuming
that it is valid. The processing continues along this "happy path".

If the bet is not valid, the exception interrupts processing.
The only way to get an invalid bet in Roulette is to have a badly
damaged implementation of the :class:`Player` class. We really need
to have the application break in a catastrophic manner.

The general principle is often described as "It's Easier to Ask Forgiveness Than To Ask Permission."
This is is implemented via exception-handling in Python.

..  exception:: InvalidBet

    :exc:`InvalidBet` is raised when a :class:`Player` instance
    attempts to place a bet which exceeds the table's limit.

    This class simply inherits all features of its superclass.


Roulette Table Design
-----------------------

..  class:: Table

    :class:`Table` contains all the :class:`Bet` instances created by a :class:`Player` object.
    A table also has a betting limit, and the sum of all of a player's
    bets must be less than or equal to this limit. We assume a single :class:`Player` object
    in the simulation.


Fields
~~~~~~~

..  attribute:: Table.limit

    This is the table limit. The sum of the bets from a :class:`Player` object
    must be less than or equal to this limit.

..  attribute:: Table.minimum
    :noindex:

    This is the table minimum. Each individual bet from a :class:`Player` object
    must be greater than this limit.


..  attribute:: Table.bets
    :noindex:

    This is a :class:`list` of the :class:`Bet` instances
    currently active. These will result in either wins or losses to the :class:`Player` object.


Constructors
~~~~~~~~~~~~~


..  method:: Table.__init__(self, *bets) -> None

    Creates an empty :class:`list` of bets. If the

    :param bets: A sequence of :class:`Bet` instances to
        initialize the table. If omitted, an empty :class:`list` will be used.


Methods
~~~~~~~


..  method:: Table.placeBet(self, bet: Bet) -> None
    :noindex:

    :param bet: A :class:`Bet` instance to be added to the table.
    :type bet: :class:`Bet`

    :raises: InvalidBet


    Adds this bet to the list of working bets.

    We'll reserve the idea of raising an exception for an individual invalid
    bet.  This is a rare circumstance, and indicates a bug in the :class:`Player` class
    more than anything else.

    We might, for example, confirm that the bet's :class:`Outcome` instance exists
    in one of the :class:`Bin` instances. We might check that the bet amount is
    greater than or equal to the table minimum.
    We might also check the upper limit on betting will be honored by
    all existing bets plus this new bet.

    It's not **necessary** to validate each bet as they're being placed. It's only necessary
    to validate the bets prior to spinning the wheel. This can be a feature
    of the :class:`Game` class.

    For an interactive game -- not a simulation -- we would want to validate
    each bet prior to accepting it so that we can provide an immediate response to the player
    that the potential bet is invalid. In this case, we'd leave the table
    untouched when a bad bet is offered.

..  method:: Table.__iter__() -> Iterator[Bet]
    :noindex:

    Returns an iterator over the available list of :class:`Bet`
    instances. This simply returns the iterator over the list of :class:`Bet` objects.

    Note that we need to be able remove bets from the table.
    Consequently, we have to update the list, which requires that we create
    a copy of the list.  This is done with :samp:`self.bets[:]`.

    This special method is invoked by the :func:`iter` built-in function.

    :return: iterator over all bets


..  method:: Table.__str__(self) -> str
    :noindex:

    Return an easy-to-read string representation of all current bets.

..  method:: Table.__repr__(self) -> str

    Return a representation of the form :samp:`Table({bet}, {bet}, ...)`.

Note that we will want to segregate validation as a separate method,
or sequence of methods. This is used by the Game just prior to
spinning the wheel (or rolling the dice, or drawing a next card.)

..  method:: Table.isValid(self)
    :noindex:

    :raises: :class:`InvalidBet` if the bets don't pass the table limit rules.

    Applies the table-limit rules:

    -   The sum of all bets is less than or equal to the table limit.

    -   All bet amounts are greater than or equal to the table minimum.

    If there's a problem an :exc:`InvalidBet` exception is raised.

Roulette Table Deliverables
----------------------------

There are three deliverables for this exercise. Each of these will have
complete Python docstring comments.

-   An :exc:`InvalidBet` exception class. This is a simple
    subclass of :class:`Exception`.

-   Since there's no unique programming here, the unit test for
    the :exc:`InvalidBet` exception.
    is pretty simple. Indeed, it can seem silly to be sure that this
    class works with the :code:`raise` statement; however, failure to extend
    :exc:`Exception` would lead to a program that more-or-less worked until
    a faulty :class:`Player` class caused the invalid bet situation.

-   The :class:`Table` class.

-   A class which performs a unit test of the :class:`Table` class.
    The unit test should create at least two instances of :class:`Bet`,
    and establish that these :class:`Bet` instances are managed by the
    table correctly.

Looking Forward
----------------

We deferred the question of winning and losing to a :class:`Game` class.
Previously, we've used the rather ambiguous name :class:`Game`. As we move forward,
it's time to rethink the name and be more specific about the class.
In the next chapter we'll look at the definition of the Roulette game as a whole.
