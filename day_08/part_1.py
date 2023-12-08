from itertools import cycle

from day_08 import get_node, parse_input


if __name__ == "__main__":
    instructions, network = parse_input()
    steps = 0
    node = "AAA"
    for instruction in cycle(instructions):
        steps += 1
        node = get_node(network, node, instruction)
        if node == "ZZZ":
            break

    print(steps)
