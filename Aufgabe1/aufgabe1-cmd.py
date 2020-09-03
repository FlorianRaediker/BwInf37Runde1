#!/usr/bin/env python3
"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 1 'Superstar'

PYTHON3

Nimmt einen Pfad zu einer TeeniGroup in Form einer Textdatei (im auf der BwInf-Webseite beschriebenen Format) als
Kommandozeilenparameter entgegen und versucht, den Superstar dieser Gruppe zu finden.
Um die Beispieldaten anzusprechen, kann 'superstar1.txt', 'superstar2.txt', ... benutzt werden. 
Sollte der zweite Parameter 'nodebug' sein, werden keine Ausgaben außer das Ergebnis gemacht (also auch nicht die
gestellten Anfragen, die ansonsten mit 'IS_FOLLOWING' beginnen).
"""
import os
import sys
cwd = os.path.dirname(__file__)  # current working directory
os.curdir = cwd  # access files in same dir
sys.path.append(cwd)  # find custom modules
import teenigroup


if len(sys.argv) == 1:  # sys.argv contains also path to this file
    print("Es muss mindestend ein Pfad als Kommandozeilenparameter angegeben werden. Siehe den docstring zu dieser "
          "Datei für mehr Informationen. ")
    sys.exit(1)
elif len(sys.argv) == 2:
    # standard is debug
    sys.argv.append("debug")
elif len(sys.argv) > 3:
    print("Es dürfen maximal zwei Parameter angegeben werden. Benutzung: 'python3 aufgabe1-cmd.py <group-path> "
          "[nodebug]'. Siehe den Docstring dieser Datei für mehr Informationen. ")
    sys.exit(1)

try:
    group = teenigroup.TeeniGroup.from_textfile(sys.argv[1])
except FileNotFoundError:
    print("Die Datei '{}' konnte nicht gefunden werden. ".format(sys.argv[1]))
    sys.exit(1)
except BaseException:
    print("Die Datei '{}' konnte nicht eingelesen werden. ".format(sys.argv[1]))
    sys.exit(1)


superstar, amount = group.get_superstar(debug=(sys.argv[2] != "nodebug"))
if superstar:
    print("Superstar ist '", superstar, "'. Es mussten ", amount, " Anfragen gestellt werden. ", sep="")
else:
    print("Oh! Es gibt keinen Superstar in dieser Gruppe, aber es mussten", amount, "Anfragen für nichts gestellt "
                                                                                     "werden (na ja, fast nichts)")