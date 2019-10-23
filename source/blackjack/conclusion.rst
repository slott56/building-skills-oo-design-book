
Conclusion
==========

The game of Blackjack has given us an opportunity to further extend and
modify a simulation application with a considerable number of classes and objects.
These exercises gave us an opportunity to work from a base of software,
extending and refining our design.

We omitted concluding exercises which would integrate this package with the
:class:`Simulator` and collect statistics. This step, while
necessary, doesn't include many interesting design decisions. The final
deliverable should be a working application that parses command-line
parameters, creates the required objects, and creates an instance of :class:`Simulator`
to collect data.

We have specifically omitted delving into the glorious details of
specific player strategies. We avoided these details because
there are so many. We've left
it to the interested student to either buy any of the available
books on Blackjack or download strategy descriptions from the Internet.

Indeed, one of the more interesting things this simulation can be used
for is to create a machine learning environment. An approach like
Simulated Annealing could be used to try different strategy variations looking
for one that's optimal.

**Next Steps**.
There are a number of logical next steps for the programmers looking to build skills
in object-oriented design.  We'll split these along several broad fronts.

-   **Additional Technology**.
    There are several technology directions that can be pursued for further
    design experience.

    Another area for building skills in design is the implementation of programs
    that make extensive use of a database. All of the statistical results
    can be accumulated in a database instead of :file:`.csv` files for analysis.

    A graphical user interface GUI can be added to show that the
    simulation is doing something.

    A web framework can be used to provide configuration changes and run
    simulations. Rather than using the command line, a RESTful API can be
    built to provide alternative strategies or rules.

-   **Application Areas**.
    We selected simulation because it's part of the historical foundation for
    object-oriented programming.  We selected casino games because they have a
    reasonable level of complexity.

    Clearly, numerous other application areas can be selected as the basis
    for problems.  The number and variety of human endevors that can be automated
    is quite large.

    Moving beyond simulation or doing simulation on something more complex
    than a casino table game is a good next step.

-   **Additional Depth in Design Patterns**.
    It's possible to use additional and different design patterns to extend
    and refine the application that you have built.

    Any book or web site on OO design patterns will provide numerous examples
    of patterns.  These can be used for add flexibility to these casino game
    simulators.

Looking Forward
---------------

The final part has some overall "fit-and-finish" topics. We'll look at a number
of tools useful for quality assurance.
After that, we'll look at the overall command-line interface for running the application.
