---
title: "A Foray into Path-finding Algorithms"
date: 2024-10-19T00:59:00+02:00
description: "A description and implementation of various basic path-finding algorithms from first principles."
draft: false
---

> A lot of the material of this post is based on the excellent book ["Classic Computer Science Problems in Python"](https://www.manning.com/books/classic-computer-science-problems-in-python) by David Kopec.

Pathfinding is finding the shortest route between two points.
Pathfinding algorithms are computer programs designed to do just that.
They're found in everything from video games to maze-solvers to your cars GPS.

This article will explore various pathfinding algorithms, namely: Breadth-first search, Depth-first search, Djikstra, and A* (pronounced "A star"), as well as their applications.
We will begin with the first two algorithms on an unweighted graph, and then move on to Dijkstra on a weighted graph.
Finally, we will refine Dijkstra slightly to arrive at A*.
## Graphs

A graph (which has its origins in discrete mathematics) is a structure consisting of vertices connected by edges.
Many structures can be represented by graphs: among them mazes, road networks, and decision trees.
If we designate one vertex as the start and another, different vertex, as the goal we may ask "what is the shortest path from the start to the goal?"
For now, we'll define the shortest path as the one that visits the fewest vertices.

To make things a bit more concrete, we'll imagine (the very real scenario!) of developing the GPS of a car.
We have been tasked with building the software to find the path from any city to any other using the local road network.
For this example we'll be looking at England.
Here's a picture from Google maps of England along with its major cities and roads.
To keep the scope relatively small we'll limit our consideration to only the cities of Derby, Nottingham, Birmingham, Convetry, Leicester, Bristol, Oxford, Northampton, Reading, Cambridge, Southhampton, and London.
We'll also not include every road, but only select, major motorways.
In reality, a real GPS would store the entirety of the road network, along with much more data.

![An image from Google maps of the major cities and roads of England](/map.png)

We cannot perform any sort of search with the data looking like this.
After all, it's just a picture of a map.
To give our algorithm any change we must change it into a graph, which is more easily worked with and readily understood by a computer.
It's also the standard structure pathfinding algorithms work with.
The cities become vertices and the roads between them edges.
Intersections of roads, even though there may not be a city there, also become vertices.

![Graph of the road network of England](/graph.png)

This is all we need to start implementing the first of our pathfinding algorithms: depth-first search!

## Depth-first search

This algorithm is very simple, but it introduces many key concepts which will be used later on.
The idea is to use a stack, initialized with the starting vertex.
We pop the top vertex of our stack and push all its connected vertices to the stack.
If at any point the vertex we pop off the stack is the goal, we are done!
The vertices currently under consideration (in our case, residing in the stack) is called the *frontier*.

To construct the path we must keep track of how we got from one vertex to another.
This is accomplished by adding one more layer of abstraction on top of a vertex: a node.
A node is nothing more than a vertex combined with information about which **node** is its parent.
That is, the vertex and the node (and through it, the vertex) we came from.
Thus, the same vertex can be represented by many different nodes, one for each edge of the vertex.
This is important (and will become even more important in later algorithms) because two different paths may visit the same vertex, but if the paths are indeed different at least one of the nodes must differ between the paths.
Put another way, two paths are the same if and only if all their nodes are the same.
This hints at the definition of a path: it is a set of nodes.[^1]
Be careful about the distinction between vertices and nodes---they are similar but not identical concepts.

[^1]: Note that a set is fine, and we do not need any ordering information, as that is contained within the nodes themselves.

We need one final piece of bookkeeping before we are ready to start writing some code.
To avoid going round-and-round in loops we must keep track of which vertices we have explored.
For this purpose, a simple list will suffice.

To keep our code clean, we'll work with two files.
The first we'll use to define general classes and implement the algorithms.
The second we'll use to define specific data to use with our algorithms, as well as run examples from.
Also note, we'll make use of type hinting throughout.
If you're unfamiliar with type hinting, you should really check it out.
It allows for cleaner, more robust Python code, and was introduced in Python 3.5.

To start with, we implement classes for vertices and nodes.

```python
# pathfinding.py

# We need this library to allow recursive type hinting in classes.
# An example is the Vertex class, which type hints that it takes a
# list of vertices.
from __future__ import annotations
from typing import Optional, TypeVar, Generic


class Vertex:
    def __init__(self, neighbors: list[Vertex], name: str) -> None:
        self.neighbors: list[Vertex] = neighbors
        self.name: str = name
    

    def __str__(self) -> str:
        return self.name


class Node:
    def __init__(self, v: Vertex, parent: Node) -> None:
        self.v: Vertex = v
        self.parent: Node = parent


    def __str__(self) -> str:
       if (self.parent is not None):                
           return str(self.vertex) + ' with parent ' + str(self.parent.vertex)
       else:
           return str(self.vertex)
```

The edge-information of a vertex is implicit by its connection to other vertices.
We also give each vertex a name.
This is not used in the algorithm, but will be nice for printing the output for us.
It's also good practice to give your objects human-friendly string representations.

Now that we've defined vertices and nodes, we can define what a graph is.
This is simply our definition from the section above: a graph is a set of vertices.

```python
# pathfinding.py

Graph = set[Vertex]
```

Python has no built-in stack structure in its standard library, so we implement that as well, using a list as the backing storage.
To make sure our stack will work regardless of its content we'll write it as a generic class.
We define `T = TypeVar('T')` near the top of our file, just below the imports.

```python
# pathfinding.py

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: list[T] = []


    def pop(self) -> T:
        return self._container.pop()

    def push(self, t: T) -> None:
        self._container.append(t)
```

We can now implement our first algorithm: depth-first search.
This algorithm will work with the graph structure we've defined.

```python
# pathfinding.py

# DFS
def dfs(graph: Graph, start: Vertex, goal: Vertex) -> Optional[Node]:
    if (start not in graph):
        print('Starting vertex not in graph!')
        return None

    if (goal not in graph):
        print('Goal vertex not in graph!')
        return None


    # We start with no explored vertices and a frontier
    # consisting of just the starting node.
    explored: list[Vertex] = []
    frontier: Stack[Node] = Stack() 
    frontier.push(Node(start))

    # Go through the stack, popping and pushing nodes as described.        
    while not frontier.empty:                                                        
        current_node: Node = frontier.pop()                                          
        current_vertex: Vertex = current_node.vertex                                         
                                                                                        
        if (current_vertex == goal):                           
            return current_node                                
                                                                  
        for neighbor in current_vertex.neighbors:              
            if (neighbor not in explored):
                frontier.push(Node(neighbor, current_node))
                   
        explored.append(current_vertex)
           
    # We didn't find the goal.
    return None
```

The algorithm returns a node containing the goal vertex if it finds a path, and `None` if it doesn't.
Like mentioned above, we'll use this node to construct the path taken.
We start with the goal node and use its parent to work our way backwards.
At the end, we'll have a list of nodes from the start to the goal.
We'll write another function to take this list and print human-readable output describing the path.
Let's put these functions just below our class definitions.

```python
# pathfinding.py

def construct_path(n: Node) -> list[Node]:
    path: list[Node] = [n]

    while (n.parent):
        path.append(n)
        n = n.parent

    return path[::-1]


def print_path(path: list[Node]) -> None:
    s: str = ''

    for i, n in enumerate(path):
        if (i == 0):
            s += f'We start at {n.vertex.name}.'
        else:
            s += f'\nWe go to {n.vertex.name}.'

    print(s)
```

That's it for now for `pathfinding.py`.
We now have to input the graph structure from the image above into our program.
We'll do this in a separate file `examples.py`.
The code to create the graph is not very interesting; we're just translating the image to a graph structure.

```python
# examples.py

from pathfinding import Vertex, Node, Graph, construct_path, print_path, dfs
from typing import Optional

# Create a graph of England.
derby: Vertex        = Vertex([], 'Derby')
nottingham: Vertex   = Vertex([], 'Nottingham')
birmingham: Vertex   = Vertex([], 'Birmingham')
bristol: Vertex      = Vertex([], 'Bristol')
southhampton: Vertex = Vertex([], 'Southhampton')
coventry: Vertex     = Vertex([], 'Coventry')
leicester: Vertex    = Vertex([], 'Leicester')
cambridge: Vertex    = Vertex([], 'Cambridge')
northhampton: Vertex = Vertex([], 'Northhampton')
oxford: Vertex       = Vertex([], 'Oxford')
reading: Vertex      = Vertex([], 'Reading')
london: Vertex       = Vertex([], "London")

inter1: Vertex = Vertex([], 'Intersection 1')
inter2: Vertex = Vertex([], 'Intersection 2')
inter3: Vertex = Vertex([], 'Intersection 3')
inter4: Vertex = Vertex([], 'Intersection 4')
inter5: Vertex = Vertex([], 'Intersection 5')
inter6: Vertex = Vertex([], 'Intersection 6')

inter1.neighbors = [derby, nottingham, leicester, birmingham]
inter2.neighbors = [birmingham, inter3, bristol]
inter3.neighbors = [inter2, coventry, inter5]
inter4.neighbors = [coventry, leicester, cambridge, northhampton]
inter5.neighbors = [inter3, london, oxford]
inter6.neighbors = [bristol, oxford, reading, southhampton]

derby.neighbors = [inter1]
nottingham.neighbors = [inter1]
birmingham.neighbors = [inter1, coventry, inter2]
bristol.neighbors = [inter2, inter6]
southhampton.neighbors = [inter6, london]
coventry.neighbors = [birmingham, leicester, inter4, inter3]
leicester.neighbors = [inter1, inter4, coventry]
cambridge.neighbors = [leicester, london]
northhampton.neighbors = [inter4, london]
oxford.neighbors = [inter5, inter6]
reading.neighbors = [inter6, london]
london.neighbors = [cambridge, northhampton, inter5, reading, southhampton]

graph: Graph = {derby, nottingham, birmingham, bristol, southhampton, coventry,
        leicester, cambridge, northhampton, oxford, reading, london, inter1,
        inter2, inter3, inter4, inter5, inter6}
```

We're now ready to test our new algorithm.
We'll pick London as our starting vertex and Oxford as our goal.
Add the following to the bottom of the file, and run it:

```python
# examples.py

### Test Algorithms ###
# DFS.
print('Testing DFS.')
end_node: Optional[Node] = dfs(graph, london, oxford)
if end_node:
    print_path(construct_path(end_node))
else:
    print('No path found using DFS!')
```

This gives us the output:

```python
Testing DFS.
We start at London.
We go to Southhampton.
We go to Intersection 6.
We go to Oxford.
```

We've successfully found a path from London to Oxford!
You may immediately notice that this is *not* the shortest path.
Indeed, DFS makes no guarantee of finding the shortest path.
It will, however, always find *a* path, if possible.

Its name comes from the fact that it will continue searching down a path until it either reaches the goal, or hits a dead-end.
If it hits a dead-end it backtracks all the way back to the latest vertex with an unexplored edge, and rushes down that path in search of the goal.
This behaviour is caused by using a stack as the backing data structure.
The stack, being LIFO (Last-in, first-out) means the algorithm will always look at the vertices next to the latest node it expanded ("Expanded" meaning marked as explored had its connected vertices added to the frontier).

The advantage of DFS is its speed.
If all you care about is finding *a* path, and do not care about its length, DFS is a good choice.
But we *do* care about path length---we're trying to find the shortest one!
To do this, we must look instead at DFS's cousin: breadth-first search.
BFS (breadth-first search) guarantees finding the shortest path (if one exists) and all we have to do is change the data structure used for the frontier!

## Breadth-first search

While DFS rushes down each path greedily by putting nodes at the top of the frontier, BFS instead puts them last.
This means BFS will "flood-fill" the graph, only moving to connecting vertices when all earlier ones have been explored.
This behavior guarantees finding the shortest path.
To see why, say the shortest path is $n$ nodes long.
In the first iteration, BFS considers all nodes with path-length 1 from the start.
When those are all considered, it moves on to their connected nodes, which lay at a distance 2 from the start.
On and on it goes, until finally it considers nodes with a distance $n$ from the start.
Here it will find the goal, and terminate.
Any nodes further away are never considered, and so the path-length of the path yielded is exactly $n$, the shortest path.

As mentioned, all we have to do to change our DFS to BFS is change the data structure from a stack to a queue.
To do this, we implement a Queue class with Deque as the backing data structure.
We prefer deque here since it allows for efficient pushing of elements to the start (left) of the queue, while a list would require shuffling all the elements down by one.

First we'll add deque at the top of `pathfinding.py`.
```python
# pathfinding.py

from collections import deque
from Typing import Deque
```

Then we'll define our Queue class, putting it just below our Stack class.

```python
#pathfinding.py

class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = deque()


    def pop(self) -> T:
        return self._container.pop()


    def push(self, t: T) -> None:
        self._container.appendleft(t)


    @property
    def empty(self) -> bool:
        return not self._container
```

Now we copy the code from our DFS function, changing only the data structure from a stack to a queue, and we're done!

```python
# BFS.
def bfs(graph: Graph, start: Vertex, goal: Vertex) -> Optional[Node]:
    if (start not in graph):
        print('Starting vertex not in graph!')
        return None

    if (goal not in graph):
        print('Goal vertex not in graph!')
        return None

    # We start with no explored vertices and a frontier
    # consisting of just the starting node.
    explored: list[Vertex] = []
    frontier: Queue[Node] = Queue()
    frontier.push(Node(start))             

    # Go through the stack, popping and pushing nodes as described.  
    while not frontier.empty:
        current_node: Node = frontier.pop()
        current_vertex: Vertex = current_node.vertex

        if (current_vertex == goal):
            return current_node

        for neighbor in current_vertex.neighbors:
            if (neighbor not in explored):
                frontier.push(Node(neighbor, current_node))

        explored.append(current_vertex)

    # We didn't find the goal.
    return None
```

Let's go back to `examples.py` and add in code to test our new algorithm.
First we must import it.

```python
# examples.py
from pathfinding import bfs
```

Next we add the bit to run the algorithm, using the same graph as before.

```python
# examples.py

print('Testing BFS.')
end_node = bfs(graph, london, oxford)
if end_node:
    print_path(construct_path(end_node))
else:
    print('No path found using BFS!')
```

Running this gives us:

```python
Testing BFS.
We start at London.
We go to Intersection 5.
We go to Oxford.
```

We've successfully found the shortest path from London to Oxford!
We pat ourselves on the back, grab a snack, and start planning our vacation.
But alas, our boss comes along: "Sure, this is the shortest path by *number of intersections*, but what people actually want is the *shortest time taken*."
Agh!
What he says is true.
So far, we've been counting path-length by the number of vertices.
In many real-world applications this is not enough.
Getting from one vertex to another is not always equally "costly": it may take more time, the terrain might be difficult, there could be heavy traffic, and so on.
We represent this by adding a "cost" to each of the edges.
This, in our example, will represent the time taken to utilize that road.
But the concept of edges having a cost can represent many other things, for instance, in a video game, you may wish to have NPCs disfavor using certain paths and prefer others.
You could also use cost to represent different widths of pipe for fluids to travel down.

By adding costs to the edges of our graph it becomes something new: a weighted graph.
Unfortunately, neither BFS nor DFS are equipped to handle weighted graphs.
They naively either insert new nodes at the top or bottom of the frontier and do not take account of any cost.
We'll need a new data structure to handle this new scenario: the priority queue.
With it, we'll also arrive at our next algorithm: Dijktra's algorithm.

## Dijkstra's Algorithm

The idea behind Dijktra's algorithm (which I'll be referring to simply as "Dijktra" from now on) is rather simple.
The order we expand the nodes in is given by the total cost of getting to that node, starting with the lowest-cost one.
Thus, when looking at the vertices connecting to the one we're considering, each of them will get a total cost of whatever it costed us to get to the current node, plus the cost of each edge, respectively.

