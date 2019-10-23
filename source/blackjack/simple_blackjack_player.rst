
Simple Blackjack Player Class
=============================

Our objective is to provide variant player strategies. This chapter will
upgrade our stub player class to give it a complete, working strategy.
This simple player can serve as the superclass for more sophisticated strategies.

We'll look at a simple strategy for play in `Blackjack Player Analysis`_.

In `Decision By Lookup`_ we'll look at an alternative design. We can use
a mapping instead of if statements.

In `SimpleBlackjackPlayer Design`_ we'll design the player. This will rework
some of the draft designs we've used earlier. We'll list all of the deliverables in
`Blackjack Player Deliverables`_.

Blackjack Player Analysis
--------------------------

In addition to the player's own hand, the player also has the dealer's
up card available for determining their response to the various offers.
The player has two slightly different goals: not bust and have a point
total larger than the dealer's. While there is some overlap between
these goals, these lead to two strategies based on the dealer's up card.
When the dealer has a relatively low card (2 through 6), the dealer has
an increased probability of going bust, so the player's strategy is to
avoid going bust. When the dealer has a relatively high card (7 through
10), the dealer will probably have a good hand, and the player has to
risk going bust when looking for a hand better than the dealer's.

**A Simple Strategy**.
We'll provide a few rules for a simple player strategy. This strategy is
not particularly good. Any book on Blackjack, and a number of web sites,
will have a superior strategy. A better strategy will also be
considerably more complex. We'll implement this one first, and leave it
to the student to research more sophisticated strategies.


#.  Reject insurance and even money offers.


#.  Accept split for aces and eights. Reject split on other pairs.


#.  Hit any hand with 9 or less. The remaining rules are presented in
    the following table.

..  csv-table:: Blackjack Player Strategy
    :header-rows: 1

    "Player Shows","2-6","7-10, Ace"
    "10 or 11","hit","double down"
    "hard 12 to 16","stand","hit"
    "soft 12 to 16","hit","hit"
    "17 to 21","stand","stand"


These rules can boil down to sequences of if-statements in the :meth:`split`,
:meth:`hit` and :meth:`doubleDown` methods.


In some contexts, complex if-statements are deplorable. Often,
a sequence of complex if-statements is a stand-in for proper allocation of
responsibility. In this class, however, the complex if-statements
implement a kind of index or lookup scheme.

If we want to reduce (or eliminate) the ``if``-statements, what can we do?

Decision By Lookup
~~~~~~~~~~~~~~~~~~

We have identified eight alternative actions which depend on a two-dimensional index.

-   One dimension contains four conditions that describe the player's hand.

-   The other dimension involves two conditions that describe the dealer's hand.

When we look at the various collections, we see that we can index into
a mapping using any kind of immutable object instance. In this case, we can index by
objects that represent the various conditions.
We would have to map each condition to a distinct object.

When we look at the conditions that describe the player's hand, these
are clearly state-like objects. Each card can be examined and a state
transition can be made based on the the current state and the card.
After accepting a card, we would check the total and locate the
appropriate state object. We can then use this state object to index
into a collection of player choices.


When we look at the conditions that describe the dealer's hand, there
are only two state-like objects. The dealer's op card can be examined,
and we can locate the appropriate state object. We can use this state
object to index into a collection.


The final strategy could be modeled as a collection with a two-part index.
This can be nested collection objects, or a Map that uses a 2-valued tuple
as an index.

Why use a mapping instead of a lot of if-statements?

We can easily change the decision by tweaking a cell in the mapping. This
seems to be easier than locating the correct conjunction of conditions.


SimpleBlackjackPlayer Design
-----------------------------

..  class:: SimpleBlackjackPlayer

    The :class:`SimpleBlackjackPlayer` ckass is a subclass of :class:`BlackjackPlayer`
    that responds to the various queries and inteactions with the game of
    Blackjack.

    This player implements a relatively simple strategy, shown above in the
    Blackjack Player Strategy table.

Methods
~~~~~~~


..  method:: SimpleBlackjackPlayer.evenMoney(self, hand: Hand) -> bool

    :param hand: the hand which is being offered even money
    :type hand: :class:`Hand`


    Returns :literal:`True` if this Player accepts the even money offer.
    This player always rejects this offer.



..  method:: SimpleBlackjackPlayer.insurance(self, hand: Hand) -> bool

    :param hand: the hand which is being offered insurance
    :type hand: :class:`Hand`


    Returns :literal:`True` if this Player accepts the insurance offer.
    This player always rejects this offer.



..  method:: SimpleBlackjackPlayer.split(self, hand: Hand) -> Hand

    :param hand: the hand which is being offered the opportunity to split
    :type hand: :class:`Hand`

    Returns a new, empty
    :class:`Hand` instance if this Player accepts the split offer for this :class:`Hand` instance.
    The Player must create a new :class:`Hand` instance, create an Ante
    :class:`Bet` instance and place the bet and the new hand on the :class:`BlackjackTable` object.

    If the offer is declined, both set :attr:`Hand.splitDeclined` to :literal:`True`
    and return :literal:`None`.

    This player splits when the hand's
    card's ranks are aces or eights, and declines the split for all
    other ranks.



..  method:: SimpleBlackjackPlayer.doubleDown(self, hand: Hand) -> bool

    :param hand: the hand which is being offered the opportunity to double down
    :type hand: :class:`Hand`



    Returns :literal:`True`
    if this Player accepts the double offer for this :class:`Hand` instance.
    The Player must also update the :class:`Bet` object associated with this
    :class:`Hand` instance.

    This player tries to accept the offer when the
    hand points are 10 or 11, and the dealer's up card is 7 to 10 or
    ace. Otherwise the offer is rejected.

    Note that some games will restrict the conditions for a double down
    offer. For example, some games only allow double down on the first
    two cards. Other games may not allow double down on hands that are
    the result of a split.



..  method:: SimpleBlackjackPlayer.hit(self, hand: Hand) -> bool

    :param hand: the hand which is being offered the opportunity to hit
    :type hand: :class:`Hand`


    Returns :literal:`True`
    if this Player accepts the hit offer for this :class:`Hand` instance.

    If the dealer up card is from 2 to 6, there are four choices for the
    player. When the hand is 11 or less, hit. When the hand is a hard 12
    to 16, stand. When the hand is a soft 12 to soft 16 (hard 2 to hard
    6), hit. When the hand is 17 or more, stand.

    If the dealer up card is from 7 to 10 or an ace, there are four
    choices for the player. When the hand is 11 or less, double down.
    When the hand is a hard 12 to 16, hit. When the hand is a soft 12 to
    soft 16 (hard 2 to hard 6), hit. When the hand is 17 or more, stand.

    Otherwise, if the point total is 9 or less, accept the hit offer.


Blackjack Player Deliverables
------------------------------

There are two deliverables for this exercise.


-   The :class:`SimpleBlackjackPlayer` class.


-   A class which performs a unit test of the :class:`SimpleBlackjackPlayer`
    class. The unit test can provide a variety of :class:`Hand` instances
    and confirm which offers are accepted and rejected.

Looking Forward
---------------

We'll look at some of the vast number of variations in the way blackjack is played.
Unlike Roulette and Craps -- where there are few variations -- Blackjack has a wide
variety of variants in betting and playing. In the next chapter we'll look at
some variants and how we'd adapt our existing application to support these options.
