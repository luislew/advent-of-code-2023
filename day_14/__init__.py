import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

"""
--- Day 14: Parabolic Reflector Dish ---

The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place.
You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....

You notice that the support beams along the north side of the platform are damaged;
to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock
to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.)
So, the amount of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1

The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north.
Afterward, what is the total load on the north support beams?

--- Part Two ---

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east.
After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction.
After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:

.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:

.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:

.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O

This process should work if you leave it running long enough, but you're still worried about the north support beams.
To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?
"""


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


class Map:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = len(lines[0])
        self.map = {}
        self.fixed_rocks_by_column = {}
        self.fixed_rocks_by_row = {}
        for y in range(self.height):
            for x in range(self.width):
                char = lines[y][x]
                if char != ".":
                    self.map[(x, y)] = char
                if char == "#":
                    self.fixed_rocks_by_column.setdefault(x, []).append(y)
                    self.fixed_rocks_by_row.setdefault(y, []).append(x)

    def __repr__(self):
        return "\n".join(
            "".join(self.get_square(x, y) for x in range(self.width))
            for y in range(self.height)
        )

    def get_square(self, x, y):
        return self.map.get((x, y), ".")

    def get_rolling_rocks(self):
        return tuple((x, y) for (x, y), c in self.map.items() if c == "O")

    def tilt_column(self, x, up=True):
        fixed_indexes = self.fixed_rocks_by_column.get(x, [])
        round_stone_indexes = []
        if up:
            for y in range(self.height):
                rock = self.get_square(x, y)
                if rock == "O":
                    # Find the first fixed index below this one
                    new_y = 0
                    for idx in reversed(fixed_indexes):
                        if idx < y:
                            if not round_stone_indexes:
                                new_y = idx + 1
                            else:
                                new_y = max(idx, round_stone_indexes[-1][1]) + 1
                            break
                    else:
                        # No fixed index below this one
                        if round_stone_indexes:
                            new_y = round_stone_indexes[-1][1] + 1
                    round_stone_indexes.append((y, new_y))
        else:
            for y in reversed(range(self.height)):
                rock = self.get_square(x, y)
                if rock == "O":
                    # Find the first fixed index above this one
                    new_y = self.height - 1
                    for idx in fixed_indexes:
                        if idx > y:
                            if not round_stone_indexes:
                                new_y = idx - 1
                            else:
                                new_y = min(idx, round_stone_indexes[-1][1]) - 1
                            break
                    else:
                        # No fixed index above this one
                        if round_stone_indexes:
                            new_y = round_stone_indexes[-1][1] - 1
                    round_stone_indexes.append((y, new_y))

        for y, new_y in round_stone_indexes:
            if y != new_y:
                self.map[(x, new_y)] = self.map.pop((x, y))

    def tilt_row(self, y, left=True):
        fixed_indexes = self.fixed_rocks_by_row.get(y, [])
        round_stone_indexes = []
        if left:
            for x in range(self.width):
                rock = self.get_square(x, y)
                if rock == "O":
                    # Find the first fixed index below this one
                    new_x = 0
                    for idx in reversed(fixed_indexes):
                        if idx < x:
                            if not round_stone_indexes:
                                new_x = idx + 1
                            else:
                                new_x = max(idx, round_stone_indexes[-1][1]) + 1
                            break
                    else:
                        # No fixed index below this one
                        if round_stone_indexes:
                            new_x = round_stone_indexes[-1][1] + 1
                    round_stone_indexes.append((x, new_x))
        else:
            for x in reversed(range(self.width)):
                rock = self.get_square(x, y)
                if rock == "O":
                    # Find the first fixed index above this one
                    new_x = self.width - 1
                    for idx in fixed_indexes:
                        if idx > x:
                            if not round_stone_indexes:
                                new_x = idx - 1
                            else:
                                new_x = min(idx, round_stone_indexes[-1][1]) - 1
                            break
                    else:
                        # No fixed index above this one
                        if round_stone_indexes:
                            new_x = round_stone_indexes[-1][1] - 1
                    round_stone_indexes.append((x, new_x))

        for x, new_x in round_stone_indexes:
            if x != new_x:
                self.map[(new_x, y)] = self.map.pop((x, y))

    def cycle(self):
        for x in range(self.width):
            self.tilt_column(x)
        for y in range(self.height):
            self.tilt_row(y)
        for x in range(self.width):
            self.tilt_column(x, up=False)
        for y in range(self.height):
            self.tilt_row(y, left=False)

    def get_total_load(self):
        return sum(self.height - y for (x, y), c in self.map.items() if c == "O")
