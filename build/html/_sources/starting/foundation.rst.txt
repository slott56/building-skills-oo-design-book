..  _`found`:

Foundations
###########

This section starts with a `Problem Statement`_.
This attempts to define the context in which the problem arises, the
problem to be solved and any forces that
influence the choice of solution. Given  this,
it can propose a solution and some consequences of the
chosen solution.

Based on the problem statement, this section describes a use
case for this software. This will be `Our Simulation Application`_.
In this section, we'll look at the
overall strategy and establish some areas of responsibility for
various software components.

We'll look at some issues in
`Methodology, Technique and Process`_ that are not technical in nature.
They're more procedural and provide some direction on development, testing
and writing documentation.

In `Additional Topics: Non-Functional Requirements`_ we'll look at issues
like Quality, Rework, Reuse, and Design Patterns.

Finally, we'll look at rework in `Rework and the Learning Process`_.
Doing rework to correct initial assumptions
is an important part of the way this book is organized.

..  important:: Fools Rush In

    It's important not to rush in to programming.

    Be sure you understand the problem being solved and how
    software solves that problem.

Let's look closely at the problem we're going to solve.

..  _found.problem:

Problem Statement
===================

**Context**.
We're going to study the "classic" casino table games
played against the house, including Roulette, Craps and Blackjack. We
want to explore the consequences of various betting strategies for
these casino games.

Questions include "How well does the
Cancellation strategy work?" "How well does the
Martingale strategy works for the Come Line odds bet in Craps?"
"How well does this Blackjack strategy I found on the Internet
compare with the strategy card I bought in the gift
shop?"

A close parallel to this is exploring variations in rules and how
these different rules have an influence on outcomes. Questions include
"What should we do with the 2× and 10× odds offers in
Craps?" "How should we modify our play for a single-deck
Blackjack game with 6:5 blackjack odds?"

Our context does not include exploring or designing new casino
games. Our context also excludes multi-player games like poker.

**Problem**.
Our problem is to answer the following question: :emphasis:`For a
given game, what player strategies produce the best
results?`

**Forces**.
There are a number of forces that influence our choice of
solution. Here's an overview:

-   We want an application that is has bounded complexity.
    Instead of producing a rich, sophisticated interactive user
    interface, we will produce raw data and statistical
    summaries. A command-line interface (CLI)
    lets the user  specify a betting strategy; the application
    will respond with a presentation of the
    results. Using a comma-separated values
    (CSV) format, the can be pasted into a
    spreadsheet for further analysis.

-   We want an application that is easy to extend to different
    betting strategies as well as new games. The customization
    is done by modifying the supplied code.
    The user can build a new betting strategy, test it, and run simulations.

-   We need to reflect actual game play.
    A long-running simulation of thousands of individual cycles of play will
    approach the theoretical results. However, people typically don't spend more than
    a few hours at a table game. If, for example, a Roulette wheel is spun
    once each minute, a player is unlikely to see more that 120 spins in
    two hours at a casino.

-   Additionally, many players have a fixed
    budget, and the betting is confined by table limits.
    This means that the betting strategy needs to address the subject of
    "money management:" a player may
    elect to stop playing when they are ahead or cut their losses
    when they are behind.


**High-Level Use Case**.
The high-level use case is the overall cycle of
investigation. The actor's goal is to find an optimal strategy for a given game.

Here's the scenario we're imagining.

1.  **Actor**:
    Uses an IDE to build new classes for a simulator and runs the
    updated simulation. The classes may provide variant game
    rules, variant play strategies, or variant betting strategies.

2.  **IDE**:
    Responds with output from running unit tests.

#.  **Actor**:
    Runs the simulator with selection of
    game and strategy.

#.  **Simulator**:
    Responds with statistical results.

#.  **Actor**.
    Evaluates the results. Uses a spreadsheet or other tool for
    analysis and visualization. Perhaps another Python application
    digests the simulation output to produce summaries.

**Consequences**.
We're going build the simulator application around the use case.

We won't address how to analyze the results. That's a separate,
and interesting topic.

One of the most important consequences of our solution is building
an application into which new player betting strategies
can be inserted. Clever gamblers invent new strategies all the time.

We will not know all of the available strategies in advance, so we
will not be able to fully specify all of the various design details in
advance. Instead, we will find ourselves reworking some parts of the
solution, to support a new player betting strategy.

Given this overview of the simulation and modeling intent, we
can look at the application program and how we'll use it. In the
next section we'll provide the overall concept behind using this application.

..  _`found.solution`:

Our Simulation Application
==========================

What will our application look like?

From reading the problem and use case information, we can identify
at least the following four elements to our application.

-   The game being simulated. This includes the various
    elements of the game: the wheel, the dice, the cards, the table,
    and the bets.

