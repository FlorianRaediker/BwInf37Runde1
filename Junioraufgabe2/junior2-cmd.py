#!/usr/bin/env python3
"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Junioraufgabe 2: 'Baywatch'

PYTHON3

Nimmt einen Kommandozeilenparameter zu einer Beispieldatendatei entgegen und berechnet sie.
Siehe die Aufgabendokumentation für mehr Informationen.
"""
import sys
import os
cwd = os.path.dirname(__file__)
os.curdir = cwd
sys.path.append(cwd)

import junior2

if len(sys.argv) != 2:  # "junior2-cmd.py" is the first arg
    print("Falsche Benutzung. Richtig: 'python3 junior2-cmd.py <pfad/zu/baywatch-datei>")
    sys.exit(1)

path = sys.argv[1]  # path to baywatch-file
try:
    with open(path, "r") as f:
        distorted, partial = f.readlines()
except FileNotFoundError:
    print("Konnte Datei '{}' nicht finden. ".format(path))
    sys.exit(2)
except BaseException:
    print("Unbekannter Fehler beim einlesen der Datei. ")
    sys.exit(2)

# same procedure as in junior2.py
distorted = (int(i) for i in distorted.strip().split(" "))
partial = [(int(i) if i != "?" else -1) for i in partial.strip().split(" ")]
results = tuple(junior2.get_rotated_lists(partial, distorted))
print("########\n"+path)
print("Länge:", len(partial))
print("Möglichkeiten:", len(results))
# print the first results
if results:  # results is not an empty sequence
	print(junior2.translate_land_tongues(results[0]), end="\n\n")
else:
	print("Keine Möglichkeiten\n")
