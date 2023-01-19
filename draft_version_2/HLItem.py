from typing import Any, NamedTuple
from constant_keys import MTIME, PTIME, ITEMID, LATEST_REVS, NAME_EXACT, UFIELDS, REVID, CONTENTTYPE, CURRENT, ITEMTYPE, ITEMTYPE_DEFAULT, ITEMTYPE_NONEXISTENT
import logging
#from constant_keys import BACKENDNAME
import Name
import Dummy
from needs_home import FieldNotUniqueError
from Content import content_registry, Content, NonExistentContent

import Revision
import IndexItem
#from Content import Content
#from Registry import RegistryItem
item_registry = RegistryItem()
def register(cls):
    item_registry.register(RegistryItem.Entry(cls._factory, cls.itemtype, cls.display_name, cls.description, cls.order),
                           cls.shown)
    return cls


def get_storage_revision(fqname, itemtype=None, contenttype=None, rev_id=CURRENT, item:IndexItem.IndexItem=None):
    """
    Get a storage Revision.

    If :item is supplied it is used as the storage Item; otherwise the storage
    Item is looked up with :name. If it is not found (either because the item
    doesn't exist or the user does not have the required permissions) a
    DummyItem is created, and a DummyRev is created with appropriate metadata
    properties and the "item" property pointing to the DummyItem. The DummyRev
    is then returned.

    If the previous step didn't end up with a DummyRev, the revision
    designated by :rev_id is then looked up. If it is not found, current
    revision is looked up and returned instead. If current revision is not
    found (i.e. the item has no revision), a DummyRev is created. (TODO: in
    the last two cases, emit warnings or throw exceptions.)

    :itemtype and :contenttype are used when creating a DummyRev, where
    metadata is not available from the storage.
    """
    rev_id = fqname.value if fqname.field == REVID else rev_id
    if item is None:
        #TODO: use protected storage. not up yet
        #Instead use indexes and  return IndexItem 
        #item = flaskg.storage.get_item(**fqname.query)
        item = IndexItem.create(**fqname.query())
    else:
        if item.fqname:
            fqname = item.fqname
    if not item.id():   # except NoSuchItemError:
        item = Dummy.Item.create(fqname)
        rev = Dummy.Rev.create(item, itemtype, contenttype)
    else:
        try:
            rev = Revision.create(item, rev_id)
        except Exception as e:
            try: 
                rev = item.get_revision(CURRENT)  # fall back to current revision
            except:
                raise ValueError("Cannot find current revision of an item...should we fall back to dummy: ", e)
        
        
    return rev

class HLItem:
    """ Highlevel (not storage) Item, wraps around a storage Revision"""
    # placeholder values for registry entry properties
    itemtype = ''
    display_name = ''
    description = ''
    shown = True
    order = 0

    @classmethod
    def _factory(cls, *args, **kw):
        return cls(*args, **kw)
    def __init__(self, fqname, rev=None, content=None):
        self.fqname = fqname
        self.rev = rev
        self.content = content
        
    def get_meta(self):
        return self.rev.meta
    meta = property(fget=get_meta)

def create(fqname=None, itemtype=None, contenttype=None, rev_id=CURRENT, item:IndexItem.IndexItem=None):
    """
    Create a highlevel Item by looking up :name or directly wrapping
    :item and extract the Revision designated by :rev_id revision.

    The highlevel HLItem is created by creating an instance of Content
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
    
    rev = get_storage_revision(fqname, itemtype, contenttype, rev_id, item)
    contenttype = rev.meta.get(CONTENTTYPE) or contenttype
    #logging.debug("Item {0!r}, got contenttype {1!r} from revision meta".format(name, contenttype))
    # logging.debug("Item %r, rev meta dict: %r" % (name, dict(rev.meta)))

    # XXX Cannot pass item=item to Content.__init__ via
    # content_registry.get yet, have to patch it later.
    print ("----------------------for Content ==================")
    content = Content.create(contenttype)

    itemtype = rev.meta.get(ITEMTYPE) or itemtype or ITEMTYPE_DEFAULT
    #logging.debug("Item {0!r}, got itemtype {1!r} from revision meta".format(name, itemtype))
    print ("----------------------for ITEM ==================")
    item = item_registry.get(itemtype, fqname, rev=rev, content=content)
    assert item is not None
    #logging.debug("Item class {0!r} handles {1!r}".format(item.__class__, itemtype))

    content.item = item
    return item

    

@register
class NonExistent(HLItem):
    """
    A dummy Item for nonexistent items (when modifying, a nonexistent item with
    undetermined itemtype)
    """
    itemtype = ITEMTYPE_NONEXISTENT
    shown = False

    def _convert(self, doc):
        #abort(404)
        raise ValueError("Not implemented yet")
    
    def do_show(self, revid, **kwargs):
        # skip the idea of finding similar ma
        #start, end, matches = find_matches(self.fqname)
        #similar_names = sorted(matches.keys())
        print ("Show on webpage")
        print (self.fqname, " ", content_registry.group_names, " ", content_registry.groups)
        # return render_template('modify_select_contenttype.html',
        #                        fqname=self.fqname,
        #                        item_name=self.name,
        #                        itemtype='default',  # create a normal wiki item
        #                        group_names=content_registry.group_names,
        #                        groups=content_registry.groups,
        #                        similar_names=similar_names,
        #                        )
        raise ValueError("Not implemented yet")

    def do_modify(self):
        raise ValueError("Not implemented yet")

    def _select_itemtype(self):
        raise ValueError("Not implemented yet")
    def rename(self, name, comment=''):
        # pointless for non-existing items
        pass

    def delete(self, comment=''):
        # pointless for non-existing items
        pass

    def revert(self, comment=''):
        # pointless for non-existing items
        pass

    def destroy(self, comment='', destroy_item=False):
        # pointless for non-existing items
        pass

