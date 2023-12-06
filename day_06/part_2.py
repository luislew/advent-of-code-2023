from day_06 import get_number_of_possible_wins, parse_input


if __name__ == "__main__":
    time_max_distance_pairs = parse_input(space_delimited=False)
    time, max_distance = time_max_distance_pairs[0]
    print(get_number_of_possible_wins(time, max_distance))
