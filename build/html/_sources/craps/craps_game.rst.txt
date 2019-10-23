
..  _`craps.game`:

CrapsGame Class
================

In :ref:`craps.throw`, we roughed out a stub version of :class:`CrapsGame`
that could be used to test :class:`Throw`. We extended that stub in :ref:`craps.table`.
In this chapter, we will revise the game to provide the complete
process for Craps. This involves a number of features, and we will have
a state hierarchy as well as the Game class itself.

In the process of completing the design for the :class:`CrapsGame` class, we
will uncover another subtlety of craps: winning bets and losing bets.
Unlike Roulette, where a :class:`Bin` contained winning :class:`Outcome` instances
and all other :class:`Outcome` instances where losers, Craps includes winning
:class:`Outcome` instances, losing :class:`Outcome` instances, and unresolved :class:`Outcome` instances.
This will lead to some rework of previously created Craps classes.

In `Craps Game Analysis`_ we'll examine the game of craps in detail.
We'll look at four topics:

-   `Game State`_ will address how the game transitions between point
    on and point off states.

-   `The Game State Class Hierarchy`_ will look at the **State** design
    pattern and how it applies here.

-   In `Resolving Bets`_ we'll look at how game, table, and player collaborate
    to resolved bets.

-   In `Movable Bets`_ we'll look at how the game collaborates with
    bets like the Pass Line bet which have an outcome that moves.

In `Design Decision -- Win, Lose, Wait`_ we'll look at bet payoff issues.

In `Additional Craps Design`_ we'll revisit our algorithm for building
:class:`Outcome` instances and :class:`Throw` instances and creating the :class:`Dice`.

This chapter involves a large amount of programming. We'll detail
this in `Craps Game Implementation Steps`_.

We'll look at preliminary rework in a number of sections:

-   `Throw Rework`_,

-   `ThrowBuilder Rework`_, and

-   `Bet Rework`_.

Once we've cleaned up the :class:`Throw` and :class:`Bet` classes, we
can focus on new development for the Craps game.

In `CrapsPlayer Class Stub`_ we'll rough out a design for a player.

We'll define the game states in the following sections:

-   `CrapsGameState Class`_ will address the superclass,

-   `CrapsGamePointOff Class`_ will look at the point off state, and

-   `CrapsGamePointOn Class`_ will look at the point on state.

In `CrapsGame Design`_ we'll define the overall game class. We'll
enumerate the deliverables for this chapter in `Craps Game Deliverables`_.

We'll look at some additional game design issues in `Optional Working Bets`_.

Craps Game Analysis
-------------------

Craps is considerably more complex than Roulette. As noted in :ref:`craps.details`,
there is a multi-step procedure that involves state changes, multiples rounds
of betting, and bets that move from generic ("Come" or "Pass Line") to specific
numbers based on the current :class:`Throw` instance.

We can see several necessary features to the :class:`CrapsGame`:

-   `Game State`_,

-   `The Game State Class Hierarchy`_,

-   `Resolving Bets`_, and

-   `Movable Bets`_ when a point is established.

Also, we will discover some additional design features to add to other classes.

..  _`craps.game.algorithm`:

Game State
~~~~~~~~~~

A :class:`CrapsGame` object cycles through the various steps of the
Craps game; this sequence is shown in :ref:`craps.game.algorithm`.
Since we will follow the :strong:`State` design pattern, we have three
basic design decisions. First, we have to design the state class
hierarchy to own responsibilities for the unique processing present in each of the
individual states. Second, we have to design an interface for the game
state objects to interact with the overall :class:`CrapsGame`.
Third, we will need to keep an object in the :class:`CrapsGame`
which contains the current state. Each throw of the dice will update the
state, and possibly resolve game bets. To restart the game, we can
create a fresh object for the initial point-off state.


The following procedure provides the detailed algorithm for the game of Craps.

..  rubric:: A Single Game of Craps

**Point Off State**.
The first throw of the dice is made with no point.  This game may
be resolved in a single throw of the dice, no point will be established.
If a point is established the game transitions to the **Point On State**.

    1.  **Place Bets**.
        The point is off; this is the come out roll. Notify the :class:`Player` instance
        to create :class:`Bet` instances. The real work of placing bets is delegated
        to the :class:`Player` class. Only Pass and Don't Pass bets will be
        allowed by the current game state.

    2.  **Odds Bet Off?**
        Optional, for some casinos only. For any odds bets behind a come point,
        interrogate the player to see if the bet is on or off. These bets were
        unresolved because the previous game ended in a winning point.

    3.  **Come-Out Roll**.
        Get the next throw of the :class:`Dice` object, giving the winning :class:`Throw` instance,
        :emphasis:`t`. The :class:`Throw` object contains the individual :class:`Outcome` instances
        that can be resolved on this throw.

    #.  **Resolve Proposition Bets**.
        For each :class:`Bet` object, :emphasis:`b`, placed on a one-roll proposition:

        ..  _`craps.game.algorithm.proposition`:

        -   **Proposition Winner?**
            If :class:`Bet` :emphasis:`b`'s :class:`Outcome` instance is in the winning
            :class:`Throw`, :emphasis:`t`, then notify the :class:`Player` object that
            :class:`Bet` :emphasis:`b` was a winner.  Update the :class:`Player`
            object's stake. Note that the odds paid for winning field bets and horn bets
            depend on the :class:`Throw` object.

        -   **Proposition Loser?**
            If :class:`Bet` :emphasis:`b`'s :class:`Outcome` is not in the winning
            :class:`Throw`, :emphasis:`t`, then notify the :class:`Player` that
            :class:`Bet` :emphasis:`b` was a loser. This allows the :class:`Player`
            to update their betting amount for the next round.


    #.  **Natural?**
        If the throw is a 7 or 11, this game is an immediate winner. The game
        state must provide the Pass Line :class:`Outcome` instance as a winner.

        For each :class:`Bet`, :emphasis:`b`:

        -   **Come-Out Roll Natural Winner?**
            If :class:`Bet` :emphasis:`b`'s :class:`Outcome` instance is in the
            winning game state, then notify the :class:`Player` object that :class:`Bet`
            :emphasis:`b` was a winner and update the :class:`Player` object's stake.
            The :class:`Throw` instance will contain outcomes to make sure
            a Pass Line bet is a winner, and a Don't Pass bet is a loser.

        -   **Come-Out Roll Natural Loser?**
            If :class:`Bet` :emphasis:`b`'s :class:`Outcome` instance is not in the
            winning game state, then notify the :class:`Player` object that :class:`Bet`
            :emphasis:`b` was a loser. This allows the :class:`Player` object to update
            the betting amount for the next round. A Pass Line bet is a loser, and a
            Don't Pass bet is a winner.

    #.  **Craps?**
        If the throw is a 2, 3, or 12, this game is an immediate loser. The game
        state must provide the Don't Pass Line :class:`Outcome` instances as a winner;
        note that 12 is a push in this case, requiring special processing by the :class:`Bet`
        or the :class:`Outcome`: the bet amount is simply returned.

        For each :class:`Bet`, :emphasis:`b`:

        a.  **Come-Out Roll Craps Winner?**
            If :class:`Bet` :emphasis:`b`'s :class:`Outcome` instance is in the
            winning game state and the bet is working, then notify the :class:`Player` object
            that :class:`Bet` :emphasis:`b` was a winner and update the :class:`Player` object's
            stake. If the bet is not working, it is ignored.

        b.  **Come-Out Roll Craps Loser?**
            If :class:`Bet` :emphasis:`b` 's :class:`Outcome` instance is not in the
            winning game state and the bet is working, then notify the :class:`Player` object
            that :class:`Bet` :emphasis:`b` was a loser. If the bet is not
            working, it is ignored.

    #.  **Point Established**.
        If the throw is a 4, 5, 6, 8, 9 or 10, a point is established. The game
        state changes, to reflect the point being on. The Pass Line and Don't
        Pass Line bets have a new :class:`Outcome` instance assigned to them, based on the point.

