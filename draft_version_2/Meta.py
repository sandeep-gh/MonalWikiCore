from dataclasses import dataclass
from constant_keys import NAME
from Name import get_proper_names
from typing import Any, NamedTuple

@dataclass
class Meta:
    revision:Any
    doc: Any
    meta:Any
    def get_names(self):
        """
         Get the (list of) names from meta data and deal with misc. bad things that
         can happen then (while not all code is fixed to do it correctly).
        
        TODO make sure meta[NAME] is always a list of str

        :param meta: a metadata dictionary that might have a NAME key
         :return: list of names
        """
        msg = "NAME is not a list but %r - fix this! Workaround enabled."
        names = meta.get(NAME)
        return get_proper_names(names)
