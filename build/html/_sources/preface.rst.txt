Preface
^^^^^^^

Why Read This Book?
===================

One way to master the OO design skill is to do the design and implementation of a large number of classes.
Mastery comes from patient, hard work, building software.

This book guides you through a series exercises to design and build dozens of classes.
The goal is
to create a large -- and reasonably complete -- application. You'll build and test
classes, write definitions, and see how the process of software construction works.

While it is also important to read examples of good design,
seeing a finished product doesn't reveal the designer's decision-making process.
Our goal in this book is to help programmer understand the design process that
leads to a final product.

This means there will be design changes and rework. One set of exercises will
suggest one solution, and another set will suggest improvements.

**Everything is Design**.
All software development involves considerable skill in design.
The distinction between "design" and "code" is blurry at best.
Pragmatically, it doesn't exist at all.

In some circles, there is an attempt to distinguish between
designers (or architects) and coders. The idea is that someone able to
work with a language -- coding -- may not quite be ready to do design work.

Consider an organization where designers are tasked to create detailed specifications.
These are given to coders to translate from natural language (e.g., English) into Python.
In this fantasy world, the coders are not expected
to make any further design decisions. They're "rewriting" natural language
to artificial language. This work is analagous to brick-layers who don't make
architectural design decisions.

The analogy, however, is flawed.

If the specification is so complete no further design decisions are required,
the specification was isomorphic to the resulting code.
A compiler could have translated the gloriously complete specification into
the target programming language. No coder is required.

Pragmatically, designers write specifications at a somewhat more abstract level.
A designer expects the coder to make a few small design decisions
as part of moving from the natural-language prose to concrete code.
The more abstract the specification, the more design work must be done.
The amount of design work is **always** non-zero; the boundary
between design and code is blurry at best.

The distinction between "design" and "code" is a matter of making informed
decisions about data structures and algorithms. This book provides a
number of contexts in which decisions must be made, and implemented.

The idea is to have a graduated sequence of decisions from relatively simple
to relatively profound.

What You'll Do
==============

This book provides a sequence of interesting and moderately complex exercises in
OO Design.  The exercises are not hypothetical,
but must lead directly to working programs. Unit tests are expected.
We'll demonstrate how to structure Python 3.7 type hints, also.

The applications we will build are a step above trivial,
and will require some careful thought to create a workable design.
Further, because the applications are largely recreational in nature, they
may be more interesting and engaging than other examples in other
books on design.

The exercises in the first part will be quite detailed.
The detail is less in the second section. The third part will summarize
the designs at a higher level of abstraction, expecting more
from the reader.

Audience
========

Our primary audience includes programmers who are new to OO Design and OO Programming.

Knowledge of the Python language is essential. Since the focus is on
OO techniques, some exposure to class definitions is important.
We will provide exercises
that have four key features:

-   complex enough to require careful design work,

-   fun enough to be engaging,

-   easy enough that results are available immediately, and

-   can be built in successive stages.

We'll provide a few
additional details on language features. We'll mark these as "Tips".
For more advanced students, these tips will be review material. We will not
provide a thorough background in any programming language. The student
is expected to know the basics of the language and tools.

Helpful additional skills include using one of the various unit test and
documentation frameworks available. We've included information in the appendices.

**Classroom Use**.
Instructors are always looking for classroom projects that are engaging,
comprehensible, and focus on perfecting language skills. Many real-world
applications require considerable explanation of the problem domain; the
time spent reviewing background information detracts from the time
available to do the programming. While all application
programming requires some domain knowledge, the idea behind these
exercises is to pick a domain that many people know a little bit about.
This allows an instructor to use some or all of these exercises without
wasting precious classroom time on incidental details required to
understand the problem.

Skills Required
================

This book assumes an introductory level of skill in the
Python language. We'll focus on Python 3.7 as a minimum.

Student skills we expect include the following.  If you can't do these
things, this book may be too advanced.

-   Install Python and various tools. The tools include
    **pytest**, **mypy**, and **sphinx**.

-   Create source files, run application programs, and run tools.
    We don't discuss any specific Integrated
    Development Environment (IDE), but learning how to use
    and IDE can be helpful. We leave it to the reader to experiment
    with IDE selection.

