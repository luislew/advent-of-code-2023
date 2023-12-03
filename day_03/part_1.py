from day_03 import get_lines, Schematic


if __name__ == "__main__":
    schematic = Schematic(list(get_lines()))
    parts_sum = sum(
        number
        for coordinates, number in schematic.numbers_by_coordinates.items()
        if schematic.is_adjacent_to_symbol(coordinates[0], coordinates[-1])
    )
    print(parts_sum)
