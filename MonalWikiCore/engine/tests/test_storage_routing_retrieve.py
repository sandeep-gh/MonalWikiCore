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
metaid =  "4c9d12b4afdf47a09e87728cc1163d45"
meta, data = storage_routing.namespace_storage_map[''].retrieve(metaid)

print ("data type =", type(data))
print ("data =", data)




