
..  _`roul.test`:

Review of Testability
=====================

This chapter presents some design rework and implementation rework for
testability purposes. While testability is very important, new
programmers can be slowed to a crawl by the mechanics of building test
drivers and test cases. We prefer to emphasize the basic design
considerations first, and address testability as a feature to be added
to a working class.

In `Test Scaffolding`_ we'll look at the basic software components
required to build unit tests.

One approach is to write tests first, then create software that passes
the tests. We'll look at this in `Test-Driven Design`_.

The application works with random numbers. This is awkward for
testing purposes. We'll show one approach to solving
this problem in `Capturing Pseudo-Random Data`_.

We'll touch on a few additional topics in `Testability Questions and Answers`_.

In `Testability Deliverables`_ we'll enumerate some deliverables that
will improve the overall quality of our application.

We'll look a little more deeply at random numbers in `Appendix: On Random Numbers`_.

Test Scaffolding
----------------------

Without pausing, we charged past an elephant standing in the saloon.
It's time to pause a moment a take a quick glance back at the pachyderm we ignored.

In the :ref:`roul.game` we encouraged creating a stub :class:`Player` class and
building a test that integrated the :class:`Game`, :class:`Table`, :class:`Wheel`,
and the stub :class:`Player` class into a kind of working application.
This is an integration test, not a proper unit test.
We've integrated our various classes into a working whole.

While this integration test reflects our overall goals, it's not always the best
way to assure that the individual classes work in isolation. We need to
refine our approach somewhat.

Back in :ref:`roul.wheel` we touched on the problem of testing an application
that includes a random number generator (RNG).
There are two questions raised:

#.  How can we develop formalized unit tests when we can't predict the
    random outcomes? This is a serious testability issue in randomized
    simulations. This question also arises when considering interactive
    applications, particularly for performance tests of web applications
    where requests are received at random intervals.

#.  Are the numbers really random? This is a more subtle issue, and is
    only relevant for more serious applications. Cryptographic
    applications may care more deeply about the randomness
    of random numbers. This is a large subject, and well beyond the
    scope of this book. We'll just assume that our random number
    generator is good enough for statistical work. It must be consistently
    difficult to predict, but also as fair as the real world.

To address the testing issue, we need to develop some scaffolding that
permits more controlled testing. We want to isolate each class so
that our testing reveals problems in the class under test.

There are two approaches to replacing the random behavior with something more controlled.

-   One approach is to create a mocked implementation of
    :class:`random.Random` that returns specific outcomes
    that are appropriate for a given test.

-   A second approach is to record the sequence
    of random numbers actually generated from a particular seed value and
    use this to define the expected test results. We suggested forcing
    the seed to be 42 with :samp:`wheel.rng.seed(42)`.



Test-Driven Design
-------------------

Good testability is achieved when classes are tested in isolation
and there are no changes to the class being tested.
We have to be careful that our design for the :class:`Wheel` class
works with a real random number generator as well as a mocked
version of a random number generator.

To facilitate this, we suggested making the
random number generator in the :class:`Wheel` class visible. Rather than
have a :class:`Wheel` instance use the :mod:`random` module directly, we
suggesting creating an instance of the :class:`random.Random` class as an
attribute of each :class:`Wheel` instance.

This design choice reveals a tension between the encapsulation principle and the testability principle.

By *Encapsulation* we mean the design strategy where we define a class to
encapsulate the details of it's implementation.  It's unclear if the
random number generator is an implementation detail or an explicit part
of the :class:`Wheel` class implementation.

By *Testability* we mean a design strategy where we can easily isolate
each class for unit testing. This is sometimes achieved by using complex
dependency injection. For testing, mock classes are injected; for
real use, the real classes are injected. The dependency injection
machinery in other languages is designed around the requirements of the compiler.
Python doesn't really need complex injection tools.

Generally, for must of the normal use cases, the random
number generator inside a :class:`Wheel` object is an invisible implementation detail.
However, for testing purposes, the random number generator needs to be a configurable feature
of the :class:`Wheel` instance.

One approach to making something more visible is to provide
default values in the constructor for the object. The following example
provides an :obj:`rng` parameter to permit inserting a mocked random
number generator.

..  rubric:: Wheel with Complex Initialization

..  include:: ../../code/wheel_examples.py
    :code: python
    :start-line: 10
    :end-line: 17

For this particular situation, this technique is noisy.
It introduces a feature that we'll never use outside writing tests.
The choice of a random number generator is made infrequently;
often the choice is made only once when a generator with desired
statistical properties is identified.

Because Python type checking happens at run time, it's
easier to patch a class as part of the unit test.

Here's a simpler :class:`Wheel` class definition with simpler
initialization.

..  rubric:: Wheel with Simpler Initialization

..  include:: ../../code/wheel_examples.py
    :code: python
    :start-line: 19
    :end-line: 27


Since we can inject anything as the random number generator in a :class:`Wheel` instance,
our unit tests can look like this:

..  rubric:: Mock Object Testing

..  include:: ../../code/test_wheel.py
    :code: python
    :start-line: 23
    :end-line: 35

This function creates a mocked instance of the :class:`random.Random` class.
The mock defines a :meth:`choice` method; this method always returns
the same value.

The test case builds a number of mocked :class:`Bin` instances. In this
case, we don't even use the :class:`Bin` class definition, we can use
a simple string object.

