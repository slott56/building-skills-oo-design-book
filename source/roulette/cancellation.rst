
..  _`roul.cancellation`:

Cancellation Player Class
==========================

This section will describe a player who has a complex internal state
that can be modeled using existing library classes.

In `Cancellation Player Analysis`_ we'll look at what this player does.

We'll turn to how the player works in `PlayerCancellation Design`_.

In `Cancellation Player Deliverables`_ we'll enumerate the deliverables for
this player.

..  _`roul.cancellation.ov`:

Cancellation Player Analysis
-----------------------------

One method for tracking the lost bets is called the "cancellation"
system or the "Labouchere" system.

The bets are designed around an ascending sequence of
values, :math:`[1, 2, 3, 4, 5, 6]`. The sum, 21, is the total budget.
Each bet will be a multiple of the table minimum, :math:`b`.
The core principle is to bet on the sum of the numbers at the end
of the sequence.

In this example, the end values of of the sequence are :math:`1+6`,
leading the player to bet :math:`7 \times b`.

On a win, the player cancels the two numbers used to make the bet. In
the event that all the numbers are cancelled, the player has doubled their
money, and can retire from the table happy.

For each loss, however, the player adds the amount of the bet to the end of the sequence; this
is a loss to be recouped. The next bet is designed to recoup the most recent loss
and provide a small gain. Multiple winning bets will recoup multiple
losses, supplemented with small gains.

**Example**.
Here's an example of the cancellation system using a budget
of 21 times the base bet, decomposed to :math:`[1, 2, 3, 4, 5, 6]`.

#.  Bet :math:`1+6`. A win. Cancel 1 and 6, leaving :math:`[2, 3, 4, 5]`.

#.  Bet :math:`2+5`. A loss. Add 7, leaving :math:`[2, 3, 4, 5, 7]`.

#.  Bet :math:`2+7`. A loss. Add 9, leaving :math:`[2, 3, 4, 5, 7, 9]`.

#.  Bet :math:`2+9`. A win. Cancel 2 and 9, leaving :math:`[3, 4, 5, 7]`.

#.  Next bet will be :math:`3+7`.


**State**. The player's state is the list of multipliers. This
list grows and shrinks; when it is empty, the player leaves the table.
The bet amount will be the first and last elements of this list. Wins will remove
elements from the collection; losses will add elements to the
collection.

..  note:: Alternative Budgets

    The system of betting shown above can involve large numbers, since
    the betting starts at :math:`7 \times` the table minimum. The numbers
    are smaller when working with a list of smaller numbers.

    Consider a starting list of :math:`[1, 1]`. The bet is 2. A win cancels both
    numbers and resets the betting.

    A loss, however, appends the bet to the sequence, leaving us with :math:`[1, 1, 2]`.
    The next bet becomes 3.

    A win will leave one uncancelled value, this can be dropped, the list
    reset to :math:`[1, 1]`, and betting can resume.

    A subsequent loss appends 3, leaving us with :math:`[1, 1, 2, 3]`.
    The next bet becomes 4.

    Almost any starting sequence will work as long as the values are positive
    integers.

PlayerCancellation Design
--------------------------

..  class:: PlayerCancellation

    :class:`PlayerCancellation` uses the cancellation betting system.
    This player allocates their available budget into a sequence of bets
    that have an accelerating potential gain as well as recouping any losses.


Fields
~~~~~~

..  attribute:: PlayerCancellation.sequence

    This :class:`List` keeps the bet amounts; wins are removed
    from this list and losses are appended to this list. The current bet
    is the first value plus the last value.

..  attribute:: PlayerCancellation.outcome

    This is the player's preferred :class:`Outcome` instance.


Constructors
~~~~~~~~~~~~


..  method:: PlayerCancellation.__init__(self, table: Table) -> None


    This uses the :meth:`PlayerCancellation.resetSequence` method to initialize the
    sequence of numbers used to establish the bet amount. This also
    picks a suitable even money :class:`Outcome`, for example, black.

    :param table: The :class:`Table` object which will accept the bets.
    :type table: :class:`Table`

Methods
~~~~~~~


..  method:: PlayerCancellation.resetSequence(self) -> None


    Puts the initial sequence
    of six values, :literal:`[1, 2, 3, 4, 5, 6]`  into the :obj:`sequence`
    variable. The sequence :literal:`[1, 1, 1, 1, 1, 1]` will also work,
    and the bets will be smaller.


..  method:: PlayerCancellation.placeBets(self) -> None


    Creates a bet from the
    sum of the first and last values of :obj:`sequence` and the preferred
    outcome.


..  method:: PlayerCancellation.win(self, bet: Bet) -> None

    :param bet: The bet which won
    :type bet: :class:`Bet`


    Uses the superclass method to update the
    stake with an amount won. It then removes the fist and last element from
    :obj:`sequence`.


..  method:: PlayerCancellation.lose(self, bet: Bet) -> None

    :param bet: The bet which lost
    :type bet: :class:`Bet`


    Uses the superclass method to update the
    stake with an amount lost. It then appends the sum of the first and
    last elements of :obj:`sequence` to the end of :obj:`sequence`
    as a new value.



Cancellation Player Deliverables
--------------------------------

There are three deliverables for this exercise.

-   The :class:`PlayerCancellation` class.

-   A unit test of the :class:`PlayerCancellation` class. This test
    should synthesize a fixed list of :class:`Outcome` instances, :class:`Bin`
    s, and calls a :class:`PlayerCancellation` instance with various
    sequences of reds and blacks. There are 16 different sequences of
    four winning and losing bets. These range from four losses in a row
    to four wins in a row. This should be sufficient to exercise the
    class and see the changes in the bet amount.

-   An update to the overall :class:`Simulator` class that uses the :class:`PlayerCancellation` class.

Looking Forward
---------------

In the :class:`SevenReds` subclass of :class:`Player`, the state was a simple
count. In the :class:`Player1326` subclass, the state was a more complex
hierarchy of classes. In this case, a built-in :class:`list` object could
maintain the player's state.
In the next chapter we'll look at one more way to maintain state of a player,
using a pair of integer values.