-   The player being simulated. This includes two separate details:

    -   Decisions the player makes based on the state of the game.
        Blackjack has complex player decisions.

    -   Betting choices based on the state of the game.
        Craps has very complex betting decisions.

-   The statistics being collected.

-   An overall control component which processes the game,
    collects the statistics, and writes the details or the final
    summary.

While potentially interesting, we will not pursue the design of a
general-purpose simulation framework. Nor will we use any of the
available general frameworks. While these are handy and powerful tools,
we want to focus on developing application software "from scratch"
(or *de novo*) as a learning exercise.

For more information on a general simulation tool, see https://mesa.readthedocs.io/en/master/.

A typical execution of the simulator application will look like the following
example:

..  _`found.solution.ex1`:

..  rubric:: Sample Execution

..  code-block:: sh

    python3 -m casino.craps --Dplayer.name="Player1326" >details.log

1.  We select the main simulator control using the package
    :mod:`casino` and the module :mod:`craps`.

#.  We define the player to use, :samp:`player.name="Player1326"`.
    The main method will use this parameter to create objects and execute the simulation.

#.  We collect the raw data in a file named :file:`details.log`.

There are a number of more technical considerations that we will
expand in :ref:`found.starting`. These include the use of an
overall application framework and an approach for unit testing.

In addition to the software itself, we also need to look closely
at how we'll build this software. In the next section, we'll
look at our overall approach, often called the "methodology".
We'll look at some specific techniques and talk about the
process of building software.

Methodology, Technique and Process
===================================

The intent of this book is to focus on programming language and design skills;
we won't narrowly follow the details any
particular software development methodology.
We prefer to lift up a few techniques which seem to have the most benefit.

-   Incremental Development. Each chapter is a "sprint" that
    produces some collection of deliverables. Each part of the book is a complete
    release.

-   Unit Testing. We don't dwell on test-driven development, but
    each chapter explicitly requires unit tests for the classes
    built. Ideally, one writes the test cases first.

-   Static Analysis. We'll provide suggested type hints. The student
    should use **mypy** to provide some confidence the code is likely
    to work as expected.

-   Embedded Documentation. We'll describe the documentation
    expectations.

The exercises are presented as if we are doing a kind of iterative
design with small deliverables. We present the exercises like
this for a number of reasons.

1.  We find design is helped by immediate feedback.
    While we present the design in considerable detail,
    we do not present the final code. Programmers new
    to OO design will benefit from repeated exposure to the
    transformation of problem statement through design to code.

2.  This presentation parallels the way software is developed.
    A project may emphasize larger collections of deliverables.
    However, the actual creation of working eventually decomposes into classes, fields and
    methods.

For developers enamored of a strict waterfall methodology --
with all design work completed before any programming work -- the book
can be read in a slightly different order. From each exercise chapter,
read only the **overview** and **design** sections. From that information,
integrate the complete design. Then proceed through the **deliverables**
sections of each chapter, removing duplicates and building only the
final form of the deliverables based on the complete design.

This preliminary work to create a waterfall project is quite difficult.

Making Technical Decisions
---------------------------

Many of the chapters will include some lengthy design discussions.
Some of these will appear to be little more than hand-wringing over nuances.
Others appear to be "thinking out loud."

Pragmatically, it helps to do a certain amount of hand-wringing over OO design.
We call it "Looking For The Big Simple". It can take a great
deal of time and effort to find a simple implementation for a complex problem.
A technique that helps is to enumerate the alternatives with pros and cons.

Our intent can be summarized as follows:

    Good design comes from a good process for
    technical decision-making.

    Admit what is unknown, and take steps to reduce
    our degrees of ignorance. Do research. Write proofs-of-concept.

    Budget time for exploring the bad designs before arriving at a good design.

    A little more
    time spent on design can result in considerable simplification,
    which will reduce overall development and maintenance costs.

It's also important to note that people are not
omniscient. Some of the exercises include intentional dead-ends. As a
practical matter, we can rarely foresee all of the consequences of a
design decision and we need to be prepared to undertake rework.

We've looked at the problem, and an overview of our solution;
these are the functional requirements for the solution.
In this section, we looked out some of the techniques and
processes. In the next section, we'll look at some additional
considerations for the product we'll create; these are
non-functional requirements.

Additional Topics: Non-Functional Requirements
===============================================

We can decompose software requirements into two broad categories:

-   **Functional Requirements**. These are the things the software
    must do. The use cases should address this completely. The point
    of use cases is to describe what the user will do with
    the software.

-   **Non-Functional Requirements**. These are the supporting
    ideals and principles that make good software. This includes
    compatibility with multiple operating systems, auditability
    of the results, retention of history, and other topics.

