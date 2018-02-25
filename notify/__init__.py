""" notify abstraction """

try:
    from .win import notify
except ImportError:
    from .linux import notify
from summary import summarize


class Alert(object):
    """ alerter """
    # pylint: disable=too-few-public-methods
    @staticmethod
    def biff(diff):
        """ biff """
        summary = summarize(diff)
        notify(summary)
