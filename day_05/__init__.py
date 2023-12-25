import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
MAP_SECTIONS = [
    ("seed", "soil"),
    ("soil", "fertilizer"),
    ("fertilizer", "water"),
    ("water", "light"),
    ("light", "temperature"),
    ("temperature", "humidity"),
    ("humidity", "location"),
]


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


def parse_input():
    seeds = []
    maps = {}
    current_map_section = None
    for line in get_lines():
        if line.startswith("seeds:"):
            seeds_str = line.split(": ")[1]
            seeds = [int(seed) for seed in seeds_str.split(" ")]
        elif line.endswith("map:"):
            map_id = line.split(" ")[0]
            current_map_section = tuple(map_id.split("-to-"))
            maps[current_map_section] = {}
        elif not line:
            current_map_section = None
        else:
            # Update current map from line e.g. 2122609492 2788703865 117293332
            # 2122609492 is destination range start
            # 2788703865 is source range start
            # 117293332 is range length
            # If map section is ("seed", "soil"), then seed 2788703865 --> soil 2122609492
            destination_start, source_start, length = [int(x) for x in line.split(" ")]
            maps[current_map_section][
                (source_start, source_start + length)
            ] = destination_start

    return seeds, maps


def get_x_for_y(maps: dict, source: str, destination: str, value: int):
    map_section = (source, destination)
    for source_range, destination_start in maps[map_section].items():
        if source_range[0] <= value < source_range[1]:
            return destination_start + (value - source_range[0])
    return value


def get_location_for_seed(maps: dict, seed: int):
    value = seed
    for source, destination in MAP_SECTIONS:
        value = get_x_for_y(maps, source, destination, value)
    return value