The number of non-functional features of software is large.
We'll talk about a few of them, specifically:

-   `General aspects of software quality`_,

-   `Reusability of code`_,

-   `Design patterns and principles`_.


General aspects of software quality
-----------------------------------

Our approach to overall quality will
focus on unit tests, static analysis, and documentation.
There are many more things which can be thought of
when considering software quality.

Here's a broad list of quality topics:

-   Need Satisfaction.

-   Performance and Resource Use.

-   Maintenance.

-   Adaptation and Change.

-   Organizational Considerations.

**Need Satisfaction**.
This is the essence of the functional requirements:
does the software meet the need? If we start with a problem
statement, and define the use cases, we'll often write software which is
focused on the user's needs.

**Performance**.
We don't address performance specifically in this book. However,
the presence of extensive unit tests allows us to alter the
implementation of classes to change the overall performance of our
application. As long as the resulting class still passes the
unit tests, we can develop numerous alternative implementations
to optimize speed, memory use, input/output, or any other
resource.

**Maintenance**.
Software is something that is subject to a great deal of change.
It changes when we uncover and fix bugs. More commonly, it changes when our
understanding of the problem, the actor, or the use case changes.

In many cases, our initial solution merely clarifies the actor's
thinking. After using an application, we'll need to alter the
software to reflect the user's deeper understanding of the problem.

Software maintenance is just another cycle of the iterative approach
we've chosen in this book. We pick a feature, create or modify
classes, and then create or modify the unit tests. In the case of
bug fixing, we often add unit tests to demonstrate the bug, and
then fix our classes to pass the revised unit tests.

**Adaptation**.
Adaptation refers to our need to adapt our software to
changes in the context where its used. The context can
include interfaces, operating systems, or platforms.
When we address issues of
interoperability with other software, portability to new
operating systems, scalability for more users, we are addressing
adaptation issues.

**Organizational**.
There are some organizational quality factors: cost of
ownership and productivity of the developers creating it. We
don't address these directly. Our approach, however, of
developing software incrementally often leads to good developer
productivity.

The non-functional requirements are secondary to the functional
requirements. If the software doesn't work in the first place,
it doesn't matter how adaptable it is.

In addition to looking at quality overall, we also need
to consider reuse of the software. This can be daunting, and
it's important to have concrete goals for the reusability
of software we write.

Reusability of code
-------------------

While there is a great deal of commonality among the three
games, the exercises do not start with an emphasis on constructing a
general, reusable framework. We find that too much generalization and too much
emphasis on reuse is not appropriate for
beginning OO designers.

Additionally, we find that projects that begin with too-lofty reuse goals often fail to
deliver valuable solutions in a timely fashion. We prefer not to start
out with a goal that amounts to boiling the ocean to make a
pot of tea.

While a promise of OO design is reuse, this
needs to be tempered with some pragmatic considerations. There are
two important areas of reuse:

-   Reusing a class specification to create objects with common
    structure and behavior, and

-   Using inheritance to reuse structure and behavior among
    multiple classes of objects.

Beyond these two areas, undue emphasis on reuse can create more cost than value.

The first step in reuse comes from isolating
responsibilities to create classes of objects. Generally, a number
of objects that have common structure and behavior is a kind of
reuse. When these objects cooperate to achieve the desired
results, this is sometimes called emergent
behavior: no single class contains the
overall functionality, it grew from the interactions among the
various objects.

The second step in OO reuse is
inheritance. The subclass-superclass relationship yields a
form of reuse: a class hierarchy with six subclasses will share
the superclass code seven times over. This, by itself, has
tremendous benefits.

We caution against any larger scope of reuse. Sharing
classes between projects may or may not work out well. The
complexity of achieving inter-project reuse can be paralyzing to
first-time designers. Often, different projects reflect different
points of view, and the amount of sharing is limited by these
points of view.

As an example, consider a product in a business
context. An external customer's view of the product (shaped by
sales and marketing) may be very different from the internal views
of the same product. Internal views of the product (for example,
finance, legal, manufacturing, shipping, support) may be very
different from each other. Reconciling these views may be far more
challenging than a single software development project. For that
reason, we don't encourage this broader view of reuse.

For our purposes in this book, there's no broader reuse goal.
We'll avoid considerations appropriate to larger frameworks,
or complex enterprise applications.

An important quality consideration is writing software that
fits commonly-understood design patterns. We'll look
at the question of design patterns next.

Design patterns and principles
------------------------------

These exercises will refer to several common design patterns.
A Design Patterns book is not a prerequisite;
a reader may want to find books on design patterns to gain additional
insight into the design patterns used here. We feel that use of common
design patterns significantly expands the programmer's repertoire of
techniques.

