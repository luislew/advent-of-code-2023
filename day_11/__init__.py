import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

"""
--- Day 11: Cosmic Expansion ---

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input).
The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies.
However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact,
the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found.
It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter.
For each pair, find any shortest path between the two galaxies using only steps that move up, down, left,
or right exactly one . or # at a time.
(The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......

This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9
(the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5

In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies.
What is the sum of these lengths?

--- Part Two ---

The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger.
That is, each empty row should be replaced with 1000000 empty rows,
and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger,
the sum of the shortest paths between every pair of galaxies would be 1030.
If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies
would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules,
then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""

def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


class Image:
    def __init__(self, lines, expansion_const=1):
        self.lines = lines
        self.expansion_const = expansion_const
        self.starting_width = len(self.lines[0])
        self.empty_row_idxs = [y for y, line in enumerate(self.lines) if "#" not in line]
        self.empty_col_idxs = [x for x in range(self.starting_width) if "#" not in [line[x] for line in self.lines]]
        self.galaxies = self.get_galaxies()
        self.height = len(lines)
        self.width = len(lines[0])

    def get_galaxies(self):
        # Get coordinates of all galaxies
        return [
            (x, y)
            for y, line in enumerate(self.lines)
            for x, char in enumerate(line)
            if char == "#"
        ]

    def get_shortest_length(self, galaxy1, galaxy2):
        # Get shortest path between two galaxies, accounting for expanded map
        x1, y1 = galaxy1
        x2, y2 = galaxy2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        width = x2 - x1
        height = y2 - y1
        empty_cols_count = sum(1 for x in self.empty_col_idxs if x1 < x < x2)
        empty_rows_count = sum(1 for y in self.empty_row_idxs if y1 < y < y2)
        return (width + empty_cols_count * self.expansion_const) + (height + empty_rows_count * self.expansion_const)
