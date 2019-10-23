..  _`start.testing`:

Python Unit Testing
####################

Unit tests are absolutely essential. It's very difficult
to consider any feature as complete without automated unit tests.

We have several ways to tackle unit tests for our application,
shown below:

-   We can create :class:`unittest.TestCase` class definitions.

-   We can include examples in the docstrings. These are called
    doctest examples.

-   We can write test functions. These tend to be simpler
    than the :class:`unittest.TestCase` classes.

We have three sets of tools available, shown below:

-   The :mod:`unittest` tool can *only* process :class:`unittest.TestCase` class
    tests.

-   The :mod:`doctest` tool can *only* process doctest examples in docstrings.

-   The :mod:`pytest` tool can comfortably find and process all three kinds of of unit tests.

We suggest always using :mod:`pytest` because it's slightly easier and more comprehensive
in what it can do. We'll describe both kinds of tests. Some developers
find it slightly easier to write test functions.

In `Using Unit Tests`_ we'll look at an overall development process
that leverages unit tests as a way to write testable specifications.

We'll show a small class which to be tested in `Example Class Definition`_.
We'll look at a :class:`unittest.TestCase`
example in `Example TestCase classes`_.
We'll also look at pytest functions in `Example Test Function`_.

In `Python doctest Testing`_ we'll look at how we can execute the test cases
in the document strings of a module, class, function, or method.

In `Building Doctest Examples`_ we'll show how we can take
interactive Python output and transform it into a doctest example.
This will involve copy and paste. It's not too challenging.

In the next section we'll overview how to structure our work
around failing and passing test cases.

Using Unit Tests
================

One approach to unit testing is to build the tests first, then write a
class which at least doesn't crash, but may not pass all the tests. Once
we have this in place, we can now debug the tests until everything looks
right. This is called test-driven development. This is called "Test-Driven
Development" (TDD) because testing drives everything.

This can be difficult in practice. In many cases, we want to work
back and forth between our target code and the unit tests for that
code. When we're learning a language or a design pattern, it can be
difficult to write the tests first.

Generally, the process for creating a class with the unit tests has the following outline.

1.  Write a skeleton for the class that will be the unit under test.
    Initially, the class doesn't really need to do anything. It only
    has to exist so the tests can run.

2.  Write the test case.  This will create instances of the class under test,
    exercise those instances, and make assertions about the state of those instances.
    The test class may create mocks for the various collaborators of the
    target class.

3.  Run the test, knowing that the first few attempts will fail.

4.  While at least one test is failing.

    a.  Fix the broken things.

    b.  Run the test suite.

5.  At this point, the  class under test passes the suite of tests.  However, it may still
    fail to meet other quality criteria.  For example, it may have a convoluted
    structure, or it may be inefficient, or it may lack appropriate documentation.
    In any case, we're not really done with development.

6.  While our target class fails to meet our quality standards.

    a.  Refactor to correct the quality problems in our target class.

    b.  Run the test suite.  If we have refactored properly, the tests still
        pass.  If we have introduced a problem, tests will fail.

The failing tests help us develop new code. Once the tests pass,
we can refactor and fine-tune the application knowing that a change
didn't break anything that used to work.

In the next section we'll look at an example test using the
:class:`unittest.TestCase` definitions.

Example Class Definition
------------------------

As an example, we'll rework  the :file:`hw.py`
module in the :file:`src` directory. The revision
will make a more complete application.

::

    """
    A hello world to be sure all our tools work.
    """

    from dataclasses import dataclass

    @dataclass
    class Greeting:
        greeting: str
        audience: str

        def __str__(self) -> str:
            return f"{self.greeting} {self.audience}"

    def main() -> None:
        g = Greeting("hello", "world")
        print(g)

    if __name__ == "__main__":
        main()

We've defined a class and a function.
We've also put the top-most code into an ``__name__ == "__main__"`` block.
This block will only be executed when we run the module
directly. If the module is imported, it won't do anything
automatically, making it much easier to test.

Example TestCase classes
------------------------