**Point On State**.
While the game remains unresolved, the following steps are performed.
The game will be resolved when the point is made or a natural is thrown.

    1.  **Place Bets**.
        Notify the player to place any additional bets. In this game state all
        bets are allowed.

    2.  **Point Roll**.
        Get the next :class:`Throw` instance from the :class:`Dice` object.

    3.  **Resolve Proposition Bets**.
        Resolve any one-roll proposition bets. This is the procedure described
        above for iterating through all one-roll propositions. See :ref:`Resolve Proposition Bets <craps.game.algorithm.proposition>`.

    4.  **Natural?**
        If the throw was 7, the game is a loser. Resolve all bets; the game
        state will show that all bets are active. The game state will include
        Don't Pass and Don't Come bets as winners, as will any of the six point
        bets created from Don't Pass and Don't Come Line bets. All other bets
        will lose, including all hardways bets.

        This throw resolves the game, changing the game state: the point is off.

    5.  **Point Made?**
        If the throw was the main game point, the game is a winner. Resolve Pass
        Line and Don't Pass Line bets, as well as the point and any odds behind
        the point.

        Come Point and Don't Come Point bets (and their odds) remain for the
        next game. A Come Line or Don't Come Line bet will be moved to the
        appropriate Come Point.

        This throw ends the game, changing the game state.
        The point is off; odds placed behind Come Line
        bets are not working for the come out roll.

    6.  **Other Point Number?**
        If the throw was any of the come point numbers, come bets on that point
        are winners. Resolve the point come bet and any odds behind the point.
        Also, any buy or lay bets will be resolved as if they were odds bets
        behind the point; recall that the buy and lay bets involved a
        commission, which was paid when the bet was created.

    7.  **Hardways?**
        For 4, 6, 8 and 10, resolve hardways bets. If the throw was made the
        hard way (both dice equal), a hardways bet on the thrown number is a
        winner. If the throw was made the easy way, a hardways bet on the thrown
        number is a loser. If the throw was a 7, all hardways bets are losers.
        Otherwise, the hardways bets remain unresolved.


The Game State Class Hierarchy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have identified some processing that is
unique to each game state. Both states will have a list of
allowed bets, a list of non-working bets, a list of throws
that cause state change and resolve game bets, and a list of throws that resolve
hardways bets.

In the Craps Table (:ref:`craps.table.ov`), we allocated some
responsibilities to the :class:`CrapsGame` class so that a :class:`CrapsTable` instance
could validate bets and determine which bets were
working.

Our further design details have shown that the work varies by game state.
Therefore, the methods in the :class:`CrapsGame` class
will delegate the real work to each state's methods. The current
stub implementation checks the value of the :obj:`point` variable to
determine the state. We'll replace this with a call to an appropriate
method of the current state object.

**State Responsibilities**.
Each :class:`CrapsGameState` subclass, therefore, will have an :meth:`isValid`
method that implements the state-specific bet validation rules. In this case, a
point-off state object only allows the two Pass Line bets: Pass Line,
Don't Pass Line. The point-on state allows all bets. Additionally, we've
assigned to the :class:`CrapsTable` class the responsibility to determine if the total
amount of all a player's bets meets or exceeds the table limits.

Each subclass of the :class:`CrapsGameState` class will override an :meth:`isWorking`
method with one that validates the state-specific rules for the working
bets. In this case, a point-off state object will identify the the six
odds bets placed behind the come point numbers (4, 5, 6, 8, 9 and 10) as
non-working bets, and all other bets will be working bets. A point-on
state object will simply identify all bets as working.

The subclasses of the :class:`CrapsGameState` class will need methods with
which to collaborate with a :class:`Throw` object to update the
state of the current :class:`CrapsGame` instance.

**Changing Game State**. We have identified two game states: point-off
(also know as the come out roll) and point-on. We have also set aside
four methods that the various :class:`Throw` objects will use to
change the game state. The interaction between the :class:`CrapsGame` class,
the four kinds of :class:`Throw` subclasses and the two subclasses of :class:`CrapsGameState` instances works as follows:

#.  There are 36 instances of :class:`Throw`,
    one of which was selected at random to be the current throw of the dice.

    The :class:`CrapsGame` object calls the :class:`Throw` object's :meth:`updateGame`
    method.  Each of the subclasses of :class:`Throw` have different implementations for this method.

#.  The :class:`Throw` object calls back to one of the :class:`CrapsGame` object's
    methods to change the state. There are four methods available: :meth:`craps`,
    :meth:`natural`, :meth:`eleven`, and :meth:`point`.
    Different subclasses of the :class:`Throw` class will call an appropriate
    method for the kind of throw.

#.  The :class:`CrapsGame` object has a current state, embodied in a :class:`CrapsGameState`
    object.  The game will delegate each of the four state change
    methods (:meth:`craps`, :meth:`natural`, :meth:`eleven`,
    and :meth:`point`) to the current :class:`CrapsGameState`
    object.

#.  In parallel with :class:`CrapsGame` class, each :class:`CrapsGameState`
    subclass has four state change methods (:meth:`craps`, :meth:`natural`,
    :meth:`eleven`, and :meth:`point`). Each state
    provides different implementations for these methods. In effect, the
    two states and four methods create a kind of table that enumerates
    all possible state change rules.

**Complex?**
At first glance the indirection and delegation seems like a lot of
overhead for a simple state change. When we consider the kinds of
decision-making this embodies, however, we can see that this is an
effective solution.

When one of the 36 available :class:`Throw` instances
has been chosen, the :class:`CrapsGame` instance calls a single method to
update the game state. Because the various subclasses of the :class:`Throw` class
are polymorphic, they all respond with unique, correct behavior based on state.

Similarly, each of the subclasses of the :class:`Throw` class use one
of four methods to update the :class:`CrapsGame` object, without having to
discern the current state of the game. We can consider the
:class:`CrapsGame` class as a kind of façade over the methods of the polymorphic
:class:`CrapsGameState` subclasses. Our objective is to do the decision-making
once when the object is created; this makes all subsequent processing
free of complex if-based decision-making.

What's important about this design is that there are no if-statements
required to make it work.  Instead, objects simply invoke methods.

..  _`craps.game.resolve`:

Resolving Bets
~~~~~~~~~~~~~~

The :class:`CrapsGame` class also has the responsibility for
matching the :class:`Outcome` instances in the current :class:`Throw` object
with the :class:`Outcome` instances of the :class:`Bet` instances held by the :class:`CrapsTable` object.

In addition to matching :class:`Outcome` instances in the :class:`Throw` object,
we also have to match the :class:`Outcome` instances of the current game
state.

Finally, the :class:`CrapsGame` class must also resolve hardways bets, which are
casually tied to the current
game state. We'll look at each of these three resolution procedures in
some detail before making any final design decisions.

-   **Resolving Bets on Proposition Outcomes**. We'll need a bet resolution
    method that handles one-roll propositions. This is similar to the bet
    resolution in the Roulette game class. The current :class:`Throw` instance
    contains a collection of :class:`Outcome` instances which are resolved as
    winners. All other :class:`Outcome` instances will be losers. While appropriate
    for the one-roll propositions, we'll see that this doesn't generalize for
    other kinds of bets.

