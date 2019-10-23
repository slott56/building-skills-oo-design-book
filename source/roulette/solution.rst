
..  _`roul.solution.ov`:

Roulette Solution Overview
==========================

The first section, `Preliminary Survey of Classes`_, is a survey of the classes gleaned from the general
problem statement.  Refer to :ref:`found.problem` as well as the problem
details in :ref:`roul.details`. This survey is drawn from a quick
overview of the key nouns in these sections.

We'll amplify this survey with some details of the
class definitions in `Preliminary Roulette Class Structure`_.

Given this preliminary of the candidate classes, `A Walk-Through of Roulette`_ is a
walk-through of the possible design that will refine the definitions, and
give us some assurance that we have a reasonable architecture. We will
make some changes to the preliminary class list, revising and expanding
on our survey.


We will also include a number of questions and answers in `Roulette Solution Questions and Answers`_.
This should help clarify the design
presentation and set the stage for the various development exercises in
the chapters that follow.

..  _`roul.solution.class`:

Preliminary Survey of Classes
-----------------------------

To provide a starting point for the development effort, we have to
identify the objects and define their responsibilities. The central
principle behind the allocation of responsibility is :emphasis:`encapsulation`;
we do this by attempting to isolate the information or
isolate the processing into separate objects. Encapsulation
assures that the methods of a class are the exclusive users of the
fields of that class. It also makes each class very loosely coupled with
other classes; this permits change without a destructive ripple through the
application.

For example, a class for each :class:`Outcome` defines objects
which can contain both the name and the payout odds.
Each :class:`Outcome` instance can be used
to compute a winning amount, and no other element of the simulation
needs to share the odds information or the payout calculation.

In reading the background information and the problem statement, we
noticed a number of nouns that seemed to be important parts of the game
we are simulating.

-   Wheel

-   Bet

-   Bin

-   Table

-   Red

-   Black

-   Green

-   Number

-   Odds

-   Player

-   House


One common development milestone is to be able to develop a class model
in the Unified Modeling Language (UML) to describe
the relationships among the various nouns in the problem statement.
Building (and interpreting) this model takes some experience with OO
programming. In this first part, we'll avoid doing extensive modeling.
Instead we'll try to identify some basic design features. We'll focus
in on the most important of these nouns and describe the kinds of
classes that you will build.


..  _`roul.solution.struct`:

Preliminary Roulette Class Structure
------------------------------------

We'll summarize some of the classes and responsibilities
that we can identify from the problem statement. This is not the
complete list of classes we need to build. As we work through the
exercises, we'll discover additional classes and rework some of these
preliminary classes more than once.

We'll describe each class with respect to the responsibility allocated
to the class and the collaborators.  Some collaborators are used by an
object to get work done.  We have a number of "uses-used by" collaborative
relationships among our various classes.

These are the classes that seem most important:

:Outcome:
    **Responsibilities**.

    A name for the bet and
    the payout odds. This isolates the calculation of the payout amount.
    Example: "Red", "1:1".

    **Collaborators**.

    Collected by a :class:`Wheel` object into the
    bins that reflect the bets that win; collected by a :class:`Table` object
    into the available bets for the :class:`Player`; used by a
    :class:`Game` object to compute the amount won from the amount that was
    bet.

:Wheel:
    **Responsibilities**.

    Selects the
    :class:`Outcome` instances that win. This isolates the use of a random
    number generator to select :class:`Outcome` instances. It encapsulates
    the set of winning :class:`Outcome` instances that are associated with each
    individual number on the wheel. Example: the "1" bin has the
    following winning :class:`Outcome` instances: "1", "Red",
    "Odd", "Low", "Column 1", "Dozen 1-12",
    "Split 1-2", "Split 1-4", "Street 1-2-3",
    "Corner 1-2-4-5", "Five Bet", "Line 1-2-3-4-5-6",
    "00-0-1-2-3", "Dozen 1", "Low" and
    "Column 1".

    **Collaborators**.

    Collects the :class:`Outcome` instances into
    bins; used by the overall :class:`Game` to get a next set of winning
    :class:`Outcome` instances.

:Table:
    **Responsibilities**.

    A collection of bets placed on :class:`Outcome` instances by a
    :class:`Player`. This isolates the set of possible bets and the
    management of the amounts currently at risk on each bet. This also
    serves as the interface between the :class:`Player` and the other
    elements of the game.

    **Collaborators**.

    Collects the :class:`Outcome` instances; used
    by :class:`Player` to place a bet amount on a specific
    :class:`Outcome`; used by :class:`Game` to compute the amount
    won from the amount that was bet.

:Player:
    **Responsibilities**.

    Places bets on
    :class:`Outcome` instances, updates the stake with amounts won and lost.

    **Collaborators**.

    Uses :class:`Table` to place bets on :class:`Outcome` instances;
    used by :class:`Game` to record wins and losses.


