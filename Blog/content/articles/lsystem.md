---
title: "L-systems"
date: 2023-09-25T00:43:00+02:00
description: "A recursive parallel rewriting system to generate self-similar structures such as plants and fractals."
draft: false
---

An L-system (Lindenmeyer system) is a parallel rewriting system.
We decide on an alphabet $V$, set of rewriting rules $P$, and a starting axiom $\omega$.
Starting from the axiom we apply all rules simultaneously, rewriting the string, and producing the next iteration.
This then repeats.

For instance, if $V = \{ A, B \}$, $\omega = \{ B \}$, and $P = \{ A \to AA, B \to BA \}$, then the first couple of iterations will look like:

| Iteration | String   |
|:---------:|:---------|
| 0         | A        |
| 1         | BA       |
| 2         | BAAA     |
| 3         | BAAAAAAA |

Notice that every rule gets applied at the same time.
At the moment, we'll only consider rules that do not conflict, meaning, for every character there is only at most one rule that applies.

L-systems are very good at modelling self-similar structures, for example fractals and plants.
Before we get to the exciting bits, let's create a function that takes an L-system and a positive integer $n$, and returns the $n$th generation.
To keep things simple, we'll let the alphabet be implied by the rules and axiom.

```python 
def lsystem(axiom: str, rules: dict[str, str], iters: int) -> str:
    if (iters == 0):
        return axiom
    else:
        return lsystem(''.join(map(lambda c: rules[c], axiom)), rules, iters-1)
```

Try this function out and make sure it reproduces the output given in the table above.

The most popular way of interpreting L-system strings is graphical.
To do this, we'll use the Turtle graphics library.
A Turtle is exactly that, a little turtle holding a pen.
The turtle can move forwards, backwards, turn left and right, as well as put his pen down or lift it up.
When the pen is down, the turtle draws as he moves.
If the pen is up the turtle can move without drawing.

```python
import turtle as t

t.fd(100)
input()
```

Try running this code.
You should see a white canvas with a black line being drawn.
The `input()` at the end is to make sure the window doesn't immediately close as soon as the turtle is done drawing.
The line `t.fd(100)` tells the turtle to move forward 100 pixels.
What do you think the following code does?

```python
t.fd(100)
t.seth(90)
t.fd(50)
input()
```

The most mystifying part is `t.seth(90)`.
This sets the turtle's heading (i.e. angle) to 90 degrees (which corresponds to "up" or "north").
Try running it and see if your guess was correct.

The idea now is to interpret the string produced by our L-system as commands for the turtle.
There's a few commands we'll consider:

| Symbol | Instruction                                                  |
|:-------|:-------------------------------------------------------------|
| F      | Move forward.                                                |
| +      | Turn right.                                                  |
| -      | Turn left.                                                   |
| [      | Save current position and heading.                           |
| ]      | Return to last saved position and heading (without drawing). |
| X      | Do nothing.                                                  |

The exact amount of pixels we'll move forward and angle to turn by will be defined in constants ahead of time.
The "X" symbol is used only for generating the L-system string, it has no effect on the turtle.
Finally, the "[" and "]" symbols allow us to draw substructures by saving, and later returning to, our position.

Let's implement a function to interpret an L-system string.
First we'll define a Stack class to handle the saving and returning of our position.

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: list[T] = []

    def push(self, t: T) -> None:
        self._container.append(t)

    def pop(self) -> T:
        return self._container.pop()
