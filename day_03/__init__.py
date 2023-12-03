import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

from typing import Tuple


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


def is_symbol(char):
    if char is None or char.isdigit() or char == ".":
        return False
    return True


class Schematic:
    def __init__(self, lines):
        self.lines = lines
        self.height = len(lines)
        self.width = len(lines[0])
        self.numbers_by_coordinates = {
            tuple(coordinates): number
            for coordinates, number in self.get_numbers_by_coordinates()
        }

    def __iter__(self):
        return iter(self.lines)

    def __str__(self):
        return "\n".join(self.lines)

    def get_square(self, x, y):
        if x < 0 or y < 0 or x > (self.width - 1) or y > (self.height - 1):
            return None
        return self.lines[y][x]

    @staticmethod
    def get_surrounding_squares(xy0: Tuple[int, int], xy1: Tuple[int, int]):
        """
        Returns a list of coordinates for the squares surrounding the line between xy0 and xy1

        .....
        .123.
        .....

        In the example, xy0 is (1, 1) and xy1 is (3, 1). The surrounding squares are:

            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
            (0, 1), (4, 1)
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)

        """
        x0, y0 = xy0
        x1, y1 = xy1
        assert y0 == y1, "Lines must be horizontal"
        candidate_squares = [(x0 - 1, y0), (x1 + 1, y0)]
        for x in range(x0 - 1, x1 + 2):
            candidate_squares.append((x, y0 - 1))
            candidate_squares.append((x, y0 + 1))
        return candidate_squares

    def get_number(self, x, y):
        """Checks for a matching number at the given coordinate, and returns the coordinates and number if found"""
        for coordinates, number in self.numbers_by_coordinates.items():
            if (x, y) in coordinates:
                return coordinates, number

    def get_gear_ratio(self, x, y) -> int:
        """Look for exactly two numbers in surrounding squares, and return the product of their values if found"""
        surrounding_squares = self.get_surrounding_squares((x, y), (x, y))
        matches = set()
        for square in surrounding_squares:
            match = self.get_number(*square)
            if match:
                matches.add(match)

        if len(matches) == 2:
            gears = [match[1] for match in matches]
            return gears[0] * gears[1]
        return 0

    def is_adjacent_to_symbol(self, xy0: Tuple[int, int], xy1: Tuple[int, int]) -> bool:
        """Checks for symbols in any of the squares surrounding the line between xy0 and xy1"""
        candidate_squares = self.get_surrounding_squares(xy0, xy1)
        return any(is_symbol(self.get_square(*xy)) for xy in candidate_squares)

    def get_numbers_by_coordinates(self):
        """Returns a generator of (coordinates, number) tuples"""
        for y, line in enumerate(self.lines):
            start_x = None
            coordinates = []
            digits = []
            for x, char in enumerate(line):
                if char.isdigit():
                    if start_x is None:
                        start_x = x
                    digits.append(char)
                    coordinates.append((x, y))
                elif start_x is not None:
                    yield coordinates, int("".join(digits))
                    start_x = None
                    digits = []
                    coordinates = []
            # Handle the case where the line ends with a number
            if start_x is not None:
                yield coordinates, int("".join(digits))
