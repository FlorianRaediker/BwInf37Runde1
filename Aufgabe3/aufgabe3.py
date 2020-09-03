#!/usr/bin/env python3
"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 3 'Voll daneben'

PYTHON3

Berechnet möglichst gute Zahlen für die Beispieldaten und gibt jeweils die Zahlen und den Profit aus.
"""
import os
import sys
cwd = os.path.dirname(__file__)  # current working directory
os.curdir = cwd  # access files in same dir
sys.path.append(cwd)  # find custom modules
import al_numbers

for i in range(1, 4):
    with open("beispiel{}.txt".format(i), "r") as f:
        print("Beispiel" + str(i))
        lucky_numbers = sorted(int(line.strip()) for line in f.readlines())
        al = al_numbers.get_al_numbers(lucky_numbers)
        print("Als Zahlen:", al)
        print("Als Profit: {}$".format(al_numbers.get_profit(lucky_numbers, al)), end="\n\n")
