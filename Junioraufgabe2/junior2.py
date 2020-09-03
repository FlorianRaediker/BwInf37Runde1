#!/usr/bin/env python3
"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Junioraufgabe 2: 'Baywatch'

PYTHON3

Dieses Programm berechnet die Beispieldaten der Aufgabe.
Für weitere Informationen siehe die Dokumentation zur Aufgabe
"""
from collections import deque


def get_rotated_lists(partial, distorted):
    """
    Rotates the list distorted until it matches partial.
    :param partial: list which may contain '-1' to mark unknown values, but is in the right order
    :param distorted: list with all values known, but randomly rotated
    :return: a generator with all possible rotations of distorted to match partial.
    """
    distorted = deque(distorted)
    for _ in range(len(distorted)):
        distorted.rotate()
        if is_similar(partial, distorted):
            yield list(distorted)


def is_similar(partial, entire):
    """
    Returns True if the two lists are equal except for unknown values marked with value -1 in the first list.
    If the two lists are of different sizes, False will be returned.
    :param partial: A list which may contain '-1' to mark unknown values
    :param entire: A list without '-1'.
    :return: True or False
    """
    if len(partial) != len(entire):
        # Länge ist nicht gleich -> Listen ähneln sich nicht
        return False
    # die Elemente gleichen Indexes vergleichen
    for p, e in zip(partial, entire):
        # Wenn das erste Element nicht -1 ist (also unbekannt und in der zweiten Liste dann beliebig), müssen die Elemente gleich sein. Ansonsten sind sich die Listen nicht ähnlich
        if not (p == -1 or p == e):
            return False
    return True


LAND_NUMS = {
    1: "Wald",
    2: "Wiese",
    3: "Häuser",
    4: "Wüste",
    5: "See",
    6: "Sumpf",
    7: "Reisfeld",
    8: "Berg",
    9: "Vulkankrater"
}
def translate_land_tongues(land_nums):
    """
    Translates a list of land_tongue values to a string.
    :param land_nums: list of nums from 1 to 9 representing one land tongue.
    :return: a string containing all land_nums as names represented in LAND_NUMS.
    """
    return " ".join(LAND_NUMS[i] for i in land_nums)


if __name__ == "__main__":
    import os
    cwd = os.path.dirname(__file__)
    os.curdir = cwd

    for num in range(1, 7):
        filename = "baywatch{}.txt".format(num)
        with open(filename, "r") as f:
            distorted, partial = f.readlines()
        distorted = (int(i) for i in distorted.strip().split(" "))
        partial = [(int(i) if i != "?" else -1) for i in partial.strip().split(" ")]
        
        results = tuple(get_rotated_lists(partial, distorted))
        print("########\n"+filename)
        print("Länge:", len(partial))
        print("Möglichkeiten:", len(results))
        # print the first results
        if results:  # results is not an empty sequence
            print(translate_land_tongues(results[0]), end="\n\n")
        else:
            print("Keine Möglichkeiten\n")
