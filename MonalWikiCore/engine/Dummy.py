from typing import Any, NamedTuple
from ..constant_keys import ITEMTYPE, CONTENTTYPE,  NAMESPACE, UFIELDS_TYPELIST, NAME_EXACT, NAME, ITEMTYPE_NONEXISTENT
from ..contenttypes import CONTENTTYPE_NONEXISTENT
from io import BytesIO
from ..needs_home import IndexQueryAnswer
from ..Name import CompositeName

class Rev(NamedTuple):
    """ if we have no stored Revision, we use this dummy """
    fqcn: Any
    idxitem: Any
    meta: Any
    data: Any
    revid: Any
    @classmethod
    def create(cls, fqcn:CompositeName, idxitem:IndexQueryAnswer,   itemtype=None, contenttype=None):
        """
        creat a dummy rev; 
        revid : None 
        data : Nonej
        idxitem : derived from whoosh query fqcn 
        """
        fqcn = fqcn
        meta = {
            ITEMTYPE: itemtype or ITEMTYPE_NONEXISTENT,
            CONTENTTYPE: contenttype or CONTENTTYPE_NONEXISTENT
        }
        data = None #BytesIO(b'')
        revid = None
        #meta = None 
        # if item:
        #     # no idea what should go into meta 
        #     meta[NAMESPACE] = fqcn[NAMESPACE]
        #     meta[NAME_EXACT]  = fqcn[NAME_EXACT]
        #     meta[NAME] = fqcn[NAME]
            # if fqname.field in UFIELDS_TYPELIST:
            #     if fqname.field == NAME_EXACT:
            #         meta[NAME] = [fqname.value]
            #     else:
            #         meta[fqname.field] = [fqname.value]
            # else:
            #     meta[fqname.field] = fqname.value
        return cls(fqcn, idxitem, meta, data, revid)
    

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
    
