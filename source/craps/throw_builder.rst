
..  _`craps.throwbuilder`:

Throw Builder Class
===================

This chapter identifies some more subtleties of bets in Craps, and proposes
some rather involved design rework to resolve the issues that are
raised.

An instance of the :class:`Dice` class  is a container
for a set of :class:`Throw` instances.  Each :class:`Throw` instance contains a
set of :class:`Outcome` instances that are the basis for bets.

One additional feature is that a :class:`Throw` object will change the state of the game.
We must be sure to account for this additional responsibility.

A further problem is that the :class:`Outcome` object doesn't have a fixed
payout in Craps. This will alter the design for the :class:`Outcome` class yet again
to handle this feature.

We'll look at this in detail in `Throw Builder Analysis`_. We'll tackle
the variable odds feature in `Outcomes with Variable Odds`_.

This will lead us to refactor the :class:`Outcome` class. We'll look at this in
`Refactoring The Outcome Hierarchy`_.

We'll digress into some other design considerations in `Soapbox on Subclasses`_,
`Soapbox on Architecture`_, and `Throw Builder Questions and Answers`_.

After considering the alternatives, we'll look at two approaches to the
rework:

-   In `Design Light`_ we'll try to minimize the rework. The details
    will be in `Minimal Outcome Rework`_.

-   In `Design Heavy`_, we'll acknowledge that there is no "simple" solution.
    We'll look at the details in:

    -   `RandomEvent class`_,

    -   `Bin Rework`_,

    -   `Throw Rework`_, and

    -   `Outcome Rework`_.

After the rework is in place, qe can then look at the common design issues.
We'll cover these in `Common Design`_. This will include
`OutcomeField Design`_, `OutcomeHorn Design`_, and `ThrowBuilder Class Design`_.

In `Throw-Builder Deliverables`_ we'll enumerate the deliverables for this chapter.


We'll present sidebars on the proper design of subclasses and the proper
architecture for the packages that make up an application. Additionally,
we'll provide a brief FAQ on the design issues raised.


..  _`craps.throwbuilder.ov`:

Throw Builder Analysis
----------------------

Enumerating each :class:`Outcome` instance in the 36 :class:`Throw` instances
could be a tedious undertaking. We'll
design a :strong:`Builder` to enumerate all of the :class:`Throw` instances
and their associated list of :class:`Outcome` instances. This will build the
:class:`Dice`, finishing the elements we deferred from  :ref:`craps.dice`.


The 36 ways the dice fall can be summarized into 15 kinds of :class:`Throw` objects,
with a fixed distribution of probabilities. We have two ways to enumerate these.

-   We could develop a :strong:`Builder` class that enumerates the 36
    possible :class:`Throw` instances, assigning
    the appropriate attribute values to each object. This will create
    a number of duplicates: in Craps, dice showing :code:`(1, 2)` are equivalent
    to dice showing :code:`(2, 1)`

-   An alternative is for a :emphasis:`Builder`
    class to step through the 15 kinds of :class:`Throw` instances, creating the
    proper number of instances of each kind. There is one instance of :code:`(1, 1)`,
    two instances of :code:`(1, 2)`, etc.

We looked at this in :ref:`craps.ov.freq`. Because of the vast number of
one-off special cases (e.g. hardways outcomes), it seems simpler to
examine each of the 36 pairs of dice and determine which kind of :class:`Throw` to build.

The proposition bets define
eight one-roll :class:`Outcome` instances that need to be assigned
to the various :class:`Throw` instances we are building. We will
share references to the following :class:`Outcome` objects among the :class:`Throw` instances:

-   The number 2 proposition, with :math:`30:1` odds. There's only one instance of this, ``(1, 1)``.

-   The number 3 proposition, with :math:`15:1` odds. There are two instances, ``(1, 2)`` and ``(2, 1)``.

-   The number 7 proposition, with :math:`4:1` odds. There are six ways to throw this.

-   The number 11 proposition, with :math:`15:1` odds. There are two instances, ``(5, 6)`` and ``(6, 5)``.

-   The number 12 proposition, with :math:`30:1` odds. There's only one instance of this, ``(6, 6)``.

