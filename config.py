#!/usr/bin/python

""" Config files made simpler """

import os
import stat
from six.moves import configparser


class Config(object):
    """ caching ConfigParser with dict method """
    def __init__(self, section, *fnames):
        """ Ctor """
        self._fnames = fnames
        self._modified = {}
        self._section = section
        self._cfg = None

    def _needs_read(self):
        """ have the files changed? """
        for fname in self._fnames:
            mod = os.stat(fname)[stat.ST_MTIME]
            if fname not in self._modified:
                self._modified[fname] = mod
                return True
            if mod > self._modified[fname]:
                self._modified[fname] = mod
                return True

    def _check(self):
        """ read """
        if self._cfg is None or self._needs_read():
            self._cfg = configparser.SafeConfigParser()
            self._cfg.read(self._fnames)

    def get(self, name):
        """ get """
        self._check()
        return self._cfg.get(self._section, name)

    def getint(self, name):
        """ get int """
        self._check()
        return self._cfg.getint(self._section, name)

    def getfloat(self, name):
        """ get float """
        self._check()
        return self._cfg.getfloat(self._section, name)

    def getboolean(self, name):
        """ get boolean """
        self._check()
        return self._cfg.getboolean(self._section, name)

    def __getitem__(self, name):
        """ Getter """
        return self.get(name)
