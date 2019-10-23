Quality Assurance
#############################

Back in :ref:`found.starting` we suggested a common kind of project organization.
There can be a :file:`src` directory with the final application and a :file:`tests` directory
with the unit test cases.

This works out extremely well because a lot of Python tools expect a structure similar
to this.

Because there are some variations, we need to include

::

    export PYTHONPATH=src
    pytest

Or, as an alternative, we can set this each time we execute the tests.

::

    PYTHONPATH=src pytest

We don't need to provide very many options to the **pytest** program because the default directory for
tests, :file:`tests` is what we set up for outselves.

In this chapter, we'll look at several other parts of test automation:

1.  `Static Type Checking`_ with **mypy**.

2.  `Static Code Quality Checks`_ with **pylint**.

3.  `Code Formatting`_ with **black**.

4.  `Test Coverage Analysis`_ with **coverage**.

5.  `Test Automation`_ suite with **tox**.

The idea behind this suite of tools it to show a number of common practices that can be applied to this
application.

Static Type Checking
====================

We've annotated all of the descriptions of classes and methods with type hints. These are relatively
new to Python. The hints have no run-time impact; they're used for static analysis of the code
to provide confidence it's likely to work. See http://mypy-lang.org for more information
on this tool.

If it's not already installed, the **mypy** tool can be installed with

::

    conda install mypy

The tool is used like this:

::

    mypy src/blackjack.py

The output will often include numerous nuanced issues where the type hints on a parameter
to a method don't precisely match the type hints on the return type of another method.

Some Common Problems
--------------------

One of the more common problems is reconciling the subclass-superclass features
with methods actually used. Python duck typing rules mean any object will be searched
for the expected attribute, either instance variable or method. The **mypy** tool
looks for evidence the attribute or method is likely to be present.

Consider the following class definition

..  include:: ../../code/wheel_examples.py
    :code: python
    :start-line: 10
    :end-line: 17
    :number-lines: 11

We've defined the second parameter, ``rng``, to be an instance
of :class:`random.Random`. The default value, however, is :literal:`None`.

We'll get the following kind of error:

::

    code/wheel_examples.py:12: error: Incompatible default for argument "rng" (default has type "None", argument has type "Random")

This kind of thing requires us to be much more explicit in our statements of what the data type is.

We need to change the type hint of ``rng: random.Random=None``.
This needs to be ``rng: Optional[random.Random]=None`` to more correctly state
what we expect for the parameter to this method.

Additionally, some assignment statements can be ambiguous. In this cases, we may need to add a type hint
to an assignment statement.

::

    some_dict: DefaultDict[str, int] = collections.defaultdict(int)

The :func:`collections.defaultdict` function only includes a function to create a value to be created when a key
is not found. It doesn't describe the type of the value or the type of the keys. The **mypy** tool can
examine the :func:`int` function to determine the type of value returned. There's no suggestion
about what the keys are, and Python doesn't really need any suggestion.

In order to be confident, we need to provide a hint, using the :class:`typing.DefaultDict` type definition.
This definition lets us provide a key type and a value type. With this additional information,
the **mypy** tool can confirm that the ``some_dict`` variable is used properly.

Static Code Quality Checks
==========================

The **pylint** tool does some checks for  "style" issues. It can also check a number of programming
techniques that -- while legal -- are likely to be a code smell. See https://www.pylint.org
for the complete list of checks that can be performed.

We install this with conda, also.

::

    conda install pylint

We run this to get a list of possible problems with the source code of the module.

