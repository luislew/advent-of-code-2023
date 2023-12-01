from day_01 import get_lines

words_to_digits = dict(one=1, two=2, three=3, four=4, five=5, six=6, seven=7, eight=8, nine=9)
words = words_to_digits.keys()

def digitize_substring(substring):
    for word, digit in words_to_digits.items():
        substring = substring.replace(word, str(digit))
    return substring


def has_word(substring):
    return any(word in substring for word in words)


def digitize_line(line, reverse=False):
    output = ""
    buffer = ""
    if reverse:
        for chr in reversed(line):
            buffer = chr + buffer
            if has_word(buffer):
                buffer = digitize_substring(buffer)
                output = buffer + output
                buffer = ""
        return buffer + output
    else:
        for chr in line:
            buffer += chr
            if has_word(buffer):
                buffer = digitize_substring(buffer)
                output += buffer
                buffer = ""
        return output + buffer


def get_calibration_value(line):
    first_digit = [s for s in digitize_line(line) if s.isdigit()][0]
    last_digit = [s for s in digitize_line(line, reverse=True) if s.isdigit()][-1]
    return int(first_digit + last_digit)


if __name__ == "__main__":
    print(sum(get_calibration_value(line) for line in get_lines()))
