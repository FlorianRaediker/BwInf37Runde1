"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 2 'Twist'

PYTHON3

Stellt eine Klasse, TwistingDict, bereit, die die Wörterliste zum Enttwisten in unterschiedlich aufbereiteter Form
präsentiert. Für mehr Informationen siehe die Dokumentation.
"""
import time
import os
from hashable_counter import HashableCounter


class TwistingDict:
    START_LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                     "v", "w", "x", "x", "y", "z", "ae", "oe", "ue"]
    END_LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                   "v", "w", "x", "x", "y", "z", "ss", "ae", "oe", "ue", "ß", "e_"]

    LETTER_NORMALIZATION = {
        "ss": "ß",
        "e_": "é",
        "ae": "ä",
        "oe": "ö",
        "ue": "ü",
        "a_": "à"
    }

    def __init__(self, words_path="", words_start_path="", words_end_path="", debug=False, encoding="utf-8"):
        self.words = {}
        self.words_lower = {}
        self.words_start = {}
        self.words_end = {}
        if words_path:
            if debug:
                print("Initialisiere Wörter...")
                t1 = time.time()
            self.init_words(words_path, encoding)
            if debug:
                t2 = time.time()
                print("  Wörter in {:.4f} initialisiert".format(t2-t1))
        if words_start_path and words_end_path:
            if debug:
                print("Initialisiere zusammengesetzte Wörter...")
                t3 = time.time()
            self.init_compound_words(words_start_path, words_end_path, encoding)
            if debug:
                t4 = time.time()
                print("  zusammengesetzte Wörter in {:.4f} initialisiert".format(t4-t3))
                print("Wörterbuch in {:.4f} initialisiert".format(t4-t1))
    
    def init_words(self, path, encoding="utf-8"):
        """
        Initializes self.words and self.words_lower (see documentation)
        :param path: path to dictfile (see documentation)
        :param encoding: (Optional, 'utf-8') encoding for the file
        """
        with open(path, "r", encoding=encoding) as f:
            for line in f.readlines():
                key, value = line.strip().split("#")
                value = value.split(",")
                self.words[key] = value
                key_lower = key.lower()
                if key_lower not in self.words_lower:
                    self.words_lower[key_lower] = value
                else:
                    self.words_lower[key_lower] += value

    def init_compound_words(self, start_dir, end_dir, encoding="utf-8"):
        """
        Initializes self.words_start and self.words_end (see documentation)
        :param start_dir: directory to files for words_start
        :param end_dir: directory to files for words_end
        :param encoding: (Optional, 'utf-8') encoding for the files
        """
        for letter in self.START_LETTERS:
            with open(start_dir+"/"+letter, "r", encoding=encoding) as f:
                if letter in self.LETTER_NORMALIZATION:
                    letter = self.LETTER_NORMALIZATION[letter]
                self.words_start[letter] = {}
                for line in f.readlines():
                    key, value = line.strip().split("#")
                    self.words_start[letter][HashableCounter(key)] = value.split(",")
        for letter in os.listdir(end_dir):
            with open(end_dir+"/"+letter, "r", encoding=encoding) as f:
                if letter in self.LETTER_NORMALIZATION:
                    letter = self.LETTER_NORMALIZATION[letter]
                self.words_end[letter] = {}
                for line in f.readlines():
                    key, value = line.strip().split("#")
                    self.words_end[letter][HashableCounter(key)] = value.split(",")
