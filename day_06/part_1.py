from functools import reduce

from day_06 import get_number_of_possible_wins, parse_input


if __name__ == "__main__":
    time_max_distance_pairs = parse_input()
    possible_wins = [
        get_number_of_possible_wins(time, max_distance)
        for time, max_distance in time_max_distance_pairs
    ]
    print(reduce(lambda x, y: x * y, possible_wins))
