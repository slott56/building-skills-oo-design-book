
Blackjack Solution Overview
===========================

In `Preliminary Survey of Classes`_ we'll present a survey of the new
classes gleaned from the general
problem statement in :ref:`found.problem` as well as the problem
details in :ref:`blackjack.details`. This survey is drawn from a quick
overview of the key nouns in these sections. We will not review those
nouns already examined for Craps and Roulette.

From the nouns we can start to define some classes. We'll
present this in `Preliminary Class Structure`_.

We'll confirm our notion with a walk-through of parts of a scenario.
We'll show this in `A Walkthrough`_.

In `Blackjack Solution Questions and Answers`_ we'll provide some
additional ideas on the overall solution.

Preliminary Survey of Classes
-----------------------------

In reading the background information and the problem statement, we
noticed a number of nouns that seemed to be new to the game of Blackjack.


-   Card

-   Deck

-   Point Value

-   Hand

-   Number Card

-   Face Card

-   Offer

-   Insurance

-   Split

-   Double

-   Hit

-   Stand

-   Player

-   Game


The following table summarizes some of the new classes and
responsibilities that we can identify from the problem statement. This
is not the complete list of classes we need to build. As we work through
the exercises, we'll discover additional classes and rework some of
these classes more than once.


We also have a legacy of classes available from the Roulette and Craps
solutions. We would like to build on this infrastructure as much as possible.



Preliminary Class Structure
---------------------------

:Card:
    **Responsibilities**

    Three apparent subclasses:
    :class:`NumberCard`, :class:`FaceCard` and :class:`AceCard`

    A standard playing card with a rank and a suit. Also has a
    :emphasis:`point value` from 1 to 11. Aces have point values that depend
    on the :class:`Hand`.

    **Collaborators**

    Collected in a :class:`Deck`;
    collected into :class:`Hand` instances for each :class:`Player`;
    collected into a :class:`Hand` for the dealer; added to by
    :class:`Game`.

:Deck:
    **Responsibilities**

    A complete set of 52 standard :class:`Card` instances.

    **Collaborators**

    Used by the :class:`Game` to contain :class:`Card` instances.

:Hand:
    **Responsibilities**

    A collection of
    :class:`Card` instances with one or two point values: a hard value (an ace
    counts as 1) and a soft value (an ace counts as 11). The house will
    reveal one :class:`Card` to the player.

    **Collaborators**

    A :class:`Player`
    may have 1 or more :class:`Hand` instances; a :class:`Hand` has 2 or
    more :class:`Card` instances. The :class:`Game` adds :class:`Card` instances
    to the :class:`Hand`. The :class:`Game` checks the number of
    cards, the point totals and the ranks of the cards to offer different
    bets. The :class:`Game` compares the point totals to resolve bets.

:Player:
    **Responsibilities**

    Places the initial ante
    :class:`Bet` instances, updates the stake with amounts won and lost. Accepts
    or declines offered additional bets, including insurance, and split.
    Accepts or declines offered resolution, including even money. Chooses
    among hit, double and stand options.

    **Collaborators**

    Uses :class:`Table`,
    and one or more :class:`Hand` instances. Examines the dealer's
    :class:`Hand`. Used by game to respond to betting offers. Used by
    :class:`Game` to record wins and losses.

:Game:
    **Responsibilities**

    Runs the game: offers bets
    to :class:`Player`, deals the :class:`Cards` from the
    :class:`Deck` to :class:`Hand` instances, updates the state of the game,
    collects losing bets, pays winning bets. Splits :class:`Hand` instances.
    Responds to player choices of hit, double and stand. This encapsulates
    the basic sequence of play into a single class.

    **Collaborators**

    Uses
    :class:`Deck`, :class:`Table`, :class:`Outcome`,
    :class:`Player`.

..  _`blackjack.solution.proc`:

A Walkthrough
-------------

The unique, new feature of Blackjack is the more sophisticated
collaboration between the game and the player. This interaction involves
a number of offers for various bets, and bet resolution. Additionally,
it includes offers to double, hit or stand. We'll examine parts of a
typical sequence of play to assure ourselves that we have all of the
necessary collaborations and responsibilities.

A good way to structure this task is to do a CRC walk-through.
For more information on this technique see :ref:`roul.solution.walkthrough`.
We'll present the overall sequence of play, and leave it to the
student to manage the CRC walk-through.

..  rubric:: Typical Blackjack Game

1.  **Place Bets**.
    The Game will ask the Player to place a bet. If the player doesn't place
    a bet, the session is over.


2.  **Create Hands**.
    The Game will deal two cards to the Player's initial Hand.

    The Game will create an initial hand of two cards for the dealer. One of
    the cards is the up card, and is visible to the player.

#.  **Insurance?**
    The Game gets the Dealer's Hand's up card. If it is an Ace, then
    insurance processing is perforemed.

    #.  **Offer Even Money**.
        The Game examines the Player's hand for two cards totalling a soft 21,
        blackjack. If so, the Game offers the Even Money resolution to the
        Player. If the player accepts, the entire game is resolved at this
        point. The ante is paid at even money; there is no insurance bet.

    #.  **Offer Insurance**.
        The Game offers insurance to the Player, who can accept by creating a
        bet. For players with blackjack, this is a second offer after even money
        is declined. If the player declines, there are no further insurance considerations.

    #.  **Examine Hole Card**.
        The Game examines the Dealer's Hand's hole card. If is is a 10-point
        value, the insurance bet is resolved as a winner, the ante is resolved
        as a loser, and for this player, the game is over. Otherwise the
        insurance is resolved as a loser, the hole card is not revealed, and
        play will continue. Note that in a casino with multiple players, it is
        possible for a player declining insurance to continue to play with the
        dealer's hole card revealed. For casinos that offer "early surrender"
        this is the time to surrender.


