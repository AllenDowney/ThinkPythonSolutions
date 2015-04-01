"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from bisect import bisect_left


def make_word_list():
    """Reads lines from a file and builds a list using append."""
    word_list = []
    fin = open('words.txt')
    for line in fin:
        word = line.strip()
        word_list.append(word)
    return word_list


def in_bisect(word_list, word):
    """Checks whether a word is in a list using bisection search.

    Precondition: the words in the list are sorted

    word_list: list of strings
    word: string
    """
    i = bisect_left(word_list, word)
    if i != len(word_list) and word_list[i] == word:
        return True
    else:
        return False


if __name__ == '__main__':
    word_list = make_word_list()
    
    for word in ['alien', 'allen']:
        print word, 'in list', in_bisect(word_list, word)