```

Next we'll implement the turtle drawing.
The one thing to keep in mind is that the turtle's home position (and the origin) is set in the middle of the screen.
We'll use the `window_width()` and `window_height()` functions to translate the turtle before we start drawing.
Also note that a heading of 0 corresponds to facing right (east).

```python
DIST = 5
ANGL = 25
START_A = 65 
START_X = -(t.window_width() // 2) + 100 
START_Y = -t.window_height() // 2 + 50

def draw(s: str) -> None:
    # Clear the screen, hide the turtle, and set the speed to
    # the highest possible.
    t.clearscreen()
    t.ht()
    t.speed('fastest')

    # Set the turtle's starting position and angle.
    t.up()
    t.setpos(START_X, START_Y)
    t.seth(START_A)
    t.down()

    # Initialize the position stack.
    saved_positions: Stack = Stack()

    # Follow instructions in the string.
    for c in s:
        if (c == 'F'):
            t.fd(DIST)

        if (c == '+'):
            t.seth(t.heading() + ANGL)

        if (c == '-'):
            t.seth(t.heading() - ANGL)

        if (c == '['):
            saved_positions.push((t.xcor(), t.ycor(), t.heading()))

        if (c == ']'):
            x, y, h = saved_positions.pop()
            t.up()
            t.setpos(x, y)
            t.seth(h)
            t.down()
    
    input()
```

Let's see what our little turtle can do.
We'll use an example for Lindenmeyer himself[^1]:

[^1]: Normally the identity rules (e.g. $[ \to [$ are left out, but it simplifies the code if we explicitly define them.

```python
axiom: str = 'X'
rules: dict[str, str] = {
    'X': 'F+[[X]-X]-F[-FX]+X',
    'F': 'FF',
    '+': '+',
    '-': '-',
    '[': '[',
    ']': ']'
    }

draw(lsystem(axiom, rules, 6))
```

Running this code produces the quite beautiful output in Figure 1.

![Barnsley fern](/fern.png "Figure 1: Barnsley fern")

A very simple modification we can make is to have the branches be thinner and the trunk wider.
To do this we store a width value along with the x, y, and heading of the turtle.
We also define a width multiplier, which defines how much the width shrinks by each time we draw a subbranch.

```python
START_W = 3.0
W_MUL = 0.85
```

In the setup code of `draw` we add the initial width.

```python
def draw(s: str) -> None:
    ...
    t.setpos(START_X, START_Y)
    t.seth(START_A)
    t.width(START_W)
    ...
```

When we push the turtle's state we also push the width, as well as shrink it by the multiplier.

```python
def draw(s: str) -> None:
    ...
    if (c == '['):
        saved_positions.push((t.xcor(), t.ycor(), t.heading(), t.width()))
        t.width(t.width * W_MUL)
```

And when the pop back we restore the width.

```python
def draw(s: str) -> None:
    ...
    if (c == ']'):
        x, y, h, w = saved_positions.pop()
        t.up()
        t.setpos(x, y)
        t.seth(h)
        t.width(w)
        t.down()
```

This produces the output in Figure 2.

![Barnsley fern with varying width](/fern2.png "Figure 2: Barnsley fern with varying width")

Of course, there's many more things one can do.
For instance, we can implement a random element to our drawing, not always turning an exact amount or drawing a set length.
Or, perhaps color information can be stored.
Either directly in the string produced by the L-system or programmatically in a similar way we did with width.
I leave implementing these ideas up to you.

L-systems are not only good at generating plant-like structures, but all sorts of self-similar structures.
This includes fractals.
The ruleset below produces the famous Sierspinski triangle as can be seen in Figure 3.

```python
START_A = 60
START_W = 1.0
...
axiom: str = 'FXF--FF--FF'
rules: dict[str, str] = {
    'F': 'FF',
    'X': '--FXF++FXF++FXF--',
    '+': '+',
    '-': '-'
    }

draw(lsystem(axiom, rules, 6))
```

![Sierspinski triangle](/sierp.png "Figure 3: Sierspinski triangle")

We've only scratched the surface of L-systems.
There's so much more they can do, from 3D implementations, to creating music and architecture, to creating robot morphologies.
For more information you can take a look at the following excellent resources:

1. [alife.pl](http://en.alife.pl/files/lsyst/d/js/lsystem.html) where you can play around with L-systems
2. [This lecture by Maciej Komosinski](https://www.youtube.com/watch?v=S1rNrD62Z7I)
3. [Accompanying lecture notes](http://www.cs.put.poznan.pl/mkomosinski/lectures/MK_ArtLife.pdf)

You can download the source code here: [lsystem.py](/lsystem.py)

