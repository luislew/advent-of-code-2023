import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


def parse_line(line):
    """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"""
    card_title, numbers = line.split(": ")
    card_id = int(card_title.split(" ")[-1])
    winning_numbers_str, card_numbers_str = numbers.split(" | ")
    winning_numbers = [
        int(number) for number in winning_numbers_str.split(" ") if number
    ]
    card_numbers = [int(number) for number in card_numbers_str.split(" ") if number]
    return card_id, winning_numbers, card_numbers
