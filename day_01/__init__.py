import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        yield from f.readlines()
