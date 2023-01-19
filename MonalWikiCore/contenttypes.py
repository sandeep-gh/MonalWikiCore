CONTENTTYPE_NONEXISTENT = 'application/x-nonexistent'
CONTENTTYPE_DEFAULT = 'application/octet-stream'
CONTENTTYPE_MARKDOWN = 'text/x-markdown;charset=utf-8'

from aenum import Enum, auto

from typing import Any, NamedTuple
from dataclasses import dataclass

#explore this approach a little later
# @dataclass
# class NonExistent(NamedTuple):
#     group: Any = None
#     item: Any = None
#     def __init__(self, item_cons):
#         group =  None
#         item = item_cons(self)


@dataclass
class NonExistent:
    group = None
    item = None

NonExistent.type = CONTENTTYPE_NONEXISTENT

@dataclass    
class CSV:
    item = None

CSV.type = "text/csv"

@dataclass
class Markdown:
    item = None

    def to_plain_text(data):
        """
        data is probably binary string
        """
        return "return plain text for markdown"
Markdown.type = CONTENTTYPE_MARKDOWN #"text/x-markdown"

    
def get(contenttype, item = None):
    # ============== the whole match-case is not working :( =============
    # match contenttype:
    #     case CONTENTTYPE_NONEXISTENT:
    #         return NonExistent()
    # match contenttype:
    #     case CONTENTTYPE_NONEXISTENT:

    # Ideally contenttype shouldn't be None
    # Allowing it for now until more clarity
    if contenttype == None:
        return NonExistent()
    
    
    if contenttype == CONTENTTYPE_NONEXISTENT:
        return NonExistent()
    # if contenttype == CONTENTTYPE_DEFAULT:
    #     return OctetStream()

    # We need a more consistent way of mapping contenttype to class
    # for now just wing it. 
    if 'text/csv' in contenttype:
        return CSV()

    if 'text/x-markdown' in contenttype:
        return Markdown()
    assert False
             