-   The "any craps" proposition, with :math:`7:1` odds. This belongs to all of the various
    combinations of dice that total 2, 3, or 12.

-   There are actually two "horn" proposition outcomes. One belongs to dice totalling 2 or 12,
    with odds of :math:`27:4`. The other belongs to dice totalling 3 or 11,
    with odds of :math:`3:1`. We'll address this below by reworking the :class:`Outcome` class.

-   There are two "field" proposition outcomes, also. One belongs to throws totalling
    2 or 12 and pays :math:`2:1`. The other belongs to throws totalling 3, 4, 9, 10, or 11
    and pays even money (:math:`1:1`
    ).

We can use the following algorithm for building the :class:`Dice`.

..  rubric:: Building Dice

**For All Faces Of Die 1**. For all :math:`d_1`, such that :math:`1 \leq d_1 < 7`:

    **For All Faces Of A Die 2**. For :math:`d_2`, such that :math:`1 \leq d_2 < 7`:

        **Sum the Dice**. Compute the sum, :math:`s \gets d_1 + d_2`.

        **Craps?** If :emphasis:`s` is in 2, 3, and 12, we create a :class:`CrapsThrow`
        instance. This will include a reference to one of the 2, 3 or 12 :class:`Outcome`
        s, plus references to the Any Craps, Horn and Field :class:`Outcome` instances.

        **Point?** For :emphasis:`s` in 4, 5, 6, 8, 9, and 10 we will create a :class:`PointThrow`
        instance.

            **Hard?** When :math:`d_1 = d_2`, this is a :emphasis:`hard` 4, 6, 8 or 10.

            **Easy?** Otherwise, :math:`d_1 \ne d_2`, this is an :emphasis:`easy` 4, 6, 8 or 10.

        **Field?** For :emphasis:`s` in 4, 9, or 10, we include a reference to the Field :class:`Outcome`.
        Note that 2, 3, and 12 Field outcomes where handled above under **Craps**.

        **Horn?** For :emphasis:`s` in 2, 3, 11, or 12, we include a reference to Horn :class:`Outcome`.

        **Natural?** For :emphasis:`s` of 7, we create a :class:`NaturalThrow`
        instance. This will also include a reference to the 7 :class:`Outcome`.

        **Eleven?** For :emphasis:`s` of 11, we create an :class:`ElevenThrow`
        instance. This will include references to the 11, Horn and Field :class:`Outcome` instances.

At this point, the algorithm is mostly a concept. We need to examine the outcomes
with variable odds, first.


Outcomes with Variable Odds
---------------------------

Our detailed examination of the bets has turned up an interesting fact
about Field bets and Horn bets: these outcomes have payoffs that depend
on the number on the dice. In the earlier chapter, :ref:`craps.outcome`,
we missed this nuance, and did not provide for a :meth:`Dice.winAmount`
method that depends on the :class:`Dice` value rolled.

We'll need to redesign the :class:`Outcome` class to handle these details.

**Problem Statement**. Unlike the Pass Line and Come Line bets, Field bets
and Horn bets have payoffs that depend on the number currently showing on the dice.
Note that Come Line bets that aren't resolved immediately are
moved on the table from the generic
Come Line to a new :class:`Outcome` object when a point is
established. This is not the case for Field and Horn bets, which aren't moved
around the table.

How do we compute the win amount for Field and Horn bets?


**Context**. Our design objective is to have a :class:`Bet` object refer to
a single :class:`Outcome` object.
Doing this allows a :class:`Bet` object's :class:`Outcome` instance to be compared
with a :class:`Set` of winning :class:`Outcome` instances.
The current :class:`Throw` object or the current :class:`Bin` object will have
collections of :class:`Outcome` objects.

We'd like to have a single horn :class:`Outcome` object and field :class:`Outcome`
object shared by multiple instances of a :class:`Throw` instance to make this
comparison work in a simple, general way.

As an example, the player can
place a bet on the Field :class:`Outcome` instance, which is shared by all
of the field numbers (2, 3, 4, 9, 10, 11, and 12). The problem we have is
that for 2 and 12, the outcome pays :math:`2:1` and for the other field numbers
it pays :math:`1:1`, and our design only has a single set of payout odds.