A weighted version of the graph we've been using so far might look like this:

![weighted graph](/weighted-graph.png)

Here I have arbitrarily chosen the weights to get a different path than before.
By weighting the direct paths very heavily (suppose, say, a traffic jam) we will see Dijkstra take a longer, but ultimately quicker, path.

We have to modify our Vertex class to support weighted edges.
We do this by introducing a new named tuple, which consists of a vertex together with a weight.
To work with named tuples we need to import the appropriate package.

```python
# pathfinding.py

from collections import namedtuple

Edge = namedtuple('Edge', ['vertex', 'weight'])
```

We also change our Vertex class' `__init__` definition to use this new edge structure.

```python
class Vertex:
    def __init__(self, edges: list[Edge], name: str) -> None:
        self.edges: list[Edge] = edges
        self.name: str = name

    ...
```

We update the code where we define our graph to reflect the weighted graph above[^2]:

[^2]: Actually, the graph we will define is a weighted *directed* graph. But because we will use the same weight in both directions this will be equivalent to an undirected graph.

```python
# examples.py

# Create a graph of England.
S = Edge(None, 0)
derby: Vertex        = Vertex([S], "Derby")
nottingham: Vertex   = Vertex([S], "Nottingham")
birmingham: Vertex   = Vertex([S], "Birmingham")
bristol: Vertex      = Vertex([S], "Bristol")
southhampton: Vertex = Vertex([S], "Southhampton")
coventry: Vertex     = Vertex([S], "Coventry")
leicester: Vertex    = Vertex([S], "Leicester")
cambridge: Vertex    = Vertex([S], "Cambridge")
northhampton: Vertex = Vertex([S], "Northhampton")
oxford: Vertex       = Vertex([S], "Oxford")
reading: Vertex      = Vertex([S], "Reading")
london: Vertex       = Vertex([S], "London")

inter1: Vertex = Vertex([S])
inter2: Vertex = Vertex([S])
inter3: Vertex = Vertex([S])
inter4: Vertex = Vertex([S])
inter5: Vertex = Vertex([S])
inter6: Vertex = Vertex([S])

inter1.edges = [Edge(derby, 5), Edge(nottingham, 5), Edge(leicester, 10), Edge(birmingham, 3)]
inter2.edges = [Edge(birmingham, 3), Edge(inter3, 2), Edge(bristol, 5)]
inter3.edges = [Edge(inter2, 2), Edge(coventry, 5), Edge(inter5, 2)]
inter4.edges = [Edge(coventry, 15), Edge(leicester, 15), Edge(cambridge, 5), Edge(northhampton, 2)]
inter5.edges = [Edge(inter3, 2), Edge(london, 100), Edge(oxford, 2)]
inter6.edges = [Edge(bristol, 2), Edge(oxford, 2), Edge(reading, 100), Edge(southhampton, 3)]

derby.edges = [Edge(inter1, 5)]
nottingham.edges = [Edge(inter1, 5)]
birmingham.edges = [Edge(inter1, 3), Edge(coventry, 2), Edge(inter2, 3)]
bristol.edges = [Edge(inter2, 5), Edge(inter6, 2)]
southhampton.edges = [Edge(inter6, 3)]
coventry.edges = [Edge(birmingham, 2), Edge(leicester, 5), Edge(inter4, 15), Edge(inter3, 5)]
leicester.edges = [Edge(inter1, 10), Edge(inter4, 15), Edge(coventry, 5)]
cambridge.edges = [Edge(inter4, 15), Edge(london, 5)]
northhampton.edges = [Edge(inter4, 2), Edge(london, 2)]
oxford.edges = [Edge(inter5, 2), Edge(inter6, 2)]
reading.edges = [Edge(inter6, 100), Edge(london, 5)]
london.edges = [Edge(cambridge, 5), Edge(northhampton, 2), Edge(inter5, 100), Edge(reading, 5)]

graph: Graph = {derby, nottingham, birmingham, bristol, southhampton, coventry,
        leicester, cambridge, northhampton, oxford, reading, london, inter1,
        inter2, inter3, inter4, inter5, inter6}
```

