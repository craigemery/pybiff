""" windows notify code """

import sys
import os.path
from win10toast import ToastNotifier


MEDIR = os.path.split(__file__)[0]
ICON = os.path.join(MEDIR, os.pardir, "mail.ico")


def notify(summary):
    """ toaster """
    toaster = ToastNotifier()
    toaster.show_toast("biff", summary, icon_path=ICON, duration=10)


if __name__ == "__main__":
    notify(" ".join(sys.argv[1:]))