-   Use of the core procedural programming constructs: variables,
    statements, exceptions, functions.

-   Some exposure to class definitions and subclasses. This includes
    managing the basic features of inheritance, as well as overloaded
    method names.

-   Some exposure to Python's variety of built-in collections.

-   Some exposure to Python's type hints.

-   Optionally, some experience with a unit testing framework. We'll
    emphasis the **pytest** framework because it's very easy to use.

Organization of This Book
=========================

This book presents a series of exercises to build simulations of the
common, popular casino table games: Roulette, Craps,
and  Blackjack. Each simulation can be extended to include
variations on the player's betting system. With a simple statistical
approach, we can show the realistic expectations for any betting system.

Each game has a separate part in this book. Each part consists
of a number of individual exercises to build the entire simulation. The
completed project results in an application that can provide
tabular results that shows the average losses expected from each betting strategy.

Yes: losses. Only the house wins in a casino.

Since the game is already rigged against the play, the
only interesting variable is the player's betting strategy.
Each design will permit easy
implementation of various betting approaches. The resulting
application program allow exploration of what (if any) player actions can
minimize the losses.

Spoiler alert: you will always lose.

Each game has unique features. We'll start with the simplest and build
out toward the most complex.

**Roulette**.
For those who've never been in a casino, or seen movies that have
casinos in them, Roulette is the game with the big wheel.  A croupier
spins the wheel and toss in a marble.  When the wheel stops spinning,
the bin in which the marble rests defines the winning outcomes.

Once the random choice has been made, the bets are resolved.
People who bet on the right things get money.  People who bet on the
wrong things lose money.

The :ref:`roul`, section describes the necessary
application classes. The first chapter provides details on the game
and the problem that the simulation solves.

The second chapter is an overview of the solution,
setting out a design for the
application software. This will provide a road-map through
the solution to be built.

Each of the remaining sixteen chapters is a design and programming
exercise to be completed by the student. Each chapter has the same
basic structure: an overview of the components being designed, some
design details, and a summary of the deliverables to be built.

The chapter overview section presents some justification and rationale for the
design. This material should help the student understand why the
particular design was chosen. The design section provides a more
detailed specification of the class or classes to be built. This will
include some technical information on implementation techniques.

Some chapters include a Frequently Asked Questions (FAQ) section,
also. This covers somewhat more advanced material as well as tangential
topics.

**Craps**.
For those who've never been in a casino, or seen the play "Guys and Dolls",
Craps is the game with the dice.  A player rolls ("shoots") the dice.  Sometimes there's
a great deal of shouting and clapping.  A throw of the dice may -- or may not --
resolve bets.  Additionally, a throw of the dice may -- or may not -- change
the state of the game.  A casino provides a number of visual cues
as to the state of the game and the various bets.

In :ref:`craps`, we build on the design patterns from Roulette.
Craps, however, is a stateful game, so there is a more sophisticated
design to handle the interactions between dice, game state, and player betting.
We exploit the :strong:`State` design pattern to show how the design
pattern can be applied to this common situation.

The first chapter of this section is background information on the game of Craps, and
the problem that the simulation solves. This will describe
some of the design considerations for a stateful game.

The second chapter is an
overview of the solution. This will summarize the design for the
application software. This chapter also provides a "walk-through"
of the design.

Each of the remaining eleven chapters is an exercise to be completed by
the student. As with the previous section, each
chapter has the same basic structure: an overview of
the component being designed, some design details, and a summary of the
deliverables to be built.

**Blackjack**.
For those who've never been in a casino, or seen a movie with Blackjack,
Blackjack is a game with cards.  The dealer deals two cards to themselves and
each player.  One of the dealer's card is revelaed, providing
a little bit of information on the dealer's hand.

The player is confronted with two separate kinds of choices.
They can place bets. They can also ask for additional cards ("take a hit") or
decline cards ("stand pat".)

In Craps and Roulette there are a lot of bets, but few player decisions.
In Blackjack, there are few bets, but more complex player decisions.

In :ref:`blackjack`, the first two chapters are background information on the game of
Blackjack, the problem that the simulation solves.
This includes an overview of the solution.

