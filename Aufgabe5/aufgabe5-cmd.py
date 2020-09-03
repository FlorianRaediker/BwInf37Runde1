#!/usr/bin/env python3
import os
import sys
import webbrowser

cwd = os.path.dirname(__file__)
sys.path.append(cwd)
os.curdir = cwd

import cmd
import traceback
import resistancefinder
import resistordiagram


class ResistorCmd(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "> "
        self.finder = None
        self.last_diagram = None

    def cmdloop(self, resistor_file, intro=None):
        print("\nLade Widerstände der Datei '{}'...".format(resistor_file))
        with open(resistor_file, "r") as f:
            resistances = tuple(int(r.strip()) for r in f.readlines())
        self.finder = resistancefinder.ResistanceFinder(resistances)
        super().cmdloop(intro)

    OHM_UNITIES = {"n": 1e-9, "m": 0.001, "µ": 1e-6, "k": 1000, "M": 1000000, "G": 1000000000}

    def parse_resistance(self, string):
        length = len(string)
        if length == 0:
            return None
        if length > 1 and string[-1] in self.OHM_UNITIES:
            return int(string[:-1]) * self.OHM_UNITIES[string[-1]]
        return float(string)

    def do_find(self, prm):
        try:
            # parse prompt
            params = prm.split(" ")
            if len(params) == 1:
                # only the first parameter is given
                search_value = float(params[0])
                k = None
            elif len(params) == 2:
                # resistance and k are given
                search_value = float(params[0])
                k = int(params[1])
                if not 0 < k < 5:
                    raise ValueError
            else:
                print("Zu viele/wenig Parameter. Siehe 'help find'")
                return
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl (int/float) als <resistance> eingeben. <k> muss sich im Bereich "
                  "1, ..., 4 befinden. Siehe 'help find'")
            return
        if k is not None:
            # k is given
            value, self.last_diagram = self.finder.find(search_value, k)
            print(value, "Ω mit k=", k, " mit Diagramm ", self.last_diagram, sep="")
        else:
            k, result = self.finder.find_best(search_value)
            value, self.last_diagram = result
            print("Beste Annäherung mit", k, "Widerständen: ")
            print(value, "Ω mit Diagramm ", self.last_diagram, sep="")

    def help_find(self):
        print("find <resistance> [<k>]\n    Findet einen Widerstandswert <resistance> "
              "oder eine Annäherung mit den eingegebenen Widerstandswerten mit maximal k benutzten Widerstandswerten. "
              "Wenn <k> nicht angegeben ist, wird die beste Kombination zu <resistance> ausgegeben. ")

    def do_save(self, path):
        if self.last_diagram:
            if not path:
                path = "diagram.svg"
            try:
                resistordiagram.parse_diagram(self.last_diagram).save(path)
            except Exception as ex:
                print("Konnte Datei '{}' nicht speichern. ".format(path))
                traceback.print_exc()
            if not webbrowser.open(os.path.abspath(path)):
                print("Datei konnte leider nicht automatisch geöffnet werden. ")
        else:
            print("Noch keine Kombination berechnet")

    def help_save(self):
        print("save [<filename>]\n    Speichert eine svg-Datei <filename>, wenn nichts anderes angegeben als 'diagram.svg' "
              "und öffnet ein Browserfenster mit der Datei (mit webbrowser.open). ")

    def do_exit(self, prm):
        print("exit...")
        return True

    def help_exit(self):
        print("exit\n    Beendet das Tool")

    def help_help(self):
        print("help <topic>\n    Zeigt Hilfe für den Befehl <topic>. ")


def get_yes_no(question):
    while True:
        answer = input(str(question) + "[y/n]")
        if answer == "y":
            return True
        elif answer == "n":
            return False
        print("Unbekannte Antwort '{}'".format(answer))


if __name__ == "__main__":
    print(
        "Dieses Kommandozeilentool berechnet optimale Widerstandskombinationen für die gegebenen Widerstandswerte, um "
        "einen gewissen Widerstand zu erhalten. \nGeschrieben für die 5. Aufabe des Bundeswettbewerbs Informatik "
        "2018. \nAutor: Florian Rädiker\n\n")
    if get_yes_no("Manuell einen Pfad zur Widerstandsliste setzen?"):
        path = input("Bitte Pfad eingeben: ")
    else:
        path = "widerstaende.txt"
    cmdl = ResistorCmd()
    cmdl.cmdloop(path, "Für mehr Informationen bitte 'help' eingeben")