:Game:
    **Responsibilities**.

    Runs the game: gets bets
    from :class:`Player`, spins :class:`Wheel`, collects losing
    bets, pays winning bets. This encapsulates the basic sequence of play
    into a single class.

    **Collaborators**.

    Uses :class:`Wheel`, :class:`Table`, :class:`Outcome`, :class:`Player`.
    The overall statistical
    analysis will play a finite number of games and collect the final value
    of the :class:`Player`'s stake.

The class :class:`Player` has the most important responsibility in
the application, since we expect to update the algorithms this class
uses to place different kinds of bets. Clearly, we need to cleanly
encapsulate the :class:`Player`, so that changes to this class have
no ripple effect in other classes of the application.

..  _`roul.solution.walkthrough`:

A Walk-Through of Roulette
--------------------------

A preliminary task is to review these responsibilities to confirm
that a complete cycle of play is possible. This will help provide some
design details for each class. It will also provide some insight into
classes that may be missing from this overview.


One way to structure this task is to do a
Class-Responsibility-Collaborators (CRC) walk-through.

As preparation, get some 5" x 8" notecards. On each card, write down
the name of a class, the responsibilities and the collaborators. Leave
plenty of room around the responsibilities and collaborators to write
notes. We've only identified five classes, so far, but others always
show up during the walk-through.

During the walk-through, we'll be identifying areas of responsibility,
allocating them to classes of objects, and defining any collaborating objects.
An area of responsibility is a thing to do, a piece of information, or a computed result.
Sometimes a complex responsibility can be decomposed into smaller
pieces, and those smaller pieces assigned to other classes. There are a
lot of reasons for decomposing, not all of which are apparent at first.


The basic processing outline is the responsibility of the :class:`Game`
class. To start, locate the :class:`Game` card.


#.  Our preliminary note was that this class "Runs the game." The
    responsibilities section has a summary of four steps involved in
    running the game.

#.  The first step is "gets bets from :class:`Player`." Find the
    :class:`Player` card.

#.  Does a :class:`Player` collaborate with a :class:`Game` to
    place bets? If not, update the cards as necessary to include this.

#.  One of the responsibilities of a :class:`Player` is to place
    bets. The step in the responsibility statement is merely
    "Places bets on :class:`Outcome` instances." Looking at the
    classes, we note that the :class:`Table` contains the amounts
    placed on the Bets. Fix the collaboration information on the :class:`Player`
    to name the :class:`Table` class. Find the :class:`Table` card.

#.  Does a :class:`Table` collaborate with a :class:`Player` to
    accept the bets? If not, update the cards as necessary to include this.

#.  What card has responsibility for the amount of the bet? It looks like
    :class:`Table`. We note one small problem: the :class:`Table`
    contains the :emphasis:`collection` of amounts bet on :class:`Outcome` instances.

    What class contains the individual "amount bet on an
    :class:`Outcome`?" This class appears to be missing. We'll call
    this new class :class:`Bet` and start a new card. We know one
    responsibility is to hold the amount bet on a particular :class:`Outcome`.

    We know three collaborators: the amount is paired with an :class:`Outcome`,
    all of the :class:`Bet` s are collected by a :class:`Table`,
    and the :class:`Bet` s are created by a :class:`Player`.
    We'll update all of the existing cards to name their collaboration with
    :class:`Bet`.

#.  What card has responsibility for keeping all of the :class:`Bet` instances?
    Does :class:`Table` list that as a responsibility? We should
    update these cards to clarify this collaboration.


You should continue this tour, working your way through spinning the :class:`Wheel`
to get a list of winning :class:`Outcome` instances. From there, the :class:`Game`
can get all of the :class:`Bet` instances from the :class:`Table` and
see which are based on winning :class:`Outcome` instances and which are
based on losing :class:`Outcome` instances. The :class:`Game` can notify the
:class:`Player` of each losing :class:`Bet`, and notify the :class:`Player`
of each winning :class:`Bet`, using the :class:`Outcome` to
compute the winning amount.


This walk-through can provide an overview of some of the interactions
among the objects in the working application. You may uncover additional
design ideas. The most important outcome of the
walk-through is a sense of the responsibilities and the
collaborations required to create the necessary application behavior.

..  _`roul.ov.qanda.main`:

Roulette Solution Questions and Answers
---------------------------------------

