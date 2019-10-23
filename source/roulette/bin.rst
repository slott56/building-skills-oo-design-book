
..  _`roul.bin`:

Bin Class
=========

This chapter will present the design for the :class:`Bin` class.
In `Bin Analysis`_ we'll look at the responsibilities and collaborators
for a bin.

As part of designing the :class:`Bin` class, we need to choose what
is the most appropriate kind of collection class to use.
We'll show how to do this in `Design Decision -- Choosing A Collection`_.

In `Wrap vs. Extend a Collection`_ we'll look at two
principle ways to embed a collection class in an application.
We'll clarify a few additional issues in `Bin Questions and Answers`_.

In the `Bin Design`_ section we'll provide the detailed design
information. In `Bin Deliverables`_ we'll enumerate what must be
built.

Bin Analysis
------------

The Roulette wheel has 38 bins, identified with a number and a color.
Each of these bins defines a number of closely related winning
:class:`Outcome` instances.

Each :class:`Bin` object will have from one to fourteen different
:class:`Outcome` instances. An individual number pays a variety
of bets because it's associated with a number of outcomes.
The number 12, for example, is also even. The exact collection
of :class:`Outcome` instances for each :class:`Bin` is
part of a later exercise.

At this time, we'll define the :class:`Bin` class, and use
this class to contain a number of :class:`Outcome` objects.

Two of the :class:`Bin` instances have relatively few :class:`Outcome` instances.
These are the exceptional cases:

-   The zero :class:`Bin` instance contains a "0"
    :class:`Outcome` object and the "00-0-1-2-3" :class:`Outcome` object.

-   The double-zero :class:`Bin` instance contains
    a "00" :class:`Outcome` object and the "00-0-1-2-3" :class:`Outcome` object.

The other 36 :class:`Bin` instances contain a mixture of bets including
a straight bet, split bets,
street bets, corner bets, line bets and all of the outside bets (column,
dozen, even or odd, red or black, high or low). Any of these bits will win
if this :class:`Bin` is selected.

Some :class:`Outcome` instances, like "red" or "black", occur in as many as 18 individual
:class:`Bin` instances. Other :class:`Outcome` instances, like the straight bet
numbers, each occur in only a single :class:`Bin`. We will have to
be sure that our :class:`Outcome` objects are shared appropriately
by the :class:`Bin` instances.

Since a :class:`Bin` is a collection of individual :class:`Outcome`
objects, we have to select a collection class to contain the objects.
In the next section we'll overview how this choice of a collection
can be made.

..  _`roul.bin.collections`:

Design Decision -- Choosing A Collection
----------------------------------------


There are five basic Python types that are a containers for other objects.

-   **Immutable Sequence**: :class:`tuple`.
    This is a good candidate for the kind of collection we need, since the
    elements of a :class:`Bin` don't change.  However, a :class:`tuple` allows
    duplicates and retains things in a specific order; we can't tolerate
    duplicates, and order doesn't matter.

-   **Mutable Sequence**: :class:`list`.
    While handy for the initial construction of the
    bin, this isn't really useful because the contents of a bin don't
    change once they have been enumerated.

-   **Mutable Mapping**: :class:`dict`.
    We don't need the key-to-value mapping feature at all.
    A map does more than we need for representing a :class:`Bin`.

-   **Mutable Set**: :class:`set`.
    Duplicates aren't allowed, membership tests are fast, and there's no inherent ordering.
    This looks close to what we need.

-   **Immutable Set**: :class:`frozenset`.
    Duplicates aren't allowed, membership tests are fast, and there's no inherent ordering.
    There's not changing it after it's been built.
    This seems to be precisely what we need.

Having looked at the fundamental collection varieties, we will elect to
use a :class:`frozenset`.

How will we use this collection?

Wrap vs. Extend a Collection
--------------------------------

There are two general ways to use a collection.

-   **Wrap**. Define a class which has an attribute that holds the collection.
    We're wrapping an existing data structure in a new class. The type
    hint suggests we can use any iterable collection of :class:`Outcome` instances
    as a source to create the :class:`frozenset` collection.

    Something like this::

        class Bin:
            def __init__(self, outcomes: Iterable[Outcome]) -> None:
                self.outcomes = frozenset(outcomes)

-   **Extend**. Define a class which **is** the collection.
    We're essentially renaming an existing data structure to provide
    a more descriptive name for the class.

    Something like this::

        class Bin(frozenset):
            pass

Both are widely-used design techniques.
The trade off between them isn't clear at first.

Considerations include the following:

-   When we **wrap**, we'll often need to write a lot of additional
    methods for representation, length, comparisons, inquiries, etc.

    In some cases, we will wrap a collection specifically so that
    these additional methods are **not** available. We want to completely
    conceal the underlying data structure.

-   When we **extend**, we get all of the base methods of the collection.
    We can add any unique features.

In this case, extending the existing data structure seems to make more sense
than wrapping a :class:`frozenset`.

Bin Questions and Answers
--------------------------

Why wasn't :class:`Bin` in the design overview?


    The definition of the Roulette game did mention the 38 bins of the
    wheel. However, when identifying the nouns, it didn't seem important.
    Then, as we started designing the :class:`Wheel` class, the
    description of the wheel as 38 bins came more fully into focus. Rework
    of the preliminary design is part of detailed design. This is the first
    of several instances of rework.


