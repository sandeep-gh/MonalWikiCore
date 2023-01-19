from io import BytesIO
import os

from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from MonalWikiCore.engine.storage_routing import storage_routing
from MonalWikiCore.engine.indexes import indexes

from MonalWikiCore.constant_keys import NAME, NAMESPACE, NAME_EXACT, NAMESPACE_DEFAULT, CURRENT, CONTENTTYPE
from MonalWikiCore.Name import CompositeName

storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"
# storage backend 
storage_routing(NAMESPACES, storage_base_dir)
# init indexes 
meta =  {'itemtype': 'default',
         'contenttype': 'text/x-markdown;charset=utf-8',
         'namespace': '',
         'summary': 'summary 9',
         'name': ['newitem9'],
         'tags': ['sfsd sfsfh tha3'],
         'comment': 'mycomment9',
         'rev_number': 1
         }
data = b"this si same string text;convereted to bytes and then to BytesIO"
metaid = storage_routing.store(meta, data)
print("metaid = ", metaid)
storage_routing.commit()
meta, data = storage_routing.namespace_storage_map[''].retrieve(metaid)

print ("data type =", type(data))
print ("data =", data)
