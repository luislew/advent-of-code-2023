import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

import sys

r"""
--- Day 16: The Floor Will Be Lava ---

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....

The beam enters in the top-left corner from the left and heading to the right.
Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror.
For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column,
while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter
as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter
would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams
going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam
that encounters a | splitter would split into two beams: one that continues upward from the splitter's column
and one that continues downward from the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through it at the same time.
A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..

Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams
moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram
but instead only showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..

Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start
by analyzing the current situation. With the beam starting in the top-left heading right,
how many tiles end up being energized?

--- Part Two ---

As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel.
There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile
and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner;
for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward),
any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left).
To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..

Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..

Find the initial beam configuration that energizes the largest number of tiles;
how many tiles are energized in that configuration?
"""

# Avoid `RecursionError: maximum recursion depth exceeded in comparison`
sys.setrecursionlimit(10000)

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


class Layout:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)
        self.map = {
            (x, y): lines[y][x]
            for x in range(self.width)
            for y in range(self.height)
        }
        self.energized = set()
        self.traversed = set()

    def __str__(self):
        return "\n".join(self.lines)

    def __repr__(self):
        return self.__str__()

    def get_square(self, x, y):
        if x < 0 or y < 0 or x > (self.width - 1) or y > (self.height - 1):
            return None
        return self.map[(x, y)]

    def get_next_square(self, x, y, direction):
        """Given a beam with direction, return the next square it will hit."""
        square = self.get_square(x, y)
        if not square:
            return None

        if square == ".":
            return [(x + direction[0], y + direction[1], direction)]
        elif square == "|" and direction in (NORTH, SOUTH):
            return [(x + direction[0], y + direction[1], direction)]
        elif square == "-" and direction in (EAST, WEST):
            return [(x + direction[0], y + direction[1], direction)]
        elif square == "/":
            if direction == NORTH:
                return [(x + 1, y, EAST)]
            elif direction == SOUTH:
                return [(x - 1, y, WEST)]
            elif direction == EAST:
                return [(x, y - 1, NORTH)]
            elif direction == WEST:
                return [(x, y + 1, SOUTH)]
        elif square == "\\":
            if direction == NORTH:
                return [(x - 1, y, WEST)]
            elif direction == SOUTH:
                return [(x + 1, y, EAST)]
            elif direction == EAST:
                return [(x, y + 1, SOUTH)]
            elif direction == WEST:
                return [(x, y - 1, NORTH)]
        # We've hit a splitter
        elif square == "|":
            return [(x, y + 1, SOUTH), (x, y - 1, NORTH)]
        elif square == "-":
            return [(x + 1, y, EAST), (x - 1, y, WEST)]

    def energize_squares(self, x=0, y=0, direction=EAST):
        self.traversed.add((x, y, direction))
        if not self.get_square(x, y):
            return

        self.energized.add((x, y))
        next_square = self.get_next_square(x, y, direction)
        if not next_square:
            return
        return [
            self.energize_squares(*square)
            for square in next_square
            if square not in self.traversed
        ]

    def reset(self):
        self.energized = set()
        self.traversed = set()