#.  **Split?**
    The Game examines the Player's Hand to see if the two cards are of equal
    rank. If so, it offers a split. The player accepts by creating an
    additional Bet. The original hand is removed; The Game splits the two
    original Cards then deals two additional Cards to create two new Hands.

    Some casinos prevent further splitting, others allow continued splitting
    of the resulting hands.


#.  **Play Out Player Hands**.
    The following are done to play out each of the Player's Hands.

    #.  **Bust? Double? Hit? Stand?**
        While the given Hand is under 21 points, the Game must extend three
        kinds of offers to the Player. If the Player accepts a Hit, the hand
        gets another card and this process repeats.

        If the Player accepts Double Down, the player must create an additional
        bet, and the hand gets one more card and play is done. If the Player
        Stands Pat, the play is done. If the hand is 21 points or over, play is done.

    #.  **Resolve Bust**.
        The Game must examine each Hand; if it is over 21, the Hand is resolved
        as a loser.

#.  **Play Out Dealer Hand**.
    The Game then examines the Dealer Hand and deals Cards on a point value
    of 16 or less, and stops dealing Cards cards on point value of 17 or more.

    #.  **Dealer Bust?**
        The Game then examines the Dealer Hand to see if it is over 21. If so,
        the player's bets are resolved as winners. Player Hands with two cards
        totalling 21 ( "blackjack" ) are paid 3:2, all other hands are
        paid 1:1.

#.  **Compare Hands**.
    For each hand still valid, the Game compares the Player's Hand point
    value against the Dealer's Hand point value. Higher point value wins. In
    the case of a tie, it is a push and the bet is returned.

    When the Player wins, a winning hand with two cards totalling 21 ("blackjack")
    is paid 3:2, any other winning hand is paid 1:1.

Blackjack Solution Questions and Answers
-----------------------------------------

Will we really need both :class:`Deck` and the multiple deck :class:`Shoe`?
Wouldn't it be simpler to combine this functionality into a single class?

    There are two separate responsibilities here. The deck owns the basic
    responsibility to build the 52 cards. The shoe, on the other hand, owns
    the responsibility to deal cards to hands without dealing all of the
    available cards. Typically, 52 to 104 cards are held back from play.


    We want to be able to simulate games with 1 to 8 decks. A single deck
    game can simply deal directly from the deck. In a multi-deck game, all
    of the decks are shuffled together and loaded into a small box (called a "shoe")
    for dealing. The difference between one deck and a five-deck shoe is
    that the shoe can produce 20 kings in a row. While rare, our simulation
    does need to cover situations like this.


    Also, we may want to build a slightly different shoe that simulates the
    continuous shuffling machine that some casinos use. In this case, each
    hand is reshuffled back into the shoe, preventing any attempt at card
    counting. We don't want to disturb the basic, common deck when
    introducing this additional feature.


Won't all those player interactions break our design?

    That's unlikely. All of the player interactions are in addition to the :meth:`placeBets`
    interface. Since we've separated the core features of all players from
    the game-specific features, we can add a subclass to player that will be
    handle the Blackjack interaction. This new player subclass will have a
    number of additional methods to handle insurance, even money, split and
    the regular play questions of hit, double and stand.


    In parallel, we've separated the core features of all games from the
    unique features for a specific game. We can now add a subclass for
    Blackjack which adds a number of methods to offer insurance, even money,
    split and the regular play questions of hit, double and stand to the
    Blackjack player.


I can't find an Outcome in Blackjack. Is it the Ante? If so, the odds
vary based on the player's Hand, but that doesn't seem to be a RandomEvent.


    Good point. We'll examine this in detail in the exercises. Clearly, the
    bets are placed on the Ante and Insurance as the two core :class:`Outcome` objects
    in Blackjack. The Insurance outcome (really a "dealer has blackjack"
    outcome) is fixed at :math:`2:1`. The ante payoff depends on a complex condition
    of the hand: for a soft 21, or blackjack, it pays :math:`3:2`; otherwise it pays
    1:1. This will lead to a new subclass of the :class:`Outcome` class that
    collaborates with the hand to determine the payout to use.


    The "even money" is offered before ordinary insurance to a player
    with blackjack. It, however, pays even money on the ante, and doesn't
    create a new bet; in this respect it could be thought of as a change in
    the outcome on which the ante bet is created. Accepting the even money
    offer is a little bit like moving the ante to a "even money for
    dealer blackjack" outcome, which has 1:1 odds instead of :math:`3:2` odds.
    Further, this special outcome is resolved before the dealer peeks at
    their hole card. Perhaps this is a special best resolution procedure,
    not a proper instance of the :class:`Outcome` class.

Looking Forward
---------------

The first part of the design for Blackjack requires a design for handling
cards, and the randomizer subclasses that model the deck and the dealering shoe.
We'll look at all of these closely-related classes in the next chapter.