Why introduce an entire class for the bins of the wheel? Why can't the
wheel be an array of 38 individual arrays?


    There are two reasons for introducing :class:`Bin` as a separate
    class:

    -   A separate class can improve the fidelity of our object model of the problem.

    -   A new class will reduce the complexity of the :class:`Wheel` class.

    The definition
    of the game describes the wheel as having 38 bins, each bin causes a
    number of individual :class:`Outcome` instances to win. Without thinking too
    deeply, we opted to define the :class:`Bin` class to hold a
    collection of :class:`Outcome` instances. At the present time, we can't
    foresee a lot of processing that is the responsibility of a :class:`Bin`.
    But allocating a class permits us some flexibility in assigning
    responsibilities there in the future. We can, specifically, change to
    alternative implementations of the :class:`Bin` to try to optimize resource
    use.


    Additionally, looking forward, it is clear that the :class:`Wheel`
    class will use a random number generator and will pick a winning :class:`Bin`.
    In order to keep this crisp definition of responsibilities for the :class:`Wheel`
    class, it makes sense to delegate all of the remaining details to
    another class.


Isn't an entire class for bins a lot of overhead?


    The short answer is no, class definitions are almost no overhead at all.
    At run-time a class definition is a namespace for methods.
    It's the class instances that cause run-time overhead.



How can you introduce Set, List, Dict and other types when these don't appear in the problem?


    We have to make a distinction between the classes that are uncovered
    during analysis of the problem in general, and classes are that are
    part of the implementation of this particular solution. This emphasizes
    the distinction between :emphasis:`the problem` as described by users and
    :emphasis:`a solution` as designed by software developers.

    The built-in collections is part of a solution, and only hinted at by the
    definition of the problem.  The whole point of creating a solution
    is to introduce the right technology choices; the solution will always
    have classes and modules never mentioned in the problem domain.


Why extend (or rename) a built-in data structure? Why not simply use it?

    There are two reasons for extending a built-in data structure:

    -   We can easily add methods when extending.  In the case of a
        :class:`Bin`, there doesn't seem to be much we want to add.
        In the future, we many uncover attributes or behaviors that we
        need to include in our software.

    -   We can easily change the underlying data structure when extending.
        For example, we might have a different set-like collection
        that also inherits from the :class:`collections.abc.Set` base class. We can
        make this change in just one place -- our class extension --
        and the entire application benefits from the alternative set
        implementation.

What about hash and equality?

    We are't going to be comparing bins against each other.
    The default rules for equality and hash computation
    will work out just fine for this class.

Bin Design
-----------

..  class:: Bin(Collections.frozenset)

    :class:`Bin` contains a collection of :class:`Outcome` instances which
    reflect the winning bets that are paid for a particular bin on a
    Roulette wheel. In Roulette, each spin of the wheel has a number of
    :class:`Outcome` instances. Example: A spin of 1, selects the "1" bin with the following winning
    :class:`Outcome` instances: "1" , "Red" , "Odd" , "Low"
    , "Column 1" , "Dozen 1-12" , "Split 1-2" ,
    "Split 1-4" , "Street 1-2-3" , "Corner 1-2-4-5" ,
    "Five Bet" , "Line 1-2-3-4-5-6" , "00-0-1-2-3" ,
    "Dozen 1" , "Low" and "Column 1" . These are
    collected into a single :class:`Bin` .


Fields
~~~~~~

Since this is an extension to the existing :class:`frozenset`, we don't
need to define any additional fields.

Constructors
~~~~~~~~~~~~

We don't really need to write any more specialized constructor
method.

We'd use this as follows:

..  rubric:: Python Bin Construction

..  code-block:: python

        five = Outcome("00-0-1-2-3", 6)
        zero = Bin([Outcome("0",35), five])
        zerozero = Bin([Outcome("00",35), five])

#.  :obj:`zero` is based on
    references to two objects: the "0" :class:`Outcome` and the
    "00-0-1-2-3" :class:`Outcome`.

#.  :obj:`zerozero` is based on references to
    two objects: the "00" :class:`Outcome` and the "00-0-1-2-3"
    :class:`Outcome`.


Methods
~~~~~~~

We don't really **need** to write any more specialized methods.

How do we accumulate several outcomes in a single :class:`Bin`?

1.  Create a simple list, tuple, or set as an interim
    structure.

2.  Create the :class:`Bin` from this.

We might have something like this:

..  code-block:: python

    >>> bin1 = Bin({outcome1, outcome2, outcome3})

We created an interim set object and built the final :class:`Bin` from
that collection object.

Bin Deliverables
-----------------

There are two deliverables for this exercise. Both should have Python docstrings.

-   The :class:`Bin` class. This is part of the :file:`roulette.py` file,
    along with the :class:`Outcome` class.

-   A class which performs a unit test of the :class:`Bin` class.
    The unit test should create several instances of :class:`Outcome`,
    two instances of :class:`Bin` and establish that :class:`Bin` instances
    can be constructed from the :class:`Outcome` instances.

    Programmers who are new to OO techniques are sometimes
    confused when reusing individual :class:`Outcome` instances.
    This unit test is a good place to examine the ways in which object :emphasis:`references`
    are shared. A single :class:`Outcome` object can be referenced
    by several :class:`Bin` instances. We will make increasing use of this
    in later sections.

Looking Forward
---------------

In the next chapter, we'll design the :class:`Wheel` class to contain
all of the :class:`Bin` objects. A :class:`Wheel` object can select
a :class:`Bin` which has a number of :class:`Outcome` objects representing
winning bets.