**Forces**. In order to handle this neatly, we have two choices.

-   Have two :class:`Outcome` instances bundled into a single :class:`Bet` object.
    This allows us to create a :class:`Bet` object include both the
    low-odds field outcome (3, 4, 9, 10 and 11) plus the high-odds field
    outcome (2 and 12). One of the nice features of this is that it is a
    small expansion to the :class:`Bet` class.

    Further research shows us
    that there are casino-specific variations on the field bet, including
    the possibility of three separate :class:`Outcome` instances for those
    casinos that pay :math:`3:1` on 12. This makes construction of the :class:`Bet`
    rather complex, and dilutes the responsibility for creating a proper :class:`Bet`.
    Once we put multiple :class:`Outcome` instances into a :class:`Bet` object,
    we need to assign responsibility for keeping the bundle of Field :class:`Outcome` instances
    together.

    Pursuing this further, we could expand the :class:`Outcome` class to follow the
    **Composite** design pattern. We could introduce a subclass
    which was a bundle of multiple :class:`Outcome` instances. This would allow
    us to keep the :class:`Bet` class very simple, but we still have to construct
    appropriate composite :class:`Outcome` instances for those complex
    :class:`Bet` instances. Rather than dive into allocating this
    responsibility, we'll look at other alternatives, and see if something
    turns up that doesn't add as much complexity.


-   Another approach is to add an optional argument to the :class:`Outcome` class
    that uses the current :class:`Throw` instance to calculate the final win amount.

    This allows us to have a single field bet :class:`Outcome` object with
    different odds for the various numbers in the field. This further allows
    us to create slightly different field bet :class:`Outcome` class
    definitions for the casino-specific variations on the rules.

**Solution**. Our first design decision, then, is to modify
the :class:`Outcome` class to calculate the win amount given the current
:class:`Throw` instance.

**Consequences**. There are a number of consequences of this design
decision.

-   Where in the :class:`Outcome` class hierarchy do we add this additional :meth:`winAmount` method?

-   We need to design the new :meth:`winAmount` method so that we don't
    break everything we've written so far.

This leads us to two rounds of additional problem-solving.

Refactoring The Outcome Hierarchy
---------------------------------

**Consequent Problem: Class Hierarchy**. While it appears simplest to add a
"variable odds" subclass of the :class:`Outcome` class with a new method that uses the number
on the dice, we find that there are some additional considerations.

Our design depends on
polymorphism among objects of the :class:`Outcome` class: all instances have the
same interface. In order to maintain this polymorphism, we need to add
this new method to the superclass. The superclass version of the new :meth:`winAmount`
based on the Craps :class:`Throw` object can return an answer computed by
the original :meth:`winAmount` method. We can then override this
in a subclass for Field and Horn bets in Craps.

An alternative is to break polymorphism and create a Craps-specific :class:`Outcome`
subclass. This would ripple out to the :class:`Throw`, :class:`Bet`,
:class:`Table`, and :class:`Player` classes. This is an unpleasant cascade
of change, easily avoided by assuring that the entire :class:`Outcome`
class hierarchy is polymorphic.

**Solution**.
Our second design decision, then, is to insert the change at the top of the :class:`Outcome`
class hierarchy, and override this new :meth:`winAmount` method in
the few subclasses that we use to create Horn and Field :class:`Outcome` instances.

-   The Horn bet :meth:`winAmount` method applies one of two odds,
    based on the event's value.

-   The Field bet may have any of two or three
    odds, depending on the casino's house rules. It is difficult to identify
    a lot of commonality between Horn bets and Field bets. Faced with these
    irreconcilable differences, we will need two different :meth:`winAmount`
    methods, leading us to create two subclasses: :class:`OutcomeField` and
    :class:`OutcomeHorn`.

The differences are minor, merely a list of numbers and odds. However,
our overall objective is to minimize ``if``-statements.
(Or, stated another way, we prefer to maximize the use of dependency
injection; or we prefer inversion of control.) We prefer many simple
classes over a single class with even a moderately complex method.

