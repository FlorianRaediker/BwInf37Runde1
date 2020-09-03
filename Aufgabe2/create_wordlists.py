#!/usr/bin/env python3
from hashable_counter import HashableCounter
import wordoperations


class StringCounter(HashableCounter):
    def __str__(self):
        return "".join(self.elements())


word_list = set()
path = "woerterliste.txt"  # change to real path

with open(path, "r") as f:
    for line in f.readlines():
        word_list.add(line.strip())
word_list = sorted(list(word_list))


words = {}
words_lower = {}
start_letters = "abcdefghijklmnopqrstuvwxyzäöü"
end_letters = "abcdefghijklmnopqrstuvwxyzäöüßéà"
words_start = {letter: {} for letter in start_letters}
words_end =   {letter: {} for letter in end_letters}
for word in word_list:
    length = len(word)
    if length > 3:  # no need of adding 3-letter words, they are not changed by twisting
        key = wordoperations.sort_word(word)
        key_lower = key.lower()
        # there are duplicates in the file (ein, eine, bietet, lange, ...), so remove them
        try:
            if word not in words[key]:  # remove doubles in list
                words[key].append(word)
        except KeyError:
            words[key] = [word]
        try:
            if word not in words_lower[key_lower]:  # remove doubles in list
                words_lower[key_lower].append(word)
        except KeyError:
            words_lower[key_lower] = [word]
    # add all size of words in case they are in composed words
    word_lower = word.lower()
    start = word_lower[0]
    end = word_lower[-1]
    end_hash = StringCounter(word_lower[:-1])
    start_hash = StringCounter(word_lower[1:])
    try:
        words_start[start][start_hash].append(word)
    except KeyError:
        # length does not exist in this letter's section
        words_start[start][start_hash] = [word]
    try:
        words_end[end][end_hash].append(word)
    except KeyError:
        # length does not exist in this letter's section
        words_end[end][end_hash] = [word]

LETTER_NORMALIZATION = {
    "ß": "ss",
    "é": "e_",
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "à": "a_"
}
with open("dict/words", "w") as f:
    for key, value in words.items():
        f.write(key + "#" + ",".join(value) + "\n")

for key, value in words_start.items():
    if key in LETTER_NORMALIZATION:
        key = LETTER_NORMALIZATION[key]
    with open("dict/start/"+key, "w") as f:
        for counter, lst in value.items():
            f.write(str(counter) + "#" + ",".join(lst) + "\n")

for key, value in words_end.items():
    if key in LETTER_NORMALIZATION:
        key = LETTER_NORMALIZATION[key]
    with open("dict/end/"+key, "w") as f:
        for counter, lst in value.items():
            f.write(str(counter) + "#" + ",".join(lst) + "\n")
