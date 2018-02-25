""" notify abstraction """

# System imports
import time
from datetime import datetime
import six

# MY imports
from .dots import Dots
from .twiddle import Twiddle
from summary import summarize


__all__ = ["Alert"]


class Alert(object):
    """ alerter """
    def __init__(self, cfg):
        """ ctor """
        self._cfg = cfg
        self._dots = Dots()
        self._twiddle = Twiddle()

    def _log(self, *args, **kwargs):
        """ logging """
        self._dots.rewind(self._twiddle)
        now = datetime.now().replace(microsecond=0)
        six.print_("%s " % now, end="")
        six.print_(*args, **kwargs)
        self._dots.replay()

    def _sleep(self, target):
        """ sleep for a target time """
        slept = 0.0
        goal = self._cfg.getfloat(target)
        while goal and slept < goal:
            time.sleep(0.1)
            slept += 0.1
            goal = self._cfg.getfloat(target)

    def connected(self):
        """ connected """
        self._log("Connected")

    def mboxes(self, _mboxes):
        """ imap knows about the mail boxes """
        pass

    def mbox_checked(self, _mbox):
        """ mbox was checked """
        self._twiddle.next()
        self._sleep("mbox-sleep")

    def mboxes_checked(self):
        """ imap finished checking mail boxes """
        pass

    @staticmethod
    def mbox_unread(_mbox, _unread):
        """ mbox has unread """
        pass
        # self._log("Unread", mbox, unread)

    def biff(self, diff):
        """ biff """
        summary = summarize(diff)
        self._log(summary)

    def looped(self):
        """ looped """
        self._dots.next(self._twiddle)
        self._sleep("loop-sleep")
