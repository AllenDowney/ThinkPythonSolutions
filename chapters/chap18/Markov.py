"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

import sys
import string
import random


class Markov(object):

    def __init__(self):
        self.suffix_map = {}        # map from prefixes to a list of suffixes
        self.prefix = ()            # current tuple of words

    def process_file(self, filename, order=2):
        """Reads a file and performs Markov analysis.

        filename: string
        order: integer number of words in the prefix

        Returns: map from prefix to list of possible suffixes.
        """
        fp = open(filename)
        self.skip_gutenberg_header(fp)

        for line in fp:
            for word in line.rstrip().split():
                self.process_word(word, order)

    def skip_gutenberg_header(self, fp):
        """Reads from fp until it finds the line that ends the header.

        fp: open file object
        """
        for line in fp:
            if line.startswith('*END*THE SMALL PRINT!'):
                break

    def process_word(self, word, order=2):
        """Processes each word.

        word: string
        order: integer

        During the first few iterations, all we do is store up the words; 
        after that we start adding entries to the dictionary.
        """
        if len(self.prefix) < order:
            self.prefix += (word,)
            return

        try:
            self.suffix_map[self.prefix].append(word)
        except KeyError:
            # if there is no entry for this prefix, make one
            self.suffix_map[self.prefix] = [word]

        self.prefix = shift(self.prefix, word)        

    def random_text(self, n=100):
        """Generates random wordsfrom the analyzed text.

        Starts with a random prefix from the dictionary.

        n: number of words to generate
        """
        # choose a random prefix (not weighted by frequency)
        start = random.choice(self.suffix_map.keys())

        for i in range(n):
            suffixes = self.suffix_map.get(start, None)
            if suffixes == None:
                # if the prefix isn't in map, we got to the end of the
                # original text, so we have to start again.
                random_text(n-i)
                return

            # choose a random suffix
            word = random.choice(suffixes)
            print word,
            start = shift(start, word)


def shift(t, word):
    """Forms a new tuple by removing the head and adding word to the tail.

    t: tuple of strings
    word: string

    Returns: tuple of strings
    """
    return t[1:] + (word,)


def main(name, filename, n=100, order=2, *args):
    try:
        n = int(n)
        order = int(order)
    except ValueError:
        print 'Usage: Markov.py filename [# of words] [prefix length]'
    else: 
        markov = Markov()
        markov.process_file(filename, order)
        markov.random_text(n)


if __name__ == '__main__':
    try:
        main(*sys.argv)
    except TypeError:
        print 'Usage: Markov.py filename [# of words] [prefix length]'
