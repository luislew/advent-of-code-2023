from day_09 import determine_previous_value, get_sequences


if __name__ == "__main__":
    print(sum(determine_previous_value(sequence) for sequence in get_sequences()))
