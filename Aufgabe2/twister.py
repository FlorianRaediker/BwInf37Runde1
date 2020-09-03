"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 2 'Twist'

PYTHON3

Dieses Modul stellt eine Klasse, Twister, bereit, die twisten und enttwisten kann.
Für mehr Informationen siehe die Dokumentation.
"""
import itertools
import re
import random
import sys
import os.path
from functools import lru_cache

sys.path.append(os.path.dirname(__file__))  # for custom modules in same directory
import wordoperations
from hashable_counter import HashableCounter
from twisting_dict import TwistingDict


class Twister:
    FAILS = 0
    CACHE_SIZE = 512
    WORD_PATTERN = r"[a-zA-ZäöüÄÖÜßẞ]{4,}"

    def __init__(self, dict_words_path="dict_words.txt", dict_words_start_path="", dict_words_end_path="", debug=False):
        self.dict = TwistingDict(dict_words_path, dict_words_start_path, dict_words_end_path, debug)

    # ########
    # ########
    # TWIST

    # word
    def twist_word(self, word):
        """
        twists the word 'word'
        :param word: string containing one word
        :return: the twisted word
        """
        if len(word) < 4:  # twisting small words has no effect
            return word
        # shuffle only the middle of word
        middle = list(word[1:-1])
        random.shuffle(middle)
        return word[0] + "".join(middle) + word[-1]

    # text
    def twist_text(self, text):
        """
        Twists the text 'text'. Words are filtered with Twister.WORD_PATTERN and twisted with self.twist_match.
        :param text: string containing text
        :return: the twisted text
        """
        return re.sub(self.WORD_PATTERN, self.twist_match, text)

    def twist_match(self, match):
        """
        twists 'match' (from module 're'). Similar to self.twist_word, but twist_word is not called in this function
        (it's a bit faster).
        :param match: re match
        :return: twisted word
        """
        word = match.group(0)
        if len(word) < 4:  # twisting small words has no effect
            return word
        # shuffle only the middle
        middle = list(word[1:-1])
        random.shuffle(middle)
        return word[0] + "".join(middle) + word[-1]

    # ########
    # ########
    # UNTWIST
    
    # ########
    # FAST and SIMPLE methods
    
    def untwist_text_fast(self, text):
        return re.sub(self.WORD_PATTERN,
                      lambda match: self.untwist_word_fast(match.group(0)),
                      text, flags=re.UNICODE)
    
    @lru_cache(CACHE_SIZE)
    def untwist_word_fast(self, word):
        sorted_word = wordoperations.sort_word(word.lower())
        res = self.untwist_sorted_word_to_list_fast(sorted_word)
        if not res:  # no match could be found
            return "(!)" + word
        for i in range(len(res)):
            res[i] = wordoperations.apply_case(word, res[i])
        return "/".join(res)
    
    @lru_cache(CACHE_SIZE)
    def untwist_sorted_word_to_list_fast(self, sorted_word):
        try:
            return self.dict.words_lower[sorted_word]
        except KeyError:
            return self.untwist_compound_word_fast(sorted_word)

    def untwist_compound_word_fast(self, sorted_word):
        """
        Tries to untwist a lower compound word containing two words.
        This function requires a fully initialized dictionary (with compounds).
        It is faster than the normal function because all options are enabled.
        :param sorted_word: string containing the already sorted (possible) compound word
        :return: list of possible untwisted words or a list containing the 'word' itself if no result could be found
        """
        if len(sorted_word) < 7:  # words with 6 letters are almost every time no compounds
            return None
        middle = sorted_word[1:-1]
        middle_hash = HashableCounter(middle)
        first_words = self.dict.words_start[sorted_word[0]]
        second_words = self.dict.words_end[sorted_word[-1]]
        results = []
        for first_hash, first_word_list in first_words.items():
            try:
                possible_second_hash = middle_hash - first_hash
            except ArithmeticError:
                continue
            try:
                second_word_list = second_words[possible_second_hash]
            except KeyError:
                if possible_second_hash["s"] > 0:
                    # the word contains an 's' (maybe an epenthesis???), so try without it again
                    possible_second_hash["s"] -= 1
                    try:
                        second_word_list = second_words[possible_second_hash]
                    except KeyError:
                        # there is no suitable second word
                        continue
                    # add results with epenthesis
                    results += (first + "s" + second for first, second in itertools.product(first_word_list,
                                                                                            second_word_list))
                    continue
                else:
                    # there is no suitable second word
                    continue
            results += (first+second for first, second in
                        itertools.product(first_word_list, second_word_list))
        return results
    
    # ########
    # methods with MORE OPTIONS, but SLOWER

    def untwist_text(self, text, case_sensitive=False, all_results=True, search_compounds=7, apply_case=True,
                     add_exclamation=True, add_warning=True):
        """
        Untwists a text 'text' with the specified options
        :param text: string containing words matching Twister.WORD_PATTERN
        :param case_sensitive: (Optional) If True, the search for a word will be case sensitive
        :param all_results: (Optional) If True, includes all results by separating them with a slash ('/').
        Otherwise only returns the first match
        :param search_compounds: (Optional) Minimum letter-count for a compound-search.
        :param apply_case: (Optional) If True, applies the case of 'word' to the results
        :param add_exclamation: (Optional) If True, adds '(!)' before words that could not be untwisted
        :param add_warning: (Optional) If True and all_results is disabled, adds '(?)' before the word if there are
        multiple results.
        :return: the untwisted text as str
        """
        return re.sub(self.WORD_PATTERN, lambda match: self.untwist_word(match.group(0), case_sensitive, all_results,
                                                                         search_compounds, apply_case, add_exclamation,
                                                                         add_warning), text, flags=re.UNICODE)

    @lru_cache(CACHE_SIZE)
    def untwist_word(self, word, case_sensitive=False, all_results=True, search_compounds=7, apply_case=True,
                     add_exclamation=True, add_warning=True):
        """
        untwists a word 'word' and returns the untwisted word as a str with the specified options.
        :param word: string containing one word
        :param case_sensitive: (Optional) If True, the search for a word will be case sensitive
        :param all_results: (Optional) If True, includes all results by separating them with a slash ('/').
        Otherwise only returns the first match
        :param search_compounds: (Optional) Minimum of letters for a compound-search.
        :param apply_case: (Optional) If True, applies the case of 'word' to the results
        :param add_exclamation: (Optional) If True, adds '(!)' before words that could not be untwisted
        :param add_warning: (Optional) If True and all_results is disabled, adds '(?)' before the word if there are
        multiple results.
        :return: the untwisted word as str
        """
        words = self.untwist_word_to_list(word, case_sensitive, search_compounds, apply_case, add_exclamation)
        if all_results:
            # show all results
            return "/".join(words)
        else:
            if len(words) > 1 and add_warning:
                # there are multiple results, but only the first result is to be shown, so add a warning
                return "(?)" + words[0]
            else:
                # there is only one result and no warning is to be shown
                return words[0]

    @lru_cache(CACHE_SIZE)
    def untwist_word_to_list(self, word, case_sensitive=False, search_compounds=7, apply_case=True,
                             add_exclamation=True):
        """
        untwists the word 'word' with the specified settings and returns a list
        :param word: string containing one word
        :param case_sensitive: (Optional) If True, the search for a word will be case sensitive
        :param search_compounds: (Optional) Minimum of letters for a compound-search.
        :param apply_case: (Optional) If True, applies the case of 'word' to the results
        :param add_exclamation: (Optional) If True, adds '(!)' before words that could not be untwisted
        :return: a list of possible untwisted words matching the given 'word'
        """
        length = len(word)
        if length < 4:  # ignore small words, they don't change
            return [word]
        # to find words in self.dict.words, sort it
        sorted_word = wordoperations.sort_word(word)
        try:
            if case_sensitive:
                res = self.dict.words[sorted_word]
            else:
                res = self.dict.words_lower[sorted_word.lower()]
        except KeyError:
            # no word could be found, so try other possibilities
            if length >= search_compounds:
                res = self.untwist_compound_word(word)
                if res:
                    # some compound words were found
                    return res
            if add_exclamation:
                # no word could be found, so add a warning
                return ["(!)" + word]
            return [word]
        if apply_case:
            for i in range(len(res)):
                res[i] = wordoperations.apply_case(word, res[i])
        return res

    def untwist_compound_word(self, word, epenthesis=True):
        """
        Tries to untwist a compound word containing two words.
        This function requires a fully initialized dictionary (with compounds)
        :param word: string containing the (possible) compound word
        :param epenthesis: if True, word with 's' as an epenthesis will be recognized
         :return: list of possible untwisted words or an empty list if no result could be found
        """
        word_lower = word.lower()
        first_words = self.dict.words_start[word_lower[0]]  # all words starting with the same letter as the word
        second_words = self.dict.words_end[word_lower[-1]]  # all words ending with the same letter as the word
        middle = word_lower[1:-1]
        middle_hash = HashableCounter(middle)  # the Counter to search for
        results = []  # saves all results
        for first_hash, first_word_list in first_words.items():
            # first_hash is a HashableCounter
            # first_word_list is a list containing all words matching first_hash
            try:
                # possible_second_hash is the HashableCounter a second word must have if the first word is correct
                possible_second_hash = middle_hash - first_hash
            except ArithmeticError:
                # first_hash contains more letters than the middle (and therefore cannot be one of the two words)
                continue
        
            try:
                second_word_list = second_words[possible_second_hash]
            except KeyError:
                if epenthesis and possible_second_hash["s"] > 0:
                    # the word contains an 's' (maybe an epenthesis???), so try without it again
                    possible_second_hash["s"] -= 1
                    try:
                        second_word_list = second_words[possible_second_hash]
                    except KeyError:
                        # there is no suitable second word
                        continue
                    # add results with epenthesis
                    separition_pos = len(first_word_list[0])
                    results += (
                        wordoperations.apply_case(word[:separition_pos] + "s" + word[separition_pos + 1:],
                                                  first + "s" + second)
                        for first, second in itertools.product(first_word_list, second_word_list))
                    continue
                else:
                    # there is no suitable second word
                    continue
            # if epenthesis_text:
            # else:
            results += (wordoperations.apply_case(word, first + second) for first, second in
                        itertools.product(first_word_list, second_word_list))
        return results
