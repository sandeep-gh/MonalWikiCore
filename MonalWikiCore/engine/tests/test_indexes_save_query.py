"""
tests creation of indexQueryAnswer which is the structure retured by
indexes.create. 
"""
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
# fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'ItemWiththisNameDoesNotExists')
# index_queryAnswer = indexes.create(**fqcn.query_terms)
# print (type(index_queryAnswer))
# print (index_queryAnswer.query)
# print (index_queryAnswer.answer)

# add a item to indexes

meta =  {'itemtype': 'default',
         'contenttype': 'text/x-markdown;charset=utf-8',
         'namespace': NAMESPACE_DEFAULT,
         'summary': 'summary 9',
         'name': ['Home2'],
         'tags': ['sfsd sfsfh tha3'],
         'comment': 'mycomment9',
         'rev_number': 1}

data = b"this si same string text;convereted to bytes and then to BytesIO"
revid = storage_routing.store(meta, data)
meta[REVID] = revid
content = indexes.indexible_content(meta, data)
indexes.index_revision(meta, content)
fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'Home2')
index_queryAnswer = indexes.create(**fqcn.query_terms)
print(index_queryAnswer)
