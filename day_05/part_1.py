from day_05 import get_location_for_seed, parse_input


if __name__ == "__main__":
    seeds, maps = parse_input()
    print(min(get_location_for_seed(maps, seed) for seed in seeds))
