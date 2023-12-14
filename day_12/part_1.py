from day_12 import get_arrangements, get_lines, parse_line


if __name__ == "__main__":
    print(sum(len(get_arrangements(*parse_line(line))) for line in get_lines()))
