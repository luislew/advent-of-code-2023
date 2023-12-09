from day_09 import determine_next_value, get_sequences


if __name__ == "__main__":
    print(sum(determine_next_value(sequence) for sequence in get_sequences()))
