import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

"""
--- Day 10: Pipe Maze ---

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile,
but your sketch doesn't show what shape the pipe has. Based on the acoustics of the animal's scurrying,
you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
"""

PP_CHAR_MAP = {
    "|": "│",
    "-": "─",
    "L": "└",
    "J": "┘",
    "7": "┐",
    "F": "┌",
    "S": "└",
    ".": "·"
}

def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


class Grid:
    def __init__(self):
        self.start = None
        self.width = self.height = 0
        self.map = {}
        for y, line in enumerate(get_lines()):
            for x, char in enumerate(line):
                self.width = max(self.width, x + 1)
                self.height = max(self.height, y + 1)
                self.map[(x, y)] = char
                if char == "S":
                    self.start = (x, y)

    def get_square(self, x, y):
        if x < 0 or y < 0 or x > (self.width - 1) or y > (self.height - 1):
            return None
        return self.map[(x, y)]

    def get_adjoining_squares(self, x, y):
        square = self.get_square(x, y)
        if square == "|":
            return [(x, y - 1), (x, y + 1)]
        elif square == "-":
            return [(x - 1, y), (x + 1, y)]
        elif square == "L":
            return [(x, y - 1), (x + 1, y)]
        elif square == "J":
            return [(x, y - 1), (x - 1, y)]
        elif square == "7":
            return [(x, y + 1), (x - 1, y)]
        elif square == "F":
            return [(x, y + 1), (x + 1, y)]
        elif square == ".":
            return []
        elif square == "S":
            # Find surrounding squares that "fit"
            adjoining_squares = []
            above = self.get_square(x, y - 1)
            below = self.get_square(x, y + 1)
            left = self.get_square(x - 1, y)
            right = self.get_square(x + 1, y)
            if above in "|7F":
                adjoining_squares.append((x, y - 1))
            if below in "|LJ":
                adjoining_squares.append((x, y + 1))
            if left in "-LF":
                adjoining_squares.append((x - 1, y))
            if right in "-7J":
                adjoining_squares.append((x + 1, y))
            return adjoining_squares

    def get_main_loop(self):
        """Returns a list of coordinates for the squares that make up the main loop"""
        main_loop = []
        current_square = self.start
        previous_square = None
        while current_square not in main_loop:
            main_loop.append(current_square)
            adjoining_squares = self.get_adjoining_squares(*current_square)
            adjoining_square = adjoining_squares[0] if adjoining_squares[0] != previous_square else adjoining_squares[1]
            previous_square = current_square
            current_square = adjoining_square
        return main_loop
