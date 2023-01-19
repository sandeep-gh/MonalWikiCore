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

meta =  {'itemtype': 'default',
         'contenttype': 'text/x-markdown;charset=utf-8',
         'namespace': NAMESPACE_DEFAULT,
         'summary': 'summary 9',
         'name': ['Home2'],
         'tags': ['sfsd sfsfh tha3'],
         'comment': 'mycomment9',
         'rev_number': 1}

data = b"this si same string text;convereted to bytes and then to BytesIO"

content = indexes.indexible_content(meta, data)
print ("indexible content = ", content)
