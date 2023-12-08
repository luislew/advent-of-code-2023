import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

"""
This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input.
In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC.
Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions,
repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL...
and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""

def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


def parse_input():
    instructions = None
    network = {}
    for line in get_lines():
        if instructions is None:
            instructions = line
        elif line:
            node, children = line.split(" = ")
            children = children[1:-1].split(", ")
            network[node] = children

    return instructions, network


def get_node(network, node, instruction):
    if instruction == "L":
        return network[node][0]
    elif instruction == "R":
        return network[node][1]
