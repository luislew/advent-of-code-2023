from day_05 import get_location_for_seed, parse_input


def get_min_location_for_seed_range(maps, seed_range):
    seed_start, range_length = seed_range
    return min(get_location_for_seed(maps, seed) for seed in range(seed_start, seed_start + range_length))


if __name__ == "__main__":
    seeds, maps = parse_input()
    seed_starts = [seed for idx, seed in enumerate(seeds) if not idx % 2]
    seed_range_lengths = [seed for idx, seed in enumerate(seeds) if idx % 2]
    seed_ranges = list(zip(seed_starts, seed_range_lengths))
    print(min(get_min_location_for_seed_range(maps, seed_range) for seed_range in seed_ranges))
