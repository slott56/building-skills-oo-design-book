
Conclusion
==========

The game of Roulette has given us an opportunity to build an application
with a considerable number of classes and objects. It is comfortably
large, but not complex; we have built tremendous fidelity to a
real-world problem. Finally, this program produces moderately
interesting simulation results.

In this section we'll look at our overall approach to design in `Exploration`_.

We'll look at some design principles in `The SOLID Principles`_.

In `Other Design Patterns`_ we'll look at some of the other design
patterns we've been using.

Exploration
-----------

We note that a great many of our design decisions were not easy to make
without exploring a great deal of the overall application's design.
We've shown how to do this exploration: design just enough but remain tolerant of our own ignorance.

There's an idealized fantasy in which a developer design an entire, complex application
before writing any software. The process for creating a complete design is still
essentially iterative. Some parts are designed in detail, with
tolerance for future changes; then other parts are designed in detail
and the two design elements reconciled. This **can** be done on paper
or on a whiteboard.

With Python, however, we can write -- and revise -- draft programming
as easily as erasing a whiteboard. It's quite easy to do incremental
design by writing and revising a working base of code.

For new designers, we can't give enough emphasis to the importance of
creating a trial design, exploring the consequences of that design, and
then doing rework of that design. Too often, we have seen trial designs
finalized into deliverables with no opportunity for meaningful rework. In
:ref:`roul.test`, we presented one common kind of rework to support
more complete testing. In :ref:`roul.player`, we presented another
kind of rework to advance a design from a stub to a complete implementation.

The SOLID Principles
---------------------

There are five principles of object-oriented design. We've touched on several.
For more information, see https://en.wikipedia.org/wiki/SOLID_(object-oriented_design).

:S: Single responsibility principle. We've emphasized this heavily by trying to
    narrow the scope of responsibility in each class.

:O: Open/closed principle. The terminology here is important. A class is open to extension
    but closed to modification. We prefer to wrap or extend classes. We prefer not to modify
    or tweak a class. When we make a change to a class, we are careful to be sure that
    the ripple touches the entire hierarchy and all of the collaborators.

:L: Liskov substitution principle. In essence, this is a test for proper polymorphism.
    If classes are truly polymorphic, one can be substituted for another. We've generally
    focused on assuring this.

:I: Interface segregation principle. In most of what we're doing, we've kept interfaces
    as narrow as possible. When confronted with **Wrap vs. Extend** distinctions, the
    idea of interface segregation suggests that we should prefer wrapping a class
    because that tends to narrow the interface.

:D: Dependency inversion principle. This principle guides us toward creating common
    abstractions. Our :class:`Player` class is an example of this. We didn't create games
    and tables that depend on a specific player. We created games and tables that would
    work with any class that met the minimal requirements for the :class:`Player` class
    interface.

Other Design Patterns
---------------------

We also feel compelled to point out the distinction between relatively
active and passive classes in this design. We had several passive
classes, like the :class:`Outcome`, :class:`Bet`, and :class:`Table` classes,
which had few responsibilities beyond collecting a number of related
attributes and providing simple functions.

These classes are slightly easier to implement using the ``@dataclass`` decorator.
It can help when a few common features get built automatically.

We also had several complex,
active classes, like the :class:`Game`, :class:`BinBuilder`, and all
of the variations on the :class:`Player` classes. These classes, typically, had
fewer attributes and more complex methods. In the middle of the spectrum
is the :class:`Wheel` class.

We find this distinction to be an enduring
feature of OO design: there are :emphasis:`things` and :emphasis:`actors`;
the things tend to be passive, acted upon by the actors. The overall
system behavior emerges from the collaboration among all of the objects
in the system; primarily -- but not exclusively -- the behavior of the
active classes.

Looking Forward
---------------

The next part of the book centers on the game of Craps. This game is stateful
with a number of more intricate betting rules. We'll start out with a discussion
of the game itself in the next chapter.
