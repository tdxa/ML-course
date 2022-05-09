import collections
from math import log2
from typing import List, Dict

from utils import Formatting


def count_class(data: List[List[str]]) -> List[int]:
    size = len(data[0])
    counts = []
    for i in range(size):
        uniques = set([val[i] for val in data])
        counts.append(len(uniques))
    return counts


def count_occurences(data: List[List[str]]) -> List[Dict[str, int]]:
    """
    Count the occurrences of the attribute in each class
    """
    occurences = []
    for column in zip(*data):  # zip transposes rows to columns
        occurences.append(dict(collections.Counter(item for item in column)))
    return occurences


def count_probabilities(occurrences: List[Dict[str, int]]) -> List[List[float]]:
    """
    Compute the probability for each attribute class
    """
    probs = []
    for column in occurrences:
        total = sum(column.values())
        probs.append([attribute / total for attribute in list(column.values())])
    return probs


def count_entropy(decision_probabilities: List[float]) -> float:
    """
    Compute entropy based on probabilities
    """
    return -(sum([p * log2(p) for p in decision_probabilities if p != 0]))


def get_entropy(probabilities: List[List[float]]) -> float:
    """
    Get entropy for the decision class
    """
    return count_entropy(probabilities[-1])


def get_info(attribute_index: int, data: List[List[str]]) -> float:
    """
    Compute the result of the information function for an attribute
    """
    occurences = count_occurences(data)
    info = 0
    for attribute in occurences[attribute_index].keys():
        subset = [row for row in data if row[attribute_index] == attribute]
        subset_probabilities = count_probabilities(count_occurences(subset))
        info += len(subset) / len(data) * get_entropy(subset_probabilities)
    return info


def get_gain(entropy: float, info: List[float]) -> List[float]:
    """
    Compute the information gain for all attribute classes
    """
    return [(entropy - attribute) for attribute in info]


def get_split_info(attribute_index: int, probabilities: List[List[float]]) -> float:
    """
    Compute the split information, i.e. calculate the entropy for each attribute
    """
    return count_entropy(probabilities[attribute_index])


def get_gain_ratio(gain: List[float], split_info: List[float]) -> List[float]:
    """
    Balance the disproportions
    """
    return [
        (gain[attribute] / split_info[attribute]) if split_info[attribute] > 0 else 0
        for attribute in range(len(gain))
    ]


def get_best_attribute(gain_ratio: List[float]) -> int:
    """
    Selection of the attribute according to which the division will be made in the decision tree.
    The function returns the index of the attribute class.
    """
    return gain_ratio.index(max(gain_ratio))


def build_tree(data, prev=-1, margin="\t\t", color=1):
    classes = count_class(data)
    occurrences = count_occurences(data)
    probabilities = count_probabilities(occurrences)
    entropy = get_entropy(probabilities)
    info = [get_info(index, data) for index in range(len(classes) - 1)]
    gain = get_gain(entropy, info)
    split_info = [
        get_split_info(index, probabilities) for index in range(len(classes) - 1)
    ]
    gain_ratio = get_gain_ratio(gain, split_info)

    max_gain_ratio = max(gain_ratio)
    best_attribute = get_best_attribute(gain_ratio)

    if max_gain_ratio > 0:  # warunek stopu
        if prev != -1:
            print(
                f"{margin}{Formatting.BOLD + Formatting.UNDERSCORE}\33[3{color}m{list(occurrences[prev].keys())[0]} --> ATTRIBUTE: {best_attribute + 1}{Formatting.END} "
            )
        else:
            print(
                f"{Formatting.BLUE_BOX + Formatting.BOLD}ATTRIBUTE: {best_attribute + 1}{Formatting.END}"
            )

        prev = best_attribute
        margin += "\t"
        new_data = [
            [x for x in data if x[best_attribute] == key]
            for key in occurrences[best_attribute]
        ]
        color += 1

        for subset in new_data:
            build_tree(subset, prev, margin, color)
    else:
        print(
            f"{margin}\33[3{color}m{list(occurrences[prev].keys())[0]} --> DECISION: {Formatting.ITALIC}{list(occurrences[len(data[0]) - 1].keys())[0]}{Formatting.END}"
        )
