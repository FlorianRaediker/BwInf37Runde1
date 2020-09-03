"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 1 'Superstar'

PYTHON3

Dieses Modul stellt eine Klasse, LoopIteratingList, bereit, die beim Iterieren immer an der Stelle anfängt, an der sie
aufgehört hat (auch, wenn das Iterieren z.B. unterbrochen wurde (in einer Schleife mit break, return, ...)
"""


class LoopIteratingList(list):
    """
    (hier mal auf Deutsch: ) Eine Liste, die sich die Stelle merkt, an der die mit einer Iteration das letzte mal
    aufgehört hat und an dieser Stelle wieder beginnt.
    Nützlich für teenigroup.TeeniGroup, damit jeder Name mal drankommt
    Beim Berechnen vom Superstar aus superstar4.txt werden teilweise 40 Anfragen weniger ausgeführt.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._next_position = 0

    def __next__(self):
        try:
            res = self[self._next_position]
        except IndexError:
            # end reached, restart
            self._next_position = 1
            return self[0]
        else:
            self._next_position += 1
            return res

    def __iter__(self):
        for i in range(len(self)):
            yield next(self)
