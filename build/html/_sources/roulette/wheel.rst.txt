
..  _roul.wheel:

Wheel Class
===========

This chapter builds on the previous two chapters, creating a more
complete composite object from the :class:`Outcome` and :class:`Bin`
classes we have already defined. In `Wheel Analysis`_ we'll look
at the responsibilities of a wheel and it's collaboration.

In the `Wheel Design`_ we'll provide the detailed design
information. In the `Test Setup`_ we'll address some considerations
for testing a class which has random behavior.
In `Wheel Deliverables`_ we'll enumerate what must
be built.

Wheel Analysis
---------------

The wheel has two responsibilities:

-   it is a container for the :class:`Bin` instances, and
-   it picks one :class:`Bin` at random.

Separately, we'll look at ways to initialize the various :class:`Bin` instances that comprise a
standard Roulette wheel.

In `The Container Responsibility`_ we'll look at the container aspect in detail.

In `The Random Bin Selection Responsibility`_ we'll look at the random selection aspects.

Based on this, the `Constructing a Wheel`_ section provides a description of
how we can build the Wheel instance.

The Container Responsibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since a :class:`Wheel` object contains 38 :class:`Bin` instances,
it is a collection. We can review our survey of available collections in
:ref:`roul.bin.collections` for some guidance on how to choose the
best collection.

In this case, the choice of the winning :class:`Bin`
will be selected by a random numeric index.  We need some kind of sequential
collection.

This makes an immutable :class:`tuple` very appealing.
This is a subclass of :class:`collections.abc.Sequence` and has
the features we're looking for.

Once we've decided to use a sequential collection, we have a second decision.
We need to choose an indexing scheme for the various :class:`Bin` instances.
In the case of Roulette, we have a problem with zero and double-zero:
there's no 00 integer.

The index values of 1
to 36 are logical mappings to :class:`Bin` instances based on the straight bet.
The roulette wheel's bins have the 36 numbers prominently displayed.
The :class:`Bin` at index 1 would contain :samp:`Outcome("1", 35)` among several others.
The :class:`Bin` at index 2 would contain :samp:`Outcome("2", 35)`.

We have a small problem, however, with 0 and 00: we need two separate indexes.
While 0 is a valid index, what do we do with 00?

The trick here is to step away from being too literal in our mappings
from numbers to bins. There's no real reason why the bin with
:samp:`Outcome("1", 35)` should be at index position 1 in the :class:`Wheel` collection.

Because the index of the :class:`Bin` doesn't have any significance at
all, we can assign the :class:`Bin` that has the :samp:`Outcome("00", 35)`
to position 37 in the :class:`Wheel` collection.
The index value doesn't actually matter because we'll never
use the index for any purpose other than random selection.

The Random Bin Selection Responsibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order for the :class:`Wheel` class to select a :class:`Bin` instance
at random, we'll need a random number from 0 to 37 that we can use an an
index. There is an alternative, however.

The :class:`random` module offers a :meth:`Random.choice` function
which picks a random value from a
sequence. This is ideal for returning a randomly selected :class:`Bin`
from our list of :class:`Bin` instances. The numeric value doesn't
matter if we use the :meth:`choice` method.

**Testability**.
Note that testing a class using random numbers isn't going to be easy.
To do testing properly, need a non-random
random number generator with predictable results.

To create a non-random random-number generator, we can do
something like the following.

1.  Set a specific seed value. This will generate
    a known sequence of values.

2.  Create a mock class for the random number generator that returns
    a known, fixed sequence of values. We can leverage the :mod:`unittest.mock`
    module for this.

We'll address this in detail in :ref:`roul.test`. For now, we'll suggest
using the first technique -- set a specific seed value.

Constructing a Wheel
~~~~~~~~~~~~~~~~~~~~~

Each instance of the :class:`Bin` class has a list of :class:`Outcome` instances.
The zero ("0") and double zero ("00") :class:`Bin` instances only have two :class:`Outcome` instances.
The other numbers have anywhere from twelve to fourteen :class:`Outcome` instances.

Clearly, there's quite a bit of complexity in building some of the bins.

