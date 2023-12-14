from day_14 import get_lines, Map


if __name__ == "__main__":
    lines = list(get_lines())
    map = Map(lines)
    cycle_tracker = {}
    cycle = 0
    cycle_tracker[map.get_rolling_rocks()] = cycle
    while True:
        map.cycle()
        cycle += 1
        rolling_rocks = map.get_rolling_rocks()
        if rolling_rocks in cycle_tracker:
            break

        cycle_tracker[rolling_rocks] = cycle

    cycle_length = cycle - cycle_tracker[rolling_rocks]
    cycle_offset = cycle_tracker[rolling_rocks]
    cycle_index = (1000000000 - cycle_offset) % cycle_length + cycle_offset
    inverse_cycle_tracker = {v: k for k, v in cycle_tracker.items()}
    rolling_rocks = inverse_cycle_tracker[cycle_index]
    print(sum(map.height - y for x, y in rolling_rocks))
