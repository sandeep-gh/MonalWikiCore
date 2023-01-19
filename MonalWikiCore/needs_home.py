from .constant_keys import NAMESPACE_DEFAULT, NAMESPACE_USERPROFILES, NAMESPACE_USERS, ITEMID
from typing import Any, NamedTuple
namespaces = {
        # maps namespace name -> backend name
        # these 3 standard namespaces are required, these have separate backends
        NAMESPACE_DEFAULT: 'default',
        NAMESPACE_USERS: 'users',
        NAMESPACE_USERPROFILES: 'userprofiles',
        # namespaces for editor help files are optional, if unwanted delete here and in backends and acls
        'help-common': 'help-common',  # contains media files used by other language helps
        'help-en': 'help-en',  # replace this with help-de, help-ru, etc.
        # define custom namespaces if desired, trailing / below causes foo to be stored in default backend
        # 'foo/': 'default',
        # custom namespace with a separate backend - note absence of trailing /
        # 'bar': 'bar',
    }


# we need the longest mountpoints first, shortest last (-> '' is very last)
namespace_mapping =  sorted(namespaces.items(), key=lambda x: len(x[0]), reverse=True)  
namespaces = {namespace.rstrip('/') for namespace, _ in namespace_mapping}
class FieldNotUniqueError(ValueError):
    """
    The Field is not a UFIELD(unique Field).
    Non unique fields can refer to more than one item.
    """

    

#putting wikiItem definition here; because its used by wiki.WikiItem and engine.indexes
#modules; and wikiItem imports indexes; basically to avoid circular dependency
class WikiItem:
    """ A stub/tag/proxy/abstract-class for realized wikiItem class 
    NonExistent|Default. A top level class used by frontend/view functions
    to render webpages. 
    """
    # # placeholder values for registry entry properties
    # # we don't use registry; lets turn it off
    # itemtype = ''
    # display_name = ''
    # description = ''
    # shown = True
    # order = 0

    # @classmethod
    # def _factory(cls, *args, **kw):
    #     return cls(*args, **kw)
    # def __init__(self, fqname, rev=None, content=None):
    #     self.fqcn = fqname
    #     self.rev = rev
    #     self.content = content
        
    # def get_meta(self):
    #     return self.rev.meta
    # meta = property(fget=get_meta)
    pass 

# Putting it here to avoid circular dependecy between WikiItem and indexes     
class IndexQueryAnswer(NamedTuple):
    """
    query: the search key-value terms used to query whoosh index
    current: the whoosh resultant query result
    """
    query: Any
    answer: Any
    # def id(self):
    #     return self.current.get(ITEMID)


