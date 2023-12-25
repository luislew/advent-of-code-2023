from day_19 import parse_lines, get_result_for_part, APPROVED


if __name__ == "__main__":
    rules_map, parts = parse_lines()
    approved_parts = [
        part for part in parts if get_result_for_part(part, rules_map) == APPROVED
    ]
    print(sum(part.total_rating for part in approved_parts))
