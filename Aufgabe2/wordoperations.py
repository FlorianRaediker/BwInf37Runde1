"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 2 'Twist'

PYTHON3

Dieses Modul stellt zwei Funtionen bereit, um Operationen auf Wörter durchzuführen, die zum Enttwisten gebraucht werden.
Es sind sort_word ("sortiert" die Mitte eines Wortes) und apply_case (Übernimmt Groß-/Kleinschreibung).
Für mehr Informationen siehe die Docstrings der Funktionen.
"""


def sort_word(word):
    """
    Sorts the middle (everything except the first and the last letter) of a given 'word' alphabetically
    :param word: the word to sort (str)
    :return: the sorted word (str)
    """
    return word[0] + "".join(sorted(word[1:-1])) + word[-1]


def apply_case(source_word, dst_word):
    """
    Takes the case of source_word and applies it to dst_word. source_word and dst_word must have the same length
    :param source_word: source
    :param dst_word: string the case of source_word is applied to
    :return: dst_word with applied case
    """
    assert len(source_word) == len(dst_word)
    res = []
    for i, letter in enumerate(list(source_word)):
        if letter.isupper():
            res.append(dst_word[i].upper())
        else:
            res.append(dst_word[i].lower())
    return "".join(res)