The :class:`Wheel` instance is built from the mocked bins. The :obj:`rng`
attribute is then patched to use the mocked random number generator.
After the patch is applied, we can exercise the :meth:`Wheel.choose` method
to confirm that it properly uses the random number generator's :meth:`choice`
method.

..  _`roul.test.random`:

Capturing Pseudo-Random Data
----------------------------

The other approach -- using a fixed seed -- means that we need to
build and execute a program that reveals the fixed
sequence of spins that are created by the non-random number generator.

We can create an instance of :class:`Wheel` class. We can set the
random number generator seed to a known, boring value, like :literal:`42`.

When can call the :meth:`Wheel.choose` method six
times, and print the winning :class:`Bin` instances. This
sequence will always be the result for a seed value of :literal:`42`.

This discovery procedure will reveal results needed to
create unit tests for :class:`Wheel` class and anything that uses
it, for example, :class:`Game`.

..  rubric:: Repeatable Random Sequences

..  include:: ../../code/seed_demo.py
    :code: python

..  _`roul.test.qanda`:

Testability Questions and Answers
------------------------------------

Why are we making the random number generator more visible? Isn't object
design about encapsulation?

    Encapsulation isn't exactly the same thing as "information hiding". For
    some people, the information hiding concept can be a useful way to begin
    to learn about encapsulation. However, information hiding is often taken to extremes.

    In this case, we want to
    encapsulate the bins of the wheel and the procedure for selecting the
    winning bin into a single object. However, the exact random-number
    generator (RNG) is a separate component, allowing us to bind
    any suitable RNG.

    Consider the situation where we are generating random numbers for a
    cryptographic application. In this case, the built-in random number
    generator may not be random enough. In this case, we may have a
    third-party Super-Random-Generator that should replace the built-in
    generator. We would prefer to minimize the changes required to introduce
    this new class.

    Our initial design has isolated the changes to the :class:`Wheel` class,
    but required us to change the constructor. Since we are changing the
    source code for a class, we must to unit test that change. Further, we
    are also obligated unit test all of the classes that depend on this
    class. Changing the source for a class deep within the application
    forces us to endure the consequence of retesting every class that
    depends on this deeply buried class. This is too much work to simply
    replace one object with another.

    We do, however, have an alternative. We can change the top-level :func:`main`
    method, altering the concrete object instances that compose the working
    application. By making the change at the top of the application, we
    don't need to change a deeply buried class and unit test all the classes
    that depend on the changed class. Instead, we are simply choosing among
    objects with the same superclass or interface.

    This is why we feel that constructors should be made very visible using
    the various design patterns for :emphasis:`Factories` and :emphasis:`Builders`.
    Further, we look at the main method as a kind of master :emphasis:`Builder`
    that assembles the objects that comprise the current execution of our application.

    See our :ref:`roul.ov.qanda.main` FAQ for more on this subject.

    Looking ahead, we will have additional notes on this topic as we add the :ref:`roul.sevenreds`
    subclass of :class:`Player` class.

If setting the seed works so well, why use a mock object?

    While setting the seed is an excellent method for setting up a test,
    it's not actually a unit test. The :class:`Wheel` is not used in isolation
    from other classes.

Why use 42 for a seed?

    It's mentioned in Douglas Adams' *The Hitchhiker's Guide to the Galaxy*.
    There are several boring numbers that are good choices
    because the numbers are otherwise mathematically uninteresting.

Testability Deliverables
-------------------------

There are two deliverables for this exercise. All of these deliverables
need Python docstrings.

-   Revised unit tests for :class:`Wheel` using a
    proper Mock for the random number generator.

-   Revised unit tests for :class:`Game` using a proper Mock for the :class:`Wheel`.


Appendix: On Random Numbers
----------------------------

Random numbers aren't actually "random." Since they are
generated by an algorithm, they are properly called pseudo-random.
The distinction is important. Pseudo-random numbers are
generated in a fixed sequence from a given seed value.
Computing the next value in the sequence involves a
calculation that is expected to overflow the available number of
bits of precision leaving apparently random bits as the next
value. This leads to results which, while predictable, are
arbitrary enough that they pass rigorous statistical tests and
are indistinguishable from data created by random processes.

We can make an application more predictable by selecting a specific
seed value. This provides reproducible results.

We can make an application less predictable by choosing a very
hard to predict seed value.
In most operating systems a special "device" is
available for producing random values. In Linux this is typically
:file:`/dev/random`. In Python, we can access this through
the :func:`os.urandom` function as well as the :mod:`secrets` module.

When we need to make an application's output repeatable,
we set a known seed value. For testing purposes, we can note the sequence of numbers
generated and use this to assure a repeatable test.

We can also write a short demonstration program to see the
effect of setting a fixed seed. This will also give us a set of
predictable answers for unit testing.

Looking Forward
---------------

We've built a simple, prototype :class:`Player` class definition.
This player only places a limited number of bets. The house edge
in Roulette assures us that the play will, before long, run
out of money.

A bet on black pays winnings as if the probability of winning were :math:`\tfrac{1}{2}`.
The actual probability is :math:`\tfrac{18}{38}`. The difference,
:math:`\tfrac{1}{38} = \tfrac{1}{2}-\tfrac{18}{38}`, tells us
that the expected number of spins is 38 before the player is out of
money.

There's little that can be done in the real world. We can, however,
simulate the variety of creative ways people apply fallacious reasoning
to try and prevent this inevitable loss. We'll start with a general :class:`Player`
class and then implement a number of stateful algorithms
for betting.