-   **Resolving Bets on Game Outcomes**. The second, and most complex, bet
    resolution method handles game outcomes. Bets on the game as a whole
    have three groups of :class:`Outcome` instances: winners, losers and
    unresolved.

    This "unresolved" outcome is fundamentally different from Roulette
    bet resolution and proposition bet resolution.

    Consider a Pass Line bet: in the point-off state, a roll of
    7 or 11 makes this bet a winner, a roll of 2, 3 or 12 makes this bet a
    loser, all other numbers leave this bet unresolved. After a point is
    established, this Pass Line bet has the following resolutions: a roll of
    7 makes this bet a loser, rolling the point makes this bet is a winner,
    all other numbers leave this bet unresolved.

    In addition to this three-way decision, we have the additional subtlety
    of Don't Pass Line bets that can lead to a fourth resolution: a push
    when the throw is 12 on a come out roll. We don't want to ignore this
    detail because it changes the odds by almost 3%.

-   **Resolving Hardways Bets**.
    We have several choices for implementation of this multi-way decision.  This
    is an overview, we'll dive into details below.

    -   We can keep separate collections of winning and losing :class:`Outcome` instances
        in each :class:`Throw` object. This will obligate the game to check
        a set of winners and a set of losers for bet resolution. Other :class:`Outcome` instances
        can remain unresolved.

    -   We can add a method to the :class:`Bet` class that will return a
        code for the effect of a win, lose, or wait for each :class:`Outcome` instance.
        A win would add money to the :class:`Player` object's stake;
        a lose would subtract money from the :class:`Player` object.
        This means that the game will have to decode this win-lose response as part
        of bet resolution.

    -   We can make each kind of resolution into a **Command** class.  Each
        subclass of :class:`BetResolution` would perform the "pay a winner",
        "collect a loser" or "leave unresolved" procedure based on the :class:`Throw` instance
        or class:`CrapsGameState` object.


Movable Bets
~~~~~~~~~~~~~~

