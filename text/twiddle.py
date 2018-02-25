#!/usr/bin/python
""" twiddler """

import six


class Twiddle(object):  # pylint: disable=too-few-public-methods
    """ twiddler """
    CHARS = "/-\\|"
    LIMIT = len(CHARS)

    def __init__(self):
        self._idx = None

    def erase(self):
        """ erase for when others are going backwards too """
        if self._idx is not None:
            six.print_(" \b", end="", flush=True)

    def next(self):
        """ show the next twiddle """
        if self._idx in [None, Twiddle.LIMIT]:
            self._idx = 0
        six.print_("%s\b" % Twiddle.CHARS[self._idx], end="", flush=True)
        self._idx += 1
