#!/usr/bin/env python3
"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 2 'Twist'

PYTHON3

Twistet und enttwistet die Beispieldaten und gibt sie mit der benötigten Zeit aus
(Zeit ist natürluch computerabhängig).
"""
import os
import sys
cwd = os.path.dirname(__file__)  # current working directory
os.curdir = cwd  # access files in same dir
sys.path.append(cwd)  # find custom modules
import time
import twister

print("DIESES PROGRAMM TWISTET UND ENTWISTET ALLE BEISPIELDATEN NACH EINER AUFGABE IM BUNDESWETTBEWERB INFORMATIK "
      "2018. \nERSTELLT VON FLORIAN RÄDIKER\n")
print("Für mehr Optionen bitte 'aufgabe2-cmd.py' benutzen. Weitere Informationen in der Dokumentation. \n")
print("Initialisiere Wörterbuch... (dauert bei mir etwa 10 Sekunden)")
tw = twister.Twister("dict/words", "dict/start/", "dict/end/", True)

for i in range(1, 6):
    print("\n\n"+"################\n"*3)
    with open("twist{}.txt".format(i), "r", encoding="utf-8") as f:
        text = f.read()
    print("Twiste 'twist{}.txt'...".format(i))
    t1 = time.perf_counter()
    twisted = tw.twist_text(text)
    t2 = time.perf_counter()
    print("Getwisted in {:.4f}: ".format(t2-t1))
    print(twisted)
    t1 = time.perf_counter()
    untwisted = tw.untwist_text_fast(twisted)
    t2 = time.perf_counter()
    print("\n\n########\nEnttwisted in {:.4f}: ".format(t2-t1))
    print(untwisted)
