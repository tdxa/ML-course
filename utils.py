import csv, collections

FILE = './data/test.txt'

def read_file(path:str, delimiter=","):
    with open(path) as file:
        return [row for row in csv.reader(file, delimiter=delimiter)]

def count_class(data):
    return len(list(collections.Counter(x for sublist in data for x in sublist).keys()))

def count_occurences(data):
    return dict(collections.Counter(x for sublist in data for x in sublist))
