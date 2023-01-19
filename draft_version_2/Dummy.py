from typing import Any, NamedTuple
from constant_keys import ITEMTYPE, CONTENTTYPE,  NAMESPACE, UFIELDS_TYPELIST, NAME_EXACT, NAME, ITEMTYPE_NONEXISTENT
from contenttypes import CONTENTTYPE_NONEXISTENT
from io import BytesIO

class Rev(NamedTuple):
    """ if we have no stored Revision, we use this dummy """
    item: Any
    meta: Any
    data: Any
    revid: Any
    @classmethod
    def create(cls, item, itemtype=None, contenttype=None):
        fqname = item.fqname
        meta = {
            ITEMTYPE: itemtype or ITEMTYPE_NONEXISTENT,
            CONTENTTYPE: contenttype or CONTENTTYPE_NONEXISTENT
        }
        data = BytesIO(b'')
        revid = None
        if item:
            meta[NAMESPACE] = fqname.namespace
            if fqname.field in UFIELDS_TYPELIST:
                if fqname.field == NAME_EXACT:
                    meta[NAME] = [fqname.value]
                else:
                    meta[fqname.field] = [fqname.value]
            else:
                meta[fqname.field] = fqname.value
        return cls(item, meta, data, revid)
    

class Item(NamedTuple):
    """ if we have no stored Item, we use this dummy """
    fqname: Any

    @classmethod
    def create(cls, fqname):
        return Item(fqname)
    
    def list_revisions(self):
        return []  # same as an empty Item
    def destroy_all_revisions(self):
        return True
    
