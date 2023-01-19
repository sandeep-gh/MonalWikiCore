#fname for Home
from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from MonalWikiCore.constant_keys import CURRENT, ITEMTYPE_DEFAULT
from MonalWikiCore.Name import url_to_compositeName
from MonalWikiCore.engine import indexes, storage_routing
from MonalWikiCore.wiki import HLItem

storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"
storage_routing.storage_routing(NAMESPACES, storage_base_dir)
indexes.indexes(storage_base_dir)

# ====================================================================
# create NonExistent Item 
# item_name = "Home"

# rev = CURRENT
# #print (f"{fqname}")
# # fqcn: fully qualified composite name
# fqcn = url_to_compositeName(item_name)
# item = HLItem.create(fqcn, rev)
# ====================================================================


# ================= create Default Item =================
contenttype = "text/csv;charset=utf-8"
itemtype = ITEMTYPE_DEFAULT
item_name = "someitemnew"
fqcn = url_to_compositeName(item_name)
rev = CURRENT
item = HLItem.create(fqcn, itemtype=itemtype, rev_id=rev, contenttype=contenttype)
#html_render(item)

