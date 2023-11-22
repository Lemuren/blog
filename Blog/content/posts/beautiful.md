---
title: "Beautiful Code Has Fewer Bugs"
date: 2023-11-22T16:45:00+01:00
draft: false
---

One pattern I've noticed in software is that beautiful code often has fewer
bugs than ugly code. Why should this be? Indeed, one can write code that is
beautiful and code that is ugly that both compile down to the same
instructions. We're often also told that code aesthetics don't matter, or at
the very least, that people put too much emphasis on it.
I think beautiful code matters for more reasons than the purely measurable,
practical ones, but also I believe code aesthetics has an impact on the
practical. In particular, I think beautiful code tends to have fewer bugs than
ugly code.

The first reason is that beautiful code is often a sign of your design being
in harmony with the design on the language---by proxy of its syntax---and as
such you are playing to the strengths of the language and less likely to do
"off the wall" or unconvential things which are apt to introduce flaws.
Thus, beautiful code is harmonious with language design. Harmonious design
is less buggy.

Second, people like looking at beautiful code. This will make you care more
about the code (In fact, you can probably remember quickly wanting to plaster
on a solution to fix a flaw in a particularly messy and ugly part of a
codebase simply so that you can stop looking at it and stuff it back down
the back of the drawer where it came from). Needless to say, code that is
cared for will be less buggy.

Third, in programming, simple is often correlated with simple and elegant.
While not an exhaustive measure, it is a common theme to what we consider
beautiful. And as you know, simple and elegant code tends to have fewer bugs
than complex and deeply nested code.

Finally, there is, admiteddly, some sort of "x-factor". Something about
beautiful code that feels "just right". I can look at it, read it, and tell
that it has no flaws, no bugs, and I know exactly what the assumptions are and
when those assumptions break. Everything unnecessary has been cut away and what
remains is beautiful, correct, and "just right". The quote by Tony Hoare:
"There are two ways to write code: write code so simple there are obviously
no bugs in it, or write code so complex that there are no obvious bugs in it."

So go out there, and write beautiful code, and don't let anyone tell you it
doesn't matter "because the compiler will just compile it down to the same
instructions anyway".
