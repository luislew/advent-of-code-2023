from day_04 import get_lines, parse_line


def get_lines_by_id():
    lines_by_id = {}
    for line in get_lines():
        card_id, winning_numbers, card_numbers = parse_line(line)
        lines_by_id[card_id] = (winning_numbers, card_numbers)
    return lines_by_id


if __name__ == "__main__":
    lines_by_id = get_lines_by_id()
    counts_by_id = {card_id: 1 for card_id in lines_by_id}
    for card_id in sorted(lines_by_id):
        winning_numbers, card_numbers = lines_by_id[card_id]
        matches_count = len(set(winning_numbers) & set(card_numbers))
        if matches_count:
            card_count = counts_by_id[card_id]
            # Add to the next N card counts * current card count
            for i in range(matches_count):
                other_card_id = card_id + i + 1
                counts_by_id[other_card_id] += card_count

    print(sum(counts_by_id.values()))