**Consequent Problem: Dependencies**.
We've decided to add a dependency to the :meth:`Outcome.winAmount`; specifically,
we've made it dependent on a :class:`Throw` object.  While this works
well for Craps, it makes no sense for Roulette.

To allow the games to evolve independently, we should not have any
dependencies between games.  This means that a general-purpose class like :class:`Outcome`
can't depend on a game-specific class like :class:`Throw`.  A general-purpose class
has to depend on some a superclass (or interface) that encompasses the Craps-specific :class:`Throw` as
well as the Roulette-specific :class:`Bin`.

**Additional Classes**. To break the dependency between a general-purposes class
and a game-specific class, we need introduce a superclass that includes both :class:`Throw`
and :class:`Bin` as subclasses.  This permits the :class:`Outcome` class to work
with either Craps and Roulette; keeping them independent of each other.

We could call the parent class a :class:`RandomEvent`.
This new class would have an integer event identifier: either the
wheel's bin number or the total of the two dice. Given this new
superclass, we could then rearrange both :class:`Throw` and :class:`Bin`
to be subclasses of :class:`RandomEvent`. This would also force us
to rework parts of the :class:`Wheel` class to create the :class:`Bin` instances.

A benefit of creating a :class:`RandomEvent` class hierarchy is that
we can change the new :meth:`winAmount` method to compute the win
amount given a :class:`RandomEvent` object instead of the highly Craps-specific
:class:`Throw` class. This makes the :meth:`winAmount` method far
more generally useful, and keeps Craps and Roulette separate from each other.

This technique of reworking the :class:`Throw` and :class:`Bin` classes to
be subclasses of a common superclass is a fairly common kind of
generalization refactoring: we found things which
needed to be unified because -- after some detailed study -- they're
closely related.

We walk a fine line here.

Sometimes, there's an urge to conflate many nearly-common features into
a single class, leading to a brittle design that cannot easily be
reworked. In our example, we considered lifting only one common attribute to
the superclass so that a related class (:class:`Outcome`) could
operate on instances of these two classes in a uniform manner. For more
information on this rework, see :ref:`soapbox.subclass`.

**Approaches**.
We will present two alternative designs paths: minimal rework, and a
design that is at the fringe of over-engineering. We're forced to
look at both options because we often have the urge (or are told
by managers) to focus on what seems like the quickest route.

..  _`soapbox.subclass`:

Soapbox on Subclasses
----------------------

Designers new to OO techniques are sometimes
uncomfortable with the notion of highly-specialized subclasses.
We'll touch on two reasons why specialized subclasses are far
superior to the alternative of highly-generalized superclasses.

One approach to creating common features is to add nested
``if``-statements instead of creating subclasses. In our example, we
might have elected to add ``if``-statements to determine if
this was a variable-odds outcome, and then determine which of
the available odds would be used. The first test (for being a
variable-odds outcome) is, in effect, a determination of which
subclass of :class:`Outcome` is being processed.

In some cases, ``if``-statements often imply a class structure.

Since an object's membership
in a class determines the available methods, there's no reason to
:emphasis:`test` for membership using ``if``-statements. In most cases,
the only relevant tests for
membership are done at construction time. If we
use an initial decision to select the subclass (with
appropriate subclass-specific methods) we do not repeat that
decision every time a method is invoked. This is the efficiency
rationale for introducing a subclass to handle these special cases.

Another more fundamental reason is specialized subclasses
usually represent distinct kinds of real-world things. We
are modeling the distinct classes of things in software-world.

In our
case, we have a number of distinct things, some of which are
related because they have common attributes and behavior. The :class:`Outcome` class
is fairly intangible, so the notion of commonality can be
difficult to see. Contrast this with the :class:`Dice` and :class:`Wheel` classes,
which are tangible, and are obviously different things,
however they have common behavior and a common relationship with
a casino game.

**Design Aid**.
Sometimes it helps to visualize this by getting pads of
different-colored sticky paper, and making a mockup of the
object structure on whiteboard. Each class is represented by a
different color of paper. Each individual object is an
individual slip of sticky paper. To show the relationship of the :class:`Dice`,
:class:`Throw` and :class:`Outcome` classes, we draw a large
space on the board for an instance of the :class:`Dice` class which
has smaller spaces for 36 individual :class:`Throw` instances.