We also have to import this new edge structure at the top of `examples.py`.

```python
# examples.py

from pathfinding import Edge
```

And we also change the DFS and BFS code to use this more general Vertex.
They will simply ignore any weight information; treating a weighted graph as an unweighted one.
To do this we just extract the neighboring vertex from each edge inside the for-loop and throw away any weight information.

```python
# pathfinding.py

# DFS
def dfs(graph: Graph, start: Vertex, goal: Vertex) -> Optional[Node]:
...
        for edge in current_vertex.edges:
            neighbor: Vertex = edge.vertex
            ...

...

# BFS
def bfs(graph: Graph, start: Vertex, goal: Vertex) -> Optional[Node]:
...
        for edge in current_vertex.edges:
            neighbor: Vertex = edge.vertex
            ...
```


Make sure to rerun the code to make sure the old DFS and BFS algorithms still work.

The data structure that makes Dijkstra tick is the priority queue, which we'll implement in `pathfinding.py` next to our other classes.
A priority queue works like the name implies.
We can push element like normal to it, but when doing so we must also assign that element a priority.
When popping elements the element with the *lowest* priority will be popped off and returned.
Of course, one can also implement a priority queue which pops off the highest priority elements.
We'll store the element and priority as a tuple, so we need to import the type hints for tuples as well.

