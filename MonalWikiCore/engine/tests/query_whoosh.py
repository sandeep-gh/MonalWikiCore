from io import BytesIO
import os
from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from MonalWikiCore.engine.storage_routing import storage_routing
from MonalWikiCore.engine.indexes import indexes

from MonalWikiCore.constant_keys import NAME, NAMESPACE, NAME_EXACT, NAMESPACE_DEFAULT, CURRENT, CONTENTTYPE, REVID
from MonalWikiCore.Name import CompositeName
from MonalWikiCore.wiki import WikiItem

storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"
# storage backend 
storage_routing(NAMESPACES, storage_base_dir)
# init indexes 
indexes(storage_base_dir)
fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'ItemWiththisNameDoesNotExists')
index_item = indexes.create(**fqcn.query_terms)
print (type(index_item))

print (index_item.query)

print (index_item.current)