In one :class:`Throw` instance, we put a sticky for :class:`Outcome`
s 2, Field, Horn, and Any Craps. We use three colors of stickies
to show that 2 and Any Craps are ordinary :class:`Outcome`
s, Field is one subclass and Horn is another subclass.


In another :class:`Throw` instance, we put a sticky for :class:`Outcome`
7, using the color of sticky for ordinary :class:`Outcome` instances.



This can help to show what the final game object examine to compute winning bets.
The game object will have a
list of winning :class:`Outcome` instances and bet :class:`Outcome` objects
on the table. When a 2 is thrown, the game process
will pick up each of the stickies, compare the winning :class:`Outcome` objects
to the bets, and then use the method appropriate to the color
of the sticky when computing the results of the bet.

..  _`soapbox.architecture`:

Soapbox on Architecture
------------------------

There are a number of advanced considerations behind the `Design Heavy`_
section. This is a digression on architecture and
packages of classes. While this is
beyond the basics of OO design, it is a kind of
justification for the architecture we've chosen.

A good design balances a number of forces. One example of this
is our use of a class hierarchy to decompose a problem into
related class descriptions, coupled with the collaboration among
individual objects to compose the desired solution. The desired
behavior emerges from this tension between decomposition of the
class design and composition of the objects to create the
desired behavior.

Another example of this decomposition vs. composition is the organization of our
classes into packages. We have, in this book, avoided discussion
of how we package classes. It is a more subtle aspect of a good
design, consequently we find it challenging to articulate sound
principles behind the layers and partitions of a good collection
of packages. There are some design patterns that give us
packaging guidance, however.

**Design Patterns**.
One packaging pattern is the **5-Layer Design**,
which encourages us to separate our design into layers
of view, control, model, access and persistence. For our
current application, the view is the output log written to :literal:`System.out`,
the control is the overall main method and the :class:`Simulation`
class, the model is the casino game model. We don't have any
data access or data persistence issues, but these are often
implemented with JDBC/ODBC and a relational database.

While one of the most helpful architectural patterns, this
version of the :strong:`5-Layer Design` still leaves us with
some unsatisfying gaps. For example, common or infrastructure
elements don't have a proper home. They seem to form another
layer (or set of layers). Further, the model layer often
decomposes into domain elements, plus elements which are
specializations focused on unique features of the business,
customer, vendor or product.

Another packaging pattern is the **Sibling Partition**,
which encourages us to separate our application-specific
elements to make them parallel siblings of a
superclass so that we can more easily add new applications or
remove obsolete applications. In this case, each casino game is
a separate application of our casino game simulator. At some
point, we may want to isolate one of the games to reuse just the
classes of that game in another application. By making the games
proper siblings of each other, and children of an abstract
parent, they can be more easily separated.

**General vs. Specific**.
Applying these layered design and application partitioning
design patterns causes us to examine our casino game model more
closely and further sub-divide the model into game-specific and
game-independent elements.

If some cases, we can partition the design elements into classes
that are part of the problem domain (casino games) and those
that are even more general application infrastructure
(e.g., simulation and statistics). Our ideal is to have a tidy,
short list of classes that provides a complete game simulation.
We can cut our current design into three parts: Roulette, Craps
and application infrastructure. This allows us to compose
Roulette from the Roulette-specific classes and the general
infrastructure classes, without including any of the
Craps-specific classes.

The following architecture diagram captures a way to structure
the packages of these applications.

..  image:: architecture.png

Our class definitions have implicitly followed this
architecture, working from general to game- and player-specific
classes. Our low-level classes evolved through several
increments. We find this to be superior to attempting to design
the general classes from the outset: it avoids any
over-engineering of the supporting infrastructure. Additionally,
we we careful to assure that our top-level classes contain
minimal processing, and are are compositions of lower-level
object instances.

**Dependencies**.
A very good design could carefully formalize this aspect of the
architecture by assuring that there are minimal references
between layers and partitions, and all references are "downward"
references from application-specific to general infrastructure
packages. In our case, a :class:`Simulator` class should have access only to
Player and Game layers.

Two Game partitions should separate there references between
these packages.

