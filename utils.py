import csv, collections
from math import log2

FILE = './data/gielda.txt'

def read_file(path:str, delimiter=","):
    with open(path) as file:
        return [row for row in csv.reader(file, delimiter=delimiter)]

def count_class(data):
    size = len(data[0])
    counts = []
    for i in range(size):
        uniques = set([val[i] for val in data])
        counts.append(len(uniques))
    return counts

def count_occurences(data):
    occurences = []
    for column in zip(*data): # zip transposes rows to columns
        occurences.append(dict(collections.Counter(item for item in column)))
    return occurences

def probabilities(data):
    probs = []
    for column in data:
        total = sum(column.values())
        probs.append([attribute / total for attribute in list(column.values())])
    return probs


def count_entropy(decision_probabilities):
    return -(sum([p * log2(p) for p in decision_probabilities if p != 0]))

def entropy(probabilities):
    """
    Wyliczanie entropii dla klasy decyzyjnej na podstawie prawdopodbieństw
    """
    return count_entropy(probabilities[-1])

def info(attribute_index, data):
    """
    Wyliczanie funkcji informacji dla atrybutu warunkowego
    """
    occurences = count_occurences(data)
    info = 0
    for attribute in occurences[attribute_index].keys():
        subset = [row for row in data if row[attribute_index] == attribute]
        subset_probabilities = probabilities(count_occurences(subset))
        info += (len(subset) / len(data) * entropy(subset_probabilities))
    return info

def gain(entropy, info):
    return [(entropy-attribute) for attribute in info]

def split_info(attribute_index, probabilities):
    """
    Wyliczanie informacji o podziale tj. liczenie entropii dla atrybutu warunkowego
    """
    return count_entropy(probabilities[attribute_index])

def gain_ratio(gain, split_info):
    return [(gain[attribute] / split_info[attribute]) for attribute in range(len(gain))]

def best_attribute(gain_ratio):
    """
    Wybranie atrybutu warunkowego według którego nastąpi podział w drzewie decyzyjnym
    """
    return gain_ratio.index(max(gainratio))

x = read_file(FILE)
clss = count_class(x)
occ= count_occurences(x)
prop = probabilities(count_occurences(x))
entr = entropy(prop)
info = [info(index, x) for index in range(len(clss) - 1)]
gai = gain(entr, info)
split = [split_info(index, prop) for index in range(len(clss) - 1)]
gainratio = gain_ratio(gai,split)
best = best_attribute(gainratio)

print("*************************")
print(x)
print(list(zip(*x)))
print(clss)
print(occ)
print(prop)
print(entr)
print(info)
print(gai)
print(split)
print(gainratio)
print(best)



