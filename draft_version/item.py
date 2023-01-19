from typing import Any, NamedTuple
from .keys import BACKENDNAME
from typing import Any, NamedTuple
from .keys import MTIME, PTIME, ITEMID, LATEST_REVS, NAME_EXACT
import logging


class Item(NamedTuple):
    _name: Any
    _current: Any


indexer = None # indexer middlerware instance
backend = None # TODO: comes with backend

def create(self, name):
    """
    Return item with <name> (may be a new or existing item).
    """
    if name.startswith('@itemid/'):
        return Item(self, **{ITEMID: name[8:]})
    fqname = split_fqname(name)
    return Item(self, **{NAME_EXACT: fqname.value, NAMESPACE: fqname.namespace})
    
def get_names(meta):
    """
    Get the (list of) names from meta data and deal with misc. bad things that
    can happen then (while not all code is fixed to do it correctly).

    TODO make sure meta[NAME] is always a list of str

    :param meta: a metadata dictionary that might have a NAME key
    :return: list of names
    """
    msg = "NAME is not a list but %r - fix this! Workaround enabled."
    names = meta.get(NAME)
    if names is None:
        logging.warning(msg % names)
        names = []
    elif isinstance(names, bytes):
        logging.warning(msg % names)
        names = [names.decode('utf-8'), ]
    elif isinstance(names, str):
        logging.warning(msg % names)
        names = [names, ]
    elif isinstance(names, tuple):
        logging.warning(msg % names)
        names = list(names)
    elif not isinstance(names, list):
        raise TypeError("NAME is not a list but %r - fix this!" % names)
    if not names:
        names = []
    return names


def parent_names(names):
    """
    Compute list of parent names (same order as in names, but no dupes)

    :param names: item NAME from whoosh index, where NAME is a list
    :return: parent names list
    """
    parents = set()
    for name in names:
        parent_tail = name.rsplit('/', 1)
        if len(parent_tail) == 2:
            parents.add(parent_tail[0])
    return parents


def item_item(latest_doc=None, **query):
    _name = query.get(NAME_EXACT)
    if latest_doc is None:
        # we need to call the method without acl check to avoid endless recursion:
        latest_doc = self.indexer._document(**query)
        if latest_doc is None:
            # no such item, create a dummy doc that has a NAME entry to
            # avoid issues in the name(s) property code. if this was a
            # lookup for some specific item (using a name_exact query), we
            # put that name into the NAME list, otherwise it'll be empty:
            latest_doc = {}
            for field, value in query.items():
                latest_doc[field] = [value] if field in UFIELDS_TYPELIST else value
                latest_doc[NAME] = latest_doc[NAME_EXACT] if NAME_EXACT in query else []
            
    return Item(_name, latest_doc)

def get_itemid(item: Item):
    return item._current.get(ITEMID)

def set_itemid(item: Item, value):
    item._current[ITEMID] = value


    
    
def iter_revs(item):
    """
        Iterate over Revisions belonging to this item.
    """
    if item:
        for rev in indexer.documents(idx_name=ALL_REVS, itemid=get_itemid(item)):
            yield rev
            
def get_revision(item, revid):
    pass


def preprocessed(meta, data):
    raise ValueError
    pass

def store_revision(item, meta, data, overwrite=False,
                                          trusted=False,  # True for loading a serialized representation or other trusted sources
                       name=None,  # TODO name we decoded from URL path
                       action=ACTION_SAVE,
                       remote_addr=None,
                       userid=None,
                       wikiname=None,
                       contenttype_current=None,
                       contenttype_guessed=None,
                       acl_parent=None,
                       return_rev=False,
                       fqname=None,
                       ):
    """
    Store a revision into the backend, write metadata and data to it.
    """

    request = None #TODO: Somehow get the request object here
    remote_addr = None #TODO : in flask its request.remote_addr
    userid = None #TODO: get the userid somehow.its probably related to itemid
    if wikiname is None:
        wikiname = None #Get it from app.cfg
    raise ValueError("not implemented")


        

def destroy_revision(item, revid):
    raise ValueError("not implemented")


def destroy_all_revisions(item):
    """
        Destroy all revisions of this item.
    """
    for rev in item.iter_revs():
        self.destroy_revision(rev.revid)

            