This goes into a file called :file:`tests/test_hw_1.py`.  The
``_1`` suffix is a hint that we'll write a second set of test
cases below, and we'll use a different suffix.

The test module will have two test cases:

-   The :class:`TestGreeting` class will tet the :class:`Greeting` class. This is
    is relatively clear because there are no dependencies in the
    :class:`Greeting` class.

-   The :class:`TestMain` class will test the :func:`main` function. This
    is more complex because the function depends on :class:`Greeting.
    A unit test should isolated from dependencies, which means
    a patch and a mock object must be used. Further, the :func:`main`
    function writes to stdout via the :func:`print` function.

We'll decompose the example into three separate sections.
First, the imports look like this:

::

    from io import StringIO
    from unittest import TestCase
    from unittest.mock import Mock, patch
    import hw

The test for the :class:`Greeting` class creates an instance of
the class, and then confirms the value of the :func:`str` function
uses the :meth:`Greeting.__str__` method.

::

    class TestGreeting(TestCase):
        def test(self):
            g = hw.Greeting("x", "y")
            self.assertEqual(str(g), "x y")

The test for the :func:`main` function is a bit more complex. The
:meth:`TestMain.setUp` method creates a mock for the :class:`Greeting`
class. The top-level :class:`Mock` instance behaves like a class
definition. When it is called as a function it returns an mock
object that behaves as an instance of the class; it's named ``"Greeting instance"``
to clarify the role it plays.

The instance mock provides an easy-to-spot response to the :meth:`__str__` method.
This will make it easier to confirm that the :func:`str` was used appropriately.


::

    class TestMain(TestCase):
        def setUp(self):
            self.mock_greeting = Mock(
                name="Greeting", return_value=Mock(
                    name="Greeting instance",
                    __str__=Mock(return_value="mock str output")
                )
            )
            self.mock_stdout = StringIO()

        def test(self):
            with patch('hw.Greeting', new=self.mock_greeting):
                with patch('sys.stdout', new=self.mock_stdout):
                    hw.main()
            self.mock_greeting.assert_called_with('hello', 'world')
            self.mock_greeting.return_value.__str__.assert_called_with()
            self.assertEqual("mock str output\n", self.mock_stdout.getvalue())

The :func:`patch` function is used to make two changes inside the :mod:`hw` module.

-   The :class:`hw.Greeting` class is replaced with the ``self.mock_greeting`` object.
    This means the :func:`main` function will interact with the mock object,
    allowing the test to confirm the :func:`main` function made valid requests.

-   The ``sys.stdout`` object is replaced with an instance of :class:`io.StringIO`.
    This object will collect output destined to standard output so it can be
    examined in the test.

The :meth:`test` method confirms the mock objects were all used properly
by the :func:`main` function:

1.  The mocked :class:`Greeting` class was called with the expected arguments.

2.  The mocked :class:`Greeting` instance had the :meth:`Greeting.__str__` method
    called with no arguments.

3.  The output sent to stdout was the output from the :meth:`Greeting.__str__` method.

This test exercises a service, the :class:`Greeting` class, and a client of that
service, the  :func:`main` function. Because the function has a direct dependence
on the service class, we're forced to use :func:`patch` to inject a different dependency
for testing.

Example Test Function
---------------------

This goes into a file called :file:`tests/test_hw_2.py`.  The
``_2`` suffix separates these tests from the tests defined above
using :class:`unittest.TestCase`.

The test module will have two test cases:

-   The :func:`test_greeting` function will tet the :class:`Greeting` class.

-   The :class:`test_main` function will test the :func:`main` function. This
    is more complex because the function depends on :class:`Greeting.
    A unit test should isolated from dependencies, which means
    mock objects must be used. Further, the :func:`main`
    function writes to stdout via the :func:`print` function,
    and this output needs to be captured.

We'll decompose the example into three separate sections.
First, the import look like this:

::

    from io import StringIO
    from unittest.mock import Mock
    import pytest
    import hw

The test for the :class:`Greeting` class looks like this:

