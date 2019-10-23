.. Building Skills in Object-Oriented Design documentation master file, created by
   sphinx-quickstart on Thu Oct 10 18:12:39 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:title:
    Building Skills in Object-Oriented Design
:subtitle:
    Step-by-Step Construction of A Complete Application
:edition:
    version 4.1910
:pubdate:
    2019-10-10
:author:
    Steven F. Lott
:copyright:
    © 2019, Steven F. Lott

=====================================================
Building Skills in Object-Oriented Design, V4
=====================================================

..  rubric:: Step-by-Step Construction of A Complete Application

This is release |release|, published |today|.

..  admonition:: Legal Notice

    ..  image:: images/somerights20.png
        :target: http://creativecommons.org/licenses/by-nc-nd/2.0/
        :alt: Creative Commons License; some rights reserved.

    This work is licensed under a `Creative Commons License <http://creativecommons.org/licenses/by-nc-nd/2.0/>`_.
    You are free to copy, distribute, display, and perform
    the work under the following conditions:

    -   **Attribution**.
        You must give the original author, Steven F. Lott, credit.

    -   **Noncommercial**.
        You may not use this work for commercial purposes.

    -   **No Derivative Works**.
        You may not alter, transform, or build upon this work.

    For any reuse or distribution, you must make clear to others the
    license terms of this work.

..  toctree::
    :maxdepth: 1

    preface

Getting Started
===============

In this part, we'll look at some general topics required to
get started. The first chapter will provide some foundations,
talking about the problem domain, the solution, and some general
ideas on how the work will proceed.

The remaining chapters will provide specific guidance on setting
up a working development environment, writing some basic unit
tests, and starting down the road to producing useful documentation.
These sections will set the stage for all of the work which follows.

..  toctree::
    :maxdepth: 2

    starting/foundation
    starting/initial_setup
    starting/python_testing
    starting/python_documentation

..  _`roul`:

Roulette
========

Roulette is a stateless game
with numerous bets and a very simple process for game play.

The chapters of this part present the details on the game, an overview
of the solution, and a series of sixteen exercises to build a complete
simulation of the game, plus a variety of betting strategies. Each
exercise chapter builds at least one class, plus unit tests; in some
cases, this includes rework of previous deliverables.

..  toctree::
    :maxdepth: 2

    roulette/details
    roulette/solution
    roulette/outcome
    roulette/bin
    roulette/wheel
    roulette/bin_builder
    roulette/bet
    roulette/roulette_table
    roulette/roulette_game
    roulette/testability
    roulette/player
    roulette/control
    roulette/sevenreds
    roulette/statistics
    roulette/random
    roulette/1_3_2_6
    roulette/cancellation
    roulette/fibonacci
    roulette/conclusion

..  _`craps`:

Craps
==========

This part describes parts of the more complex game of Craps.  Craps
is played with dice.
Craps is a game with two states and a number of state-change rules. It has a
variety betting alternatives, some of which are quite complex.

The chapters of this part presents the details on the game, an overview
of the solution, and a series of eleven exercises to build a complete
simulation of the game, with a variety of betting strategies. The
exercises in this part are more advanced; unlike :ref:`roul`, we will
often combine several classes into a single batch of deliverables.

There are several examples of rework in this part, some of them quite
extensive. This kind of rework reflects three more advanced scenarios:
refactoring to generalize and add features, renaming to rationalize the
architecture, and refactoring to extract features. Each of these is the
result of learning; they are design issues that can't easily be located
or explained in advance.


..  toctree::
    :maxdepth: 2

    craps/details
    craps/solution
    craps/outcome
    craps/throw
    craps/dice
    craps/throw_builder
    craps/bet
    craps/craps_table
    craps/craps_game
    craps/craps_player
    craps/refactoring
    craps/simple_craps_player
    craps/roll_counting_player
    craps/conclusion

..  _`blackjack`:

Blackjack
==========

This part describes the more complex game of Blackjack.
This game has a
number of states and a number of complex state-change rules.
While the betting rules are simple, the game play is more complex.

The chapters of this part presents the details on the game, an overview
of the solution, and a series of six relatively complex exercises to
build a complete simulation of the game. In the case of Blackjack, we
have to create a design that allows for considerable variation in the
rules of the game as well as variation in the player's betting strategies.


..  toctree::
    :maxdepth: 2

    blackjack/details
    blackjack/solution
    blackjack/card_deck_shoe
    blackjack/hand
    blackjack/blackjack_table
    blackjack/blackjack_game
    blackjack/simple_blackjack_player
    blackjack/variant_game
    blackjack/conclusion

..  _`finish`:

Fit and Finish
==============

A finished application includes more than just a collection of packages.
We'll need to build a Command-Line Interface (CLI) to operate this program.
This isn't a sophisticated OO design problem. This is a collection
of exercises in using the standard library to create the final
application.

..  toctree::

    finish/test_automation
    finish/command_line_interface
    finish/management_handwringing


Production
==========

This book was built with Python 3.7

-  Sphinx 2.2.0

-  MacTeX 2019


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
