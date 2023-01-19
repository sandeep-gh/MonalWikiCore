from typing import Any, NamedTuple
from constant_keys import CURRENT, ALL_REVS, BACKENDNAME, REVID 
import time
from indexes import indexes

from Meta import Meta
INDEXER_TIMEOUT = 20.0

class Revision(NamedTuple):
    idxitem: Any
    revid: Any
    doc: Any
    meta : Any
    name : Any

def retry_until_succeed(**kw):
    """
    
    """
    until = time.time() + INDEXER_TIMEOUT
    while True:
        indexer = indexes.document_search(**kw)
        if indexer is not None:
            break
        time.sleep(2)
        if time.time() > until:
            raise KeyError(kw.get('revid', '') + ' - server overload or corrupt index')
    return indexer

from Meta import Meta

def create(idxitem, revid, doc=None, name=None):
    
    #assert doc is not None
    is_current = revid  == CURRENT
    doc = retry_until_succeed(idx_name=ALL_REVS, revid=revid)

    if is_current:
        revid = doc.get(REVID)
        if revid is None:
            raise KeyError
    #backend_name = doc[BACKENDNAME]
    #Meta(Revision, doc, meta)
    meta = Meta(None, doc, None)
    names = meta.get_names()
    if name and name in names:
        _name = name
    else:
        _name = None
    revision = Revision(idxitem, revid, doc, meta, names)
    meta.revision = revision
    return revision 