Why does the :class:`Game` class run the sequence of steps? Isn't
that the responsibility of some "main program?"


    **Coffee Shop Answer**. We haven't finished designing the entire
    application, so we need to reflect our own ignorance of how the final
    application will be assembled from the various parts. Rather than
    allocate too many responsibilities to :class:`Game`, and possibly
    finding conflicts or complication, we'd rather allocate too few
    responsibilities until we know more.

    From another point of view, designing the main program is premature
    because we haven't finished designing the :emphasis:`entire`
    application. We anticipate a :class:`Game` object being invoked from
    some statistical data gathering object to run one game. The data
    gathering object will then get the final stake from the player and
    record this. :class:`Game` object's responsibilities are focused on
    playing the game itself. We'll need to add a responsibility to :class:`Game`
    to collaborate with the data gathering class to run a number of games as a
    "session".

    **Technical Answer**. In procedural programming (especially in languages like
    COBOL), the "main program" is allocated almost all of the
    responsibilities. These procedural main programs usually contain a
    number of elements, all of which are very tightly coupled. This is
    a bad design, since the responsibilities aren't allocated as narrowly
    as possible. One small change in one place breaks the whole program.

    In OO
    languages, we can reduce the main program to a short list of object constructors, with
    the real work delegated to the objects. This level of coupling assures
    us that a small change to one class has no impact on other classes
    or the program as a whole.

..  _`roul.ov.qanda.outcome`:

Why is :class:`Outcome` a separate class? Each object that is an
instance of :class:`Outcome` only has two attributes; why not use an
array of Strings for the names, and a parallel array of integers for the odds?

    **Representation**. We prefer not to decompose an object into separate
    data elements. If we do decompose this object, we will have to ask which
    class would own these two arrays? If :class:`Wheel` keeps these, then
    :class:`Table` becomes very tightly coupled to these two arrays that
    should be :class:`Wheel` object's responsibility. If :class:`Table`
    keeps these, then :class:`Wheel` is privileged to know details of how
    :class:`Table` is implemented. If we need to change these arrays to
    another storage structure, two classes would change instead of one.

    Having the name and odds in a single :class:`Outcome` object allows
    us to change the representation of an :class:`Outcome`. For
    example, we might replace the String as the identification of the
    outcome, with a collection of the individual numbers that comprise this
    outcome. This would identify a straight bet by the single winning
    number; an even money bet would be identified by an array of the 18
    winning numbers.

    **Responsibility**. The principle of isolating responsibility would be
    broken by this "two parallel arrays" design because now the :class:`Game`
    class would need to know how to compute odds. In more complex games,
    there would be the added complication of figuring the rake. Consider a
    game where the :class:`Player` object's strategy depends on the potential
    payout. Now the :class:`Game` and the :class:`Player` both have
    copies of the algorithm for computing the payout. A change to one must
    be paired with a change to the other.

    The alternative we have chosen is to encapsulate the payout algorithm
    along with the relevant data items in a single bundle.


If :class:`Outcome` encapsulates the function to compute the amount
won, isn't it just a glorified subroutine?

    If you're background is BASIC or FORTRAN, this can seem to be true.
    A class can be thought of as a glorified
    subroutine library that captures and isolates data elements
    along with their associated functions.

    A class is more powerful than a subroutine
    library with private data. For example, classes introduce
    inheritance as a way to create a family of
    closely-related definitions.

    We discourage trying to mapping OO concepts back to other non-OO languages.


What is the distinction between an :class:`Outcome` and a :class:`Bet`?


    We need to describe the propositions on the table on which you can place
    bets. The propositions are distinct from an actual amount of money
    wagered on a proposition. There are a lot of terms to choose from,
    including bet, wager, proposition, place, location, or outcome. We opted
    for using :class:`Outcome` because it seemed to express the
    open-ended nature of a potential outcome, different from an amount bet
    on a potential outcome. We're considering the :class:`Outcome`
    as an abstract possibility, and the :class:`Bet` as a concrete
    action taken by a player.


    Also, as we expand this simulation to cover other games, we will find
    that the randomized outcome is not something we can directly bet on. In
    Roulette, however, all outcomes are something we can be bet on, as well
    as a great many combinations of outcomes. We will revisit this design
    decision as we move on to other games.


Why are the classes so small?


    First-time designers of OO applications are sometimes
    uncomfortable with the notion of :emphasis:`emergent behavior`. In
    procedural programming languages, the application's features are always
    embodied in a few key procedures. Sometimes a single procedure, named :func:`main`.


    A good OO design partitions responsibility. In many cases,
    this subdivision of the application's features means that the overall
    behavior is not captured in one central place. Rather, it emerges from
    the interactions of a number of objects.


    We have found that smaller elements, with very finely divided
    responsibilities, are more flexible and permit change. If a change will
    only alter a portion of a large class, it can make that portion
    incompatible with other portions of the same class. A symptom of this is
    a bewildering nest of ``if``-statements to sort out the various
    alternatives. When the design is decomposed down more finely, a change
    can be more easily isolated to a single class. A sequence
    of ``if``-statements can be focused on selecting the proper class, which can
    then carry out the desired functions.


Looking Forward
---------------

Now that we've considered the overall structure of the solution, we can
start to look at the class definitions.

We'll take a "bottom-up" approach to the classes. The idea is to define
the small things first, and then combine those things into larger and
more sophisticated components.

The simplest thing we've seen is an individual outcome. For example,
a bin on the wheel contains "Red" as an actual outcome. A player will make
a bet on "Red" as an expected outcome. We'll start there in the next chapter.