```python
# pathfinding.py

from typing import Tuple
```

```python
# pathfinding.py

class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: list[Tuple[T, float]] = []


    def push(self, t: T, w: float) -> None:
        self._container.append((t, w))
        self._container.sort(key=lambda x: x[1], reverse=True)


    def pop(self) -> Tuple[T, float]:
        return self._container.pop()


    @property
    def empty(self) -> bool:
        return not self._container


    # We implement a string representation for demonstrating A-star later on.
    def __str__(self) -> str:
        return str(self._container)
```

Our frontier will use a priority queue, where we keep track of nodes as well as the cost of getting from the start to that node.
Normally in Dijkstra you would keep track of which vertices are in your frontier, and make sure to overrite the parent vertex as well as the total cost if you found a new path to that vertex with a lower cost.
Because we are keeping nodes in our frontier, which have parent information baked-in, we don't have to do this.

```python
# pathfinding.py

# Dijkstra.
def dijkstra(graph: Graph, start: Vertex, goal: Vertex) -> Optional[Node]:
    if (start not in graph):
        print('Starting vertex not in graph!')
        return None

    if (goal not in graph):
        print('Goal vertex not in graph!')
        return None

    # We start with no explored vertices and a frontier
    # consisting of just the starting node.
    explored: list[Vertex] = []
    frontier: PriorityQueue[Node] = PriorityQueue()
    frontier.push(Node(start), 0)

    while not frontier.empty:
        current_node: Node
        current_weight: float
        current_node, current_weight = frontier.pop()
        current_vertex: Vertex = current_node.vertex

        if (current_vertex == goal):
            return current_node

        for edge in current_vertex.edges:
            neighbor: Vertex = edge.vertex
            if (neighbor not in explored):
                frontier.push(Node(neighbor, current_node), edge.weight + current_weight)

        explored.append(current_vertex)

    # We didn't find the goal!
    return None
```

