Command-Line Interface (CLI)
#############################

..  todo:: Finish this section.

In :ref:`roul.control` we talked about the overall :class:`Simulation` class --
the component that ran the entire application, creating objects, running
the simulation, gathering the data, writing a log, and saving files with
the interesting, useful results.

We suggested a class definition, but never followed through to the OS-level
interface for the application as a whole. There are several ways an application
like this can be packaged, we'll look at how to make a final command-line
interface (CLI) for this simulation application.

In `CLI Analysis`_, we'll look at the general problem of the CLI, to
decide what it should do and how it supports the rest of the application.

There will be a few design decisions. In `Design Decision -- CLI Library`_ we'll
address the choice of libraries. In `Design Decision -- Class vs. Function`_
we'll decide if this should be a kind of :strong:**Singleton** class or
a simpler collection of functions.

In `CLI Design`_ we'll describe the final design of the CLI. In `CLI Deliverables`_
we'll enumerate the components to be built and tested.

CLI Analysis
------------

The CLI will be part of the overall user story described in :ref:`found`.
In :ref:`found.solution` we described a hypothetical command for
running the simulation:

..  code-block:: sh

    python3 -m casino.craps --Dplayer.name="Player1326" >details.log

This shows a number of features that drive the design:

-   The app runs from the OS terminal prompt.
    It uses POSIX command-line arguments. (It's possible to use the
    Python CLI libraries to create Windows-like commands, also.)

-   The app is a package, :mod:`casino`, with a sub-package, :mod:`craps`,
    that contains a :mod:`main` function that does the real work.

-   The detailed output was written to standard output. A shell redirect
    (``>details.log``) was used to capture the output into a file for further
    analysis.

This concept has some room for improvement, but it points to a number of
detailed responsibilities we can use to drive the design.

We can pull out three diffient kinds of responsibilities, shown below:

-   Parse command line options and arguments. This is something we'll
    delegate to a separate library. We have two choices and `Design Decision -- CLI Library`_
    will address the library choice.

-   Write to standard output and standard error. This is a built-in
    feature of the :func:`print` function. In the long run, however, we
    need to move away from the simple use of :func:`print` and separate
    output into two parts: a log to summarize what work is being
    done, and the final output files in CSV format, created as
    part of the statistical summary of the :class:`Simulator` class.

-   Have a structure that permits easy access via the ``python -m`` command.



Design Decision -- CLI Library
------------------------------

There are several popular packages for building CLI's.

**Problem**. Which CLI library should we use? Two of the popular
packages are the :mod:`argparse` package, which
is part of the Python standard library, and the :mod:`click` library,
which must be installed separately.

**Forces**. Both packages solve the core problems
of parsing command-line options.

When we look at simplicity or convenience, the :mod:`argparse` package
is part of the Python standard library. This makes it very handy.

The :mod:`click` library must be installed separately. It offers a number
of handy features, and seems slightly easier to work with than :mod:`argparse`.

In particular, the :mod:`click` library works as a collection of decorators,
slightly reducing the overall complexity of the main application.

**Solution**.
We'll recommend using :mod:`click`  to build CLI's for command-line applications.


**Consequences**.
We'll need to install ``click`` and add it to the project's :file:`requirements.txt`.

::

    conda install click

The core use case for :mod:`click` looks a little bit like this example:

..  rubric:: Example CLI module

..  include:: ../../demo/src/cli.py
    :code: python

The :func:`main` function here needs to build the instance of the :class:`Simulator`
with the proper game, players, and casino-specific table subclass.

Because each game is quite different, it's sensible to create three separate
packages, one for each game.

Design Decision -- Class vs. Function
-------------------------------------

In Python, the top level of an application doesn't have to stick
closely to object-oriented programming techniques. The top-level features
are often better described by separate functions.

**Problem**.
How do we implement the OS interface? A :func:`main` function, or a class
that must be instantiated, or a class with a ``@staticmethod`` that
can be used to do the work?

**Forces**.
There are a number of alternatives for structuring the top-level main program.

-   A simple script of statements. This is very, very difficult to unit test.
    We discourage the use of flat script-like Python modules.

-   A :func:`main` function. Often called ``main()``. In order to be part of
    a top-level program, there must **also** be a script present in the module.
    This leads to a module with an overall layout like the following:

    ::

        imports
        class definitions

        def main():
            the real work

        if __name__ == "__main__":
            main()  # pragma: no cover

-   A class with that must be instantiated. This is nearly identical to the function
    example shown above. The following example shows this variation. It's not clear
    that this is advantageous.

    ::

        imports
        class definitions

        class Main:
            def main(self):
                the real work

        if __name__ == "__main__":
            Main().main()  # pragma: no cover

-   A class with a ``@staticmethod``. This paralles the Java concept of a static
    ``main`` function that's required by the JVM. This would lead to a module
    with the following kind of organization.

    ::

        imports
        class definitions

        class Main:
            @staticmethod
            def main():
                the real work

        if __name__ == "__main__":
            Main.main()  # pragma: no cover

The two class-based alternatives don't seem to offer material advantages.
The script only creates a single instance of the class, or uses the
class directly. Any class with only a single instance can be viewed
as a **Big Hammer** solution.

**Solution**.
The conventional approach in most Python code is a top-level function,
often with a name like ``main()``. We can apply the :mod:`click` decorations
to this function easily and use it to define the main application.

**Consequences**.
We'll need to create proper unit tests for the top-level :func:`main` function.
This will require using the :mod:`click` unit testing features to
invoke the command with appropriate arguments.

CLI Design
----------

We've (intentionally) provied little guidance on the structure of
the modules and packages in this application. The following organization
may require rework to restructure the classes into the four modules
within the :mod:`casino` package.

The :mod:`casino` package is the top-level package for the entire
suite of simulation components. The top-level package has no
components, since its purposes is to act as a namespace for the
various simulators. The package is implemented as a directory
named :file:`casino` with an empty :file:`__init__.py` file.

A :mod:`casino.common` module will have the abstract superclasses for the other modules.
This module is implemented as the :file:`common.py` file in the :file:`casino` directory.
The remaining modules are similarly a simple :file:`.py` file filled with class definitions,
and a top-level :func:`main` function.

The :mod:`casino.craps` module with the complete definition for
Craps. The module will import
common definitions from the :mod:`casino.common` module.

The :mod:`casino.roulette` module with the complete definition for
Roulette. The module will import
common definitions from the :mod:`casino.common` module.

Similar to the above modules, a :mod:`casino.blackjack` module
will have the complete Blackjack simulation.


..  module:: casino.craps

..  function:: casino.craps.main

    The main function for the Craps simulation. This will have
    ``@click.command()`` and ``@click.option`` decorators to define
    the various options

..  module:: casino.roulette

..  function:: casino.roulette.main

    The main function for the Roulette simulation. This will have
    ``@click.command()`` and ``@click.option`` decorators to define
    the various options

..  module:: casino.blackjack

..  function:: casino.blackjack.main

    The main function for the Blackjack simulation. This will have
    ``@click.command()`` and ``@click.option`` decorators to define
    the various options



CLI Deliverables
----------------

The following components will be built:

-   The top-level :mod:`casino` module.

-   The lower-level modules:

    -   :mod:`casino.common`

    -   :mod:`casino.craps`

    -   :mod:`casino.roulette`

    -   :mod:`casino.blackjack`

-   Any revisions to the unit tests required to reflect the new organization.

-   Unit tests for the three :func:`main` functions.

