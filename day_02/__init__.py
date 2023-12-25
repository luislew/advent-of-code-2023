import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        yield from f.readlines()


def parse_line(line):
    game_title, cube_sets = line.strip().split(": ")
    game_id = int(game_title.split(" ")[1])
    results = []
    for cube_set in cube_sets.split("; "):
        result = {}
        for group in cube_set.split(", "):
            amount, color = group.split(" ")
            result[color] = int(amount)
        results.append(result)

    return game_id, results


def get_maxima_by_color(results):
    maxima = {}
    for result in results:
        for color, amount in result.items():
            if color not in maxima or amount > maxima[color]:
                maxima[color] = amount
    return maxima
