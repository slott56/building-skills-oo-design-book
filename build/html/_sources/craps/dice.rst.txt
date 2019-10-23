
..  _`craps.dice`:

Dice Class
==========

Unlike Roulette, where a single :class:`Bin` instance could be identified by
the number in the bin, each :class:`Throw` object is a pair of numbers.

The idea is to have the :class:`Dice` class parallel to the Roulette :class:`Wheel` class.
A :class:`Dice` instance is a collection of :class:`Throw` instances. The :class:`Dice` instance
is responsible to picking a :class:`Throw` object at random. We'll look at this in detail in
`Dice Analysis`_.

We'll reconsider some features of :class:`Throw`  class in `Throw Rework`_.

Once we've settled on the features, we'll look at the details
in `Dice Design`_. We'll enumerate the deliverables in `Dice Deliverables`_.

We'll look at the subject of performance improvements in `Dice Optimization`_.

Dice Analysis
-------------

The dice have two responsibilities: they are a container for the :class:`Throw` instances
and they pick one of the :class:`Throw` instances at random.


We find that we have a potential naming problem: both the :class:`Wheel`
and the :class:`Dice` classes are somehow instances of a common abstraction.
Looking forward, we may wind up wrestling with a deck of cards trying to
invent a common nomenclature for the classes. They create random events,
and this leads us to a possible superclass: a :class:`Randomizer` class.
Rather than over-engineer this, we'll hold off on adding this design
element until we find something else that is common among them.


**Container**. Since a :class:`Dice` object has 36 possible :class:`Throw` instances,
it is a collection. We can review our survey of the collections in :ref:`roul.bin.collections`
for some guidance here. In this case, we note that the choice of :class:`Throw` instance
can be selected by a random numeric index.


For Python  programmers, this makes the a :class:`tuple` very appealing.
The collection of outcomes is fixed, and an immutable structure makes
the most sense.


After selection a collection type, we must then deciding how to index each
:class:`Throw` object in the :class:`Dice` collection.  Recall that in Roulette, we had 38
numbers: 1 to 36, plus 0 and 00. By using 37 for the index of the
:class:`Bin` instance that contained 00, we had a simple integer index for each :class:`Bin` instance.

For Craps it seems better to use a two-part index with the values of two independent
dice.

**Index Choices**.
In this case, we have two choices for computing the index into the collection,

-   We can rethink our use of a simple sequential structure.
    If we use a :class:`dict`, we can use an object representing
    the pair of numbers as an index instead of a single int value.

-   We can compute a unique index position from the two dice values.

**Decision Forces**.
There are a number of considerations to choosing between these two representations.

#.  If we create an object with each unique pair of integers, we
    can then use that object to be the index for a :class:`dict`. The
    type hint is ``Dict[Tuple[int, int], Throw]`` which seems
    to describe things succinctly.

#.  We can transform the two numeric dice values to a single index value
    for the sequence. This is a technique called
    :emphasis:`Key Address Transformation`; we transform the keys into
    the address (or index) of the data.

    We create the index, :math:`i`, from two dice, :math:`d_1`, :math:`d_2`,
    via a simple linear equation:  :math:`i = 6(d_1-1) + (d_2-1)`.

    We can reverse this calculation to determine the two dice values from an index.
    :math:`d_1 = \lfloor i \div 6 \rfloor + 1; d_2 = (i \bmod 6) + 1`.
    Python offers a :func:`divmod` function which does precisely this
    calculation.


    This doesn't obviously scale to larger collections of dice very well.
    While Craps is a two-dice game, we can imagine simulating
    a game with larger number of dice, making this technique complex.


Because of encapsulation, the choice of algorithm is completely hidden
within the implementation of :class:`Dice` class.


**Solution**.
Our recommendation is to encapsulate the
pair of dice in a :class:`tuple` instance.  We can use
this object as index into a :class:`dict` collection to associate a :class:`tuple`
of two integers with a :class:`Throw` object.

More advanced students
can create a class hierarchy for :class:`Dice` to include
both implementations as alternative subclasses.

**Random Selection**. The random number generator in :class:`random.Random`
helps us locate a :class:`Throw` instance at random.

First, we can get the :class:`list` of keys from the :class:`dict`
that associates  a :class:`tuple` of dice numbers with a :class:`Throw` instance.

Second, we use :meth:`Random.choice` to pick one of these  :class:`tuple` instances.

We use this randomly selected  :class:`tuple` object to return the selected
:class:`Throw` object.


Throw Rework
-------------

We need to update :class:`Throw` instance to return an appropriate key object.

There are two general strategies available for this kind of computation:

-   **Eager**. This means we calculate the key as soon as we know
    the two dice values. They key can be an attribute which is
    fetched like any other.
    This is computed in the :class:`Throw` class constructor method.
    This will allow all parts of the application to share references to a single instance
    of the key.

-   **Lazy**. This means we don't calculate the key until its required.
    We often use the :code:`@property` decorator for methods which
    embody a lazy calculation that we want to appear as if it was an
    attribute.
    For this, We add a method to :class:`Throw` to return the :class:`tuple`
    that is a key for this :class:`Throw`.

    ..  method:: Throw.key(self) -> Tuple[int, int]


It's very difficult to make an **eager vs. lazy** decision
until the entire application has been built and we know **all** the places
where an object is used.

Dice Design
-----------

