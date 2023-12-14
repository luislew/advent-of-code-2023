from day_14 import get_lines, Map


if __name__ == "__main__":
    lines = list(get_lines())
    map = Map(lines)
    for x in range(map.width):
        map.tilt_column(x)
    print(map.get_total_load())
