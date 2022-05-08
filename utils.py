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
    # return dict(collections.Counter(x for sublist in data for x in sublist)) # płaska lista
    occurences = []
    for column in zip(*data): # zip transposes rows to columns
        occurences.append(dict(collections.Counter(item for item in column)))
    return occurences

def get_probabilities(data):
    probabilities = []
    for column in data:
        total = sum(column.values())
        probabilities.append([attribute/total for attribute in list(column.values())])
    return probabilities


def count_entropy(decision_probabilities):
    return -(sum([p * log2(p) for p in decision_probabilities if p != 0]))

def get_entropy(probabilities):
    """
    Wyliczanie entropii dla klasy decyzyjnej na podstawie prawdopodbieństw
    """
    return count_entropy(probabilities[-1])

def get_info(attribute_class, data):
    """
    Wyliczanie funkcji informacji dla podanej klasy atrybutu warunkowego
    """
    occurences = count_occurences(data)
    info = 0
    for attribute in occurences[attribute_class].keys():
        subset = [row for row in x if row[attribute_class] == attribute]
        subset_probabilities = get_probabilities(count_occurences(subset))
        info += (len(subset) / len(x) * get_entropy(subset_probabilities))
    return info


x = read_file(FILE)
clss = count_class(x)
occ= count_occurences(x)
prop = get_probabilities(count_occurences(x))
entr = get_entropy(prop)
info = [get_info(index, x) for index in range(len(clss)-1)]

print("*************************")
print(x)
print(list(zip(*x)))
print(clss)
print(occ)
print(prop)
print(entr)
print(info)
print()

