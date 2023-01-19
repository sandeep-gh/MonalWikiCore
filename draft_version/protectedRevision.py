from typing import Any, NamedTuple
from .keys import BACKENDNAME
from typing import Any, NamedTuple
from .keys import MTIME, PTIME, ITEMID, LATEST_REVS, NAME_EXACT
import logging
from utilshelpermisc import parentids


class ProtectedRevision(NamedTuple):
    protector: Any
    rev: any
    item: Any

def instantiate(protector, rev, p_item):
    if p_item:
        return ProtectedRevision(protector, rev, p_item)
    return ProtectedRevision(protector, rev, ProtectedItem(protector, rev.item))


def require(pr:ProtectedRevision, *capabilities):
    """require that at least one of the capabilities is allowed"""
    if not any(allows(pr.item, c) for c in capabilities):
        capability = " or ".join(capabilities)
        raise AccessDenied("revision does not allow user '{0!r}' to '{1!r}' [{2!r}]".format(
                           pr.protector.user.name, capability, pr.item.item.acl))




