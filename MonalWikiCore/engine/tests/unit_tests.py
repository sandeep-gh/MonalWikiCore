#fname for Home
name = "Home"
fqname = split_fqname(name)



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
indexes(storage_base_dir)
fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'ekitem')

# search index for fqcn 
# in moin -- ProtectingMiddleware.get_item is called ; which calls Indexing.get_item
# which creates an Item object, which calls indexer._document which picks up the
# Whoosh index-seracher which call returns searcher.document

# here we directly call indexes.document_search 
index_item = indexes.document_search(**fqcn.query_terms)
currentrev = None
contenttype_current = None

if not index_item:
    currentrev = index_item.get_revision(CURRENT)
    contenttype_current = index_item.meta.get(CONTENTTYPE)

meta =  {'itemtype': 'default', 'contenttype': 'text/x-markdown;charset=utf-8', 'namespace': '', 'summary': 'summary 9', 'name': ['newitem9'], 'tags': ['sfsd sfsfh tha3'], 'comment': 'mycomment9', 'rev_number': 1}

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
            

#storage_routing.namespace_storage_map['default'].store({NAME: 'test'}, BytesIO(b''))
revid = storage_routing.store(meta, data)
index_content =  indexes.indexible_content(meta, data, is_new = True)
#indexes.index_revision(meta, 

# store a revision in the store