..  class:: Dice

    A :class:`Dice` instance contains the 36 individual throws of two dice, plus a
    random number generator. It can select a :class:`Throw` object at random,
    simulating a throw of dice.


Fields
~~~~~~~


..  attribute:: Dice.throws

    This is a :class:`dict` that maps a two-tuple to a :class:`Throw` instance.
    The type hint is ``Dict[Tuple[int, int], Throw]``.

..  attribute:: Dice.rng

    An instance of :class:`random.Random`

    Generates the next random number, used to select a :class:`Throw` instance
    from the :obj:`throws` collection.

Constructors
~~~~~~~~~~~~~


..  method:: Dice.__init__(self) -> None

    Build the dictionary of :class:`Throw` instances.


At the present time, this does not do the full initialization of all of the :class:`Throw` instances.
We're only building the features of :class:`Dice` related to random selection.
We'll extend this class in a future exercise to build all of the :class:`Throw` objects.


Methods
~~~~~~~~


..  method:: addThrow(self, throw: Throw) -> None

    :param throw: The :class:`Throw` to add.
    :type throw: :class:`Throw`


    Adds the given :class:`Throw` to the mapping maintained by this instance
    of :class:`Dice`.  The key for this :class:`Throw` is available from the
    :meth:`Throw.getKey` method.




..  method:: roll(self) -> Throw

    Returns the randomly selected :class:`Throw` instance.

    First, get the :class:`list` of keys from the :obj:`throws`.

    The :meth:`random.Random.choice` method will select one of the available
    keys from the the list.

    This is used to get the corresponding :class:`Throw` from the :obj:`throws`
    :class:`Map`.




..  method:: Dice.getThrow(self, d1: int, d2: int) -> Throw

    :param d1: The value of one die
    :param d2: The other die


    This method takes a particular combination of
    dice, locates (or creates) a :class:`NumberPair`, and returns the appropriate :class:`Throw`.

    This is not needed by the application. However, unit tests will need a method
    to return a specific :class:`Throw` rather than a randomly selected
    :class:`Throw`.


Dice Deliverables
------------------

There are three deliverables for this exercise. In considering the unit
test requirements, we note that we will have to follow the design of the :class:`Wheel`
class for convenient testability: we will need a way to get a particular :class:`Throw` instance
from the :class:`Dice` collection, as well as replacing the random number
generator with one that produces a known sequence of numbers.

-   The :class:`Dice` class.

-   A class which performs a unit test of building the :class:`Dice`
    class. The unit test should create several instances of the :class:`Outcome` class,
    two instances of a :class:`Throw` subclass, and an instance of the :class:`Dice` class.
    The unit test should establish that :class:`Throw` instances can be
    added to the :class:`Dice` object.

-   A class which performs a demonstration of selecting non-random
    values from the :class:`Dice` class. By setting a particular
    seed, the :class:`Throw` instances will be returned in a fixed order. To
    discover this non-random order, a demonstration should be built
    which includes the following.

    #.  Create several instances of the :class:`Outcome` class.

    #.  Create two instances of a :class:`Throw` subclass using the available
        :class:`Outcome` instances.

    #.  Create one instance of the :class:`Dice` class using the two :class:`Throw` instances.

    #.  A number of calls to the :meth:`Dice.roll` method should return
        randomly selected :class:`Throw` instances.

    Note that the sequence of random numbers is fixed by the seed value.
    The default constructor for a random number generator creates a seed
    based on the system clock. If your unit test sets a particular seed
    value, you will get a fixed sequence of numbers that can be used to
    get a consistent result.

Dice Optimization
------------------

First, we note that premature optimization is a common trap.

    "We should forget about small efficiencies, say about 97% of the time:
    premature optimization is the root of all evil. Yet we should not pass up
    our opportunities in that critical 3%.  A good programmer will not be lulled
    into complacency by such reasoning, he will be wise to look carefully at the
    critical code; but only after that code has been identified"

    -- Donald Knuth

    "Structured Programming with Goto Statements". Computing Surveys 6:4 (1974), 261-301.

The eager vs. lazy calculation of the key associated with a pair of dice
is something that seems like it should have one "best" way. It seems like
we should be able to chose between eager and lazy calculation of key values.

This decision is actually quite difficult to make.

Eager calculation seems optimal: get it done once and reuse the answer
many times. However, in some cases, the calculation is rather expensive
and isn't always needed. In this case, the key involves the creation of
a new object, and this can be a costly operation.

We've made an effort to optimize this by thinking of the collection
of :class:`Throw` instances as a fixed pool of objects, allocated once, and then never
created again. It appears that they key associated with a :class:`Throw` object is only computed
once.

For this example, the **Eager v. Lazy** decision seems to be moot.

In other cases, it's a significant optimization.

In all cases, we need to use a profiler to see if this particular piece of the
application is slowest. We should only optimize the parts which are demonstrably
slowest. Optimizing parts which aren't slow (or aren't even correct) is simply
a waste of time.

We should articulate alternative designs. We should leave a note in the
docstrings about alternative implementations. We should not, however, pursue
each alternative until we know that it adds significant value to explore
the alternatives carefully.

Looking Forward
---------------

Now that we have the :class:`Dice` as a container of :class:`Throw` instances,
we can build the pool of 36 individual :class:`Throw` objects.  This throw-builder
will parallel the Roulette :class:`BinBuilder`.

In the next chapter, we'll look closely at a class to build the individual :class:`Throw` objects.
