#!/usr/bin/python
""" dots shower """

import six


class Dots(object):
    """ Dots shower """
    DOTS = [".", "..", "...", ".."]
    DCOUNT = len(DOTS)

    def __init__(self):
        """ Ctor """
        self._idx = None

    def rewind(self, twiddler=None):
        """ go back enough characters """
        if twiddler:
            twiddler.erase()
        if self._idx is not None:
            count = len(Dots.DOTS[self._idx])
            back = "\b" * count
            six.print_(back, end="", flush=True)

    def replay(self):
        """ replay the dots """
        if self._idx is not None:
            six.print_(Dots.DOTS[self._idx], end="", flush=True)

    def erase(self):
        """ erase the dots """
        count = len(Dots.DOTS[self._idx])
        back = "\b" * count
        wipe = " " * count
        six.print_("%s%s%s" % (back, wipe, back), end="", flush=True)

    def next(self, twiddler=None):
        """ next """
        if self._idx is None:
            self._idx = 0
            six.print_(Dots.DOTS[self._idx], end="", flush=True)
        else:
            if twiddler:
                twiddler.erase()
            self.erase()
            self._idx = (self._idx + 1) % Dots.DCOUNT
            six.print_(Dots.DOTS[self._idx], end="", flush=True)