Finally, we would like to assure that the Player and Game don't
have invalid "upward" references to the Simulator. This is a matter
of discipline in the unit test cases.

Throw Builder Questions and Answers
------------------------------------

Why do we need the :class:`RandomEvent` class? Isn't this over-engineering?

    Clean separation between Craps and Roulette isn't necessary, but is
    highly desirable. We prefer not to have Roulette classes depend in any
    way on Craps classes. Instead of having them entangled, we factor out
    the entanglement and make a new class from this. This is also called
    reducing the coupling between classes. We prefer the term "entanglement"
    because it has a suitably negative connotation.


Why couldn't we spot the need for the :class:`RandomEvent` class earlier
in the design process?

    Some experienced designers do notice this kind of commonality between
    the :class:`Throw` and :class:`Bin` classes, and can handle it without
    getting badly side-tracked.

    Other designers can spend
    too much time searching for this kind of commonality. We prefer to
    wait until we are sure we've understood the problem and the solution
    before committing to a particular class design.


Isn't the goal to leave Roulette alone? Isn't the ideal to extend the
design with subclasses, leaving the original design in place?

    Yes, the goal is to extend a design via subclasses. But, this is only
    possible if the original design is suitable for extension by
    subclassing. We find that it is very difficult to create a design that
    both solves a problem and can be extended to solve a number of related problems.

    Note that a general, extensible design has two independent feature sets.
    On one level it solves a useful problem. Often, this is a difficult
    problem in its own right, and requires considerable skill merely to
    ferret out the actual problem and craft a usable solution within budget,
    time and skill constraints.

    On another, deeper level, our ideal design can be extended. This is a
    different kind of problem that requires us to consider the various kinds of
    design mutations that may occur as the software
    is maintained and adapted. This requires some in-depth knowledge of the
    problem domain. We need to know how the current problem is a
    specialization of other more general problems. We also need to note how
    our solution is only one of many solutions to the current problem. We
    have two dimensions of generalization: problem generalization as well as
    solution generalization.

    Our initial design for roulette just barely provided the first level of
    solution. We didn't make any effort to plan for generalization. The
    "Design Heavy" solution generalizes Roulette to make it more
    suitable for Craps, also. Looking forward, we'll have to make even more
    adjustments before we have a very tidy, general solution.


..  _`craps.throwbuilder.design.light`:

Design Light
------------

In order to get the Craps game to work, we can minimize the amount of
design. This minimal rework is a revision to the :class:`Outcome` class.

This is followed by `Common Design`_: the
two subclasses of the :class:`Outcome` class (:class:`OutcomeField`, and :class:`OutcomeHorn`),
and the initializer for the :class:`Dice` class.

This minimal design effort has one unpleasant consequence: Roulette's :class:`Outcome`
instances will depend on the Craps-specific :class:`Throw` class.
This entangles Roulette and Craps around a feature that is really a
special case for Craps only. This kind of entanglement often limits our
ability to successfully package and reuse these classes.

Minimal Outcome Rework
~~~~~~~~~~~~~~~~~~~~~~~~

The  :class:`Outcome` class needs a method to compute the win amount
based on a :class:`Throw`.


In Python, it's sensible to use optional parameters to achieve the same degree of
flexibility.

..  method:: Outcome.winAmount(self, throw: Throw=None) -> int
    :noindex:

    Returns the product this :class:`Outcome` instances
    odds numerator by the given amount, divided by the odds denominator.

    :param throw: An optional :class:`Throw` instance, used to determines the actual odds to use.
        If not provided, this :class:`Outcome` object's odds are used.
    :type throw: :class:`Throw`

    For Craps Horn bet and Field bets, a subclass will
    override this method to check the specific value of the :obj:`throw`
    and compute appropriate odds.

    All other classes will ignore the optional :obj:`throw` parameter.

In principle, this is all we need.

What's wrong? We've hopeless entangled Roulette and Craps at a deep level.
Roulette now depends on Craps details.

Sigh.

..  _`craps.throwbuilder.design.heavy`:

Design Heavy
------------

