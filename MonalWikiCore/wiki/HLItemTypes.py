from typing import Any, NamedTuple
from ..constant_keys import ITEMTYPE_NONEXISTENT, ITEMTYPE_DEFAULT

class NonExistent(NamedTuple):
    shown:Any = False
    
NonExistent.itemtype = ITEMTYPE_NONEXISTENT

class Default(NamedTuple):
    fqname: Any
    rev: Any 
    content: Any

Default.itemtype = ITEMTYPE_DEFAULT
