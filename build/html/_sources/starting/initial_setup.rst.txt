..  _`found.starting`:

Development Environment
########################

In this chapter, we'll build the initial working development
environment. We'll install some tools, create a template directory
structure, and run the first round of tests to be sure
things work.

We'll start with an overview of what we're going to build.
In `Deliverables_`, we'll address the kinds of deliverables
that should be produced. These kinds of deliverables form the basis for each chapter.


Deliverables
============

Each chapter defines the classes to be built and the unit testing
that is expected. A third category of deliverable -- documentation -- is merely implied.

The purpose of
each chapter is to write the source files for one or more classes, the
source files for one or more unit tests, and assure that a minimal set
of API documentation is available.

-   **Source Files**.
    The source files are the most important deliverable. In effect,
    this is the working application program. Generally, we will be
    running this application from within the Integrated Development
    Environment (IDE).

    We can always run the Python as a stand-alone program, if we want
    to exercise it the way end-users will see it.

    In the case of Python, a "program" is the collection of
    :file:`.py` files. There really isn't much more to deliver.
    This makes our life simpler than in other languages with
    complex compilers and other tools.

-   **Unit Test Files**.
    The deliverables section of each chapter summarizes the unit
    testing that is expected, in addition to the classes to be built. We
    feel that unit testing is a critical skill, and emphasize it
    throughout the individual exercises.

    There are two broad approaches for unit tests.

    -   The built-in :mod:`unittest` module has facilities
        for defining test classes.

    -   The add-on :mod:`pytest` package has facilities
        for writing somewhat simpler test functions.
        The ``pytest`` tool can collect :class:`unittest.TestCase`
        classes as part of a test suite, making this
        an ideal choice for running unit tests.

    We'll look closely at the overall project structure in the next section.

-   **Documentation**.
    The job isn't over until the paperwork is done.
    The internal documentation is generally built from
    specially formatted blocks of comments within the source itself.
    We can use **sphinx** to create
    documentation based on the code.

We'll be building three separate, but closely-related things:
the code, the test cases, and the documentation. In the next
section we'll organize our tools.

Tools
=====

Perhaps one of the most important considerations is to have
a way to manage multiple Python environments. Each
project will often have a unique combination of
add-on libraries and tools. There are a number
of "virtual environment" managers available. In this book,
we're going to suggest using **conda** to manage Python
installation and environment setup.

While Python is often available on modern OS's, it tends
to be out-of-date. The OS Python often requires privileges
to do installs and upgrades.

..  important:: Don't Use the OS Python

    Even if Python is already installed, don't use it.

    Always install your own, so you can keep it up-to-date
    without worrying about OS conflicts or privileges.

    It's rare to have a one-size-fits-all Python environment.
    It's more common to have a unique virtual environment for
    each project.

Here's a good way to proceed.

1.  Download Miniconda.  https://docs.conda.io/en/latest/miniconda.html

2.  Follow the installation instructions: https://conda.io/projects/conda/en/latest/user-guide/install/index.html

#.  Once conda is installed, create a working environment in your favorite
    terminal window.

    ::

        conda create --name oo-design python=3.7 pytest sphinx

#.  Activate the working environment.

    ::

        conda activate oo-design

#.  Add ``tox`` to the environment. This isn't available from the libraries
    searched by ``conda``, so we'll use ``pip`` to install it.

    ::

        python -m pip install tox

At this point, we can enter the following command to see we have a useful,
working virtual environment.

    ::

        (oo-design) slott@MacBookPro-SLott % python -V
        Python 3.7.4

Python is relatively easy to work with: any text editor will serve
a developer's needs. Something as simple as Atom (https://atom.io) or something
as sophisticated as PyCharm (https://www.jetbrains.com/pycharm/)
are both acceptable as IDE's.

Once we have our tools installed, the next section describes
how we can organize the working directories of our project.

Working Directories
===================

Because Python is a very flexible language, there are a variety of ways
of organizing the software being built. We'll provide a structure
here which seems like it might be helpful. It's not required,
and a number of alternatives are possible.

The project can start out looking like this:

::

    oo-design
    |
    |-- docs
    |-- src
    |-- tests
    |-- tox.ini

This can be built by creating three empty directories: ``docs``, ``src``, and ``tests``.
The remaining file, ``tox.ini`` is something we'll look at in the :ref:`start.testing`
chapter.

We'll build our application in the ``src`` directory. The test cases
will be in the ``tests`` directory. The documentation is something will look
at in :ref:`documentation`.

To see how things will work in general, we'll create a file in the ``src`` directory
and execute it.

1.  Edit a file, :file:`hw.py` in the :file:`src` directory with the following content:

    ::

        print("hello world")

2.  From the top-level of the project, the following command be used to execute the
    file:

    ::

        (oo-design) slott@MacBookPro-SLott project % python src/hw.py
        hello world

    We've started the Python run-time with the path of the :file:`src/hw.py` file.
    This works reasonably well for small programs, but it doesn't work out well
    when we start creating larger applications.

3.  From the top-level of the project, the following can also be used to execute the
    file.

    ::

        (oo-design) slott@MacBookPro-SLott project % PYTHONPATH=src python -m hw
        hello world

    This sets the OS environment variable, :envvar:`PYTHONPATH` to include
    the :file:`src` directory. The ``-m`` option locates a Python module
    named ``hw``.  Module names map to file names in a simple way.
    This command requires Python to search through the directories named
    in the :envvar:`PYTHONPATH` for the target module's source file, :file:`hw.py`.

    Many IDE's, like PyCharm, can add the ``src`` directory to the ``PYTHONPATH``
    automatically.

4.  We can simplify option three with the following one-time setup:

    ::

        (oo-design) slott@MacBookPro-SLott project % export PYTHONPATH=src

    After this, the environment variable it persistent for the duration
    of the terminal session.

    We can then run our application like this:

    ::

        (oo-design) slott@MacBookPro-SLott project % python -m hw
        hello world

Looking Forward
===============

Once we have our tools installed and running, we can begin to
look at general features of building applications in Python.
This involves creating a few directories to separate our application
from out test cases and documentation.

In the next chapter, we'll look at setting up an initial set of unit
tests. This will show the concept of unit testing, and it will also
confirm the environment is setup correctly.
