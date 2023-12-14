from day_12 import get_arrangements, get_lines, parse_line


def parse_unfolded_line(line):
    inventory, counts = parse_line(line)
    unfolded_inventory = "?".join([inventory] * 5)
    unfolded_counts = counts * 5
    return unfolded_inventory, unfolded_counts


if __name__ == "__main__":
    print(sum(len(get_arrangements(*parse_line(line))) for line in get_lines()))
