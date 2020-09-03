#!/usr/bin/env python3
"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 1 'Superstar'

PYTHON3

Berechnet die Superstars (soweit vorhanden) der Beispieldaten.
Für weitere Informationen siehe die Dokumentation zur Aufgabe.
"""
import os
import sys
cwd = os.path.dirname(__file__)  # current working directory
os.curdir = cwd  # access files in same dir
sys.path.append(cwd)  # find custom modules
import teenigroup


# calculate superstars of groups 1 to 4
for i in range(1, 5):
    print("\n###############################\n"
          "Calculating Superstar of 'Group{}'...".format(i))

    # create the group with the specific textfile
    group = teenigroup.TeeniGroup.from_textfile("superstar{}.txt".format(i))
    superstar, amount = group.get_superstar(debug=True)

    if superstar:
        print("Superstar is '", superstar, "'. We had to send ", amount, " requests. ", sep="")
    else:
        # get_superstar returned None, no superstar was found
        print("Oh! There is no superstar in this group, but we sent", amount, "requests for nothing (well, almost "
                                                                              "nothing)...")
