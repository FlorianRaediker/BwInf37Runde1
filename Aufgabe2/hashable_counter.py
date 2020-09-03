"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 2 'Twist'

PYTHON3

Stellt eine Klasse, HashableCounter, bereit, die von Counter aus dem Modul collections erbt und zwei Funktionaltäten
hinzufügt:
  - die Funktion __hash__, um zwei HashableCounter mit __eq__ vergleichen zu können
  - die Funktion __sub__, um zwei HashableCounter voneinander subtrahieren zu können
Für mehr Informationen siehe die Dokumentation.
"""
from collections import Counter


class HashableCounter(Counter):
    """
    Inherits from collections.Counter. Is hashable and can be subtracted from another HashableCounter (see doc __sub__)
    """
    def __hash__(self):
        return hash(frozenset(self.items()))

    def clean(self):
        """
        :return: A HashableCounter with every zero-element removed.
        """
        return HashableCounter({key:value for key, value in self.items() if value != 0})

    def __sub__(self, other):
        """
        Subtracts other from self as long as self has more elements than other; otherwise raises ArithmeticError.
        :param other: another HashableCounter which is subtracted from this one.
        :return:
        """
        res = self.copy()
        for key, value in other.items():
            res_value = res[key]
            if res_value >= value:
                res[key] = res_value - value
            else:
                raise ArithmeticError
        return res.clean()

    def __eq__(self, other):
        """
        :param other: other HashableCounter to compare
        :return: True if the two HashableCounters are equal, otherwise False
        """
        return hash(self) == hash(other)
