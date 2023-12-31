import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

import sys
from operator import itemgetter

"""
--- Day 18: Lavaduct Lagoon ---

However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan
(your puzzle input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)

The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D),
left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above,
so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that
the edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#)
having been dug out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######

At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon;
the next step is to dig out the interior so that it is one meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######

Now, the lagoon can contain a much more respectable 62 cubic meters of lava.
While the interior is dug out, the edges are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan,
how many cubic meters of lava could it hold?
"""

DIRECTIONS = {
    "U": (0, -1),
    "D": (0, 1),
    "R": (1, 0),
    "L": (-1, 0),
}


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


def parse_lines():
    for line in get_lines():
        direction, distance, color = line.split(" ")
        yield direction, int(distance), color[1:-1]


class Lagoon:
    def __init__(self):
        self.trench = []
        self.position = (0, 0)

    def process_step(self, direction, distance):
        vector = DIRECTIONS[direction]
        for _ in range(distance):
            self.position = (self.position[0] + vector[0], self.position[1] + vector[1])
            self.trench.append(self.position)

    def fill_trench(self):
        self.trench.sort(key=itemgetter(1))
        fills = []
        inside = True
        last_x, last_y = self.trench[0]
        for x, y in self.trench[1:]:
            if last_y == y:
                if x != last_x + 1:
                    if inside:
                        for fill_x in range(last_x + 1, x):
                            fills.append((fill_x, y))
                    inside = not inside
            else:
                inside = True
            last_x, last_y = x, y

        return self.trench + fills
