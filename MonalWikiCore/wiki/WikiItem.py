"""
defines surface/API and data structures to interact with core wiki. 
For e.g. frontend calls routines from this file only. 
"""

from typing import Any, NamedTuple
from ..constant_keys import MTIME, PTIME, ITEMID, LATEST_REVS, NAME_EXACT, UFIELDS, REVID, CONTENTTYPE, CURRENT, ITEMTYPE, ITEMTYPE_DEFAULT, ITEMTYPE_NONEXISTENT
from ..contenttypes import CONTENTTYPE_NONEXISTENT, CONTENTTYPE_DEFAULT
import logging
#from constant_keys import BACKENDNAME
from .. import Name
#from . import Dummy
from ..needs_home import FieldNotUniqueError, WikiItem, IndexQueryAnswer
#from Content import content_registry, Content, NonExistentContent
from ..contenttypes import NonExistent as NonExistent_Content, Markdown as Markdown_Content, get as get_content 
from .wikiItemTypes import NonExistent, Default
from ..engine import indexes
#import Revision
#import IndexItem
#from Content import Content
# from Registry import RegistryItem
# item_registry = RegistryItem()
# def register(cls):
#     item_registry.register(RegistryItem.Entry(cls._factory, cls.itemtype, cls.display_name, cls.description, cls.order),
#                            cls.shown)
#     return cls





def create(fqcn:Name.CompositeName, itemtype=ITEMTYPE_NONEXISTENT, contenttype=CONTENTTYPE_NONEXISTENT, rev_id=CURRENT, item:IndexQueryAnswer=None):
    """
    Create a highlevel Item by looking up :name or directly wrapping
    :item and extract the Revision designated by :rev_id revision.

    The highlevel wikiItem is created by creating an instance of Content
    subclass according to the item's contenttype metadata entry; The
    :contenttype argument can be used to override contenttype. It is used
    only when handling +convert (when deciding the contenttype of target
    item), +modify (when creating a new item whose contenttype is not yet
    decided), +diff and +diffraw (to coerce the Content to a common
    super-contenttype of both revisions).

    After that the Content instance, an instance of Item subclass is
    created according to the item's itemtype metadata entry, and the
    previously created Content instance is assigned to its content
    property.
    """

    # TODO: is the below check really necessary.
    # 
    # fqname = Name.split_fqname(item_name)
    # if fqname.field not in UFIELDS:  # Need a unique key to extract stored item.
    #     raise FieldNotUniqueError("field {0} is not in UFIELDS".format(fqname.field))

    assert item is None
    # we currently allow only.rev to be created via query over indexes 
    rev = indexes.get_storage_revision(fqcn, itemtype, contenttype, rev_id)
    print (f'for rev_id got rev: {rev}')
    # TODO: we do need some highlevel mechanism for going from rev to
    
    if rev.idxitem.answer is not None:
        # if there is already an entry for the 
        contenttype = rev.idxitem.answer.get(CONTENTTYPE) or contenttype
    #contenttype = rev.meta.get(CONTENTTYPE) or contenttypep
    #logging.debug("Item {0!r}, got contenttype {1!r} from revision meta".format(name, contenttype))
    # logging.debug("Item %r, rev meta dict: %r" % (name, dict(rev.meta)))

    # XXX Cannot pass item=item to Content.__init__ via
    # content_registry.get yet, have to patch it later.
    #print ("----------------------for Content ==================")
    #content = Content.create(contenttype)
    content = get_content(contenttype)
    
    #itemtype = rev.meta.get(ITEMTYPE) or itemtype or ITEMTYPE_DEFAULT
    if  rev.idxitem.answer  is not None:
        itemtype = rev.idxitem.answer.get(ITEMTYPE) or itemtype or ITEMTYPE_DEFAULT

    #logging.debug("Item {0!r}, got itemtype {1!r} from revision meta".format(name, itemtype))
    print ("----------------------for ITEM ==================")
    print (f"itemtype = {itemtype}")
    item = get_item(itemtype, fqcn, rev=rev, content=content)
    #item = item_registry.get(itemtype, fqname, rev=rev, content=content)
    #assert item is not None
    #logging.debug("Item class {0!r} handles {1!r}".format(item.__class__, itemtype))

    content.item = item
    print (f"item = {item}")
    return item


def get_item(itemtype, fqcn, **kwargs):
    #TODO: try to use match case here 
    if itemtype == ITEMTYPE_NONEXISTENT:
        return NonExistent(fqcn)
    if itemtype == ITEMTYPE_DEFAULT:
        return Default(fqcn, **kwargs)
    assert False
    
    


        
# class NonExistent(NamedTuple):
#     itemtype = ITEMTYPE_NONEXISTENT
#     shown = False
#     def render_html():
#         raise ValueError("not implemented")
    
    
# @register
# class NonExistent(wikiItem):
#     """
#     A dummy Item for nonexistent items (when modifying, a nonexistent item with
#     undetermined itemtype)
#     """
#     itemtype = ITEMTYPE_NONEXISTENT
#     shown = False

#     def _convert(self, doc):
#         #abort(404)
#         raise ValueError("Not implemented yet")
    
#     def do_show(self, revid, **kwargs):
#         # skip the idea of finding similar ma
#         #start, end, matches = find_matches(self.fqname)
#         #similar_names = sorted(matches.keys())
#         print ("Show on webpage")
#         print (self.fqname, " ", content_registry.group_names, " ", content_registry.groups)
#         # return render_template('modify_select_contenttype.html',
#         #                        fqname=self.fqname,
#         #                        item_name=self.name,
#         #                        itemtype='default',  # create a normal wiki item
#         #                        group_names=content_registry.group_names,
#         #                        groups=content_registry.groups,
#         #                        similar_names=similar_names,
#         #                        )
#         raise ValueError("Not implemented yet")

#     def do_modify(self):
#         raise ValueError("Not implemented yet")

#     def _select_itemtype(self):
#         raise ValueError("Not implemented yet")
#     def rename(self, name, comment=''):
#         # pointless for non-existing items
#         pass

#     def delete(self, comment=''):
#         # pointless for non-existing items
#         pass

#     def revert(self, comment=''):
#         # pointless for non-existing items
#         pass

#     def destroy(self, comment='', destroy_item=False):
#         # pointless for non-existing items
#         pass

