"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Aufgabe 1 'Superstar'

PYTHON3

Dieses Modul enthält eine Klasse, TeeniGroup, die eine Gruppe im beschriebenen Netzwerk repräsentatiert.
Es kann z.B. geprüft werden, ob eine Person einer anderen folgt, diese Anfragen können gezählt werden und es kann ein
Superstar (sofern es einen gibt) mit möglichst wenig Anfragen bestimmt werden.
Für weitere Informationen siehe die Dokumentation zur Aufgabe.
"""
import random
import time
from functools import lru_cache

from loop_list import *


class TeeniGroup:
    def __init__(self, names, followers):
        """
        :param names: list of all names in the group
        :param followers: dict matching a person's name to a list of all the persons he/she is following
        """
        try:
            self.names = LoopIteratingList(names)
        except TypeError:
            raise TypeError("parameter 'names' must be convertible to 'list'")
        
        try:
            self.followers = dict(followers)
        except TypeError:
            raise TypeError("parameter 'followers' must be convertible to 'dict'")
        
        # validate data
        for person, followers in self.followers.items():
            if person not in self.names or not all((i in self.names for i in followers)):
                raise ValueError("'followers' contains unknown names")
            if person in followers:
                raise ValueError("person '{}' cannot follow oneself".format(person))
        self.start_request_counting()
    
    @staticmethod
    def from_textfile(path):
        """
        creates a TeeniGroup by parsing a text file specified by the BwInf-Website
        :param path: path to text file
        """
        with open(path, "r") as f:
            # read first line with all the names and split it
            names = f.readline().strip().split(" ")
            # read all followers
            followers = {}
            for i in f.readlines():
                info = i.strip().split(" ")
                if len(info) != 2:  # for empty lines
                    continue
                follower, person = info
                # add to dictionary
                try:
                    followers[follower].add(person)
                except KeyError:
                    # 'follower' is new
                    followers[follower] = {person}
        return TeeniGroup(names, followers)
    
    def start_request_counting(self):
        """
        resets the counter counting all requests with TeeniGroup.is_following
        :return:
        """
        # clear the cache and set the counter to zero
        self._is_following_raw.cache_clear()
        self._request_amount = 0
    
    def get_request_amount(self):
        """
        :return: The requests sent with is_following since the last time the counter was reset.
        """
        return self._request_amount
    
    def is_following(self, possible_follower, possible_followed_person, debug=False):
        """
        test if 'possible_follower' follows 'person' according to TeeniGroup.followers
        cached, no request will be counted twice
        :param possible_follower: str out of TeeniGroup.names
        :param possible_followed_person: str out of TeeniGroup.names
        :param debug: if True, shows debug info
        :return: True or False
        """
        if debug:
            current_size = self._is_following_raw.cache_info().currsize
            result = self._is_following_raw(possible_follower, possible_followed_person)
            # if the size hasn't changed, it was cached
            if current_size == self._is_following_raw.cache_info().currsize:
                # got info out of cache
                print("    IS_FOLLOWING", result, "CACHED", possible_follower,
                      ("follows" if result else "doesn't follow"), possible_followed_person)
            else:
                print("    IS_FOLLOWING", result, possible_follower,
                      ("follows" if result else "doesn't follow"), possible_followed_person)
            return result
        else:
            return self._is_following_raw(possible_follower, possible_followed_person)
    
    @lru_cache(None)  # unlimited, prevents from counting the same request twice
    def _is_following_raw(self, possible_follower, possible_followed_person):
        """
        test if 'possible_follower' follows 'person' according to TeeniGroup.followers
        cached, no request will be counted twice
        See the doc for TeeniGroup.is_following for more information.
        You should not use this function directly if you want debug information about cached requests.
        """
        if possible_follower not in self.names:  # validate parameter
            raise ValueError("unknown follower '{}'".format(possible_follower))
        # count this request
        self._request_amount += 1
        
        if possible_follower in self.followers:
            if possible_followed_person in self.followers[possible_follower]:
                result = True
            else:
                result = False
        else:
            result = False
        return result
    
    def is_not_following_anyone(self, possible_superstar, debug=False):
        """
        verifies that possible_superstar doesn't follow anyone
        Additionally, returns a person which could be the superstar because possible_superstar is following him/her
        and returns a list of non_superstars which are all not followed by possible_superstar and therefore cannot be
        superstars themselves
        :param possible_superstar:
        :param debug: if True, shows debug info
        :return: (True if possible_superstar follows no one, otherwise False;
        a person which could be the superstar;
        a set of non-superstars)
        """
        # test if possible_superstar does not follow anyone
        if debug:
            print("  verifying", possible_superstar, "follows no one")
        non_superstars = set()
        for possible_follower in self.names:
            # verify possible_follower is not followed by possible_superstar
            if possible_follower != possible_superstar:
                if self.is_following(possible_superstar, possible_follower, debug):
                    if debug:
                        print("   ", possible_superstar, "follows", possible_follower)
                    # a person (possible_follower) which is followed by someone *could* be the superstar, so return it
                    return False, possible_follower, non_superstars
                else:
                    # possible_follower is no superstar because he/she follows possible_superstar
                    if debug:
                        print("     ", possible_follower, "is no superstar, he/she is not followed by",
                              possible_superstar)
                    non_superstars.add(possible_follower)
        return True, None, non_superstars  # no person following another was found, so no possible superstar was found
    
    def is_followed_by_everyone(self, possible_superstar, debug=True):
        """
        tests if everyone listed in self.names follows possible_superstar
        Additionally returns a list of non-superstars which all follow the possible_superstar and therefore can't be
        superstars themselves
        :param possible_superstar:
        :param debug: if True,
        shows debug info
        :return: (True if everyone follows possible_superstar, otherwise False;
        a person which could be the superstar;
        a set of non-superstars)
        """
        if debug:
            print("  verifying", possible_superstar, "is followed by everyone")
        non_superstars = set()  # set of non-superstars
        for possible_follower in self.names:  # check every name
            if possible_follower != possible_superstar:
                if not self.is_following(possible_follower, possible_superstar, debug):
                    # possible_follower doesn't follow possible_superstar
                    if debug:
                        print("   ", possible_superstar, "is not followed by", possible_follower)
                    return False, possible_follower, non_superstars
                else:
                    # possible_follower is no superstar because he/she follows possible_superstar
                    if debug:
                        print("     ", possible_follower, "is no superstar, he/she follows", possible_superstar)
                    non_superstars.add(possible_follower)
        return True, None, non_superstars

    def get_superstar(self, shuffle=True, first_condition="not_following", debug=False):
        """
        Returns the calculated superstar as requested in the task by using Group.is_following.
        This method expects there is only one superstar
        :param shuffle: If True, shuffles the names in self.names for different results
        :param first_condition: 'not_following' or 'followed'. Specifies the first condition
        (TeeniGroup.is_not_following_anyone or TeeniGroup.is_followed_by_everyone) to be tested.
        :param debug: if True, shows debug info
        :return: (the name of the superstar, the amount for finding the superstar)
        """
        if first_condition == "not_following":
            first_condition = self.is_not_following_anyone
            second_condition = self.is_followed_by_everyone
        elif first_condition == "followed":
            first_condition = self.is_followed_by_everyone
            second_condition = self.is_not_following_anyone
        else:
            raise ValueError("Parameter 'first_condition' must be 'not_following' or 'followed'")
        
        self.start_request_counting()
        
        names = list(self.names).copy()
        if shuffle:
            # shuffle the names for different results.txt (there is no 'best' order)
            random.seed(time.time())
            random.shuffle(names)
        self.names = LoopIteratingList(names)
        possible_superstars = names.copy()
        
        # a possible superstar which should be tested next calculated by TeeniGroup.is_not_following_anyone
        next_possible_superstar = None
        
        while len(possible_superstars) > 0:
            if debug:
                print("\npossible", possible_superstars)
            
            # get the next superstar for testing
            if next_possible_superstar in possible_superstars:
                # a superstar found by TeeniGroup.is_not_following_anyone from last testing
                possible_superstar = next_possible_superstar
                possible_superstars.remove(next_possible_superstar)
                if debug:
                    print("TESTING", possible_superstar, "for superstar (found he/she is followed by someone while "
                                                         "testing)...")
            else:
                possible_superstar = possible_superstars.pop()
                if debug:
                    print("TESTING", possible_superstar, "for superstar...")
            
            # test the first condition
            first_condition_result, next_possible_superstar, non_superstars = first_condition(possible_superstar,
                                                                                                  debug)
            if first_condition_result:  # do not test further when this is not the superstar
                # as there will be either one or none superstar, the next superstar and non-superstars are not required
                second_condition_result, _, _ = second_condition(possible_superstar, debug)
                if second_condition_result:
                    # possible_superstar is not following anyone and followed by everyone! We found her/him!!!
                    return possible_superstar, self.get_request_amount()
                else:
                    # possible_superstar follows no one, but not everyone follows possible_superstar
                    # there is no superstar in this group
                    return None, self.get_request_amount()
            # remove all non_superstars
            for no_superstar in non_superstars:
                if no_superstar in possible_superstars:
                    possible_superstars.remove(no_superstar)
        return None, self.get_request_amount()
    
    def get_mean(self, count=10000):
        return sum(self.get_superstar()[1] for _ in range(count)) / count
    
    def get_max(self, count=1000):
        return max(self.get_superstar()[1] for _ in range(count))
