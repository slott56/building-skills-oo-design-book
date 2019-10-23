

Rework and Management Hand-Wringing: A Post-Script
----------------------------------------------------

A great deal of this book involves rework. This is in spite of it
often being difficult to justify design rework in an enterprise
development environment. Some managers have an amazingly large
blind-spot covering the amount of evidence
required to justify rework. The conversations have the following form.

**Architect**. We need to disentangle Roulette and Craps so that
Craps is not a subclass of Roulette. I've got a revised design
that will take :emphasis:`X` hours of effort to implement.

**Manager**. I'll need some justification. Why do we have to fix it?

**Architect**. The structure is illogical: Craps isn't a special
case of Roulette, they're independent specializations of
something more general.

**Manager**. (Pounds Table) Illogical! Illogical!  That's insane!
Illogical isn't a good enough justification. Our
overall problem domain always contains illogical special cases
and user-oriented considerations. You'll have to provide
something more concrete that a hand-waving nonsense about Illogical.

**Architect**. Okay, in addition to being illogical, it will
become too complex: in the future, we'll probably have trouble
implementing other games.

**Manager**. How much trouble? Will it be more than :emphasis:`X`
hours of effort? How can you be sure sure you're :emphasis:`X` of effort
now will have any payoff in the future? You're gambling with the
stakeholder's money. I need proof.

**Architect**. When we include maintenance, adaptation and
debugging, the potential future cost is probably larger than :emphasis:`2X`
hours of effort. And it's illogical.

**Manager**. Probably larger?  Probably? First you have illogic? Now you
have probably? This is all guess-work. We can't be guessing!
(More Table Pounding.) We can't justify rework based on
probable costs. You'll need something tangible. Will it save us
any lines of code?

**Architect**. No, it will add lines of code. But it will reduce
maintenance and adaptation costs because it will be more logical.

**Manager**. I conclude that the change is unjustified. You can't use
guesswork. Go away. Get back on schedule.

**Architect**. The initial schedule was guesswork.


In many cases, we have a manager who's mind is only influenced by the tangible schedule.
The schedule that was created prior to any deep knowledge of the
software being built. Once focused on the schedule, a manager may be reluctant
to deal in new facts that have been learned along the way.

However, in some cases, conversation continues in the following vein.

**Architect**. If guesswork isn't good enough, please define what constitutes
adequate justification for improvements?

**Manager**. Real savings. Real money. Measurable dollars and sense. I'm a plain
old count-the-money kind of manager. Ideas like "illogical" don't map to money.
A measurable, definite quantity of labor effort is the only justification for
disrupting the schedule.

**Architect**. And future effort doesn't count?

**Manager**. The probability of savings in the future isn't tangible. It's not
real. It's made-up pie-in-the-sky pipe-dreams of some possible future state.

**Architect**. And software that's more logical doesn't count?

**Manager**. If course not; it doesn't result in real schedule savings.
Logic isn't money. It's pretty pictures on UML diagrams. It's a slide-deck with
bubbles and arrows. That's not the schedule, that's just information.

**Architect**. The schedule
was only a notional projection of possible effort based on no actual hands-on
knowledge. At this point, we have knowledge. A :emphasis:`possible`
reduction in the possible effort has more factual basis than the original schedule.

**Manager**. Forget about the refactoring. I have an idea. Wouldn't it be simpler to...?


For reasons we don't fully understand, a schedule becomes a kind
of established fact. Any change to the schedule requires other
established facts, not the conjecture of design.

By some magical process, the schedule is transformed from a conjecture, based
on a previously conjectured design. Managers
can often cling to the schedule when it's little more than conjecture.
In effect, no level of proof can ever
override the precedence-setting fact of the schedule.
This makes it nearly impossible
to justify making a design change. In the worst cases, the only way to accumulate
enough evidence is to actually implement the change and then measure
the impact of the change.


To continue this rant, the same kind of "inadequate evidence"
issue seems to surround many technology changes. We have had
conversations like the one shown above regarding object-oriented
design, the use of objects in relational databases, the use of
object-oriented databases, the use of open-source software, and
the use of the star-schema data model for reporting and
analysis. Here's the summary

    Change can only be considered based on established facts.

    The facts can only be established by making a change.

While this
chicken-and-egg problem is easily resolved by recognizing that
the current architecture or schedule is actually :emphasis:`not`
an established fact, this is a difficult mental step to take.


As a final complaint, we note that all "wouldn't it be simpler..."
gambits can be described as a management trump card. The
point is rarely an effort to reduce code complexity, but to
promote management understanding of the design. While this is a
noble effort, there is sometimes a communication gap between
designers and managers. It is incumbent both on designers to
communicate fully, and on managers to provide time, budget and
positive reinforcement for detailed communication of design
considerations and consequences.

The "tl;dr" here is that rework leads to worry and it shouldn't.

Rework reflects valuable lessons learned, and is perhaps the most
important work than can be done.
