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

def get_probabilities(decision_keys, data):
    decision_occurences = {key:count_occurences(data)[key] for key in decision_keys }
    return [val/len(data) for val in decision_occurences.values()]

def get_entropy(probabilities):
    return -(sum([p * log2(p) for p in probabilities if p !=0]))

def get_info(decision_keys, data):
    attributes_occurences = count_occurences(data)
    for key in decision_keys:
        attributes_occurences.pop(key, None)





x = read_file(FILE)
print(x)
print(count_class(x))
print(count_occurences(x))
print(get_probabilities(["down","up"],x))
print(get_entropy(get_probabilities(["down","up"],x)))
get_info(["down","up"],x)