We add some code to `examples.py` to run Dijkstra:

```python
# examples.py
from pathfinding import dijkstra

...

# Dijkstra.
print('Testing Dijkstra.')
end_node = dijkstra(graph, london, oxford)
if end_node:
    print_path(construct_path(end_node))
else:
    print('No path found using Dijkstra!')
```

Running the code yields:

```python
Testing Dijkstra.
We start at London.
We go to Northhampton.
We go to Intersection 4.
We go to Coventry.
We go to Intersection 3.
We go to Intersection 5.
We go to Oxford.
```

As we can see, Dijkstra is a powerful and flexible algorithm.
In fact, it is the basis for most pathfinding algorithms in use today, and the basis for much of the research being done in the area.
There is one small refinement we can make to it, however.
The issue with Dijkstra is that it always expands the shortest path first, and doesn't consider whether or not we're going in the correct direction.
This is what A* attempts to solve.

## A-Star

Consider the example below:

![pernicious-example](/pernicious.png)

Suppose we start at the left vertex, and our goal is the vertex at the top.
Dijkstra will run down towards the right, and keep going, until the total cost exceeds 21, at which point it will finally expand the top node---finding the goal.

Let's create this new graph in `examples.py` and try to run Dijkstra on it to see this.

```python
# examples.py

# Construct a pernicious graph.
A: Vertex = Vertex([S], 'A')
B: Vertex = Vertex([S], 'B')
C: Vertex = Vertex([S], 'C')
D: Vertex = Vertex([S], 'D')
E: Vertex = Vertex([S], 'E')
F: Vertex = Vertex([S], 'F')
G: Vertex = Vertex([S], 'G')
H: Vertex = Vertex([S], 'H')
I: Vertex = Vertex([S], 'I')
J: Vertex = Vertex([S], 'J')

A.edges = [Edge(C, 5)]
B.edges = [Edge(C, 1)]
C.edges = [Edge(B, 1), Edge(D, 1), Edge(A, 5)]
D.edges = [Edge(C, 1), Edge(E, 1)]
E.edges = [Edge(D, 1), Edge(F, 1)]
F.edges = [Edge(E, 1), Edge(G, 1)]
G.edges = [Edge(F, 1), Edge(H, 1)]
H.edges = [Edge(G, 1), Edge(I, 1)]
I.edges = [Edge(H, 1), Edge(J, 1)]
J.edges = [Edge(I, 1)]

graph2: Graph = {A, B, C, D, E, F, G, H, I, J}

...

# Dijkstra on Graph 2.
print('Testing Dijkstra on Graph 2')
end_node = dijkstra(graph2, B, A)
if end_node:
    print_path(construct_path(end_node))
else:
    print('No path found using Dijkstra on Graph 2!')
```

