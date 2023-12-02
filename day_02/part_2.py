from day_02 import get_lines, get_maxima_by_color, parse_line


def get_power_for_line(line):
    _, results = parse_line(line)
    maxima = get_maxima_by_color(results)
    return maxima.get("red", 0) * maxima.get("green", 0) * maxima.get("blue", 0)


if __name__ == "__main__":
    print(sum(get_power_for_line(line) for line in get_lines()))
