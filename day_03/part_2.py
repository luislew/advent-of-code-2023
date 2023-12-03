from day_03 import get_lines, Schematic


if __name__ == "__main__":
    schematic = Schematic(list(get_lines()))
    gear_ratios_sum = sum(
        schematic.get_gear_ratio(x, y)
        for y, line in enumerate(schematic.lines)
        for x, char in enumerate(line)
        if char == "*"
    )
    print(gear_ratios_sum)
