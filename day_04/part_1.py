from day_04 import get_lines, parse_line


if __name__ == "__main__":
    total_points = 0
    for line in get_lines():
        _, winning_numbers, card_numbers = parse_line(line)
        matches = set(winning_numbers) & set(card_numbers)
        if matches:
            total_points += 2 ** (len(matches) - 1)
    print(total_points)
