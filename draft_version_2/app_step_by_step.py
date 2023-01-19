from constant_keys import CURRENT, NAME_EXACT, UFIELDS
# add url handlers
import HLItem
import Name
import indexes

from wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from storage_routing import storage_routing
from constant_keys import NAME, NAMESPACE, TRASH
from io import BytesIO
import os
import indexes
storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"

# after invocation storage_routing is both function and a class instance (kind-of-like global-static class instance. it has member store(meta, data) and stuff
storage_routing(NAMESPACES, storage_base_dir)
indexes.indexes(storage_base_dir)

def flash_if_item_deleted(item_name, rev_id, itemrev):
    """
    Show flash info message if target item is deleted, show another message if revision is deleted.
    Return True if item is deleted or this revision is deleted.
    """
    if not rev_id == CURRENT:
        ret = False
        current_item = Item.create(item_name, rev_id=CURRENT)
        if TRASH in current_item.meta and current_item.meta[TRASH]:
            #flash(_('This item is deleted.'), "info")
            raise ValueError("not yet  impmented")
            ret = True
        if TRASH in itemrev.meta and itemrev.meta[TRASH]:
            ##flash(_('This item revision is deleted.'), "info")
            raise ValueError("not yet  impmented")
            ret = True
        return ret
    elif TRASH in itemrev.meta and itemrev.meta[TRASH]:
        #flash(_('This item is deleted.'), "info")
        raise ValueError("Not yet implemented")
        return True
    return False



def show_home():
    item_name = "Home"
    
    rev_id  = CURRENT
    fqname = Name.split_fqname(item_name)
    # if fqname.field not in UFIELDS:  # Need a unique key to extract stored item.
    #     raise FieldNotUniqueError("field {0} is not in UFIELDS".format(fqname.field))
    if not fqname.value and fqname.field == NAME_EXACT:
        fqname = fqname.get_root_fqname()
        raise ValueError("Not yet implemented")
        #return redirect(url_for_item(fqname))

    hlitem = HLItem.create(fqname, rev_id = rev_id)
    # TODO: 
    #flaskg.user.add_trail(item_name)
    item_is_deleted = flash_if_item_deleted(item_name, rev_id, hlitem)
    result = hlitem.do_show(rev_id, item_is_deleted=item_is_deleted)
    return result 

    # except Exception as e:
    #     raise ValueError("not yet implemented: ", e)


show_home()    
