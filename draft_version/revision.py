from typing import Any, NamedTuple
from .keys import BACKENDNAME
from typing import Any, NamedTuple
from .keys import MTIME, PTIME
common_fields = [] #TODO: if this is static then statically use it


class RevisionItem(NamedTuple):
    item: Any
    revid: Any
    doc: Any
    #meta: Any
    name: Any


def rev_item(item, revid, doc=None, name=None):
    is_current = revid == CURRENT
    if doc is None:
        if is_current:
            doc = item._current
        else:
            doc = get_indexer(item.indexer._document, idx_name=ALL_REVS, revid=revid)
    if is_current:
        revid = doc.get(REVID)
        if revid is None:
            raise KeyError

    # this meta story is highly dubious
    # there is also no _data 
    #meta = Meta()
    #meta.doc = doc
    if name and name in self.names:
        _name = name
    else:
        _name = None
    rev_item = RevisionItem(item, revid, doc, _name)
    #meta.rev_item = rev_item
    return rev_item

            
            
def load(rev_item:Revision):
    """
    try to use and close data
    """
    backend_name = rev_item.doc.get_item(BACKENDNAME)
    meta, data = rev_item.item.backend.retrieve(backend_name, rev_item.revid)
    # since rev_item is immutable
    # something tells me that it should be immutable
    # TODO: the lifecycle of data is not clear
    # we need to data.close
    returm meta, data

    

def get_data(rev_item:RevisionItem):
    raise ValueError("not implemented")

def close_data(rev_item:RevisionItem):
    raise ValueError("not implemented")

def get_value(rev_item, meta, key):
    """
    look around and find value for a key associated with rev_item


    """
    if meta:
        return meta.get_item(key)
    elif rev_item.doc and key in common_fields:
        value = rev_item.doc.get_item(key)
        if key in [MTIME, PTIME]:
            # whoosh has a datetime object, but we want a UNIX timestamp
            value = utctimestamp(value)
            return value
    else:
        meta, data  = revision.load(rev_item)
        return meta.get_item(key)jb
        
        
    
    
