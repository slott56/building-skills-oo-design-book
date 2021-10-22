
Craps Solution Overview
=======================

We will present a survey of the classes gleaned from the general problem
statement in `Preliminary Survey of Classes`_.
In `Preliminary Craps Class Structure`_ we'll describe some potential
class definitions.

Given this survey of the candidate classes, we will then do a
walk-through to refine the definitions. We'll show this in `A Walk-Through of Craps`_.
We can use assure ourselves that we have a reasonable architecture.
We will make some changes to the preliminary class list, revising and expanding on our survey.

We will also include a number of questions and answers in `Craps Solution Questions and Answers`_.
This should help clarify the design presentation and set the stage for the various development exercises in
the chapters that follow.


Preliminary Survey of Classes
-----------------------------

We have divided up the responsibilities to provide a starting point for
the development effort. The central principle behind the allocation of
responsibility is to encapsulate the information or algorithm into a class.
In reading the background
information and the problem statement, we noticed a number of nouns that
seemed to be important parts of the Craps game.

-   Dice

-   Bet

-   Table

-   Point

-   Proposition

-   Number

-   Odds

-   Player

-   House


The following table summarizes some of the classes and responsibilities
that we can identify from the problem statement. This is not the
complete list of classes we need to build. As we work through the
exercises, we'll discover additional classes and rework some of these
classes more than once.


We also have a legacy of classes available from the Roulette solution.
We would like to build on this infrastructure as much as possible.


Preliminary Craps Class Structure
---------------------------------


:Outcome:
    **Responsibilities**

    A name for a particular
    betting opportunity. Most outcomes have fixed odds, but the behind the
    line odds bets have odds that depend on a point value.

    **Collaborators**

    Collected
    by a :class:`Table` object into the available bets for the
    :class:`Player`; used by :class:`Game` instance to compute the amount
    won from the amount that was bet.

:Dice:
    **Responsibilities**

    Selects any winning
    propositions as well as next state of the game.

    **Collaborators**

    Used by the
    overall :class:`Game` instance to get a next set of winning
    :class:`Outcome` instances, as well as change the state of the
    :class:`Game` instance.

:Table:
    **Responsibilities**

    A collection of bets placed on :class:`Outcome` instances by a
    :class:`Player`. This isolates the set of possible bets and the
    management of the amounts currently at risk on each bet. This also
    serves as the interface between the :class:`Player` and the other
    elements of the game.

    **Collaborators**

    Collects the :class:`Outcome` instances; used
    by :class:`Player` to place a bet amount on a specific
    :class:`Outcome` objects; used by :class:`Game` instance to compute the amount
    won from the amount that was bet.

:Player:
    **Responsibilities**

    Places bets on
    :class:`Outcome` instances, updates the stake with amounts won and lost.
    This is the most important responsibility in the application, since we
    expect to update the algorithms this class uses to place different kinds
    of bets. Clearly, we need to cleanly encapsulate the :class:`Player` class,
    so that changes to this class have no ripple effect in other classes
    of the application.

    **Collaborators**

    Uses :class:`Table` object to place
    :class:`Bet` instances on preferred :class:`Outcome` instances; used by
    :class:`Game` object to record wins and losses.

:Game:
    **Responsibilities**

    Runs the game: gets bets
    from :class:`Player` object, throws the :class:`Dice` objects, updates the
    state of the game, collects losing bets, pays winning bets. This
    encapsulates the basic sequence of play into a single class. The overall
    statistical analysis is based on playing a finite number of games and
    seeing the final value of the :class:`Player` object's stake.

    **Collaborators**

    Uses
    :class:`Dice`, :class:`Table`, :class:`Outcome`,
    and :class:`Player` objects.


A Walk-through of Craps
------------------------

A good preliminary task is to review these responsibilities to confirm
that a complete cycle of play is possible. This will help provide some
design details for each class. It will also provide some insight into
classes that may be missing from this overview. A good way to structure
this task is to do a CRC walk-through. For more information on
this technique see :ref:`roul.solution.walkthrough`.


The basic processing outline is the responsibility of the :class:`Game`
class. To start, locate the :class:`Game` card.


#.  Our preliminary note was that this class "Runs the game." The
    responsibilities section has a summary of five steps involved in
    running the game.


#.  The first step is "gets bets from :class:`Player`." Find the
    :class:`Player` card.


#.  Does a :class:`Player` instance collaborate with a :class:`Game` instance to
    place bets? Note that the game state influences the allowed bets. Does
    :class:`Game` instance collaborate with :class:`Player` instance to provide
    the state information? If not, add this information to one or both cards.