Each of the remaining six chapters is an exercise to be
completed by the student. Since this is more advanced material, and
builds on previous work, this part has multiple deliverables
compressed into the individual chapters.

**Fit and Finish**.
We include a few fit-and-finish issues in :ref:`finish`.  This
includes more information and examples on packaging, test automation, and documentation.

Additionally, this section will cover some "main program" issues required to knit
all of the software components together into a finished whole.
This is the Command-Line Interface (CLI) for running the
complete application.


Why This Subject?
=================

Casino table games may seem like an odd choice of subject
matter for programming exercises. We find that casino games have a
number of advantages for teaching OO design and OO programming.
Here are some of the key points:

-   Casino games have an almost ideal level of complexity. If the games were
    too simple, the house's edge in the outcomes would be too obvious and
    people would not play. If the games were too complex, people would
    not enjoy them as recreation. Years (centuries?) of
    experience in the gaming industry has fine-tuned the table games to
    fit nicely with the limits of our human intellect.

-   Simulation of discrete phenomena lies at the origin of
    OO design. We have found it easier to
    motivate, explain and justify OO design when
    solving simulation problems of various types. The student can then leverage this
    insight for other, non-simulation problem domains.

-   The results are statistically simple, and easy to interpret.
    Probability theory has been applied by others to develop
    precise expectations for each game. A simulation should produce
    results consistent with the known probabilities.

-   They're more fun than most other programming problems.

This book does not endorse casino gaming. Indeed, one of the messages of
this book is that all casino games are biased against the player. Even
the most casual study of the results of the exercises will allow the
student to see the magnitude of the house edge in
each of the games presented. The question is not whether or not the
player in a casino loses; that's a given. The question is "how much?"

Mathematical Background
=======================

Among the topics this book deals with in a casual -- possibly
misleading -- manner are probability and statitics. Experts may spot a
gaps in our exposition. For example, there isn't a compelling
need for simulation of the simpler games of Craps and Roulette, since
they can be completely analyzed.

Because our primary objective is to
study programming, not casino games, we don't mind re-solving
well-known problems. Consequently, we tend to gloss over some
foundational mathematics to focus on the programming.



Conventions Used in This Book
=============================

Here is how we might present code.

..  rubric:: Typical Code Python Example

..  include:: ../code/preface.py
    :code: python

#.  We create a Python dictionary, a map from key to value. We
    use the :class:`collections.defaultdict` so that missing keys are
    created in the dictionary with an initial value created by the :func:`int`
    function.

#.  We iterate through all combinations of two dice, using
    variables :obj:`i` and :obj:`j` to represent each die.

#.  We sum the dice to create a roll.  We increment the value
    in the dictionary based on the roll.

#.  Finally, we print each member of the resulting dictionary.
    We've used a sophisticated format string that interpolates
    a decimal value and a floating-point percentage value.

The output from the above program will be shown as follows:

..  parsed-literal::

     2  2.78%
     3  5.56%
     4  8.33%
     5 11.11%
     6 13.89%
     7 16.67%
     8 13.89%
     9 11.11%
    10  8.33%
    11  5.56%
    12  2.78%

In some cases, we'll show examples based on interactive Python.

::

    >>> from collections import Counter
    >>> import random
    >>> random.seed(100)
    >>> rolls = [random.randint(1,6) + random.randint(1, 6) for _ in range(1_000)]
    >>> Counter(rolls).most_common()
    [(8, 151), (7, 150), (6, 132), (9, 108), (5, 93), (10, 87),
     (4, 77), (11, 68), (3, 65), (12, 35), (2, 34)]

The `>>>` prompt comes from the Python run-time. In this example,
there are five statements. The result is a list of pairs, showing
the results created by a :class:`collections.Counter` object.

These examples show work to be done to confirm something
or learn what the proper syntax is. These kinds of examples
of interaction with Python don't form part of the final, deliverable
software.

We will use the following type styles for references to a specific :class:`Class`,
:meth:`method`, or :obj:`variable`.

..  tip:: Tips Look Like This

    There will be design tips, and warnings, in the material for each
    exercise. These reflect considerations and lessons learned that
    aren't typically clear to starting OO designers.

