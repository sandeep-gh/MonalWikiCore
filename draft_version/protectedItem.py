from typing import Any, NamedTuple
from .keys import BACKENDNAME
from typing import Any, NamedTuple
from .keys import MTIME, PTIME, ITEMID, LATEST_REVS, NAME_EXACT
import logging
from utilshelpermisc import parentids


class ProtectedItem(NamedTuple):
    protector: Any
    item: Any

# def get_itemid(pitem:ProtectedItem):
#     #ideally we should call get_itemid(pitem.item) but this is fine too
#     return pitem.item._current.get(ITEMID)


def full_acls(pitem: ProtectedItem):
    acl_cfg = pitem.protector._get_configured_acls(pitem.item.fqname)
    before_acl = acl_cfg['before']
    after_acl = acl_cfg['after']
    for item_acl in pitem.protector.get_acls(pitem.item._current.get(ITEMID), pitem.item.fqname):
        if item_acl is None:
            item_acl = acl_cfg['default']
            yield ' '.join([before_acl, item_acl, after_acl])

            

def allows(pitem, right, user_names=None):
    """ Check if usernames may have <right> access on this item.

    :param right: the right to check
    :param user_names: user names to use for permissions check (default is to
                      use the user names doing the current request)
    :rtype: bool
    :returns: True if you have permission or False
    """
    if user_names is None:
        user_names = pitem.protector.user.name
    # must be a non-empty list of user names
    assert isinstance(user_names, list)
    assert user_names
    acl_cfg = pitem.protector._get_configured_acls(get_fqname(pitem.item))
    for user_name in user_names:
        for full_acl in self.full_acls():
            allowed = self.protector.eval_acl(full_acl, acl_cfg['default'], user_name, right)
            if allowed is True and pchecker(right, allowed, self.item):
                return True
    return False            

def require(pitem:ProtectedItem, *capabilities):
    """require that at least one of the capabilities is allowed"""
    if not any(allows(pitem, c) for c in capabilities):
        capability = " or ".join(capabilities)
        raise AccessDenied("item does not allow user '{0!r}' to '{1!r}' [{2!r}]".format(
                           pitem.protector.user.name, capability, self.item.acl))


def iter_revs(pitem:ProtectedItem):
    require(pitem, READ)
    if pitem:
        for rev in iter_revs(pitem.item()):
            yield ProtectedRevision(pitem.protector, rev, p_item=pitem)


            
def get_revid(pitem:ProtectedItem, revid:Any):
    require(pitem, PUBREAD)
    rev_item = get_revision(pitem.item, revid)
    return ProtectedRevision(pitem.protector, rev, p_item=pitem)

def store_revision(pitem, meta, data, overwrite=False, return_rev=False, return_meta=False, fqname=None, **kw):
    require(pitem, WRITE)
    if not pitem:
        require(pitem, CREATE)
    if overwrite:
        require(pitem, DESTROY)
    if meta.get(ACL) != pitem.item.meta.get(ACL)
        require(pitem, ADMIN)
    rev = store_revision(pitem.item, meta, data, overwrite=overwrite, return_rev=return_rev, fqname=fqname, **kw)
    if rev:  # tests may return None
        close_file(rev.data)
    if return_meta:
        # handle odd case where user changes or reverts ACLs and loses read permission
        # email notifications will be sent and user will get 403 on item show
        pr = ProtectedRevision(self.protector, rev, p_item=self)
        self.protector._clear_acl_cache()
        return (pr.fqname, pr.meta)
    pitem.protector._clear_acl_cache()
    if return_rev:
        return ProtectedRevision(pitem.protector, rev, p_item=pitem)

def store_all_revisions(pitem, meta, data):
    raise ValueError("Not Implemented")


def destroy_revision(pitem, revid):
    raise ValueError("Not Implemented")

def destroy_all_revisions(pitem):
    raise ValueError("Not Implemented")

    



