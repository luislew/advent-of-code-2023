from day_10 import Grid


if __name__ == "__main__":
    grid = Grid()
    main_loop_points = set(grid.get_main_loop())
    # Manually set grid start point to correct square type
    grid.map[grid.start] = "L"

    inside_points = set()
    # Rule: points are inside when they cross an odd number of pipes
    # Pipe crossings are either |, L(-)7, or F(-)J
    for y in range(grid.height):
        crossed = 0
        current_hor = None
        for x in range(grid.width):
            if (x, y) in main_loop_points:
                pipe = grid.get_square(x, y)
                if pipe == "|":
                    crossed += 1
                elif not current_hor and pipe in "LF":
                    current_hor = pipe
                elif current_hor and pipe in "7J":
                    if current_hor == "L" and pipe == "7":
                        crossed += 1
                    elif current_hor == "F" and pipe == "J":
                        crossed += 1
                    current_hor = None
            elif crossed % 2:
                inside_points.add((x, y))

    print(len(inside_points))
