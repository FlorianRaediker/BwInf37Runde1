#!/usr/bin/env python3
"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 2 'Twist'

PYTHON3

Stellt ein Kommandozeilentool bereit, um Texte zu (ent-)twisten.
Für eine Liste der Befehle nach dem Starten 'help' eingeben.
'help <topic>' gibt weitere Informationen zum Befehl <topic>.
"""
import os
import sys
cwd = os.path.dirname(__file__)  # current working directory
os.curdir = cwd  # access files in same dir
sys.path.append(cwd)  # find custom modules
import cmd
import twister


class TwisterCmd(cmd.Cmd):
    def __init__(self, twister_object, search_compounds=6, case_sensitive=False, all_results=True, apply_case=True,
                 exclamation=True, warning=True):
        super().__init__()
        self.prompt = "> "
        self.twister = twister_object
        self.settings = {"compounds": search_compounds, "case_sensitive": case_sensitive, "all_results": all_results,
                         "apply_case": apply_case, "exclamation": exclamation, "warning": warning}

    # ########
    # TWIST
    def do_twist(self, prm):
        print(self.twister.twist_text(prm))

    def help_twist(self):
        print("twist <text>\n    Twistet den Text <text> und gibt ihn aus. ")

    def do_twistfile(self, prm):
        try:
            with open(prm, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print("Konnte Datei '{}' nicht finden. ".format(prm))
        except BaseException as e:
            print(e)
            print("Konnte Datei '{}' nicht einlesen. ".format(prm))
        else:
            self.do_twist(text)

    def help_twistfile(self):
        print("twistfile <path>\n    Twistet die Textdatei unter <path> und gibt das Ergebnis aus. ")

    # ########
    # UNTWIST
    def do_untwist(self, prm):
        print(self.twister.untwist_text(prm, self.settings["case_sensitive"], self.settings["all_results"],
                                   self.settings["compounds"], self.settings["apply_case"],
                                   self.settings["exclamation"], self.settings["warning"]))

    def help_untwist(self):
        print("untwist <text>\n    Enttwistet den Text <text> gemäß den Einstellungen (siehe 'help set' für mehr "
              "Informationen) und gibt ihn aus")

    def do_untwistfile(self, prm):
        try:
            with open(prm, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print("Konnte Datei '{}' nicht finden. ".format(prm))
        except BaseException as e:
            print(e)
            print("Konnte Datei '{}' nicht einlesen. ".format(prm))
        else:
            print("Enttwiste Datei '{}'".format(prm))
            self.do_untwist(text)

    def help_untwistfile(self):
        print("untwistfile <path>\n    Enttwistet die Textdatei unter <path> gemäß den Einstellungen (siehe 'help set' "
              "für mehr Informationen) und gibt das Ergebnis aus")

    # ########
    # SETTINGS
    def do_set(self, prm):
        try:
            key, value = prm.split(" ")
            if key not in self.settings:
                raise ValueError
        except ValueError:
            print("Falsche Benutzung von 'set'. Siehe 'help set' für mehr Informationen")
        else:
            if key == "compounds":  # value is a number
                try:
                    value = int(value)
                except ValueError:
                    print("'{}' ist als <value> unzulässig. Siehe 'help set' für mehr Informationen. ".format(value))
                    return
                self.settings["compounds"] = value
                return
            
            value = value.lower()
            # check if value is number (0 is False, others are True)
            try:
                value = bool(int(value))
            except ValueError:
                if value in ("true", "t", "yes", "y"):
                    value = True
                elif value in ("false", "f", "no", "n"):
                    value = False
                else:
                    print("'{}' ist als <value> unzulässig. Siehe 'help set' für mehr Informationen. ".format(value))
                    return
            self.settings[key] = value
            print(self.settings)

    def help_set(self):
        print("""set <setting> <value> Setzt eine Einstellungsoption <setting> zum Enttwisten auf <value>. 
    <value> muss nach 'bool' konvertierbar sein (außer 'compounds', siehe dort)
    Alle für <setting> zulässige Einstellungen sind: 
      - compounds: Mindestanzahl an Buchstaben, damit ein getwistetes Wort auf eine Wortverbindung geprüft wird
      - case_sensitive: beim Suchen auf Groß-/Kleinschreibung achten
      - all_results: Wenn es mehrere Möglichkeiten gibt, ein Wort zu enttwisten, alle durch '/' getrennt ausgeben
      - apply_case: Übernimmt die Groß-/Kleinschreibung für das Ergebnis/die Ergebnisse vom getwisteten Wort
      - exclamation: fügt '(!)' vor  Wörtern ein, die nicht enttwistet werden konnten
      - warning: Wenn all_results False ist: Fügt '(?)' vor Wörter ein, bei denen es mehrere Möglichkeiten gibt""")

    # ########
    # OTHER
    def do_exit(self, prm):
        print("exit...")
        return True

    def help_exit(self):
        print("Beendet das Tool")

    def help_help(self):
        print("help <topic>\n    Zeigt Hilfe für den Befehl <topic>. ")


if __name__ == "__main__":
    print("DIESES KOMMANDOZEILENTOOL TWISTET UND ENTWISTET TEXTE NACH EINER AUFGABE IM BUNDESWETTBEWERB INFORMATIK "
    "2018. \nERSTELLT VON FLORIAN RÄDIKER\n")
    print("Initialisiere Wörterbuch mit allen Funktionen... (dauert bei mir etwa 10 Sekunden)")
    tw = twister.Twister("dict/words", "dict/start/", "dict/end/", True)
    cmdl = TwisterCmd(tw)
    cmdl.cmdloop("Für eine Liste von Befehlen 'help' eingeben. ")
