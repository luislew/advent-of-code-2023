from itertools import cycle
from math import lcm

from day_08 import get_node, parse_input


def get_steps_to_z_node(network, node, instructions):
    steps = 0
    for instruction in cycle(instructions):
        steps += 1
        node = get_node(network, node, instruction)
        if node.endswith("Z"):
            break

    return steps


if __name__ == "__main__":
    instructions, network = parse_input()
    steps = 0
    nodes = [node for node in network if node.endswith("A")]
    cycle_lenths = [get_steps_to_z_node(network, node, instructions) for node in nodes]
    print(lcm(*cycle_lenths))