::

     pylint code/blackjack.py
    ************* Module code.blackjack
    code/blackjack.py:17:0: C0115: Missing class docstring (missing-class-docstring)
    code/blackjack.py:35:4: C0103: Attribute name "hardValue" doesn't conform to snake_case naming style (invalid-name)
    code/blackjack.py:35:4: C0116: Missing function or method docstring (missing-function-docstring)
    code/blackjack.py:39:4: C0103: Attribute name "softValue" doesn't conform to snake_case naming style (invalid-name)
    code/blackjack.py:39:4: C0116: Missing function or method docstring (missing-function-docstring)
    code/blackjack.py:49:4: C0116: Missing function or method docstring (missing-function-docstring)
    code/blackjack.py:50:8: C0103: Variable name "s" doesn't conform to snake_case naming style (invalid-name)
    code/blackjack.py:56:8: C0103: Variable name "r" doesn't conform to snake_case naming style (invalid-name)
    code/blackjack.py:81:0: C0115: Missing class docstring (missing-class-docstring)
    code/blackjack.py:99:0: C0115: Missing class docstring (missing-class-docstring)
    code/blackjack.py:117:0: C0116: Missing function or method docstring (missing-function-docstring)

    -----------------------------------
    Your code has been rated at 8.38/10

This outout lists a number of problems that are either omissions of docstrings or variables
with names that don't follow the typical Python style, called "snake_case". The names ``hardValue``
and ``softValue`` should be ``hard_value`` and ``soft_value``.

This a pervasive change to the code examples throughout this book. We haven't made the change, but
the reader can consider revising their own code to reduce the number of pylint problems.

The rating, ``8.38/10``, clearly shows room for improvement. Adding the required docstrings, for example,
would lead to a dramatic improvement in the quality metric.

Code Formatting
===============

One way to achieve consistent and easy-to-read code is to use a code formatting tool.
One of the more popular tools is **black**. This tool is described as "uncompromising."
It has relatively few options and produces consistent, easy-to-read code.

::

    conda install black

The tool will simply reformat any valid Python to fit the recommended style. The **black** tool
can also be used to confirm that a module is already formatted correctly. This becomes
a kind of testing tool to confirm the formatting before doing a Git checkin, or starting
a long integration and deployment process.

We can use it to reformat an entire directory tree like this:

::

    black src

That's all there is to it. It provides a very small summary of what it did.
This is delightfully simple and creates consistent-looking source files.

Test Coverage Analysis
======================

Generally, we want test cases to confirm the application under test will work. It's difficult writing
a good application, and it's difficult writing good test cases. One of the key questions is how much of
the software is covered by test cases.  Ideally, a vague "all of the software" has been tested. The
difficult problem is defining what "all" means.

There are a number of ways to measure software and decide if "all" of it has been tested.

-   Tests execute code in all of the modules.

-   Tests execute code in all of the classes.

-   Tests execute code in all of the methods of all of the classes.

-   Test execute all of the statements.

-   Tests evaluate both true and false for each condition expressed in an ``if``, ``elif``, or ``while`` statement;
    the implicit condition of each ``else``,
    so each each exception in a ``try`` statement; also a test for each ``for`` statement.
    These are the places were there's a choice among statements to be executed.

-   Tests exercise each possible combination of the conditional processing choices (``if``, ``elif``, ``else``, etc.)

Clearly, some of these don't test very much, and some are quite complex to design.

It's very easy to measure whether or not a test touches all of the statements. We'll focus on this.

The Test Coverage Tool
-----------------------

Since we're using ``pytest``, we can install the ``pytest-cov`` plug-in. This will, in turn, install the ``coverage``
tool.

::

    conda install pytest-cov

To use the coverage tool, we need to provide a top-level module (or package of modules) for which we'd like
coverage metrics.

::

    PYTHONPATH=src pytest --cov=src

Here's what the output looks like:

::

    ================================= test session starts =================================
    platform darwin -- Python 3.7.4, pytest-5.0.1, py-1.8.0, pluggy-0.13.0
    rootdir: /Users/slott/Documents/Writing/Technical/building-skills-oo-design-book/demo
    plugins: cov-2.7.1
    collected 4 items

    tests/test_hw_1.py ..                                                           [ 50%]
    tests/test_hw_2.py ..                                                           [100%]

    ---------- coverage: platform darwin, python 3.7.4-final-0 -----------
    Name        Stmts   Miss  Cover
    -------------------------------
    src/hw.py      11      1    91%


    ============================== 4 passed in 0.06 seconds ===============================

