
Conclusion
==========

The game of Craps has given us an opportunity to extend and modify an
application with a considerable number of classes and objects. It is
large, with a number of complexities, and produces interesting results.
Further, as a maintenance and enhancement exercise, it gave us an
opportunity to work from a base of software, extending and refining the
quality of the design.


We omitted exercises which would integrate this package with the :class:`Simulator` class
and collect statistics. This step, while necessary, doesn't include many
interesting design decisions. The final deliverable should be a working
application that parses command-line parameters, creates the required
objects, and creates an instance of the :class:`Simulator` class to collect data.


**Refactoring**.
We note that many design decisions required us to explore and refactor a great deal
of the application's design.  In writing this part, we found it
very difficult to stick to our purpose of building up the design using
realistic steps and realistic problem solving.

Our goal is explicitly **not** to be a book with a description
of an already-completed structure. Exposing a carefully-planned design does not help new designers learn the *process* of
design. It does not help people to identify design problems and correct
them. This philosophy is required setting up the situation where the complete refactoring of the design
in the :ref:`craps.refactor` chapter was an important activity.
A resilient and adaptable implementation is an important quality measure;
it is a skill perfected through extensive practice.

We observe this kind of
design rework happening late in the life of a project. Project
managers are often uncomfortable evaluating the cost and benefit of significant changes.
Further, programmers are unable to express the cost of
technical debt increased through a series of less-than-optimal decisions.

**Simpler is Better**.
Perhaps, the most important lesson  is the constant search
for something we call **The Big Simple**. We see the
history of science as a search for simpler explanations of natural
phenomena. The canonical example of this is the distinction between the
geocentric model and the heliocentric model of the solar system. Both
can be made to work: astronomers carefully built extremely elaborate
models of the geocentric heavens and produced accurate predictions of
planetary positions. However, the model of planetary motion around the
sun describes real phenomena more accurately and has the added benefit
of being much simpler than competing models.


To continue this rant, we find that software designers and their
managers do not feel the compulsion and do not budget the time to
identify the grand simplifications that are possible. In some cases, the
result of simplifying the design on one axis will create more classes.
Designers lack a handy metric for "understandability"; managers
are able to count individual classes, no matter how transparently
simple. Designers often face difficulties in defending a design with
many simple classes; some people feel that a few complex classes is "simpler"
because it has fewer classes.


As our trump card, we reference the metrics for complexity:

-   McCabe's Cyclomatic Complexity penalizes if-statements. By reducing the number of
    if-statements to just those required to create an object of the proper
    class, we reduce the complexity.

-   The Halstead metrics penalize programs with many
    internal operators and operands when compared with few
    interface operands. Halstead emphasizes simple,
    transparent classes.

Neither measure penalizes overall size in lines of code,
but rather they penalize decision-making and
hidden, internal state. A badly designed, complex class has hidden
internal states, often buried in nested if-statements. We emphasize
small, simple classes with no hidden features and few if-statements.


Our concrete examples of this simplification process are contained in
three large design exercises. In :ref:`craps.throwbuilder`, we showed
a kind of rework necessary to both generalize and isolate the special
processing for Craps. In :ref:`craps.refactor`, we reworked classes to
create an easy-to-explain architecture with layers and partitions of
responsibility. Finally, in :ref:`craps.count`, we uncovered a clean
separation between game rules and betting strategies.

Looking Forward
----------------

The next part of the book centers on the game of Blackjack. This game is stateful
with a number of more intricate playing rules. We'll start out with a discussion
of the game itself in the next chapter.
