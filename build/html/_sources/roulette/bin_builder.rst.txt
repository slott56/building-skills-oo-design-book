
Bin Builder Class
=================

We'll look at the question of filling in the :class:`Outcome` objects
in each :class:`Bin` container of
the :class:`Wheel` collection. The `Bin Builder Analysis`_ section will address the
various outcomes in details.

In `Bin Builder Algorithms`_ we'll look at eight algorithms for allocating
appropriate outcomes to appropriate bins of the wheel.

The `BinBuilder Design`_ section will present the detailed design
for this class. In `Bin Builder Deliverables`_ we'll define the specific
deliverables.

In `Internationalization and Localization`_ we'll identify some considerations
for providing local language names for the outcomes.


Bin Builder Analysis
--------------------

Enumerating each :class:`Outcome` in the 38 :class:`Bin` instances
by hand is a tedious undertaking. Most :class:`Bin` instances contain about
fourteen individual :class:`Outcome` instances. An algorithm seems like
a better, less error-prone way to do this job.

It is often helpful to create a class that is used to build an instance of another class. This
is a design pattern sometimes called a **Builder**. We'll
design an object that builds the various :class:`Bin` instances and assigns
them to a :class:`Wheel` object. This will fill the need left open in the
:ref:`roul.wheel`.

Additionally, we note that the complex algorithms to construct the :class:`Bin` instances
are only tangential to the operation of the :class:`Wheel` object.
Because these are not essential to the design of the :class:`Wheel` class, we
find it helpful to segregate the builder methods into a separate class.


The :class:`BinBuilder` class will have a method that enumerates the
contents of each of the 36 number :class:`Bin` instances, building the individual
:class:`Outcome` objects. We can then assign these :class:`Outcome`
objects to the :class:`Bin` instances of a :class:`Wheel` instance. We
will use a number of steps to create the various types of :class:`Outcome` instances,
and depend on the :class:`Wheel` to assign each :class:`Outcome`
object to the correct :class:`Bin`.

The Roulette Outcomes
~~~~~~~~~~~~~~~~~~~~~~

Looking at the :ref:`roul.details.bets` gives us a number of
:class:`Outcome` instances that
are combinations of individual numbers on the Roulette table.
These combinations apply to the numbers
from one to thirty-six. A different -- and much simpler -- set of rules
applies to 0 and 00.

First, we'll survey the table geometry and the profusion of bets
based on locations of the numbers. Then we'll
develop specific algorithms for each kind of bet.

