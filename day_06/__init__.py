import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


def parse_input(space_delimited=True):
    for line in get_lines():
        if line.startswith("Time"):
            if space_delimited:
                times = [int(t) for t in line.split("Time:")[1].split(" ") if t]
            else:
                times = [int(line.split("Time:")[1].replace(" ", ""))]
        elif line.startswith("Distance"):
            if space_delimited:
                distances = [int(d) for d in line.split("Distance:")[1].split(" ") if d]
            else:
                distances = [int(line.split("Distance:")[1].replace(" ", ""))]
    return list(zip(times, distances))


def get_distance_for_time_and_button_hold(time, button_hold):
    return button_hold * (time - button_hold)


def get_number_of_possible_wins(time, max_distance):
    return sum(
        1
        for button_hold in range(time + 1)
        if get_distance_for_time_and_button_hold(time, button_hold) > max_distance
    )
