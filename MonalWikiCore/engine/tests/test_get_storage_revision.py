from io import BytesIO
import os
from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from MonalWikiCore.engine.storage_routing import storage_routing
from MonalWikiCore.engine.indexes import indexes, get_storage_revision # 

from MonalWikiCore.constant_keys import NAME, NAMESPACE, NAME_EXACT, NAMESPACE_DEFAULT, CURRENT, CONTENTTYPE, REVID
from MonalWikiCore.constant_keys import MTIME, PTIME, ITEMID, LATEST_REVS, NAME_EXACT, UFIELDS, REVID, CONTENTTYPE, CURRENT, ITEMTYPE, ITEMTYPE_DEFAULT, ITEMTYPE_NONEXISTENT


from MonalWikiCore.Name import CompositeName
from MonalWikiCore.wiki import WikiItem
from MonalWikiCore.contenttypes import CONTENTTYPE_NONEXISTENT, CONTENTTYPE_DEFAULT, CONTENTTYPE_MARKDOWN

storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"
# storage backend 
storage_routing(NAMESPACES, storage_base_dir)
# init indexes 
indexes(storage_base_dir)
# ============================ scenario 1 ============================
fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'ItemWiththisNameDoesNotExists')

rev = get_storage_revision(fqcn)
# print ("scenario 1")
# print (type(rev))
# print ("idxitem = ", rev.idxitem)
# print ("revid = ", rev.revid)
# print ("meta =", rev.meta)
# print ("name =", rev.fqcn)
# print ("==============end=============")
# ================================ end ===============================


# ======================== add item to storage =======================

meta =  {'itemtype': 'default',
         'contenttype': 'text/x-markdown;charset=utf-8',
         'namespace': NAMESPACE_DEFAULT,
         'summary': 'summary 9',
         'name': ['for_GSR_test1'],
         'tags': ['sfsd sfsfh tha3'],
         'comment': 'mycomment9',
         'rev_number': 1}

data = b"this si same string text;convereted to bytes and then to BytesIO"

revid = storage_routing.store(meta, data)
meta[REVID] = revid 
content = indexes.indexible_content(meta, data)
indexes.index_revision(meta, content)



# ================================ end ===============================

fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'for_GSR_test1')

rev = get_storage_revision(fqcn)
print ("scenario 2")
print (type(rev))

print ("idxitem = ", rev.idxitem)

print ("revid = ", rev.revid)

print ("meta =", rev.meta)

#print ("name =", rev.fqcn)

# print ("==============end=============")