-   **Split Bets**.
    Each numbered square on the layout is adjacent to two, three or four other
    numbers. There are horizontal (left-right( splits and vertical (up-down) splits.
    For example, “5” is part of “4-5”, “5-6”, “2-5”, and “5-8”. Around the
    edges of the layout, a number will be part of fewer splits.

-   **Street Bets**.
    Each number is a member of one of the twelve street bets.
    For example "9" is part of the "7-8-9" street.

-   **Corner Bets**.
    Each number is a member of one, two or four corner
    bets.
    A number in the center column (5, 8, 11, ..., 32) is a member of
    four corners. For example, "8" is part of "5-6-8-9", "4-5-7-8",
    "7-8-11-12", and "8-9-11-12". At the edges, a number is part of
    fewer corners.

-   **Line Bets**.
    Six adjacent numbers comprise a line. A line is two adjacent street bets.
    Each number will be part of one or two lines.
    For example "9" is part of the "7-8-9-10-11-12" line as well
    as the "4-5-6-7-8-9" line.

-   **Dozen Bets**.
    Each number is a member of one of available dozen bets.
    The three ranges are from 1 to 12, 13 to 24 and 25 to 36, making it
    very easy to associate a numbers with one of the dozens.

-   **Column Bets**.
    Each number is a member of one of the three columns.
    Each of the columns has a number numeric relationship. The values
    are :math:`3c+1`, :math:`3c+2`, and :math:`3c+3`, where
    :math:`0 \leq c < 12`.

-   **The Even-Money or "Outside" Bets**.
    These include Red, Black, Even, Odd, High,
    Low. Each number on the layout will be associated with
    three of the six possible even money :class:`Outcome` instances.

-   **The Five Bet**.
    The :class:`Bin` instances for zero and double zero are special cases.
    Each of these :class:`Bin` instances has a straight number bet :class:`Outcome`,
    plus the "Five Bet" :class:`Outcome` object. This is a bet on (00-0-1-2-3, which pays :math:`6:1`).

One other thing we'll probably want are handy names for the various
kinds of odds. We might want to define a collection of constants
for this.

While can define an :class:`Outcome` as
:samp:`Outcome("Number 1", 35)` , this is a little opaque. A
slightly nicer form is :samp:`Outcome("Number 1",
Game.StraightBet)`. Naming the odds makes it easier to
make a consistent change to the odds to represent some localized
change in house rules.


..  _roul.binbuilder.algorithms:

Bin Builder Algorithms
----------------------

This section provides the algorithms for nine kinds of bets.

Note that we're going to be accumulating sets (or lists) of individual
:class:`Outcome` objects. These are interim objects that will be used
to create the final :class:`Bin` objects which are assigned to the
:class:`Wheel`.

We'll be happiest using the core Python :class:`set` structure to accumulate
these collections. The type hint will be ``Set[Outcome]``.

Generating Straight Bets
~~~~~~~~~~~~~~~~~~~~~~~~

Straight bet :class:`Outcome` instances are the easiest to generate.

    **For All Numbers**. For each number, :math:`n`, in the range :math:`1 \leq n < 37`:

        **Create Outcome**. Create an :class:`Outcome` object from the number, :emphasis:`n`,
        with straight bet odds of :math:`35:1`.

        **Assign to Bin**. Append the :class:`Outcome` object to :class:`Bin` instance
        :emphasis:`n`.

    **Zero**.  Create an :class:`Outcome` object from the "0" with straight bet odds of :math:`35:1`.
    Assign this to the :class:`Bin` instance at index 0 in the :class:`Wheel`.

    **Double Zero**.  Create an :class:`Outcome` from the "00" with odds of :math:`35:1`.
    Assign this to :class:`Bin` instance at index 37 in the :class:`Wheel`.

Generating Split Bets
~~~~~~~~~~~~~~~~~~~~~

Split bet :class:`Outcome` instances are more complex because of the various
edge and corner cases.

The table geometry has two kinds of split bets:

-   **left-right split**.
    These pairs all have the form :math:`\{n, n+1\}`.

-   **up-down split**.
    These pairs have the form :math:`\{n, n+3\}` .

We can look at the number 5 as being part of 4 different pairs:
:math:`\{4,4+1\}, \{5,5+1\}, \{2,2+3\}, \{5,5+3\}`. The corner number 1 is part of 2
split bets: :math:`\{1,1+1\}, \{1,1+3\}`.


We can generate all of the "left-right" split bets by iterating through
the left two columns; the numbers :math:`1, 4, 7, \dots, 34` and :math:`2, 5, 8, \dots, 35`.

    **For All Rows**. For each row, :math:`r`, in the range :math:`0 \leq r < 12`:

        **First Column Number**. Set :math:`n \gets 3r+1`.
        This will create values :math:`n \in \{1, 4, 7, \dots, 34\}`.

        **Column 1-2 Split**. Create a :math:`\{n, n+1\}` split :class:`Outcome` object with split bet odds of :math:`17:1`.

        **Assign to Bins**. Associate this object with two :class:`Bin` instances: :math:`n`
        and :math:`n+1`.

        **Second Column Number**. Set :math:`n \gets 3r+2`.
        This will create values :math:`n \in \{2, 5, 8, \dots, 35\}`.

        **Column 2-3 Split**. Create a :math:`\{n, n+1\}` split :class:`Outcome` object.

        **Assign to Bins**. Associate this object to two :class:`Bin` instances: :math:`n`
        and :math:`n+1`.

A similar algorithm must be used for the numbers 1 through 33, to generate the "up-down"
split bets. For each number, :math:`n`, we generate a :math:`\{n, n+3\}` split bet.
This :class:`Outcome` object belongs to two :class:`Bin` instances: :math:`n` and :math:`n+3`.


Generating Street Bets
~~~~~~~~~~~~~~~~~~~~~~

Street bet :class:`Outcome` instances follow a very regular pattern.

We can generate the street bets by iterating through the twelve rows of
the layout.


    **For All Rows**. For each row, :math:`r`, in the range :math:`0 \leq r < 12`:

        **First Column Number**. Set :math:`n \gets 3r+1`.
        This assure :math:`n \in \{1, 4, 7, ..., 34\}`.

        **Street**. Create a :math:`\{n, n+1, n+2\}` street :class:`Outcome` with street bet odds of :math:`11:1`.

        **Assign to Bins**. Associate this object to three :class:`Bin` instances: :math:`n`,
        :math:`n+1`, :math:`n+2`.


Generating Corner Bets
~~~~~~~~~~~~~~~~~~~~~~

Corner bet :class:`Outcome` instances are as complex as split bets because of
the various cases: corners, edges and down-the-middle.

Each corner has four numbers, :math:`\{n, n+1, n+3, n+4\}`.
This is two numbers in the same row, and two numbers in the next higher row.

We can generate the corner bets by iterating
through the numbers :math:`1, 4, 7, \dots, 31` and :math:`2, 5, 8, \dots, 32`. For each number,
:math:`n`, we generate a corner bet. This :class:`Outcome`
object belongs to four :class:`Bin` instances.

We generate corner bets by iterating through the various corners based on rows and
columns. There is room for two corners within the three columns of the layout:
one corner starts at column 1 and the other corner starts at column 2.
There is room for 11 corners within the 12 rows of the layout.


    **For All Lines Between Rows**. For each row, :math:`r`, in the range :math:`0 \leq r < 11`:

        **First Column Number**. Set :math:`n \gets 3r+1`.
        This will assure :math:`n \in \{1, 4, 7, ..., 31\}`.

        **Column 1-2 Corner**. Create a :math:`\{n, n+1, n+3, n+4\}` corner :class:`Outcome` with
        corner bet odds of :math:`8:1`.

        **Assign to Bins**. Associate this object to four :class:`Bin` instances: :math:`n`,
        :math:`n+1`, :math:`n+3`, :math:`n+4`.

        **Second Column Number**. Set :math:`n \gets 3r+2`.
        This will assure :math:`n \in \{2, 5, 8, ..., 32\}`.

        **Column 2-3 Corner**. Create a :math:`\{n, n+1, n+3, n+4\}` corner :class:`Outcome` with
        odds of :math:`8:1`.

        **Assign to Bins**. Associate this object to four :class:`Bin` instances: :math:`n`,
        :math:`n+1`, :math:`n+3`, :math:`n+4`.



Generating Line Bets
~~~~~~~~~~~~~~~~~~~~

Line bet :class:`Outcome` instances are similar to street bets. However,
these are based around the 11 lines between the 12 rows.

For lines :math:`s` numbered 0 to 10, the numbers on the line bet
can be computed as follows: :math:`{3s+1, 3s+2, 3s+3, 3s+4, 3s+5, 3s+6}`. This :class:`Outcome`
object belongs to six individual :class:`Bin` instances.

    **For All Lines Between Rows**. For each row, :math:`r`, in the range :math:`0 \leq r < 11`:

        **First Column Number**. Set :math:`n \gets 3r+1`.
        This will assure :math:`n \in \{ 1, 4, 7, ..., 31\}`.

        **Line**. Create a :math:`\{n, n+1, n+2, n+3, n+4, n+5\}` line :class:`Outcome`
        withs odds of :math:`5:1`.

        **Assign to Bins**. Associate this object to six :class:`Bin` instances: :math:`n`,
        :math:`n+1`, :math:`n+2`, :math:`n+3`, :math:`n+4`, :math:`n+5`.


Generating Dozen Bets
~~~~~~~~~~~~~~~~~~~~~

Dozen bet :class:`Outcome` instances require enumerating all twelve numbers
in each of three groups.


    **For All Dozens**. For each dozen, :math:`d`,  in the range :math:`0 \leq d < 3`:

        **Create Dozen**. Create an :class:`Outcome` for dozen :math:`d+1` with odds of :math:`2:1`.

        **For All Numbers**. For each number, :math:`m`, in the range :math:`0 \leq m < 12`:

            **Assign to Bin**. Associate this object to :class:`Bin` :math:`12d+m+1`.


Generating Column Bets
~~~~~~~~~~~~~~~~~~~~~~

Column bet :class:`Outcome` instances require enumerating all twelve numbers
in each of three groups. While the outline of the algorithm is the same
as the dozen bets, the enumeration of the individual numbers in the
inner loop is slightly different.


    **For All Columns**. For each column, :math:`c`, in the range :math:`0 \leq c < 3`:


        **Create Column**. Create an :class:`Outcome` for column :math:`c+1` with odds of :math:`2:1`.


        **For All Rows**. For each row, :emphasis:`r`, in the range :math:`0 \leq r < 12`:


            **Assign to Bin**. Associate this object to :class:`Bin` :math:`3r+c+1`.


Generating Even-Money Bets
~~~~~~~~~~~~~~~~~~~~~~~~~~

The even money bet :class:`Outcome` instances are relatively easy to generate.


    Create the Red outcome, with odds of :math:`1:1`.

    Create the Black outcome, with odds of :math:`1:1`.

    Create the Even outcome, with odds of :math:`1:1`.

    Create the Odd outcome, with odds of :math:`1:1`.

    Create the High outcome, with odds of :math:`1:1`.

    Create the Low outcome, with odds of :math:`1:1`.


    **For All Numbers**. For each number, :math:`n`, in the range :math:`1 \leq n < 37`:

        **Low?** If :math:`1 \leq n < 19`, associate the **Low** :class:`Outcome`
        with :class:`Bin` :math:`n`.

        **High?** Otherwise, :math:`19 \leq n < 37`, associate the **High** :class:`Outcome`
        with :class:`Bin` :math:`n`.

        **Even?** If :math:`n \mod 2 = 0`, associate the **Even** :class:`Outcome`
        with :class:`Bin` :math:`n`.

        **Odd?** Otherwise, :math:`n \mod 2 \ne 0`, associate the **Odd** :class:`Outcome`
        with :class:`Bin` :math:`n`.

        **Red?** If :math:`n \in \{1, 3, 5, 7, 9, 12, 14, 16, 18, 19,
        21, 23, 25, 27, 30, 32, 34, 36\}`, associate the **Red** :class:`Outcome`
        with :class:`Bin` :math:`n`. There's no simplifying rule, it's a list of
        seemingly arbitrary numbers.

        **Black?** If it's not **Red**, associate the **Black** :class:`Outcome` with :class:`Bin`
        :math:`n`.

    Note that zero and double-zero are not included in any of these.

Generating the Five Bet
~~~~~~~~~~~~~~~~~~~~~~~~

The Five bet :class:`Outcome` instance is relatively easy to generate.
This has :math:`6:1` odds. It belongs to five separate bins: 0, 37, 1, 2, and 3.
It's a special case that has to be build separately.

BinBuilder Design
------------------

We'll show the :class:`BinBuilder` as a class definition.
It's not perfectly clear that a class is necessary for this.
We could think of this is a collection of closely-related functions,
instead of a single class.

..  class:: BinBuilder

    :class:`BinBuilder` creates the :class:`Outcome` instances for all of
    the 38 individual :class:`Bin` on a Roulette wheel.

Constructors
~~~~~~~~~~~~


..  method:: BinBuilder.__init__(self) -> None

    Initializes the :class:`BinBuilder`.

Methods
~~~~~~~


..  method:: BinBuilder.buildBins(self, wheel: Wheel) -> None

    Creates the :class:`Outcome` instances
    and uses the :meth:`addOutcome` method to place each :class:`Outcome`
    in the appropriate :class:`Bin` of :obj:`wheel`.

    It's then the :class:`Bin` instances responsibility to update the
    data structure used to store the :class:`Outcome` instances.

    :param wheel: The Wheel with Bins that must be populated with :class:`Outcome` instances.
    :type wheel: :class:`Wheel`

There should be separate methods to generate the straight bets,
split bets, street bets, corner bets, line bets, dozen bets and
column bets, even money bets, and the special five bet.

Bin Builder Deliverables
-------------------------

There are three deliverables for this exercise. The new classes should have
meaningful Python docstrings.

-   The :class:`BinBuilder` class. This is part of the :file:`roulette.py` file.

-   A class which performs a unit test of the :class:`BinBuilder`
    class. The unit test invoke each of the various methods that create :class:`Outcome`
    instances. There are a lot of potential :class:`Outcome` instances in various
    :class:`Bin` collections. We don't need to check them all, we'll use the idea of boundaries
    to check selected cases.

    -   Test straight bet :class:`Outcome` instances in the :class:`Bin` objects
        for positions 0, 00, 1, and 36 on the :class:`Wheel`.

    -   Test split bets at positions 1 and 36.
        There will be "1-2" and "1-4" :class:`Outcome`
        objects in the :class:`Bin` instance at position 1.
        Similarly, there will be
        "33-36" and "35-36" :class:`Outcome`
        objects in the :class:`Bin` instance at position 36.

    -   Test street bets at positions 1 and 36.

    -   Test corner bets around positions 1, 4, and 5. Since 1 is on the edge, it's only part
        of one corner. 4, however, is part of two corners, and 5 will be part of 4 corner bets.

    -   Test line bets to be sure that 1 is only in a single line bet, where 4 is part of two
        separate line bets.

    -   Test dozens and columns by checking 1, 17, and 36 for membership in appropriate dozens
        and columns.

    -   Use 1, 17, 18, and 36 to check low, high, red, black, even, and odd outside bets.

    -   Finally. (Whew!) confirm that 0 and 00 participate in the five bet.

-   (Optional.) Extend the unit test of the :class:`Wheel` class to create a more complex
    integration test. The test
    should create and initialize a :class:`Wheel`. It can use the :meth:`Wheel.getBin`
    method to check selected :class:`Bin` instances for the correct :class:`Outcome` instances.


Internationalization and Localization
-------------------------------------

An an advanced topic, we would like to avoid using a lot of string literals
the names of the bets. Python offers extensive
tools for localization (l10n) of programs. Since Python
works with Unicode strings, it supports non-Latin
characters, supporting internationalization (i18n), also.

This is an advanced topic. It's tightly coupled with the names
provided to the :class:`Outcome` instances. This is a place
to consider translating the labels for outcomes in the bins.

Looking Forward
---------------

Once we've populated the :class:`Wheel` instance, we can move on to looking
at how a player interacts with the game. In the case of Roulette, the
player's primary interaction is to place bets. We'll start with a model
for the :class:`Bet` class.