In order to produce a solution that has a better architecture with more
reusable components, we need to do some additional generalization. This
design effort disentangles Roulette and Craps; they will not share the :class:`Throw`
class that should only be part of Craps. Instead, the highly reused :class:`Outcome`
class will depend only on a new superclass, :class:`RandomEvent`, which
is not specific to either game.

Given the new generalization, the :class:`RandomEvent` class, we can rework the
:class:`Outcome` class to use this for computing win amounts.  We will have
to rework the :class:`Bin`, :class:`Wheel`, and :class:`Throw` classes
to make proper use of this new superclass.

Then we can move to the `Common Design`_ features: the
craps-specific subclasses (:class:`OutcomeField`, and :class:`OutcomeHorn`),
and the initializer for :class:`Dice`.

RandomEvent class
~~~~~~~~~~~~~~~~~

..  class:: RandomEvent(frozenset)

    The class :class:`RandomEvent` is the superclass for the random
    events on which a player bets. This includes the :class:`Bin` class of a
    Roulette wheel and the :class:`Throw` class of Craps dice.

    An event is a collection of individual :class:`Outcome` instances.
    Instances of the :class:`Bin` and :class:`Throw` classes can leverage
    this collection instead of leveraging :class:`frozenset` directly.

Using a common class of our definition is slightly better
than using a generic built-in class. The improvement is
that we can extend our class to add features.

Note that there's no real implementation. We can use the
:code:`pass` statement for the body.

Bin Rework
~~~~~~~~~~~~~~~~~~~~~~~~~

The  :class:`Bin` class needs to be a subclass of the :class:`RandomEvent` class.

The set of outcomes is removed from  the :class:`Bin` class; it's defined in the :class:`RandomEvent` class.

Throw Rework
~~~~~~~~~~~~

The  :class:`Throw` class needs to be a subclass of the :class:`RandomEvent` class.

The set of outcomes is removed from the :class:`Throw` class; it's defined in the :class:`RandomEvent` class.

Outcome Rework
~~~~~~~~~~~~~~

The  :class:`Outcome` class needs a method to compute the win amount
based on a :class:`RandomEvent` instance.

In Python, we use optional parameters for this

..  method:: Outcome.winAmount(self, event: RandomEvent=None) -> int
    :noindex:

    Returns the product this :class:`Outcome` instances
    odds numerator by the given amount, divided by the odds denominator.

    :param event: An optional :class:`RandomEvent` instance to determine the actual odds to use.
        If not provided, this :class:`Outcome` instance's odds are used.
    :type event: :class:`Throw`


    For Craps Horn bet and Field bets, a subclass will
    override this method to check the specific value of the :obj:`event`
    and compute appropriate odds.


Common Design
--------------

Once we've finished the rework, we can design the various specialized
outcomes required by Craps. We'll look at the two special cases we
identified:

-   `OutcomeField Design`_ will cover Field bets.

-   `OutcomeHorn Design`_ will cover Horn bets.

Once we've defined all of the possible outcomes, we can move forward
to building all of the throws. We'll examine this in `ThrowBuilder Class Design`_.

OutcomeField Design
~~~~~~~~~~~~~~~~~~~

..  class:: OutcomeField

    :class:`OutcomeField` contains a single outcome for a field bets
    that has a number of different odds, and the odds used depend on a :class:`RandomEvent`.

Methods
#######


..  method:: OutcomeField.winAmount(self, throw: Throw=None) -> int

    Returns the product this :class:`Outcome` object's
    odds numerator by the given amount, divided by the odds denominator.

    :param throw: An optional :class:`Throw` instance that determines the actual odds to use.
        If not provided, this :class:`Outcome` object's odds are used.
    :type throw: :class:`Throw`

..  method:: OutcomeField.__str__(self) -> str

    This should
    return a :class:`str` representation of the name and the odds. A
    form that looks like :literal:`Field (1:1, 2 and 12 2:1)` works nicely.



OutcomeHorn Design
~~~~~~~~~~~~~~~~~~

..  class:: OutcomeHorn

    :class:`OutcomeHorn` contains a single outcome for a Horn bet that
    has a number of different odds, and the odds used depend on a :class:`RandomEvent` instance.


Methods
#######



