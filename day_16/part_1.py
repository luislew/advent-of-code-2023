from day_16 import get_lines, Layout


if __name__ == "__main__":
    lines = list(get_lines())
    layout = Layout(lines)
    layout.energize_squares()
    print(len(layout.energized))
