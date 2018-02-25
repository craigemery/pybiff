#!/usr/bin/python

""" IMAP fun """

import imaplib

__all__ = ["Server", "Monitor"]


def quote(name):
    """ quote if need be """
    return '"%s"' % name if " " in name else name


def dequote(name):
    """ dequote if need be """
    if name[0] == '"' and name[-1] == '"':
        return name[1:-1]
    return name


def asint(chars):
    """ is a string an integer """
    try:
        return int(chars)
    except ValueError:
        pass


class Server(object):
    """ wrap server operations with helpers & re-connects """
    def __init__(self, hostname, user, password):
        self._host = hostname
        self._user = user
        self._cred = password
        self._conn = None

    def shutdown(self):
        """ shutdown """
        try:
            if self._conn:
                self._conn.shutdown()
            self._conn = None
        except Exception:  # pylint: disable=broad-except
            pass

    def _do(self, command, *args, **kwargs):
        """ do a command on the server, retry once """
        retry = 2
        answer = None
        while retry > 0:
            try:
                func = getattr(self.connection, command)
                status, answer = func(*args, **kwargs)
                assert status == 'OK', "imap answer %s not OK" % answer
                retry = -1
            except AttributeError:
                exit(-1)
            except (IOError, imaplib.IMAP4_SSL.abort) as exx:
                self.shutdown()
                retry -= 1
                if answer == 0:
                    raise RuntimeError(exx)
        return answer

    @property
    def connection(self):
        """ connection attrib """
        if self._conn is None:
            self._conn = imaplib.IMAP4_SSL(self._host)
            try:
                self._do("login", self._user, self._cred)
            except AssertionError:
                self.shutdown()
                raise
        return self._conn

    def __nonzero__(self):
        """ bool means connected & logged on """
        return self.connection is not None

    @property
    def folders(self):
        """ folders getter """
        for ent in self._do("list"):
            yield dequote(ent.decode().split(' "." ')[-1])

    def unseen(self, mbox):
        """ the unseen email ID's in an mbox """
        self._do("select", quote(mbox), True)
        answer = self._do("search", 'US-ASCII', 'UNSEEN')
        return set(asint(i) for i in answer[0].split() if asint(i) is not None) or None


class Monitor(object):  # pylint: disable=too-few-public-methods
    """ Monitor folders """
    def __init__(self, config, *observers):
        self._cfg = config
        self._observers = observers
        self._server = Server(self._cfg["hostname"],
                              self._cfg["username"],
                              self._cfg["password"])
        self._data = {}

    def _publish(self, message, *args, **kwargs):
        """ publish """
        for obs in self._observers:
            try:
                func = getattr(obs, message)
                func(*args, **kwargs)
            except AttributeError:
                pass  # if the observer doesn'y have the method, ignore this

    def _watching(self, exclude):
        """ folder watchlist """
        def elide(folder):
            """ a filter """
            if exclude is None:
                return True
            for pattern in exclude:
                if pattern[-1] == ".":
                    if folder.startswith(pattern):
                        return True
                    pattern = pattern[:-1]
                    if folder == pattern:
                        return True
                elif folder == pattern:
                    return True
            return False

        for folder in self._server.folders:
            if not elide(folder):
                yield folder

    def _has_new(self, mbox):
        """ does the mbox have new emails? return the unseen ID's """
        ret = None
        new = self._server.unseen(mbox)
        self._publish("mbox_checked", mbox)
        if new:
            self._publish("mbox_unread", mbox, new)
        if new and mbox in self._data and new != self._data[mbox]:
            ret = new
        self._data[mbox] = new
        return ret

    def _all_new(self, folders):
        """ All the new unseen email ID's """
        self._publish("mboxes", folders)
        ret = {}
        for mbox in folders:
            val = self._has_new(mbox)
            if val:
                ret[mbox] = val
        self._publish("mboxes_checked")
        return ret

    def watch(self, *exclude):
        """ Scan folders, alert the observers """
        if not self._server.connection:
            return
        self._publish("connected")
        while True:
            diff = self._all_new(self._watching(exclude))
            if diff:
                self._publish("biff", diff)
            self._publish("looped")
