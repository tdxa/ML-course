from utils import read_file
from tree import build_tree

if __name__ == "__main__":
    FILE = "./data/gielda.txt"

    data = read_file(FILE)
    build_tree(data)