Many design pattern books are focused on languages like C++ and Java,
where language rules can create sticky situations requiring some
moderately clever and insightful programming techniques.
Python has a different set of language features, changing several
classic design patterns in profound ways. For this reason, we don't
strongly recommend spending a lot of time studying design patterns
outside the Python language context.

While well-known design patterns can be helpful, they often require
some experience to see how they work and what the possible value is.
We suggest paying close attention other software, reading widely,
and looking for common features that form recognizable patterns.

The process of writing software often involves dead-ends, mistakes,
and rework. In the next section, we'll address the concept of rework
and how this book helps you to tackle the inevitable rework problems
that arise.

In the next section we'll look at an important part of the overall
process for building software. We need to understand lessons learned
along the way, and deal gracefully with the need to rework software.


Rework and the Learning Process
================================

In :ref:`found.problem`, we described the problem.
In :ref:`found.solution`, we provided an overview of the
solution. The following parts will guide you through an incremental
design process; a process that involves learning and exploring. This
means that we will coach you to build classes and then modify those
classes based on lessons learned during later steps in the design
process. See our :ref:`Soapbox on Rework <soapbox.rework>`
for an opinion on the absolute necessity for design rework.

We don't present a complete design for the entire application.
We feel that it is very important follow a realistic problem-solving trajectory.
Beginning designers should be exposed to the
decisions involved in creating a complete design. In our experience,
all problems involve a considerable amount of "learn as you go".

We want to reflect this in our series of exercises. In
many respects, a successful OO design is one that
respects the degrees of ignorance that people have
when starting to build software. We will try to present the exercises
in a way that teaches the reader how to manage ignorance and still
develop valuable software.


..  sidebar:: Soapbox on Rework

    ..  _soapbox.rework:

    .. important::

        The best way to learn is to make mistakes.

        Rework is a consequence of learning.

    All of software development can be described as various
    forms of knowledge capture. A project begins with
    many kinds of ignorance and takes steps to reduce
    that ignorance. Some of those steps should involve revising or
    consolidating previous learnings.

    A project without rework is suspiciously
    under-engineered.

For some, the word :emphasis:`rework` has a negative
connotation. If you find the word distasteful, please replace every
occurrence with any of the synonyms: adaptation, evolution,
enhancement, mutation. We prefer the slightly negative connotation
of the word rework because it helps managers realize the importance
of incremental learning and how it changes the requirements, the
design and the resulting software.

Since learning will involve mistakes, good management plans
for the costs and risks of those mistakes. Generally, our approach
is to manage our ignorance; we try to create a design such that
correcting a mistake only fixes a few classes.

We often observe denial of the amount of ignorance involved in
creating IT solutions. It is sometimes very
difficult to make it clear that if the problem was well-understood,
or the solution was well-defined there would be immediately
applicable off-the-shelf or open-source solutions. The absence of a
ready-to-hand solution generally means the problem is hard. It also
means that there are several degrees of ignorance: ignorance of the
problem, solution and technology; not to mention ignorance of the
amount of ignorance involved in each of these areas.

We see a number of consequences of denying the degrees of
ignorance.

-   **Programmers**.
    For programmers experienced in non-OO
    (e.g. procedural) languages, learning OO design
    can be difficult and frustrating. When this is
    new, it helps to make mistakes to learn effectively.
    Programmers need time and space to explore and make mistakes.
    Feel free to rework your solutions to make them better. Above all, do not attempt to
    design a solution that is complete and perfect the very first
    time. We can't emphasize enough the need to do design many times
    before understanding what is important and what is not important
    in coping with ignorance.

-   **Managers**.
    For managers, the
    design rework appears to be contrary to the fanciful expectation of
    reduced development effort from OO techniques.
    The usual form for the complaint is the following: "I
    thought that OO design was supposed to be easier
    than non-OO design." We're not sure where
    the expectation originates, but good design takes time, and
    learning to do good design seems to require making mistakes. Every
    project needs a budget for making the necessary mistakes,
    reworking bad ideas to make them good, and searching for
    simplifications.

We find that early "high-level" designs will
miss details of the problem domain. This will lead to rework.
Forbidding rework amounts to mandating a full understanding of the
problem prior to any code.

In most cases, our users do not fully understand their
problem any more than our developers understand our users.
Generally, it is very hard to understand the problem, the technology,
and the solution. We find that hands-on use of preliminary versions of
software can help more than endless conversations about what could
be built.

Looking Forward
===============

We've looked at the problem, the general form of the solution.
We've talked a bit about the process or methodology to be used,
and some of the non-functional requirements. We've even acknowledged
that mistakes will be made, and rework will be part of the process.


In the next chapter, we'll talk specifically about the what
tools to install, and what deliverables will be created.