..  method:: OutcomeHorn.winAmount(self, throw: Throw=None) -> int

    Returns the product this :class:`Outcome` object's
    odds numerator by the given amount, divided by the odds denominator.

    :param throw: An optional :class:`Throw` object to determines the actual odds to use.
        If not provided, this :class:`Outcome` object's odds are used.
    :type throw: :class:`Throw`

..  method:: OutcomeHorn.__str__(self) -> str

    This should
    return a :class:`str` representation of the name and the odds. A
    form that looks like :literal:`Horn (27:4, 3:1)` works nicely.



ThrowBuilder Class Design
~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  class:: ThrowBuilder

    :class:`ThrowBuilder` initializes the 36 :class:`Throw` instances, each
    initialized with the appropriate :class:`Outcome` instances. Subclasses can
    override this to reflect different casino-specific rules for odds on
    Field bets.


Constructors
############


..  method:: ThrowBuilder.__init__(self) -> None


    Initializes the ThrowBuilder.


Methods
#######


..  method:: ThrowBuilder.buildThrows(self, dice: Dice) -> None
    :noindex:


    Creates the 8 one-roll :class:`Outcome`
    instances (2, 3, 7, 11, 12, Field, Horn, Any Craps).

    It then creates
    each of the 36 :class:`Throw` instances, each of which has the
    appropriate combination of :class:`Outcome` instances. The :class:`Throw` instances
    are assigned to :obj:`dice`.



Throw-Builder Deliverables
---------------------------

There are two deliverables for the light version of this exercise.

-   Rework the :class:`Outcome` class to add the new :meth:`winAmount`
    method that uses a :class:`Throw`.

-   Rework the :class:`Outcome` class unit test to exercise the new :meth:`winAmount`
    method that uses a :class:`Throw`. For all current subclasses of
    :class:`Outcome`, the results of both versions of the :meth:`winAmount`
    method produce the same results.

There are five deliverables for the heavy version of this exercise.

-   Create the :class:`RandomEvent` class.

-   Rework the :class:`Bin` class to be a subclass of :class:`RandomEvent`.
    The existing unit tests for :class:`Bin` should continue to
    work correctly.

-   Rework the :class:`Throw` class to be a subclass of :class:`RandomEvent`.
    The existing unit tests should continue to work correctly.

-   Rework the :class:`Outcome` class to add the new :meth:`winAmount`
    method that uses a :class:`RandomEvent`.

-   Rework the :class:`Outcome` class unit test to exercise the new :meth:`winAmount`
    method that uses a :class:`RandomEvent`. For all current
    subclasses of :class:`Outcome`, the results of both versions of the
    :meth:`winAmount` method produce the same results.

There a six common deliverables no matter which approach you take.

-   Create the :class:`OutcomeField` class.

-   Create a unit test for the :class:`OutcomeField` class. Two
    instances of :class:`Throw` are required: a 2 and a 3. This
    should confirm that there are different values for :meth:`winAmount`
    for the two different :class:`Throw` instances.

-   Create the :class:`OutcomeHorn` class.

-   Create a unit test for the :class:`OutcomeHorn` class. Two
    instances of :class:`Throw` are required: a 2 and a 3. This
    should confirm that there are different values for :meth:`winAmount`
    for the two different :class:`Throw` instances.

-   Create the :class:`ThrowBuilder`. This was our objective, after all.

-   Rework the unit test of the :class:`Dice` class. The unit test
    should create and initialize a :class:`Dice`. It can use the :meth:`getThrow`
    method to check selected :class:`Throw` instances for the correct :class:`Outcome` instances.


The correct distribution of throws is as follows. This information will
help confirm the results of :class:`ThrowBuilder`.


..  csv-table::

    "Throw","Frequency"
    2,1
    3,2
    "easy 4",2
    "hard 4",1
    5,4
    "easy 6",4
    "hard 6",1
    7,6
    "easy 8",4
    "hard 8",1
    9,4
    "easy 10",2
    "hard 10",1
    11,2
    12,1

Looking Forward
----------------

We've build the the core random event features of the Craps game.
We'll need to revisit the :class:`Bet` class and see how that has changed
as the other parts of the :class:`Outcome` and :class:`RandomEvent` classes
have changed.
