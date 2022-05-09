import csv


class Formatting:
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERSCORE = "\33[4m"
    END = "\x1b[0m"
    BLUE_BOX = "\x1b[0;30;44m"


def read_file(path: str, delimiter=","):
    with open(path) as file:
        return [row for row in csv.reader(file, delimiter=delimiter)]
