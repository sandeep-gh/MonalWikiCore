
# there is only one indexer

from whoosh.fields import Schema, TEXT, ID, IDLIST, NUMERIC, DATETIME, KEYWORD, BOOLEAN, NGRAMWORDS
from whoosh.query import And, Every, Prefix, Term
from whoosh.filedb.filestore import FileStorage
from constant_keys import LATEST_REVS, ALL_REVS
import os
INDEXES = [LATEST_REVS, ALL_REVS, ]

def indexes(storage_base_dir):
    """
    - assumes that  index_dir and index is already created.
    - the indexes function behaves like a global/static instance. Do not make multiple calls to it. 
    """
    index_dir = f"{storage_base_dir}/whoosh"
    # try:
    #     os.mkdir(index_dir)
    # except:
    #     #don't worry if dir is already been created 
    #     pass
    index_store = FileStorage(index_dir)
    indexes_map = {}
    def open():

        for name in INDEXES:
            indexes_map[name] = index_store.open_index(name)

    def document_search(idx_name=LATEST_REVS, **kw):
        with indexes_map[idx_name].searcher() as searcher:
            return searcher.document(**kw)
        
    # def document(idx_name=LATEST_REVS, **kw):
        # Convenience method returns the stored fields of a document matching the given keyword arguments
        # with self.ix[idx_name].searcher() as searcher:
        #     return searcher.document(**kw)
        # return  document_searcher(idx_name, **kw)
        # if doc:
        #     latest_doc = doc if idx_name == LATEST_REVS else None
        #     return latest_doc
        # return None
            # #item = IndexItem(self, latest_doc=latest_doc, itemid=doc[ITEMID])
            # # why pass document_searcher
            # # to avoid circular dependency
            # # Item needs indexes which needs IndexItem which needs  revision which needs indexes
            # return ( doc[REVID], document_searcher, doc=doc)

    
    open()
    indexes.document_search = document_search
    
    
