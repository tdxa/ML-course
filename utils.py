import collections
import csv
from math import log2

FILE = './data/gielda.txt'

def read_file(path: str, delimiter=","):
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
    for column in zip(*data):  # zip transposes rows to columns
        occurences.append(dict(collections.Counter(item for item in column)))
    return occurences


def count_probabilities(data):
    probs = []
    for column in data:
        total = sum(column.values())
        probs.append([attribute / total for attribute in list(column.values())])
    return probs


def count_entropy(decision_probabilities):
    return -(sum([p * log2(p) for p in decision_probabilities if p != 0]))


def get_entropy(probabilities):
    """
    Wyliczanie entropii dla klasy decyzyjnej na podstawie prawdopodbieństw
    """
    return count_entropy(probabilities[-1])


def get_info(attribute_index, data):
    """
    Wyliczanie funkcji informacji dla atrybutu warunkowego
    """
    occurences = count_occurences(data)
    info = 0
    for attribute in occurences[attribute_index].keys():
        subset = [row for row in data if row[attribute_index] == attribute]
        subset_probabilities = count_probabilities(count_occurences(subset))
        info += (len(subset) / len(data) * get_entropy(subset_probabilities))
    return info


def get_gain(entropy, info):
    return [(entropy - attribute) for attribute in info]


def get_split_info(attribute_index, probabilities):
    """
    Wyliczanie informacji o podziale tj. liczenie entropii dla atrybutu warunkowego
    """
    return count_entropy(probabilities[attribute_index])


def get_gain_ratio(gain, split_info):
    return [(gain[attribute] / split_info[attribute]) if split_info[attribute] > 0 else 0 for attribute in
            range(len(gain))]


def get_best_attribute(gain_ratio):
    """
    Wybranie atrybutu warunkowego według którego nastąpi podział w drzewie decyzyjnym
    """
    return gain_ratio.index(max(gain_ratio))


def build_tree(data, prev=-1, margin='\t\t'):
    # print("DATA   ", data)
    classes = count_class(data)
    # print("CLASSES   ", classes)
    occurences = count_occurences(data)
    # print("OCCURENCES   ", occurences)
    probabilities = count_probabilities(occurences)
    # print("PROBABILITIES   ", probabilities)
    entropy = get_entropy(probabilities)
    # print("ENTROPY   ", entropy)
    info = [get_info(index, data) for index in range(len(classes) - 1)]
    # print("INFO   ", info)
    gain = get_gain(entropy, info)
    # print("GAIN   ", gain)
    split_info = [get_split_info(index, probabilities) for index in range(len(classes) - 1)]
    gain_ratio = get_gain_ratio(gain, split_info)

    max_gain_ratio = max(gain_ratio)
    best_attribute = get_best_attribute(gain_ratio)

    if max_gain_ratio > 0:  # warunek stopu
        if prev != -1:
            print(f'{margin}{list(occurences[prev].keys())[0]} --> ATTRIBUTE: {best_attribute + 1}')
        else:
            print(f'ATTRIBUTE: {best_attribute + 1}')

        prev = best_attribute
        margin += '\t'
        new = [[x for x in data if x[best_attribute] == key] for key in occurences[best_attribute]]

        for x in new:
            build_tree(x, prev, margin)
    else:
        print(f'{margin}{list(occurences[prev].keys())[0]} --> DECISION: {list(occurences[len(data[0]) - 1].keys())[0]}')


x = read_file(FILE)
build_tree(x)

