from day_01 import get_lines


def get_calibration_value(line):
    digits = [s for s in line if s.isdigit()]
    return int(digits[0] + digits[-1])


if __name__ == "__main__":
    print(sum(get_calibration_value(line) for line in get_lines()))
