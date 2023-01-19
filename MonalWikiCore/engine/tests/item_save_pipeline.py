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
fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'Home2')

#index_item = indexes.document_search(**fqcn.query_terms)
# currentrev = None
# contenttype_current = None

# if  index_item:
#     currentrev = index_item.get_revision(CURRENT)
#     contenttype_current = index_item.meta.get(CONTENTTYPE)

meta =  {'itemtype': 'default',
         'contenttype': 'text/x-markdown;charset=utf-8',
         'namespace': NAMESPACE_DEFAULT,
         'summary': 'summary 9',
         'name': ['Home2'],
         'tags': ['sfsd sfsfh tha3'],
         'comment': 'mycomment9',
         'rev_number': 1}
data = BytesIO(b"this si same string text;convereted to bytes and then to BytesIO")
# indexes.store_revision(meta, 
#                        data,
#                        overwrite=False,
#                        action=str(ACTION_SAVE),
#                        contenttype_current = None,
#                        contenttype_guessed = "text/plain;charset=utf-8",
#                        return_meta = True,
#                        return_rev = True
#                        )
            

#storage_routing.namespace_storage_map['default'].store({NAME: 'Home'}, BytesIO(b''))



#==============We start from here"
# store in store done 
revid = storage_routing.store(meta, data)
print ("revid =", revid)

#revid = "5d9cfed83f8f44559eecb356f3308d19"
content =  indexes.indexible_content(meta, data, is_new = True)
itemtype =  'default'
contenttype =  'text/x-markdown;charset=utf-8'
#item_name = "eknayaite"
#placeholder_item is to capture the initial request. Actual index item is create post storage and indexing
#fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'ekitem')
wikiitem = WikiItem.create(fqcn, itemtype=itemtype, contenttype=contenttype)
print ("wikiitem = ", wikiitem)
#meta[REVID] = revid 
#indexes.index_revision(meta, content)
indexes.save(wikiitem, meta, data,  storage_revid = revid)

# store a revision in the store


whoosh_doc = indexes.document_search(**fqcn.query_terms)
print ("whoosh_doc = ", whoosh_doc)