::

    def test_greeting():
        g = hw.Greeting("x", "y")
        assert str(g) == "x y"

As with the :class:`unittest.TestCase` example, the test is a exercises
the class to confirm the expected behavior.
Unlike the :class:`unittest.TestCase` class, we use the built-in ``assert``
statement when working with the :mod:`pytest` tool.

The mock object created for use with the  :mod:`pytest` tool is a
complete repeat of the example :class:`Mock` object shown above.
The :mod:`unittest.mock` module is used both by the :mod:`pytest` tool
as well as the :mod:`unittest` tool.

The ``@pytest.fixture`` decoration is used to identify functions
that create test fixtures. In this case, the fixture is a :class:`Mock`
object that can be shared by multiple tests.

::

    @pytest.fixture
    def mock_greeting(monkeypatch):
        greeting = Mock(
            name="Greeting", return_value=Mock(
                name="Greeting instance",
                __str__=Mock(return_value="mock str output")
            )
        )
        monkeypatch.setattr(hw, 'Greeting', greeting)
        return greeting

    def test_main(mock_greeting, capsys):
        hw.main()

        mock_greeting.assert_called_with('hello', 'world')
        mock_greeting.return_value.__str__.assert_called_with()

        out, err = capsys.readouterr()
        assert out == "mock str output\n"

The test for the :func:`main` function is similar in many respects
to the :class:`unittest.TestCase` version. The test asserts that
the mock was used correctly, and it examines the captured standard output.

The ``mock_greeting`` and ``capsys`` parameters are supplied automatically
by the :mod:`pytest` tool when the test is run. The ``mock_greeting`` value will
be the results of the :func:`mock_greeting` fixture. The ``capsys`` value
will be a built-in fixture that captures the ``sys.stdout`` and ``sys.stderr``
output for the test.

Running Pytest
--------------

We can run the tests with the following command.

..  code-block:: sh

    PYTHONPATH=src python -m pytest tests

The :mod:`pytest` tool will find *all* of the files with names starting with ``test_``.
Any :class:`unittest.TestCase` classes will be processed.
Any functions with names starting with ``test_`` will also be processed.

This one tool lets us use either style of testing. After looking
at the very sophisticated :mod:`unittest` tool and :mod:`pytest` tool,
the next section will look at the :mod:`doctest` tool. This tool
has some limitations, and doesn't support comprehensive tests. It
is, however, so easy to use that it can be the first thing
we turn to.

Python doctest Testing
=============================

Python :mod:`doctest`  module requires us to put our test cases
and expected results into the docstring comments on a class, method
or function.  Since we're going to write docstring comments, and
we're going to provide examples, there's very little overhead to this testing.

The test case information becomes a formal part of the API
documentation.  When a docstring includes doctest comments, the string
serves dual duty as formal test and a working example.

**Workflow**.
To use   :mod:`doctest` is to build the class, exercise it in the
Python interpreter, then put snippets of the interactive log into our
docstrings.

Generally, we follow this outline.

1.  Write and debug the class, including docstring comments.

2.  Exercise the class in an interactive Python interpreter.

3.  Copy the snippets out of the interactive log.  Paste them into
    the docstring comments.

4.  Run doctest to be sure that you've copied and pasted correctly.

**Example**. This is an example of what a module with
doctest docstrings looks like.

..  rubric:: Module with doctest examples.

..  include:: ../../code/blackjack_doctest.py
    :code: python
    :start-line: 11
    :end-line: 45

Running Doctest
---------------

There are two ways to use doctest: you can run it directly,
or use it as part of :mod:`pytest`.

..  rubric:: Running Doctest from the Command Line

..  code-block:: sh

    python -m doctest -v code/blackjack_doctest.py

This runs doctest and examines the specific module for comments
that can be taken as useful examples.

..  rubric:: Running Doctest via Pytest

..  code-block:: sh

    python -m pytest --doctest-modules code/blackjack_doctest.py

The ``--doctest-modules`` option is used to examine all of the
modules named for doctest examples. This can be done for the
entire ``src`` directory.

