from day_02 import get_lines, get_maxima_by_color, parse_line

MAXIMA = dict(red=12, green=13, blue=14)


def possible_game(maxima):
    for color, amount in maxima.items():
        if amount > MAXIMA[color]:
            return False
    return True


if __name__ == "__main__":
    ids_sum = 0
    for line in get_lines():
        game_id, results = parse_line(line)
        maxima = get_maxima_by_color(results)
        if possible_game(maxima):
            ids_sum += game_id
    print(ids_sum)
