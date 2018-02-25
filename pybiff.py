#!/usr/bin/python

""" Biff on IMAP folders """

# System imports
import os

# MY imports
from config import Config
import text
import notify
from imap import Monitor

ME = os.path.splitext(__file__)[0]
CONFIG_PATH = ME + ".cfg"
SECTION = "email"


def main():
    """ entry point """
    cfg = Config(SECTION, CONFIG_PATH)
    mon = Monitor(cfg, text.Alert(cfg), notify.Alert())
    mon.watch("Archives.", "Spam", "Drafts", "Trash", "Templates", "Sent")


if __name__ == "__main__":
    main()