Rather than dwell on these algorithms, we'll apply a common OO principle of
deferred binding. We'll build a very basic wheel first
and work on the bin-building algorithms in the next chapter.

It's often simplest to build a class incrementally. This is an example where
a simpler overall structure includes rather complex details.

Wheel Design
------------

..  class:: Wheel

    :class:`Wheel` contains the 38 individual bins on a Roulette wheel,
    plus a random number generator. It can select a :class:`Bin` at
    random, simulating a spin of the Roulette wheel.

Fields
~~~~~~


..  attribute:: Wheel.bins

    Contains the individual :class:`Bin` instances.

    This is a :class:`tuple` of 38 elements.  This can be built
    with :samp:`tuple(Bin() for i in range(38))`

..  attribute:: Wheel.rng

    A random number generator to select a :class:`Bin`
    from the :obj:`bins` collection.

    For testing, we'll often want to seed this generator.
    For simulation processing, we can set the seed value using :func:`os.urandom`.

Constructors
~~~~~~~~~~~~


..  method:: Wheel.__init__(self) -> None
    :noindex:

    Creates a new wheel with 38 empty :class:`Bin` instances. It will also
    create a new random number generator instance.

    At the present time, this does not do the full initialization of the :class:`Bin` instances.
    We'll rework this in a future exercise.


Methods
~~~~~~~


..  method:: Wheel.addOutcome(number: int, outcome: Outcome) -> None
    :noindex:

    Adds the given :class:`Outcome` object to the
    :class:`Bin` instance with the given number.

    :param bin: bin number, in the range zero to 37 inclusive.
    :type bin: int

    :param outcome: The Outcome to add to this Bin
    :type outcome: Outcome

..  method:: Wheel.choose() -> Bin

    Generates a random number between 0
    and 37, and returns the randomly selected :class:`Bin` instance.

    The :meth:`Random.choice` function of the :class:`random`
    module will select one of the available :class:`Bin` instances from the :obj:`bins`
    collection.

    :returns: A Bin selected at random from the wheel.
    :rtype: Bin

..  method:: Wheel.get(bin: int) -> Bin

    Returns the given :class:`Bin` instance from the
    internal collection.

    :param bin: bin number, in the range zero to 37 inclusive.
    :type bin: int

    :returns: The requested Bin.
    :rtype: Bin

Test Setup
-----------------

We need a controlled kind of random number generation for testing
purposes. This is done with tests that look like the following:

..  rubric:: Test Outline

..  code-block:: python

    def test_wheel_sequence():
        wheel = Wheel()
        wheel.addOutcome(8, Outcome("test", 1))
        wheel.rng.seed(1)
        assert Outcome("test", 1) in wheel.choose()

The values delivered from this seeded random number generator
can be seen from this experiment.

..  rubric:: Fixed pseudo-random sequence

..  code-block:: python

    >>> x = random.Random()
    >>> x.seed(1)
    >>> [x.randint(0,37) for i in range(10)]
    [8, 36, 4, 16, 7, 31, 28, 30, 24, 13]

This allows us to predict the output from the :meth:`Wheel.next` method.
Because the first value is 8, we only need to put an outcome into
:class:`Bin` instance at position 8 in the :class:`Wheel` collection.

The special `` Outcome("test", 1)`` object should be found
in the expected :class:`Bin` instance.

Wheel Deliverables
------------------

There are three deliverables for this exercise. The new class and the
unit test will have Python docstrings.

-   The :class:`Wheel` class. This is part of the :file:`roulette.py` file,
    along with the :class:`Outcome` and :class:`Bin` classes.

-   A class which performs a unit test of building the :class:`Wheel`
    class. The unit test should create several instances of the :class:`Outcome` class,
    two instances of the :class:`Bin` class, and an instance of the :class:`Wheel` class.
    The unit test should establish that :class:`Bin` instances can be
    added to the :class:`Wheel`.

-   A class which tests the Wheel class by selecting "random" values
    from a :class:`Wheel` object using a fixed seed value.

Looking Forward
---------------

Given the overall structure of the :class:`Wheel` object, the next
chapter will show how to build the collection of individual :class:`Outcome`
instances in each :class:`Bin` instance.
