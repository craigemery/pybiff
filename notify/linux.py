""" Linux notify """

import sys
import os


def notify(summary, log=None):
    """ toaster """
    cmd = 'notify-send -t 10000 biff "%s"' % summary
    if log:
        log("os.system('%s')" % cmd)
    os.system(cmd)


if __name__ == "__main__":
    notify(" ".join(sys.argv[1:]))