Building Doctest Examples
--------------------------

Let's assume we've built two classes; for example, :class:`Card` and :class:`Deck`.
One class defines a standard
playing card and the other class deals individual card instances. We'll
define some minimal doctests.

The first step is to develop our baseline class. See `Example Class Definition`_
for a version of the blackjack module with the :class:`Card` class definition
that we might start with.

**Exercise the Class**.
Once we have the class, we need to exercise it using interactive Python.
Here's what we saw.


..  code-block::

    MacBookPro-SLott:OODesign-3.1 slott$ python3
    Python 3.7.4 (default, Aug 13 2019, 15:17:50)
    [Clang 4.0.1 (tags/RELEASE_401/final)] :: Anaconda, Inc. on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from blackjack import Card, AceCard, FaceCard
    >>> c2d = Card(2, Card.Diamonds)
    >>> str(c2d)
    ' 2♢'
    >>> cas = AceCard(Card.Ace, Card.Spades)
    >>> str(cas)
    ' A♠'
    >>> cas.softValue
    11

During our session, we played with the preferred use
cases for our class. We can copy the examples from the interactive session and
paste them into our class docstrings.


**Update the Docstrings**.
After we have some output that shows correct behavior of our class, we
can put that output into the class docstrings. Here's our updated :file:`card.py`
module with doctest comments.


..  rubric:: blackjack.py With Doctests Included

..  include:: ../../code/blackjack_doctest.py
    :code: python
    :start-line: 97
    :end-line: 120

We've only shown the docstrings from two classes within
the overall module file.

In both cases, we've copied and pasted lines from
an interactive session to show show the class definitions
shold behave.  When we process this module with
:mod:`doctest` we can confirm that the advertised behavior
matches the actual behavior of the classes.

Handling Dependencies
======================

Let's assume we've built two classes in some chapter; for example, we're building
:class:`Card` and :class:`Deck`. One class defines a standard
playing card and the other class deals individual card instances. We
need unit tests for each class.

Generally, unit tests are taken to mean that a class is tested in
isolation. In our case, a unit test for the :class:`Card` class is completely isolated because
it has no dependencies.

However, our :class:`Deck` class depends on the :class:`Card` class, leading us to make a choice
between the following two alternatives:

-   Create a :class:`Mock` object to stand in for the :class:`Card` class.
    This lets us test the :class:`Deck` class in complete isolation. Doing
    this means we either use :func:`patch` (or :func:`monkeypatch.setattr`),
    or we design the :class:`Deck` class so it doesn't have a direct dependency
    on :class:`Card`.

-   Test the :class:`Deck` class knowing it depends on the :class:`Card` class. In this case
    we haven't isolated the two classes, pushing the edge of the envelope on
    one of the ideas behind unit testing. It's not clear that this is utterly
    evil, however. It's acceptable when we can create
    an integrated test of the :class:`Deck` class which also tests all of the
    features of the :class:`Card` class.

The choice depends on the relative complexity of the :class:`Card` class,
whether or not the :class:`Deck` class and :class:`Card` class will evolve independently,
and whether or not we can test all of the :class:`Card` class and :class:`Deck` class.

Some folks demand that **all** testing be done in "complete" isolation with
:class:`Mock` objects. In order to reduce the number of patches, we need to consider
ways of making the the two classes independent. We could, for example, provide
the :class:`Card` class as a parameter to the :class:`Deck` class, removing
the implicit dependency, and making testing simpler.

Looking Forward
===============

Programming involves writing application code as well as test code.
In many cases, we'll write a great deal of test code for relatively
small -- but important -- pieces of application code.

It helps to have an easy-to-use testing tool. The :mod:`pytest` tool
makes it easy to run a complete suite of unit tests, confirming that
everything we write behaves as we expected.

In the next chapter we'll look at one of the other important parts
of creating trusted, high-quality code: the documentation. While a simple
:file:`README.rst` is helpful, using the :mod:`sphinx` tool produces
more complete, and easier to use documentation with relatively little work.
