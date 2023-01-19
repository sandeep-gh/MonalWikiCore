
from io import BytesIO
import os

from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from MonalWikiCore.engine.storage_routing import storage_routing
from MonalWikiCore.engine.indexes import indexes

from MonalWikiCore.constant_keys import NAME, NAMESPACE, NAME_EXACT, NAMESPACE_DEFAULT, CURRENT, CONTENTTYPE, REVID
from MonalWikiCore.Name import CompositeName
from MonalWikiCore.wiki import WikiItem, wikiItemTypes

storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"
# storage backend 
storage_routing(NAMESPACES, storage_base_dir)
# init indexes 
indexes(storage_base_dir)

# fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'unkown')

# # An item not yet in the store; unspecified itemtype/contentype 
# wikiitem = WikiItem.create(fqcn)

# # unknown item with specific contenttype/itemtype
# fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'unkown')
# itemtype =  'default'
# contenttype =  'text/x-markdown;charset=utf-8'
# wikiitem = WikiItem.create(fqcn, itemtype=itemtype, contenttype=contenttype)
# print(wikiitem)
# An item in the store

# =========================== store an item ==========================
meta =  {'itemtype': 'default',
         'contenttype': 'text/x-markdown;charset=utf-8',
         'namespace': NAMESPACE_DEFAULT,
         'summary': 'summary 9',
         'name': ['for_test_wikiItem'],
         'tags': ['sfsd sfsfh tha3'],
         'comment': 'mycomment9',
         'rev_number': 1}

data = b"this si same string text;convereted to bytes and then to BytesIO"

revid = storage_routing.store(meta, data)
meta[REVID] = revid 
content = indexes.indexible_content(meta, data)
indexes.index_revision(meta, content)


# ================================ end ===============================
item_name = "for_test_wikiItem"
fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, item_name)
# whoosh_doc = indexes.document_search(**fqcn.query_terms)
# print ("whoosh_doc = ", whoosh_doc)

wikiitem = WikiItem.create(fqcn)

print(type(wikiitem))
print ("==========================")
print("wikiitem = ", wikiitem)
# if not isinstance(wikiitem, wikiItemTypes.NonExistent):
#     print("wikiitem = ", wikiitem.rev)


# # An item in the store; with conflicting contenttype/storetype 
# item_name = "eknayaite"
# wikiitem = WikiItem.create(fqcn, itemtype=itemtype, contenttype=contenttype)
# print(wikiitem)

