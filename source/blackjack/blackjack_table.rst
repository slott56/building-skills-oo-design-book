
Blackjack Table Class
=====================

The bets in Blackjack are associated with a hand. A player may have
more than one hand in play. This will lead us to
create a subclass of table to handle this complexity. In order to manage
the relationships between hand and bet, we'll rework hand, also.

We'll look at the table in `Blackjack Table Analysis`_.

Based on the classes defined so far, we can look at the design
for the table in `BlackjackTable Class`_.

We'll look at some minor rework to :class:`Hand` in `Hand Rework`_.

In `Blackjack Table Deliverables`_ we'll enumerate the deliverables for this chapter.

Blackjack Table Analysis
-------------------------

When we look at the game of Blackjack, we note that a player's :class:`Hand` object
can be split into multiple :class:`Hand` instances.
In some casinos, resplits are allowed, leading to the
possibility of three or more :class:`Hand` instances. Each individual :class:`Hand` object
has a separate ante :class:`Bet` and seperate resolution. This is
different from the way bets are currently managed for Roulette and Craps,
where the bets are associated with  the player.

We have several alternatives for modeling this:

-   Assign responsibility to the :class:`Table` class to keep track of bets
    tied to the various :class:`Hand` instances.
    This would make the :class:`Hand` a potential
    key into a mapping to associate a :class:`Hand` object with one or more :class:`Bet` instances.
    Because :class:`Hand` instances change state, this is a  poor choice
    for keys to a dictionary.

-   We could put a reference to a :class:`Hand` object
    into each :class:`Bet` object.  In this way, as each :class:`Bet` object
    is resolved, the relevant :class:`Hand` object can be evaluated to
    determine the :class:`Outcome` instance that applies and what they payout odds are.

-   We could put a reference to the Ante
    :class:`Bet` object into the :class:`Hand` instance. In this way, as each :class:`Hand` instance
    is resolved, the relevant :class:`Bet` instances can be paid or lost.

It's helpful to look at the alternatives carefullly and try to identify
the various forces and consequences.

We suggest designing the :class:`Hand` class to contain the associated ante :class:`Bet` object.
This is least disruptive to the :class:`Bet` class definition, which is a simple thing
used widely in other games.

**Additional Bets**.
While most :class:`Bet` instances are associated with a specific :class:`Hand` object,
the insurance :class:`Bet` instance is always resolved before an additional hand
can be created. There doesn't seem to be an essential association between
the initial :class:`Hand` object and the insurance :class:`Bet` object. We
can treat insurance as a :class:`Bet` instance that follows the model
established for Craps and Roulette -- it belongs to the player, rather than a particular hand.


Currently, the :class:`Bet` instances are collected by the :class:`Table` instance. If
we create a :class:`BlackjackTable` subclass to use a :class:`Hand` object
when creating a :class:`Bet` instance, we can have this method do both
tasks: it can attach the :class:`Bet` object to the :class:`Hand` instance, and
it can save the :class:`Bet` object on the :class:`Table` instance, also.


BlackjackTable Class
--------------------

..  class:: BlackjackTable

    The :class:`BlackjackTable` class is an extension to :class:`Table` that handles the
    additional association between :class:`Bet` instances and specific :class:`Hand` instances
    in Blackjack.


Constructors
~~~~~~~~~~~~


..  method:: BlackjackTable.__init__(self) -> None

    Uses the superclass constructor to create an empty :class:`Table` instance.


Methods
~~~~~~~~


..  method:: BlackjackTable.placeBet(self, bet: Bet, hand: Hand) -> None

    :param bet: A bet for this hand; an ante bet is required.  An insurance
        bet, even money bet or double down bet is optional.
    :type bet: :class:`Bet`

    :param hand: A hand on which the player is creating a Bet.
    :type hand: :class:`Hand`


    Updates the given :obj:`hand`
    to reference the given :obj:`bet`. Then uses the superclass :meth:`placeBet`
    to add this bet to the list of working bets.




..  method:: BlackjackTable.__str__(self) -> str

    Provides a nice string display of the state of the table.


Hand Rework
-----------

The :class:`Hand` class contains a collection of individual :class:`Card` instances,
and determines an appropriate total point value for the hand.

We need to add a field and some appropriate methods for associating
a Bet with a Hand.

Fields
~~~~~~~~~

..  attribute:: Hand.ante

    Holds a reference to the ante :class:`Bet` for this hand. When
    this hand is resolved, the associated bet is paid and removed from
    the table.

Methods
~~~~~~~~

We have two implementation choices here. We'll show these as
setters and getters. However, it's common to make these
both properties of a hand.


..  method:: setBet(self, ante: Bet) -> None

    :param ante: The initial bet required to play
    :type ante: :class:`Bet`


    Sets the ante :class:`Bet`
    that will be resolved when this hand is finished.



..  method:: getBet(self) -> Bet


    Returns the ante :class:`Bet` for this hand.

Here's the alternative implementation. We can use properties
for this feature.

..  rubric:: Properties for getter and setter

..  code-block:: python

    class Hand:

        @property
        def bet(self):
            return self.ante

        @bet.setter
        def bet(self, bet):
            self.ante = bet

In this example, we've created a property, ``bet``, so that can  write code
like this: :code:`h.bet` to fetch the bet associated with the hand.

By itself, this isn't too useful. The setter property, however, allows us
to write code like this :code:`h.bet = Bet("Ante",1)`. We can then implement
any additional processing in the hand that needs to be done when the bet is changed.

Blackjack Table Deliverables
-----------------------------

There are four deliverables for this exercise.

-   The revised :class:`Hand` class.

-   A class which performs a unit tests of the :class:`Hand` class.
    The unit test should create several instances of :class:`Card`, :class:`FaceCard`
    and :class:`AceCard`, and add these to instances of :class:`Hand`,
    to create various point totals. Additionally, the unit test should
    create a :class:`Bet` and associate it with the :class:`Hand`.

-   The :class:`BlackjackTable` class.

-   A class which performs a unit tests of the :class:`BlackjackTable`
    class. The unit test should create several instances of :class:`Hand`
    and :class:`Bet` to create multiple :class:`Hand` instances, each
    with unique :class:`Bet` instances.

Looking Forward
---------------

Now that we have the core objects -- card, deck, hand, and table -- we can
look at the details of how the game proceeds. This involves creating multiple
hands, oferring specialized betting and playing choices, and tracking the evolving
state of a number of hands. The next chapter will look at the :class:`Game` subclass
for Blackjack.
