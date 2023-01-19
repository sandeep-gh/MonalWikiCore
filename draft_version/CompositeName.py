from typing import Any, NamedTuple
from .keys import BACKENDNAME
from typing import Any, NamedTuple
from .keys import MTIME, PTIME, ITEMID, LATEST_REVS, NAME_EXACT
import logging
from utilshelpermisc import parentids, get_fqname



app = None 
class CompositeName(NamedTuple):
    namespace: Any
    field: Any
    value: Any

def fullname(cn:CompositeName):
    return get_fqname(cn.value, cn.field, cn.namespace)

def query(cn:CompositeName):
    field = NAME_EXACT if not cn.field else cn.field
    return {NAMESPACE: cn.namespace, field: cn.value}

# why do we need app here
def get_root_fqname(cn:CompositeName):
    """
        Set value to the item_root of that namespace, and return
        the new CompositeName.
    """
    return CompositeName(cn.namespace, NAME_EXACT, app.cfg.root_mapping.get(cn.namespace, app.cfg.default_root))

