from day_13 import parse_lines


if __name__ == "__main__":
    maps = parse_lines()
    reflections = [map.find_reflection(with_smudge=True) for map in maps]
    print(sum(x or 100 * y for x, y in reflections))
