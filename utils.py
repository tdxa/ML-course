import csv, collections
from math import log2

FILE = './data/gielda.txt'

def read_file(path:str, delimiter=","):
    with open(path) as file:
        return [row for row in csv.reader(file, delimiter=delimiter)]

def count_class(data):
    # return len(list(collections.Counter(x for sublist in data for x in sublist).keys()))
    size = len(data[0])
    counts = []
    for i in range(size):
        uniques = set([val[i] for val in data])
        counts.append(len(uniques))
    return counts

def count_occurences(data):
    return dict(collections.Counter(x for sublist in data for x in sublist))

def get_probabilities(data):
    # print(count_occurences(data).values())
    return [val/len(data) for val in count_occurences(data).values()]

def get_entropy(probabilities):
    return -(sum([p * log2(p) for p in probabilities if p !=0]))



x = read_file(FILE)
print(x)
print(count_class(x))
print(count_occurences(x))
print(get_probabilities(x))
print(get_entropy(probabilities=get_probabilities(x)))