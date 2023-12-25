import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

"""
--- Day 13: Point of Incidence ---

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input);
perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

To find the reflection in each pattern, you need to find a perfect reflection
across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns;
arrows on each of the two columns point at the line between the columns:

123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789

In this pattern, the line of reflection is the vertical line between columns 5 and 6.
Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1)
has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern
and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7

This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8,
but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match:
row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection;
to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example,
the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it,
a total of 405.

Find the line of reflection in each of the patterns in your notes.
What number do you get after summarizing all of your notes?

--- Part Two ---

You resume walking through the valley of mirrors and - SMACK! - run directly into one.
Hopefully nobody was watching, because that must have been pretty embarrassing.

Upon closer inspection, you discover that every mirror has exactly one smudge:
exactly one . or # should be the opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid.
(The old reflection line won't necessarily continue being valid after the smudge is fixed.)

Here's the above example again:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

The first pattern's smudge is in the top-left corner. If the top-left # were instead .,
it would have a different, horizontal line of reflection:

1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7

With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows 3 and 4 now exists.
Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly:
row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:

1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7

Now, the pattern has a different horizontal line of reflection between rows 1 and 2.

Summarize your notes as before, but instead use the new different reflection lines.
In this example, the first pattern's new horizontal line has 3 rows above it
and the second pattern's new horizontal line has 1 row above it, summarizing to the value 400.

In each pattern, fix the smudge and find the different line of reflection.
What number do you get after summarizing the new reflection line in each pattern in your notes?
"""


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


def parse_lines():
    lines = []
    maps = []
    for line in get_lines():
        if line:
            lines.append(line)
        else:
            maps.append(Map(lines))
            lines = []

    maps.append(Map(lines))
    return maps


def is_off_by_one(array1, array2):
    return sum(1 for a, b in zip(array1, array2) if a != b) == 1


class Map:
    def __init__(self, lines):
        self.lines = lines
        self.height = len(lines)
        self.width = len(lines[0])
        self.map = {
            (x, y): lines[y][x] for x in range(self.width) for y in range(self.height)
        }

    def __repr__(self):
        return "\n".join(self.lines)

    def get_column(self, x):
        return [self.map[(x, y)] for y in range(self.height)]

    def get_row(self, y):
        return [self.map[(x, y)] for x in range(self.width)]

    def is_vertical_reflection(self, x, with_smudge=False):
        # x is the line between columns x - 1 and x
        pairs_to_check = [
            (x - 1 - i, x + i)
            for i in range(self.width)
            if x - 1 - i >= 0 and x + i < self.width
        ]
        if with_smudge:
            off_by_ones_count = 0
            for x1, x2 in pairs_to_check:
                column1 = self.get_column(x1)
                column2 = self.get_column(x2)
                if column1 == column2:
                    continue
                elif is_off_by_one(column1, column2):
                    off_by_ones_count += 1
                else:
                    return False
            return off_by_ones_count == 1

        return all(
            self.get_column(x1) == self.get_column(x2) for x1, x2 in pairs_to_check
        )

    def is_horizontal_reflection(self, y, with_smudge=False):
        # y is the line between rows y - 1 and y
        pairs_to_check = [
            (y - 1 - i, y + i)
            for i in range(self.height)
            if y - 1 - i >= 0 and y + i < self.height
        ]
        if with_smudge:
            off_by_ones_count = 0
            for y1, y2 in pairs_to_check:
                row1 = self.get_row(y1)
                row2 = self.get_row(y2)
                if row1 == row2:
                    continue
                elif is_off_by_one(self.get_row(y1), self.get_row(y2)):
                    off_by_ones_count += 1
                else:
                    return False
            return off_by_ones_count == 1

        return all(self.get_row(y1) == self.get_row(y2) for y1, y2 in pairs_to_check)

    def find_reflection(self, with_smudge=False):
        # Look for a vertical line of symmetry
        for x in range(1, self.width):
            if self.is_vertical_reflection(x, with_smudge):
                return x, 0
        for y in range(1, self.height):
            if self.is_horizontal_reflection(y, with_smudge):
                return 0, y
        return None
