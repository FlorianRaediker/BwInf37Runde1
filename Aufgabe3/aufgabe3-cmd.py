"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 3 'Voll daneben'

PYTHON3

Bekommt einen Pfad zu einer Datei mit Glückszahlen als Kommandozeilenparameter.
Berechnet gute Zahlen und gibt den Profit aus.
Die Beispieldaten können direkt über 'beispiel1.txt", ... angesprochen werden.
"""
import os
import sys
cwd = os.path.dirname(__file__)  # current working directory
os.curdir = cwd  # access files in same dir
sys.path.append(cwd)  # find custom modules
import al_numbers
if len(sys.argv) != 2:
    print("Falsche Benutzung. Richtig: python3 aufgabe3-cmd.py <path>")
    sys.exit(1)
path = sys.argv[1]
try:
    with open(path, "r") as f:
        lucky_numbers = sorted(int(line.strip()) for line in f.readlines())
except FileNotFoundError:
    print("Datei '{}' konnte nicht gefunden werden")
    sys.exit(1)
except BaseException:
    print("Datei '{}' konnte aus unbekanntem Grund nicht eingelesen werden. ")
    sys.exit(1)

al = al_numbers.get_al_numbers(lucky_numbers)
print("Als Zahlen:", al)
print("Als Profit: {}$".format(al_numbers.get_profit(lucky_numbers, al)), end="\n\n")