We also make sure to append this line to our implementation of Dijkstra in `pathfinding.py`, so that we can see which nodes the algorithm is considering:

```python
# pathfinding.py

...
def dijkstra(graph: Graph, start: Vertex, goal: Vertex) -> Optional[Node]:
    ...

    while not frontier.empty:
        print(frontier)
        ...
```

If we now run the code we'll see the following:

```python
Testing Dijkstra on Graph 2
[(<pathfinding.Node object at 0x7efc42ec08b0>, 0)]
[(<pathfinding.Node object at 0x7efc42ec0670>, 1)]
[(<pathfinding.Node object at 0x7efc42ec1180>, 6), (<pathfinding.Node object at 0x7efc42ec0880>, 2)]
[(<pathfinding.Node object at 0x7efc42ec1180>, 6), (<pathfinding.Node object at 0x7efc42ec05e0>, 3)]
[(<pathfinding.Node object at 0x7efc42ec1180>, 6), (<pathfinding.Node object at 0x7efc42ec1060>, 4)]
[(<pathfinding.Node object at 0x7efc42ec1180>, 6), (<pathfinding.Node object at 0x7efc42ec0760>, 5)]
[(<pathfinding.Node object at 0x7efc42ec1180>, 6), (<pathfinding.Node object at 0x7efc42ec06d0>, 6)]
[(<pathfinding.Node object at 0x7efc42ec12a0>, 7), (<pathfinding.Node object at 0x7efc42ec1180>, 6)]
We start at B.
We go to C.
We go to A.
```