In the casino, the Come (and Don't Come) Line bets start on the given
line. If a come point is established, the come line bet is moved to a
box with the point. When you add behind the line odds bets, you place the
chips directly on the numbered box for the Come Point number.

This procedure is different from the Pass (and Don't Pass) Line bet. The bet is is
placed on the line. If a point is established, a large white "On" token shows
the numbered box where, in effect, the behind the line odds chips belong.

Note that the net effect of both bets is identical.  The pass line and behind-the-line odds bets
have a payout that depends on the "On" token.  The come line bets are moved and odds a place in a
box on which the payout depends.

One of the things the :class:`CrapsGame` class does is change the :class:`Outcome` instance
of the Come and Don't Come Line bets. If a Come or Don't Come Line bet is placed and the throw
is a point number (4, 5, 6, 8, 9, or 10), the bet is not resolved on the first
throw; it is moved to one of the six point number :class:`Outcome` instances.

When designing the :class:`Bet` class, in the
Craps Bet section (:ref:`craps.bet.ov`,) we recognized the need to change the :class:`Outcome` instance
from a generic "Pass Line Odds" to a specific point with specific
odds of :math:`2:1`, :math:`3:2`, or :math:`6:5`.

We'll develop a :meth:`moveToThrow` method that accepts a :class:`Bet` object
and the current :class:`Throw` instance so it can move the bet to the new
:class:`Outcome` instance.

In addition to moving bets, we also need to create bets based on
the currently established point.  We also need to deactivate bets
based on the established point.

As an example, the Pass Line Odds and Don't Pass Odds are created after the point is
established. Since the point is already known, creating these bets is
best done by adding a :meth:`CrapsGame.pointOutcome` method
that returns an :class:`Outcome` instance based on the current point. This
allows the :class:`CrapsPlayer` object to get the necessary :class:`Outcome`
object, create a :class:`Bet` instance and give that :class:`Bet` instance to the :class:`CrapsTable` object.


Design Decision -- Win, Lose, Wait
----------------------------------

Bet resolution in Craps is more complex than simply paying winners
and collecting all other bets as losers.  In Craps, bets can be winners, losers
or unresolved.  Further, some bets have a "push" resolution in which
only the original price of the bet is returned.  This is a kind of :math:`1:1` odds
special case.

**Problem**.  What's the best way to retain a collection
of :class:`Outcome` instances that are resolved as a mixture of winning, losing, unresolved, and
pushes.

Note that if we elect to introduce a more complex multi-way bet resolution, we
have to decide if we should re-implement the bet resolution in Roulette.
Using very different bet resolution algorithms for Craps and Roulette
doesn't seem appealing. While a uniform
approach is beneficial, it would involve some rework of the Roulette
game to work correctly in spite of a more sophisticated design.

**Alternatives**.
We'll look at three alternative responsibility assignments in some depth.

-   **Winning and Losing Collections**.

-   **Winning and Losing Status Codes**.

-   **Wining and Losing Command Objects**.

Each of these is a profoundly different way to assign responsibilities.

**Winning and Losing Collections**. We could expand the :class:`Throw` class to keep separate
collections of winners and losers.  We could expand the :class:`CrapsGameState` class
to detail the winning and losing
:class:`Outcome` instances for each state. All other :class:`Outcome` instances
would be left unresolved.

This is a minor revision to the :class:`Dice` and
:class:`Throw` classes to properly create the two groups of :class:`Outcome` instances.
Consequently :class:`ThrowBuilder` class will have to be expanded to
identify losing :class:`Outcome` instances in addition to the existing winning
:class:`Outcome` instances.

This will also require the :class:`CrapsGame` class to make
two passes through the bets.  It must match all active :class:`Bet` instances
on the table against the winning :class:`Outcome` instances
in the current state; the matches are paid a
winning amount and removed. It must also match match all active :class:`Bet` instances
on the table against the losing :class:`Outcome` instances
in the current state; these are removed as losers.

**Winning and Losing Codes, Evaluated by CrapsGame**. We could
enumerate three code values that represent actions to take:  these actions
are "win", "lose", and "unresolved".
The class :class:`CrapsGame` and
each subclass of :class:`GameState` would have a resolution method that examines a :class:`Bet` and
returns the appropriate code value.

This is a minor revision to :class:`Dice` and
:class:`Throw` to properly associate a special code with each :class:`Outcome`.
Consequently :class:`ThrowBuilder` will have to be expanded to
identify losing :class:`Outcome` instances in addition to the existing winning :class:`Outcome` instances.

Each `GameState` would also need to respond with appropriate codes.

This will require the :class:`CrapsGame` to make one pass through the
:class:`Bet` instances, passing each
each bet to the :class:`GameState` resolution method.  Based on the
code returned, the :class:`CrapsGame` would then have an if-statement to decide
to provide bets to the :meth:`Player.win` or :meth:`Player.lose` method.

**Wining and Losing Commands**.  We could define a hierarchy of three subclasses.
Each subclass implements
winning, losing or leaving a bet unresolved.

This is a minor revision to :class:`Dice` and
:class:`Throw` to properly associate a special object with each :class:`Outcome`.
We would create
single objects of each resolution subclass.
The :class:`ThrowBuilder` will have to be expanded to
associate the loser Command or winner command with each :class:`Outcome`.
Further, the unresolved Command would have to be associated with all `Outcome` instances
that are not resolved by the `Throw` or `GameState`.

This will require the :class:`CrapsGame` to make one pass through the
:class:`Bet` instances, using the associated resolution object.  The resolution
object would then handle winning, losing and leaving the bet unresolved.


Before making a determination, we'll examine the remaining bet
resolution issue to see if a single approach can cover single-roll, game
and hardways outcomes.

**Resolving Bets on Hardways Outcomes**. In addition to methods to resolve
one roll and game bets, we have to resolve the hardways bets. Hardways
bets are similar to game bets. For :class:`Throw` instances of 4, 6, 8 or 10
there will be one of three outcomes:

-   when the number is made the hard way, the matching hardways bet is a winner;

-   when the number is made the easy way, the matching hardways bet is a loser;
    otherwise the hardways bet is unresolved;

-   on a roll of seven, all hardways bets are losers.

Since this parallels the game rules, but applies to an individual :class:`Throw` object,
it leads us to consider the design of the :class:`Throw` class to be
parallel to the design of the :class:`CrapsGame` class. We can use either a
collection of losing :class:`Outcome` instances in addition to the
collection of winning :class:`Outcome` instances, or create a multi-way
discrimination method, or have the :class:`Throw` class call appropriate
methods of :class:`CrapsTable` object to resolve the bet.

**Solution**. A reasonably flexible design for bet
resolution that works for all three kinds of bet resolutions is to have the :class:`Throw`
and :class:`CrapsGameState` classes call specific bet resolution methods in the :class:`CrapsPlayer` class.

This unifies one-roll, game and hardways bets into a single mechanism.
It requires us to provide methods for win, lose and push in the :class:`CrapsPlayer` class.
We can slightly simplify this to treat a push as a kind of win that
returns the bet amount.

**Consequences**.
The :class:`CrapsGame` class will iterate through the active :class:`Bet` instances.
Each :class:`Bet` object and the :class:`Player` object will be provided to
the current :class:`Throw` instance for resolving one-roll and hardways bets. Each
:class:`Bet` object and the :class:`Player` object will also be provided to
the :class:`CrapsGameState` instance to resolve the winning and losing game bets.

We can further simplify this if each :class:`Bet` object carries a reference to the owning :class:`Player`.
In this way, the :class:`Bet` object has all the information necessary to
notify the :class:`Player` instance of the outcome.

In the long run, this reflects the reality of Craps table where the table
operators assure that each bet has an owning player.


Additional Craps Design
-------------------------

We will have to rework our design for the :class:`Throw` class to have both a
one-roll resolution method and a hardways resolution method. Each of
these methods will accept a single active :class:`Bet` instance.
Each resolution method could use a set of winner :class:`Outcome` instances
and a set of loser :class:`Outcome` instances to attempt to resolve the bet.

We will also need to rework our design for the :class:`Dice` class to
correctly set both winners and losers for both one-roll and hardways bets
when constructing the 36 individual :class:`Throw` instances.

We can use the following expanded algorithm for building the :class:`Dice` collection
of :class:`Throw` instances.
This is a revision to :ref:`craps.throwbuilder.ov` to include
lists of losing bets as well as winning bets.


..  rubric:: Building Dice With Winning and Losing Outcomes

**For All Faces Of Die 1**. For all :math:`d_1`, such that :math:`1 \leq d_1 < 7`:

    **For All Faces Of A Die 2**. For :math:`d_2`, such that :math:`1 \leq d_2 < 7`:

        **Sum the Dice**. Compute the sum, :math:`s \gets d_1 + d_2`.

        **Craps?** If :emphasis:`s` is in 2, 3, and 12, we create a :class:`CrapsThrow`
        instance. The winning bets include one of the 2, 3 or 12 number :class:`Outcome` objects,
        plus all craps, horn and field :class:`Outcome` instances. The losing bets include the other number
        :class:`Outcome` instances. This throw does not resolve
        hardways bets.

        **Point?** For :emphasis:`s` in 4, 5, 6, 8, 9, and 10 we will create a :class:`PointThrow`
        instance.

            **Hard way?** When  :math:`d_1 = d_2`,
            this is a :emphasis:`hard` 4, 6, 8 or 10. The appropriate hard number :class:`Outcome` object
            is a winner.

            **Easy way?**  Otherwise, :math:`d_1 \ne d_2`, this is an :emphasis:`easy` 4, 6, 8 or 10. The
            appropriate hard number :class:`Outcome` object is a loser.

        **Field?** For :emphasis:`s` in 4, 9 and 10 we include the field :class:`Outcome` object
        as a winner. Otherwise the field :class:`Outcome` object is a loser.
        Note that 2, 3, and 12 Field outcomes where handled above under **Craps**.

        **Losing Propositions**. Other one-roll :class:`Outcome` instances, including
        2, 3, 7, 11, 12, Horn and Any Craps :class:`Outcome` instances are all losers.

        **Natural?** If :emphasis:`s` is 7, we create a :class:`NaturalThrow`
        instance. This will also include a 7 :class:`Outcome` object as a winner.
        It will have numbers 2, 3, 11, 12, Horn, Field and Any Craps :class:`Outcome` instances  as
        losers. Also, all four hardways are losers for this throw.

        **Eleven?** If :emphasis:`s` is 11, we create an :class:`ElevenThrow`
        instance. This will include 11, Horn and Field :class:`Outcome` instances as
        winners. It will have numbers 2, 3, 7, 12 and Any Craps :class:`Outcome` instances as losers.
        There is no hardways resolution.


**Craps Player Class Hierarchy**. We have not designed the actual :class:`CrapsPlayer` class yet.
This is really a complete tree of classes, each of which provides a
different betting strategy. We will defer this design work until later.
For the purposes of making the :class:`CrapsGame` class, we can
develop our unit tests with a kind of stub for the :class:`CrapsPlayer` class
which simply creates a single Pass Line :class:`Bet` instance. In several
future exercises, we'll revisit this design to make more sophisticated players.

See :ref:`craps.game.ov.workingbets` for a further discussion on an
additional player decision offered by some variant games. Our design can
be expanded to cover this. We'll leave this as an exercise for the more
advanced student. This involves a level of collaboration between the :class:`CrapsPlayer`
and :class:`CrapsGame` classes that is over the top for this part. We'll
address this kind of very rich interaction in :ref:`blackjack`.


Craps Game Implementation Steps
----------------------------------

We have identified the following things that must be done to
implement the craps game.

1.  Change the :class:`Throw` class to include both winning and losing :class:`Outcome` instances

2.  Once we have fixed the :class:`Throw` class,
    we can update the :class:`ThrowBuilder` class to do a correct
    initialization using both winners and losers. Note that we have
    encapsulated this information so that there is no change to the :class:`Dice` class.

3.  We will also update the :class:`Bet` class to carry a reference to the :class:`Player` class
    to make it easier to post winning and losing information directly to the
    player object.

4.  We will need to create a stub :class:`CrapsPlayer` class for testing purposes.

5.  We will also need to create our :class:`CrapsGameState` class
    hierarchy to represent the two states of the game.

6.  Once the preliminary work is complete, we can then transform the :class:`CrapsGame` class
    we started in :ref:`craps.game.stub`
    into a final version. This will collaborate
    with a :class:`CrapsPlayer` instance and maintain a correct :class:`CrapsGameState` object.
    It will be able to get a random :class:`Throw` object and resolve :class:`Bet` instances
    on the :class:`CrapsTable`.

We'll address each of these separately.

Throw Rework
------------

The :class:`Throw` cass is the superclass for the various throws of the dice.
A :class:`Throw` instance identifies two sets of :class:`Outcome` instances:
immediate winners and immediate losers. Each subclass is a different
grouping of the numbers, based on the state-change rules for Craps.


Fields
~~~~~~~

..  attribute:: Throw.win1Roll

    A :class:`set` of of one-roll :class:`Outcomes` that win with this throw.

..  attribute:: Throw.lose1Roll

    A :class:`set` of one-roll :class:`Outcomes` that lose with this throw.

..  attribute:: Throw.winHardway

    A :class:`set` of hardways :class:`Outcomes` that win with this
    throw. Not all throws resolve hardways bets, so this and the
    loseHardway Set may both be empty.

..  attribute:: Throw.loseHardway

    A :class:`set` of hardways :class:`Outcomes` that lose with this
    throw. Not all throws resolve hardways bets, so this and the
    winHardway Set may both be empty.

..  attribute:: Throw.d1

    One of the two die values, from 1 to 6.

..  attribute:: Throw.d2

    The other of the two die values, from 1 to 6.


Constructors
~~~~~~~~~~~~~


..  method:: Throw.__init__(self, d1: int, d2: int, winners: Optional[Set[Outcome]]=None, losers: Optional[Set[Outcome]]=None) -> None

    :param d1: One die value.
    :type d1: int

    :param d2: The other die value.
    :type d2: int

    :param winners: All the outcomes which will be paid as winners for this Throw.
    :type winners: Optional[Set[:class:`Outcome`]]

    :param losers: All the outcomes which will be collected as winners for this Throw.
    :type winners: Optional[Set[:class:`Outcome`]]


    Creates this throw, and associates the two given sets of :class:`Outcome`
    instances that are winning one-roll propositions and losing one-roll propositions.


Methods
~~~~~~~


..  method:: Throw.add1Roll(self, winners: Set[Outcome], losers: Set[Outcome]) -> None

    :param winners: All the outcomes which will be paid as winners for this Throw.
    :type winners: Set[:class:`Outcome`]

    :param losers: All the outcomes which will be collected as winners for this Throw.
    :type winners: Set[:class:`Outcome`]


    Adds outcomes to the one-roll winners and
    one-roll losers Sets.



..  method:: Throw.addHardways(self, winners: Set[Outcome], losers: Set[Outcome]) -> None

    :param winners: All the outcomes which will be paid as winners for this Throw.
    :type winners: Set[:class:`Outcome`]

    :param losers: All the outcomes which will be collected as winners for this Throw.
    :type winners: Set[:class:`Outcome`]


    Adds outcomes to the hardways winners and hardways losers Sets.



..  method:: Throw.hard(self) -> bool


    Returns :literal:`True`
    if :obj:`d1` is equal to :obj:`d2`.

    This helps determine if
    hardways bets have been won or lost.



..  method:: Throw.updateGame(self, game: CrapsGame) -> None

    :param game: CrapsGame instance to be updated with the results of this throw
    :type game: :class:`CrapsGame`


    Calls one of the state change methods: :meth:`CrapsGame.craps`, :meth:`CrapsGame.natural`,
    :meth:`CrapsGame.eleven`, :meth:`CrapsGame.point`. This may change the
    game state and resolve bets.



..  method:: Throw.resolveOneRoll(self, bet: Bet) -> None

    :param bet: The bet to to be resolved
    :type bet: :class:`Bet`


    If this :class:`Bet` object's :class:`Outcome` instance is in the set of one-roll winners,
    pay the :class:`Player` object
    that created the :class:`Bet`. Return :literal:`True` so this
    :class:`Bet` can be removed.

    If this :class:`Bet` object's :class:`Outcome` instance is in the set of
    one-roll losers, return :literal:`True` so that this :class:`Bet` object
    is removed.

    Otherwise, return :literal:`False` to leave this :class:`Bet` object on
    the table.


..  method:: Throw.resolveHardways(self, bet: Bet) -> None

    :param bet: The bet to to be resolved
    :type bet: :class:`Bet`



    If this :class:`Bet` object's :class:`Outcome` instance is in the set of hardways winners,
    pay the :class:`Player` object
    that created the bet. Return :literal:`True` so that this
    :class:`Bet` is removed.

    If this :class:`Bet` object's :class:`Outcome` instance is in the set of
    hardways losers, return :literal:`True` so that this :class:`Bet` instance
    is removed.

    Otherwise, return :literal:`False` to leave this :class:`Bet` instance on
    the table.



..  method:: Throw.__str__(self) -> str


    This should
    return a string representation of the dice modeled by this :class:`Throw` instance.
    A form that looks like :literal:`"1,2"` works nicely.


ThrowBuilder Rework
--------------------

The :class:`ThrowBuilder` class initializes the 36 :class:`Throw` instances, each
initialized with the appropriate :class:`Outcome` instances. Subclasses can
override this to reflect different casino-specific rules for the variations of odds on
Field bets.


Methods
~~~~~~~~


..  method:: ThrowBuilder.buildThrows(self, dice: Dice) -> None

    :para dice: The Dice to initialize
    :type dice: :class:`Dice`


    Creates the 8 one-roll :class:`Outcome`
    instances (2, 3, 7, 11, 12, Field, Horn, Any Craps), as well as the
    8 hardways :class:`Outcome` instances (easy 4, hard 4, easy 6,
    hard 6, easy 8, hard 8, easy 10, hard 10).

    It then creates each of
    the 36 :class:`Throw` instances, each of which has the appropriate
    combination of :class:`Outcome` instances for one-roll and hardways.
    The various :class:`Throw` instances are assigned to :obj:`dice`.


Bet Rework
-----------

The :class:`Bet` class associates an amount, an :class:`Outcome` instance and a :class:`Player` instance.
The :class:`CrapsGame` class may move a :class:`Bet` instance to a different :class:`Outcome` instance
to reflect a change in the odds used to resolve the final bet.

This will change the underlying definition of the :class:`Bet` class
from immutable to mutable. The initial definition of this class relied
on either :class:`typing.NamedTuple` to ``@dataclass(frozen=True)``.
This revision is mutable, and ``@dataclass(frozen=False)`` is an appropriate
decoration for the :class:`Bet` class.

This can lead to rework in the Roulette definitions to add the :class:`Player` object
reference to each :class:`Bet` instance that's created. We can avoid the rework
if we make the :class:`Player` reference optional, this isn't a good idea in the
long run because it can become confusing.

Constructors
~~~~~~~~~~~~~~


..  method:: Bet.__init__(self, amount: int, outcome: Outcome, player: CrapsPlayer) -> None

    This replaces the existing constructor and adds
    an optional parameter.

    :param amount: The amount being wagered.
    :type amount: int

    :param outcome: The specific outcome on which the wager is placed.
    :type outcome: :class:`Outcome`

    :param player: The player who will pay a losing bet or be paid by a winning bet.
    :type player: :class:`CrapsPlayer`

    Initialize the instance variables of this bet.  This works by saving
    the additional player information.

..  _`craps.game.playerstub`:

CrapsPlayer Class Stub
-----------------------

The :class:`CrapsPlayer` class constructs a :class:`Bet` instance based on the :class:`Outcome` instance
named :literal:`"Pass Line"`. This is a very persistent player.


Fields
~~~~~~~~

..  attribute:: CrapsPlayer.passLine

    This is the :class:`Outcome` on which this player focuses their betting. It
    will be an instance of the :literal:`"Pass Line"` :class:`Outcome`,
    with 1:1 odds.

..  attribute:: CrapsPlayer.workingBet

    This is the current Pass Line :class:`Bet`.


    Initially this is :literal:`None`.
    Each time the bet is resolved, this is reset to :literal:`None`.


    This assures that only one bet is working at a time.

..  attribute:: CrapsPlayer.table

    That :class:`Table`  which collects all bets.


Constructors
~~~~~~~~~~~~~


..  method:: CrapsPlayer.__init__(self, table: Table) -> None

    :param table: The :class:`Table` for placing bets
    :type table: :class:`Table`


    Constructs the :class:`CrapsPlayer` instance with a specific table for
    placing bets. The player creates a single :literal:`"Pass Line"` :class:`Outcome` object,
    which is saved in the :obj:`passLine` variable for use in creating
    :class:`Bet` instances.



Methods
~~~~~~~


..  method::CrapsPlayer.placeBets(self) -> None


    If :obj:`workingBet` is :literal:`None`, create a new Pass Line :class:`Bet`, and use
    :class:`Table` :meth:`placeBet` to place that bet.


    If :obj:`workingBet` is not :literal:`None`, the bet is still
    working. Do not place any more bets.


..  method::CrapsPlayer.win(self, bet: Bet) -> None

    :param bet: The bet that was a winner
    :type bet: :class:`Bet`


    Notification from the :class:`CrapsGame`
    that the :class:`Bet` was a winner. The amount of money won is
    available via :obj:`theBet` :meth:`winAmount`.



..  method::CrapsPlayer.lose(self, bet: Bet) -> None

    :param bet: The bet that was a loser
    :type bet: :class:`Bet`


    Notification from the :class:`CrapsGame`
    that the :class:`Bet` was a loser.


CrapsGameState Class
---------------------

..  class:: CrapsGameState

    The :class:`CrapsGameState` class defines the state-specific behavior of a
    Craps game. Individual subclasses provide methods used by the :class:`CrapsTable` class
    to validate bets and determine the active bets. Subclasses provide
    state-specific methods used by a :class:`Throw` object to possibly change
    the state and resolve bets.


Fields
~~~~~~~

..  attribute:: CrapsGameState.game

    The overall :class:`CrapsGame` object for which this is a specific state.
    From this object, the various next
    state-change methods can get the :class:`CrapsTable` instance and an :class:`Iterator`
    over the active :class:`Bet` instances.


Constructors
~~~~~~~~~~~~


..  method:: CrapsGameState.__init__(self, game: Game) -> None

    :param game: The game to which this state applies
    :type game: :class:`Game`


    Saves the overall :class:`CrapsGame` object to which this state applies.


Methods
~~~~~~~~


..  method:: CrapsGameState.isValid(self, outcome: Outcome) -> bool

    :param outcome: The outcome to be tested for validity
    :type outcome: :class:`Outcome`


    Returns true if this is a valid outcome for creating bets in the current game state.

    Each  subclass provides a unique definition of valid bets for their game state.




..  method:: CrapsGameState.isWorking(self, outcome: Outcome) -> bool

    :param outcome: The outcome to be tested for if it's working
    :type outcome: :class:`Outcome`


    Returns true if this is a working outcome for existing bets in the current game state.

    Each subclass provides a unique definition of active bets for their game state.




..  method:: CrapsGameState.craps(self, throw: Throw) -> CrapsGameState

    :param throw: The throw that is associated with craps.
    :type throw: :class:`Throw`


    Return an appropriate state when a 2, 3 or 12 is
    rolled. It then resolves any game bets.

    Each subclass provides a unique definition of what new state
    and what bet resolution happens.




..  method:: CrapsGameState.natural(self, throw: Throw) -> CrapsGameState

    :param throw: The throw that is associated with a natural seven.
    :type throw: :class:`Throw`


    Returns an appropriate state when a 7 is
    rolled. It then resolves any game bets.

    Each subclass provides a unique definition of what new state
    and what bet resolution happens.




..  method:: CrapsGameState.eleven(self, throw: Throw) -> CrapsGameState

    :param throw: The throw that is associated an eleven.
    :type throw: :class:`Throw`


    Returns an appropriate state when an 11 is rolled. It
    then resolves any game bets.

    Each subclass provides a unique definition of what new state
    and what bet resolution happens.




..  method:: CrapsGameState.point(self, throw: Throw) -> CrapsGameState

    :param throw: The throw that is associated with a point number.
    :type throw: :class:`Throw`


    Returns an appropriate state when the given point number is rolled.
    It then resolves any game bets.

    Each subclass provides a unique definition of what new state
    and what bet resolution happens.





..  method:: CrapsGameState.pointOutcome(self) -> Outcome


    Returns the :class:`Outcome` object based on the current point. This is
    used to create Pass Line Odds or Don't Pass Odds bets. This
    delegates the real work to the current :class:`CrapsGameState` object.



..  method:: CrapsGameState.moveToThrow(self, bet: Bet, throw: Throw) -> None

    :param bet: The Bet to update based on the current Throw
    :type bet: :class:`Bet`

    :param throw: The Throw to which the outcome is changed
    :type throw: :class:`Throw`


    Moves a Come Line or Don't Come Line bet
    to a new :class:`Outcome` instance based on the current :class:`Throw` instance.
    If the value of the :obj:`theThrow` instance is 4, 5, 6, 8, 9 or 10, this delegates
    the move to the current :class:`CrapsGameState` object. For
    values of 4 and 10, the odds are 2:1. For values of 5 and 9, the
    odds are 3:2. For values of 6 and 8, the odds are 6:5. For other
    values of the :obj:`theThrow` object, this method does nothing.




..  method:: CrapsGameState.__str__(self) -> str


    In the superclass, this doesn't do anything. Each subclass, however,
    should display something useful.


CrapsGamePointOff Class
-----------------------

..  class:: CrapsGamePointOff


    The :class:`CrapsGamePointOff` class defines the unique behavior of the Craps game
    when the point is off. It defines the allowed bets and the active bets.
    It provides methods used by a :class:`Throw` instance to change the state and
    resolve bets.


    All four of the game update methods (craps, natural, eleven and point)
    use the same basic algorithm. The method will get the :class:`CrapsTable` object
    from :obj:`theGame`. From the :class:`CrapsTable` object, the method
    gets an :class:`Iterator` over the :class:`Bet` instances. It can then
    match each :class:`Bet` object's :class:`Outcome` against the various :class:`Outcome` instances
    of the current :class:`Throw` object which win and lose, and resolve the bets.

Constructors
~~~~~~~~~~~~~~


..  method:: CrapsGamePointOff.__init__(self, game: CrapsGame) -> None

    :param game: The game to which this state applies.
    :type game: :class:`CrapsGame`


    Uses the superclass constructor to save the overall :class:`CrapsGame` object.


Methods
~~~~~~~~~


..  method:: CrapsGamePointOff.isValid(self, outcome: Outcome) -> bool

    :param outcome: The outcome to be tested for validity
    :type outcome: :class:`Outcome`


    There are
    two valid :class:`Outcome` instances: Pass Line, Don't Pass Line. All other
    :class:`Outcome` instances are invalid.



..  method:: CrapsGamePointOff.isWorking(self, outcome: Outcome) -> bool

    :param outcome: The outcome to be tested to see if it's working
    :type outcome: :class:`Outcome`



    There are six non-working :class:`Outcome` instances: "Come Odds 4",
    "Come Odds 5", "Come Odds 6", "Come Odds 8",
    "Come Odds 9" and "Come Odds 10". All other :class:`Outcome` instances
    are working.




..  method:: CrapsGamePointOff.craps(self, throw: Throw) -> None

    :param throw: The throw that is associated with craps.
    :type throw: :class:`Throw`


    When the
    point is off, a roll of 2, 3 or 12 means the game is an immediate
    loser. The Pass Line :class:`Outcome` is a loser. If the :class:`Throw`
    value is 12, a Don't Pass Line :class:`Outcome` is a push,
    otherwise the Don't Pass Line :class:`Outcome` is a winner. The
    next state is the same as this state, and the method should return :literal:`this`.



..  method:: CrapsGamePointOff.natural(self, throw: Throw) -> None

    :param throw: The throw that is associated with a natural seven.
    :type throw: :class:`Throw`


    When the point is off, 7 means the game is an immediate
    winner. The Pass Line :class:`Outcome` is a winner, the Don't
    Pass Line :class:`Outcome` is a loser. The next state is the
    same as this state, and the method should return :literal:`this`.



..  method:: CrapsGamePointOff.eleven(self, throw: Throw) -> None

    :param throw: The throw that is associated an eleven.
    :type throw: :class:`Throw`


    When the point is off, 11 means the game is an immediate winner. The
    Pass Line :class:`Outcome` is a winner, the Don't Pass Line :class:`Outcome`
    is a loser. The next state is the same as this state, and the method
    should return :literal:`this`.



..  method:: CrapsGamePointOff.point(self, throw: Throw) -> None

    :param throw: The throw that is associated with a point number.
    :type throw: :class:`Throw`


    When the point
    is off, a new point is established. This method should return a new
    instance of :class:`CrapsGamePointOn` created with the given :class:`Throw`'s value.
    Note that any Come Point bets or Don't Come Point bets
    that may be on this point are pushed to player: they can't be legal
    bets in the next game state.



..  method:: CrapsGamePointOff.pointOutcome(self) -> Outcome


    Returns the :class:`Outcome` based on the current point. This is
    used to create Pass Line Odds or Don't Pass Odds bets. This
    delegates the real work to the current :class:`CrapsGameState`
    object. Since no point has been established, this returns :literal:`null`.



..  method:: CrapsGamePointOff.__str__(self) -> str


    The point-off state should simply report that the point is off, or
    that this is the come out roll.


CrapsGamePointOn Class
-----------------------

..  class:: CrapsGamePointOn

    The :class:`CrapsGamePointOn` class defines the behavior of the Craps game
    when the point is on. It defines the allowed bets and the active bets.
    It provides methods used by a :class:`Throw` object to change the state and
    resolve bets.


Fields
~~~~~~~

..  attribute:: CrapsGamePointOn.point

    The point value.


Constructors
~~~~~~~~~~~~~~



..  method:: CrapsGamePointOff.__init__(self, point: Outcome, game: CrapsGame) -> None


    Saves the given     point value.
    Uses the superclass constructor to save the overall :class:`CrapsGame` object.

    :param point: the outcome which defines the point set but the current :class:`Throw` instance.
    :type point: :class: `Outcome`

    :param game: the current CrapsGame instance
    :type game: :class:`CrapsGame`


Methods
~~~~~~~~


..  method:: CrapsGamePointOff.isValid(self, outcome: Outcome) -> bool

    :param outcome: The outcome to be tested for validity
    :type outcome: :class:`Outcome`


    It is
    invalid to Buy or Lay the :class:`Outcome` instances that match the
    point. If the point is 6, for example, it is invalid to buy the
    "Come Point 6" :class:`Outcome`. All other :class:`Outcome` instances
    are valid.



..  method:: CrapsGamePointOff.isWorking(self, outcome: Outcome) -> bool

    :param outcome: The outcome to be tested to see if it's working
    :type outcome: :class:`Outcome`


    All :class:`Outcome` instances are working.




..  method:: CrapsGamePointOff.craps(self, throw: Outcome) -> None

    :param throw: The throw that is associated with craps.
    :type throw: :class:`Throw`


    When the
    point is on, 2, 3 and 12 do not change the game state. The Come Line :class:`Outcome`
    is a loser, the Don't Come Line :class:`Outcome` is a winner.
    The next state is the same as this state, and the method should return
    :literal:`this`.




..  method:: CrapsGamePointOff.natural(self, outcome: Outcome) -> None

    :param throw: The throw that is associated with a natural seven.
    :type throw: :class:`Throw`


    When the point is on, 7 means the game is a loss. Pass Line
    :class:`Outcome` instances lose, as do the pass-line odds :class:`Outcome`
    s based on the point. Don't Pass Line :class:`Outcome` instances win, as
    do all Don't Pass odds :class:`Outcome` based on the point. The
    Come Line :class:`Outcome` is a winner, the Don't Come Line :class:`Outcome`
    is a loser. However, all Come Point number :class:`Outcome` instances
    and Come Point Number odds :class:`Outcome` are all losers. All
    Don't Come Point number :class:`Outcome` instances and Don't Come Point odds
    :class:`Outcome` instances are all winners. The next state is a new
    instance of the :class:`CrapsGamePointOff` state.


    Also note that the :class:`Throw` of 7 also resolved all
    hardways bets. A consequence of this is that all :class:`Bets`
    on the :class:`CrapsTable` are resolved.




..  method:: CrapsGamePointOff.eleven(self, throw: Throw) -> None

    :param throw: The throw that is associated an eleven.
    :type throw: :class:`Throw`


    When the point is on, 11 does not change the game state. The Come Line
    :class:`Outcome` is a winner, and the Don't Come Line :class:`Outcome`
    is a loser. The next state is the same as this state, and the method
    should return :literal:`this`.




..  method:: CrapsGamePointOff.point(self, throw: Throw) -> None

    :param throw: The throw that is associated with a point number.
    :type throw: :class:`Throw`


    When the point
    is on and the value of :obj:`throw` doesn't match :obj:`point`,
    then the various Come Line bets can be resolved. Come Point :class:`Outcome`
    s for this number (and their odds) are winners. Don't Come Line :class:`Outcome`
    s for this number (and their odds) are losers. Other Come Point
    number and Don't Come Point numbers remain, unresolved. Any Come
    Line bets are moved to the Come Point number :class:`Outcome` instances.
    For example, a throw of 6 moves the :class:`Outcome` of the Come Line
    :class:`Bet` to Come Point 6. Don't Come Line bets are moved to
    be Don't Come number :class:`Outcome` instances. The method should return
    :literal:`this`.


    When the point is on and the value of :obj:`throw` matches :obj:`point`,
    the game is a winner. Pass Line :class:`Outcome` instances are all
    winners, as are the behind the line odds :class:`Outcome` instances.
    Don't Pass line :class:`Outcome` instances are all losers, as are the
    Don't Pass Odds :class:`Outcome` instances. Come Line bets are moved to
    thee Come Point number :class:`Outcome` instances. Don't Come Line bets
    are moved to be Don't Come number :class:`Outcome` instances. The next
    state is a new instance of the :class:`CrapsGamePointOff` state.



..  method:: CrapsGamePointOff.pointOutcome(self) -> Outcome


    Returns the :class:`Outcome` based on the current point. This is
    used to create Pass Line Odds or Don't Pass Odds bets. This
    delegates the real work to the current :class:`CrapsGameState`
    object. For points of 4 and 10, the :class:`Outcome` odds are
    2:1. For points of 5 and 9, the odds are 3:2. For points of 6 and 8,
    the odds are 6:5.




..  method:: CrapsGamePointOff.__str__(self) -> str


    The point-off state should simply report that the point is off, or
    that this is the come out roll.


CrapsGame Design
----------------------

..  class:: CrapsGame

    The :class:`CrapsGame` class manages the sequence of actions that defines the
    game of Craps. This includes notifying the :class:`Player` to place
    bets, throwing the :class:`Dice` instance and resolving the :class:`Bet` objects
    actually present in the :class:`Table` object's collection of bets.

    Note that a single cycle of play is one throw of the dice, not a
    complete craps game. The state of the game may or may not change
    with each throw of the dice.


Fields
~~~~~~~~

..  attribute:: CrapsGame.dice

    Contains the dice that returns a randomly selected :class:`Throw`
    with winning and losing :class:`Outcome` instances.  This is an instance
    of the :class:`Dice` class.

..  attribute:: CrapsGame.table

    The  :class:`CrapsTable` instance contains the bets placed by the player.

..  attribute:: CrapsGame.player

    The :class:`CrapsPlayer` instance to place bets on the :class:`CrapsTable` instance.


Constructors
~~~~~~~~~~~~~

We based this constructor on an design that allows any of these
objects to be replaced. This is the :strong:`Strategy` design
pattern. Each of these objects is a replaceable strategy, and can be
changed by the client that uses this game.


Additionally, we specifically do not include the :class:`Player`
instance in the constructor. The :class:`CrapsGame` object exists
independently of any particular :class:`Player` instance, and we defer
binding the :class:`Player` instance and :class:`CrapsGame` object until we are
gathering statistical samples.


..  method:: CrapsGame.__init__(self, dice: Dice, table: CrapsTable) -> None

    :param dice: The dice to use
    :type dice: :class:`Dice`

    :param table: The table to use for collecting bets
    :param table: :class:`CrapsTable`


    Constructs a new :class:`CrapsGame` instance, using a given :class:`Dice` instance
    and :class:`CrapsTable` instance.

    The player is not defined at this time, since we may
    want to run several simulations with different players.


Methods
~~~~~~~~~~


..  method:: CrapsGame.__init__(self, player: CrapsPlayer) -> None

    :param player: The player who will place bets on this game
    :type player: :class:`CrapsPlayer`


    This will execute a single cycle of play
    with a given :class:`CrapsPlayer`.

    #.  It will call :meth:`CrapsPlayer.placeBets` to get
        bets. It will validate the bets, both individually, based on the
        game state, and collectively to see that the table limits are met.

    #.  It will call :meth:`Dice.roll` to get the
        next winning :class:`Throw` instance.

    #.  It will use the :class:`Throw` object's :meth:`updateGame`
        to advance the game state.

    #.  It will then call :meth:`CrapsTable.bets` to get an
        :class:`Iterator` over individual :class:`Bet` objects.

        -   It will use the :class:`Throw` object's :meth:`resolveOneRoll`
            method to check one-roll propositions. If the method returns
            true, the :class:`Bet` instance is resolved and should be deleted.

        -   It will use the :class:`Throw` object's :meth:`resolveHardways`
            method to check the hardways bets. If the method returns
            true, the :class:`Bet` instance is resolved and should be deleted.

        Note we can't delete from a simple iterator over a list. If we make
        a copy of the list, we can iterate over the copy and delete from the
        original list.



..  method:: CrapsGame.pointOutcome(self) -> Outcome


    Returns the :class:`Outcome`
    based on the current point. This is used to create Pass Line Odds or
    Don't Pass Odds bets. This delegates the real work to the current :class:`CrapsGameState`
    object.




..  method:: CrapsGame.moveToThrow(self, bet: Bet, throw: Throw) -> None

    :param bet: The Bet to move based on the current throw
    :type bet: :class:`Bet`

    :param throw: The Throw to which to move the Bet's Outcome
    :type throw: :class:`Throw`


    Moves a Come Line or Don't Come Line bet
    to a new :class:`Outcome` instance based on the current throw. This delegates
    the move to the current :class:`CrapsGameState` object.

    This method should -- just as a precaution -- assert that the
    value of :obj:`theThrow` is 4, 5, 6, 8, 9 or 10.  These
    point values indicate that a Line bet can be moved.
    For other values of :obj:`theThrow`, this method should raise an
    exception, since there's no reason for attempting to move a line bet
    on anything but a point throw.



..  method:: CrapsGame.reset(self) -> None


    This will reset the game
    by setting the state to a new instance of :class:`GamePointOff`.
    It will also tell the table to clear all bets.
    This can be used during the overall simulation or unit testing to reset the object.

    This method is optional. In many cases, it's easier to simply delete the object and create
    a fresh, new copy.


Craps Game Deliverables
------------------------

There are over a dozen deliverables for this exercise. This includes
significant rework for the :class:`Throw` and :class:`Dice` classes. It
also includes development of a stub :class:`CrapsPlayer` class, the :class:`CrapsGameState` class
hierarchy and the first version of the :class:`CrapsGame` class. We will
break the deliverables down into two groups.

**Rework**. The first group of deliverables includes the rework for the :class:`Throw`
and :class:`Dice` classes, and all of the associated unit testing.

-   The revised and expanded :class:`Throw` class. This will ripple
    through the constructors for all four subclasses, :class:`NaturalThrow`,
    :class:`CrapsThrow`, :class:`ElevenThrow`, :class:`PointThrow`.

-   Five updated unit tests for the classes in the :class:`Throw`
    class hierarchy. This will confirm the new functionality for holding
    winning as well as losing :class:`Outcome` instances.

-   The revised and expanded :class:`ThrowBuilder` class. This will construct
    :class:`Throw` instances with winning as well as losing :class:`Outcome` instances.

-   A unit test for the :class:`Dice` class that confirms the new
    initializer that creates winning as well as losing :class:`Outcome` instances.


**New Development**. The second group of deliverables includes development
of a stub :class:`CrapsPlayer` class, the :class:`CrapsGameState` class
hierarchy and the first version of the :class:`CrapsGame` class. This
also includes significant unit testing.

-   The :class:`CrapsPlayer` class stub. We will rework this design
    later. This class places a bet on the Pass Line when there is no
    Pass Line :class:`Bet` on the table. One consequence of this is
    that the player will be given some opportunities to place bets, but
    will decline. Since this is simply used to test :class:`CrapsGame` class,
    it doesn't deserve a very sophisticated unit test of its own. It
    will be replaced in a future exercise.

-   A revised :class:`Bet` class, which carries a reference to the :class:`Player` object
    who created the :class:`Bet` instance. This will ripple through all
    subclasses of the :class:`Player` class, forcing them to all add the :literal:`self`
    parameter when constructing a new :class:`Bet` instance.

-   This will lead to rework in the Roulette definitions to add the :class:`Player` object
    reference to each :class:`Bet` instance that's created.

-   The :class:`CrapsGame` class.

-   A class which performs a demonstration of the :class:`CrapsGame`
    class. This demo program creates the :class:`Dice` object, the stub :class:`CrapsPlayer` object,
    and the :class:`CrapsTable` object. It creates the :class:`CrapsGame`
    object and cycles a few times. Note that we will need to configure the
    :class:`Dice` object to return non-random results.

We could, with some care, refactor our design to create some common
superclasses between Roulette and Craps to extract features of :class:`Throw` class
so they can be shared by the :class:`Throw` and :class:`Bin` classes.
Similarly, there may be more common features between the :class:`RouletteGame`
and :class:`CrapsGame` classes. We'll leave that as an exercise for more
advanced students.

Optional Working Bets
----------------------

Some casinos may give the player an option to declare the odds
bet behind a come point as "on" or "off". This is
should not be particularly complex to implement.
There are a number of
simple changes required if we want to add this interaction between
the :class:`CrapsPlayer` and :class:`CrapsGame` classes.

1.  We must add a method to the :class:`CrapsPlayer`  class to respond to
    a query from the :class:`CrapsGame` instance that determines if the
    player wants their come point odds bet on or off.

2.  We need to update :class:`Bet` instance to store the :class:`Player` instance
    who created the :class:`Bet` object.

3.  The :class:`CrapsGame` instance must get the relevant :class:`Bet` instances
    from the :class:`Table` object,
    and interrogates the :class:`Player` object for the disposition
    of the bet.

Looking Forward
---------------

This was a lot of work. The craps game, and the stateful behavior is an important
OO design exercise. Coping with state change is central to all programming, and
OO design uses class encapsulation to isolate the responsibilities, leading to
more reliable and robust application software.

The craps player has two kinds of decisions. They can place bets, and they
can use various strategies to adjust the amounts of the bets. This double-layer
of decision-making will lead to rather complex player class definitions.
In the next section, we'll address the craps player in some depth.