#.  The :class:`Game` object's second step is to throw the :class:`Dice` objects.
    Is this collaboration on the :class:`Dice` card?


#.  The :class:`Game` object's third step is to update the state of the
    game. While the state appears to be internal to the :class:`Game` class,
    requiring no collaboration, we note that the :class:`Player` instance
    needs to know the state, and therefore should collaborate with the :class:`Game` class.
    Be sure this collaboration is documented.


#.  The :class:`Game` object's fourth and fifth steps are to pay winning
    bets and collect losing bets. Does the :class:`Game` instance collaborate
    with the :class:`Table` object to get the working bets? If not, update
    the collaborations.


Something we'll need to consider is the complex relationship between the
dice, the number rolled on the dice, the game state and the various
bets. In Roulette, a :class:`Wheel` instance picked a random :class:`Bin` object;
the bin had a simple list of winning :class:`Outcome` instances.
All :class:`Bet` instances on other :class:`Outcome` instances were losers. In Craps,
however, we find that we have game bets that are based on changes to the
game state, not simply the number on the dice. The random outcome is
used to resolve one-roll proposition bets, resolve hardways bets, change
the game state, and resolve game bets. It is not a simple :class:`Outcome` collection.


We also note that the house moves Come Line (and Don't Come) bets from
the Come Line to the numbered spaces. In effect, the bet is changed from a generic
:class:`Outcome` instance to a more specific :class:`Outcome` instance.
This means that a :class:`Bet` object has a kind of state change.
This parallels the :class:`Game` instance's
state change and any possible :class:`Player` instance state change.


..  important:: Stateful Objects

    Many interesting applications
    involve stateful objects. Everything that has a state or status or
    attributes that change, is stateful. State
    changes are almost universally accompanied by rules that determine
    legal changes, events that precipitate changes, and actions that
    accompany a state change.

    Stateful objects must be taken very seriously. The consequence of
    ignoring state change complications is software that performs invalid or unexpected state
    transitions.


A walk-through gives an overview of the interactions among the
objects in the working application. You may uncover additional design
ideas from this walk-through. The most important outcome of the
walk-through is a clear sense of the responsibilities and the
collaborations required to create the necessary application behavior.


Craps Solution Questions and Answers
-------------------------------------

Why is the :class:`Outcome` class distinct? Each object that is an
instance of the :class:`Outcome` class is merely a number from 2 to 12.

    We have complex interdependency between the dice, the game states,
    the bets and outcomes. An outcome has different meanings in different
    game states: sometimes a 7 is an immediate winner, other times it is an
    immediate loser. Clearly, we need to isolate these various rules into
    separate objects to be sure that we have captured them accurately
    without any confusion, gaps or conflicts.


    We can foresee three general kinds of :class:`Outcome` classes: the
    propositions that are resolved by a single throw of the dice, the
    hardways that are resolved periodically, and the game bets which are
    resolved when a point is made or missed. Some of the outcomes are only
    available in certain game states.


    The alternative is deeply nested if-statements. Multiple objects
    introduce some additional details in the form of class declarations, but
    objects have the advantage of clearly isolating responsibilities.
    Clear, narrow responsibilities makes
    us more confident that our design will work properly. If-statements only
    conflate all of the various conditions into a tangle that includes a
    huge risk of missing an important and rare condition.

    See the discussion under :ref:`roul.outcome.identity`  for more discussion
    on object identity and why each Outcome is a separate object.


What is the real difference between the classes :class:`Dice` and :class:`Wheel`?
Don't they both represent simple collections with random selection?


    Perhaps. At the present time, the distinction appears to be in the
    initialization. A :class:`Wheel` instance is a collection of :class:`Bin`
    objects. The :class:`Dice` object has 36 outcomes, each with a number
    of meanings.

    Generally, we are slow to merge classes together without evidence that
    they are really the same thing. In this case, they appear very similar,
    so we will note the similarities and differences as we work through the
    design details. There is a fine line between putting too many things
    together and splitting too many things apart.

    Generally, the bigger mistake seems to be conflating too many distinct things,
    and resolving the differences through complex if-statements and other hidden processing logic.


Looking Forward
---------------

In the next chapter we'll look closely at the various outcomes that stem from
rolling the dice. This will lead us to a deeper understanding of the existing
:class:`Outcome` class definition, and some rework to make it suitable for
both games.