As you can see Dijkstra did indeed find the shortest path.
However, to do so it had to travel quite a few nodes to the right.
This is inefficient.

We want to capture the fact that as we get further from the goal we should increase the cost, so as to punish behavior like this.
We do this through a *heuristic*, a kind of guess on what the total cost is to get from where we are to the goal.
Put another way, it's our guess of how much additional cost it would take to complete the current path.
Of course, we don't know the exact cost, but a good-enough guess that is as close to the real cost as possible, without going over (so called "admissible"---more on this later) will make sure we don't run away like this.

The heurstic is a function that takes two vertices and returns a real number.
However, when the goal is fixed we often omit the goal as one of the parameters, which we'll do here.

The new cost function $f$ for our priority queue for a node $n$ will therefore be the sum of the cost so far and our guessed remaining cost, that is, $f(n) = g(n) + h(n)$, where $g(n)$ is the cost from the start to the current node $n$, i.e. the current running total cost of the path we are considering, and $h(n)$ is our heuristic---guess---of the cost of getting from $n$ to the goal.

One can either precompute the heuristic from any node to the goal (or, indeed, from any node to any other node if the start and goal are apt to change) or one may compute it one the fly.
In our case we shall precompute the cost.

A-star has the property that if the heuristic is admissible, we are guaranteed to find the shortest path.
Otherwise, we may overestimate the cost and thus overlook the shortest path, thinking it more expensive than what it really is.
Here's a short proof on why an admissible heuristic guarantees finding the shortest path:

PROOF HERE

The burning question is how to define $h$.
A good first heuristic would be the Euclidean distance between two vertices.
This makes sense in our map-example.
However, we will actually use a much simpler heuristic to demonstrate the concept on this new graph.
We shall simply let it be the number of vertices between the current node and the goal.
Again, just as a weighted graph may be directed, so too a heuristic can be.
If $A$ and $B$ are nodes, it is not necessarily true that $h(A, B) = h(B, A)$.
However, in our case it will be.

We'll define the Heuristic type, making sure to put it below our class definition of Vertex:

```python
# pathfinding.py
...
Heuristic = dict[tuple[Vertex, Vertex], float]
...
```

```python
# examples.py
from pathfinding import Heuristic

...

heuristic: dict[tuple[Vertex, Vertex], float]  = {} 
heuristic[(A, A)] = heuristic[(A, A)] = 0
heuristic[(B, A)] = heuristic[(A, B)] = 1
heuristic[(C, A)] = heuristic[(A, C)] = 2
heuristic[(D, A)] = heuristic[(A, D)] = 3
heuristic[(E, A)] = heuristic[(A, E)] = 4
heuristic[(F, A)] = heuristic[(A, F)] = 5
heuristic[(G, A)] = heuristic[(A, G)] = 6
heuristic[(H, A)] = heuristic[(A, H)] = 7
heuristic[(I, A)] = heuristic[(I, H)] = 8
heuristic[(J, A)] = heuristic[(J, H)] = 9
```

Let's now actually implement A-star.
We take Dijkstra as our base, and then all we need to do is modify the weight we pass to the frontier when pushing nodes onto it.

```python
def astar(graph: Graph, start: Vertex, goal: Vertex) -> Optional[Node]:
    if (start not in graph):
        print('Starting vertex not in graph!')
        return None

    if (goal not in graph):
        print('Goal vertex not in graph!')
        return None

    # We start with no explored vertices and a frontier
    # consisting of just the starting node.
    explored: list[Vertex] = []
    frontier: PriorityQueue[Node] = PriorityQueue()
    frontier.push(Node(start), 0)

    while not frontier.empty:
        print(frontier)
        current_node: Node
        current_weight: float
        current_node, current_weight = frontier.pop()
        current_vertex: Vertex = current_node.vertex

        if (current_vertex == goal):
            return current_node

        for edge in current_vertex.edges:
            neighbor: Vertex = edge.vertex
            if (neighbor not in explored):
                frontier.push(Node(neighbor, current_node), edge.weight + current_weight + heuristic[(current_vertex, goal)])

        explored.append(current_vertex)

    # We didn't find the goal!
    return None
```

As you can see, only one line differs: the one where we add the heursitic cost to the new node in the priority queue.
Let's try running A* on our new graph, and see how it performs.

```python
# examples.py
from pathfinding import astar

...

# A-star on Graph 2.
print('Testing A* on Graph 2')
end_node = astar(graph2, B, A, heuristic)
if end_node:
    print_path(construct_path(end_node))
else:
    print('No path found using A* on Graph 2!')
```

This gives us the output:

```python
Testing A* on Graph 2
[(<pathfinding.Node object at 0x7fb0d4865b40>, 0)]
[(<pathfinding.Node object at 0x7fb0d4865570>, 2)]
[(<pathfinding.Node object at 0x7fb0d48658a0>, 9), (<pathfinding.Node object at 0x7fb0d48656c0>, 5)]
[(<pathfinding.Node object at 0x7fb0d48658a0>, 9), (<pathfinding.Node object at 0x7fb0d48652d0>, 9)]
[(<pathfinding.Node object at 0x7fb0d4865540>, 14), (<pathfinding.Node object at 0x7fb0d48658a0>, 9)]
We start at B.
We go to C.
We go to A.
```

As we can see, A-star considered fewer nodes.
The heuristic correctly punished the algorithm for getting too far off-track, by weighting the nodes far away more heavily.
As long as the heuristic is quick to compute, this often leads to an increase in speed of execution.

