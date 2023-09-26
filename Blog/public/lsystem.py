from typing import Set
from typing import Generic, TypeVar
import turtle as t

T = TypeVar('T')
DIST = 5
ANGL = 60
START_A = 60
START_X = -(t.window_width() // 2) + 100 
#START_X = 0
START_Y = -t.window_height() // 2 + 50
START_W = 1.0
W_MUL = 0.85


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: list[T] = []

    def push(self, t: T) -> None:
        self._container.append(t)

    def pop(self) -> T:
        return self._container.pop()


def lsystem(axiom: str, rules: dict[str, str], iters: int) -> str:
    if (iters == 0):
        return axiom
    else:
        return lsystem(''.join(map(lambda c: rules[c], axiom)), rules, iters-1)


def draw(s: str) -> None:
    # Clear the screen, hide the turtle, and set the speed to the highest possible.
    t.clearscreen()
    t.ht()
    t.speed('fastest')

    # Set the turtle's starting position and angle.
    t.up()
    t.setpos(START_X, START_Y)
    t.seth(START_A)
    t.width(START_W)
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
            saved_positions.push((t.xcor(), t.ycor(), t.heading(), t.width()))
            t.width(t.width() * W_MUL)

        if (c == ']'):
            x, y, h, w = saved_positions.pop()
            t.up()
            t.setpos(x, y)
            t.seth(h)
            t.width(w)
            t.down()
    
    input()


#axiom: str = 'X'
#rules: dict[str, str] = {
#    'X': 'F+[[X]-X]-F[-FX]+X',
#    'F': 'FF',
#    '+': '+',
#    '-': '-',
#    '[': '[',
#    ']': ']'
#    }

axiom: str = 'FXF--FF--FF'
rules: dict[str, str] = {
    'F': 'FF',
    'X': '--FXF++FXF++FXF--',
    '+': '+',
    '-': '-'
    }

draw(lsystem(axiom, rules, 6))

