"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 3 'Voll daneben'

PYTHON3

Stellt Funktionen bereit, um möglichst gute Zahlen zu berechnen.
"""
import math
import numpy as np


def get_al_numbers(lucky_numbers):
    if len(lucky_numbers) < 11:
        return list(lucky_numbers) + [0]*(10-len(lucky_numbers))
    al_numbers = [(i, 1) for i in sorted(lucky_numbers)]  # will be modified to get Al's numbers
    while True:
        # search for groups with a diff, a start and a stop index
        groups = {}  # group_diff: <list of all groups with that diff, every group as a slice (with start and stop)
        group_diff = None
        group_start = 0
        group_end = 0
        # start with the second, so the last number is the first
        last_num = al_numbers[0][0]
        for i in range(1, len(al_numbers)):
            num = al_numbers[i][0]  # the number for this index (i)
            diff = num-last_num
            if diff != group_diff:
                # start a new group, because this number has a different diff
                if group_end-group_start > 1:
                    # only groups longer than 1 element
                    if group_diff not in groups:
                        groups[group_diff] = [slice(group_start, group_end)]
                    else:
                        # groups with the same diff were found before
                        groups[group_diff].append(slice(group_start, group_end))
                # set the new diff
                group_diff = diff
                # the group starts with last_num
                group_start = i-1
            # the group end is now this element, but +1 for slice
            group_end = i+1
            last_num = num
        # the last group was not added to the dict, so do it now
        if group_end - group_start > 1:
            if group_diff not in groups:
                groups[group_diff] = [slice(group_start, group_end)]
            else:
                groups[group_diff].append(slice(group_start, group_end))

        min_groups = groups[min(groups)]  # list of groups with the smallest diff
        group_len = sum(g.stop-g.start for g in min_groups)  # size of the groups
        if len(al_numbers) - group_len + len(min_groups) < 10:
            # the resulting length would be smaller than 10, so simplify every group in min_groups,
            # but to more than only one new element per group
            max_len = 10 - (len(al_numbers) - group_len)  # count of elements which must be added
            # calculate the length of replace-elements for every group
            # the length is defined by the group's count of elements from the count of all elements
            lengths = [round(((g.stop-g.start)/group_len)*max_len) for g in min_groups[::-1]]
            # as the lengths are rounded, there could be too much or less
            diff = sum(lengths) - max_len
            if diff > 0:
                # the lengths are too small
                # the missing length is added to the smallest
                lengths[lengths.index(min(lengths))] += diff
            elif diff < 0:
                # the lengths are too big, the diff is substracted from the biggest length
                # the length normally does not get negative, because the diff is very small
                lengths[lengths.index(max(lengths))] += diff

            for group_slice, length in zip(min_groups[::-1], lengths):
                if length == 0:
                    # the group is too small (in proportion to the others)
                    # so it is replaced by an empty list
                    replace = []
                else:
                    start_num = al_numbers[group_slice.start][0]  # the first num in the group
                    end_num = al_numbers[group_slice.stop-1][0]  # the last num in the group
                    num_diff = end_num-start_num
                    step = num_diff / length
                    replace_nums = list(
                        np.arange(math.floor(start_num + step / 2), math.floor(end_num - step / 2 + 1), step))
                    replace = [(i, 1) for i in replace_nums]
                # replace the group with the new list
                al_numbers[group_slice.start:group_slice.stop] = replace
            # al_numbers contains 10 values, so return the rounded values (convert to 'int' to remove '.0')
            return [int(round(i[0])) for i in al_numbers]
        for group_slice in min_groups[::-1]:
            group = al_numbers[group_slice.start:group_slice.stop]
            group_weight_sum = sum(i[1] for i in group)  # sum of all weights in the group
            group_num_sum = sum(i[0]*i[1] for i in group)  # sum of all nums multiplied by the weight in the group
            new_num = group_num_sum / group_weight_sum  # mean value
            al_numbers[group_slice.start:group_slice.stop] = [(new_num, group_weight_sum)]
        if len(al_numbers) == 10:
            # al_numbers contains 10 values, so return the rounded values (convert to 'int' to remove '.0')
            return [int(round(i[0])) for i in al_numbers]
        elif len(al_numbers) < 10:
            raise ValueError("An unexpected error: Too many numbers have been removed")


def get_winnings(lucky_numbers, al_numbers):
    return sum(abs(num-get_nearest_number(list(al_numbers), num)) for num in lucky_numbers)


def get_profit(lucky_numbers, al_numbers):
    return len(lucky_numbers)*25 - get_winnings(lucky_numbers, al_numbers)


def get_nearest_number(iterable, value):
    """
    returns the nearest number in iterable to value
    """
    return min(iterable, key=lambda x: abs(x-value))
