from itertools import combinations

from day_11 import get_lines, Image


if __name__ == "__main__":
    lines = list(get_lines())
    image = Image(lines)
    print(sum(image.get_shortest_length(galaxy1, galaxy2) for galaxy1, galaxy2 in combinations(image.galaxies, 2)))
