""" summarize a biff alert """

__all__ = ["summarize"]


def plural(num, single="", many="s"):
    """ plural """
    return single if num == 1 else many


def sane_fname(mbox):
    """ sanitise the mailbox name for notification """
    ret = str(mbox)
    if "." in ret:
        ret = ret.split(".")[-1]
    return ret


def summarize(diff):
    """ summarize """
    fhavenew = sorted(sane_fname(f) for f in diff.keys())
    mcount = sum(len(u) for u in diff.values())
    if len(fhavenew) == 1:
        fhavenew = fhavenew[0]
        summary = "folder %s has %s new message%s" % (fhavenew,
                                                      mcount,
                                                      plural(mcount))
    else:
        fhavenew = ", ".join(fhavenew[:-1]) + " & " + fhavenew[-1]
        summary = "folders %s have %s new message%s" % (fhavenew,
                                                        mcount,
                                                        plural(mcount))
    return summary