The pytest tool tells us it's running two tests, ``test_hw_1.py`` and ``test_hw_2.py``.
The final coverage report says the 91% of the code has been exercised.

What's missing?

We an add the ``--cov-report=term-missing`` option to see which lines were not tested.
Here's the revised command.

::

    PYTHONPATH=src pytest --cov=src --cov-report=term-missing

Here's the revised coverage report

::

    ---------- coverage: platform darwin, python 3.7.4-final-0 -----------
    Name        Stmts   Miss  Cover   Missing
    -----------------------------------------
    src/hw.py      11      1    91%   25

Line 25 is not exercised by the test. What is this difficult-to-test line?

..  include:: ../../demo/src/hw.py
    :code: python
    :start-line: 22
    :number-lines: 24

Line 25 is very hard to test with conventional unit testing approaches.
It's not impossible, but it's difficult and the extra effort doesn't create
a lot of value.

We can add a special ``# pragma: no cover`` comment to tell the coverage
tool to apply this "fact" or "pragma" to the line in question. This improves
the coverage score and adds a comment informing everyone of what line was
skipped.



Test Automation
===============

We have a large suite of testing tools to provide real confidence in the quality
of the application programming. It can seem daunting to keep all of the tools straight.
The **tox** tool, however, gives us a path forward. We can use **tox** to run our
suite of static and dynamic tests.

We'll use **pip** to install tox.

::

    python -m pip install tox

This is required because **tox** is not in any of the common respositories
searched by **conda**.

Once we have **tox** installed, we need to create a configuration file.
This can be called ``pyproject.toml`` or ``tox.ini``. The content of the
file will look like the following example:

::

    [tox]
    skipsdist = True
    requires =
        tox==3.14.0

    [testenv]
    ignore_errors = True
    deps =
        mypy==0.720
        pylint==2.4.2
        black==19.3b0
        pytest==5.0.1
        pytest-cov==2.7.1
    setenv =
        PYTHONPATH=src
    commands =
        mypy src
        pylint src
        black src
        pytest --doctest-modules src
        pytest --cov=src


The first section, ``[tox]`` is general information about **tox**. The ``skipsdist`` avoids
building a source distribution kit. We're  not going to upload this code to
the Python Package Index (https://pypi.org) sometimes called the "Cheese Shop." Since
we're not building a source distribution, we don't need some of the overheads associated
with that step.

The main section, ``[testenv]`` is repeated for each distinct test environment.
In this case, we only need one test environment, so we don't have a complex configuration.
We've provided four distinct configuration values:

-   The ``ignore_errors`` makes sure the testing continues even if an error in one step
    has been found. This lets us run the whole suite of tests, then fix all of the problems.

-   The ``deps`` defines the dependencies required to run the tests. We've listed
    specific versions of each tool.

-   THe ``setenv`` defines the environment variables to provide when running the tests.
    The default setup provides very few environment settings. Because our application
    is located in a ``src`` directory, we need this to be on the :envvar:`PYTHONPATH`
    environment variable.

-   The ``commands`` is a sequence of commands to execute. There are strict limitations
    on these commands. This allows the ``tox`` tool to run in a wide variety of
    environments and remain perfectly consistent.

To run tox, we use the command

::

    tox

If we're in the same working directy as the ``tox.ini`` (or ``pyproject.toml``) file, then
**tox** will execute each of the commands, giving us a detailed view of how well our application
passes the suite of quality assurance tests.

The use of a tool like **tox** makes test execution simple and consistent. It gives us
a lot of help in producing useful, trustworthy, reliable software.

Looking Forward
---------------

In the next chapter we'll look at what's required to create a final,
command line interface (CLI) to run the simulation command
with various options and arguments.
