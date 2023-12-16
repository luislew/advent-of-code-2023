from day_16 import get_lines, Layout, NORTH, SOUTH, EAST, WEST


if __name__ == "__main__":
    lines = list(get_lines())
    layout = Layout(lines)
    candidate_starts = []
    for x in range(layout.width):
        candidate_starts.append((x, 0, SOUTH))
        candidate_starts.append((x, layout.height - 1, NORTH))
    for y in range(layout.height):
        candidate_starts.append((0, y, EAST))
        candidate_starts.append((layout.width - 1, y, WEST))

    max_energized = 0
    for start in candidate_starts:
        layout.energize_squares(*start)
        max_energized = max(len(layout.energized), max_energized)
        layout.reset()

    print(max_energized)
