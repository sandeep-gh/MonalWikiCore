
# there is only one indexer
import datetime
from dataclasses import dataclass
from typing import Any, NamedTuple
from io import BytesIO

from whoosh.fields import Schema, TEXT, ID, IDLIST, NUMERIC, DATETIME, KEYWORD, BOOLEAN, NGRAMWORDS
from whoosh.query import And, Every, Prefix, Term
from whoosh.filedb.filestore import FileStorage
from whoosh.writing import AsyncWriter

from ..constant_keys import LATEST_REVS, ALL_REVS, NAMESPACE, NAME, CONTENTTYPE, MTIME, PTIME, NAME_EXACT, WIKINAME, CONTENT, BACKENDNAME, CONTENTNGRAM, SUMMARYNGRAM, TAGS, HAS_TAG, ACTION_SAVE, UFIELDS, NAMESPACE, NAME, UFIELDS_TYPELIST, ITEMID, SUMMARY, NAMENGRAM, NAMES, NAME_SORT, CURRENT, REVID, SIZE, COMMENT, REV_NUMBER, PARENTID, REVID

import os
from .IndexSchema import all_revisions_schema, latest_revisions_schema
from .. import Name
from . import Dummy
from .. import wikicfg
import time
from MonalWikiCore.needs_home import WikiItem, IndexQueryAnswer
from ..contenttypes import  NonExistent as Content_NonExistent, Markdown as Content_Markdown
#, Default as Content_Default

INDEXER_TIMEOUT = 20.0
INDEXES = [LATEST_REVS, ALL_REVS, ]
SCHEMAS = {ALL_REVS : all_revisions_schema,
           LATEST_REVS: latest_revisions_schema
    }


    
@dataclass
class Meta:
    revision: Any
    doc: Any
    meta: Any # a key,value dictionary

class Revision(NamedTuple):
    idxitem: Any
    revid: Any
    doc: Any
    meta : Any
    name : Any
    #data: Any <-- data field is missing 
    def create(idxitem, revid):
        is_current = revid  == CURRENT
        # we should call doc as whoosh-result doc 
        if is_current:
            doc = idxitem.answer
        else:
            doc = indexes.retry_document_search_until_succeed(idx_name=ALL_REVS, revid=revid)
            print ("whoosh doc = ", doc)
            assert False 
        if is_current:
            revid = doc.get(REVID)
            if revid is None:
                raise KeyError
        #backend_name = doc[BACKENDNAME]
        #Meta(Revision, doc, meta)
        meta = Meta(None, doc, None)
        names = Name.get_names(doc)
        revision = Revision(idxitem, revid, doc, meta, names)
        meta.revision = revision
        return revision 



def indexible_content(meta, data, is_new=False):
    """
    return a string that would be indexed by whoosh for the data. For test purposes
    returning a simple string

    """
    doc = "doc is simply a string derived from  of input data: which can be markdown; html; images"
    assert CONTENTTYPE in meta
    assert meta[CONTENTTYPE] is not None

    match meta[CONTENTTYPE]:
        case Content_NonExistent.type:
            assert False
            
        case Content_Markdown.type:
            doc  = Content_Markdown.to_plain_text(data)
        
    return doc

# def indexible_content(meta, data, is_new=False):
#     """
#     Convert revision data to a indexable content.
#     :param meta: revision metadata (gets updated as a side effect)
#     :param data: revision data (file-like)
#                  please make sure that the content file is
#                  ready to read all indexable content from it. if you have just
#                  written that content or already read from it, you need to call
#                  rev.seek(0) before calling convert_to_indexable(rev).
#     :param is_new: if this is for a new revision and we shall modify
#                    metadata as a side effect
#     :returns: indexable content, text/plain, unicode object
#     """

#     assert meta[NAMESPACE]
#     assert meta[NAME][0]
#     item_name = meta[NAMESPACE] + '/' + meta[NAME][0]
#     fqname = split_fqname(item_name)

#     class PseudoRev:
#         def __init__(self, meta, data):
#             self.meta = meta
#             self.data = data
#             self.revid = meta.get(REVID)

#             class PseudoItem:
#                 def __init__(self, fqname):
#                     self.fqname = fqname
#                     self.name = fqname.value
#             self.item = PseudoItem(fqname)

#         def read(self, *args, **kw):
#             return self.data.read(*args, **kw)

#         def seek(self, *args, **kw):
#             return self.data.seek(*args, **kw)

#         def tell(self, *args, **kw):
#             return self.data.tell(*args, **kw)

#     rev = PseudoRev(meta, data)
#     try:
#         # TODO use different converter mode?
#         # Maybe we want some special mode for the input converters so they emit
#         # different output than for normal rendering), esp. for the non-markup
#         # content types (images, etc.).
#         input_contenttype = meta[CONTENTTYPE]
#         output_contenttype = 'text/plain'
        #type_input_contenttype = Type(input_contenttype)
        #type_output_contenttype = Type(output_contenttype)
        #reg = default_registry
        # first try a direct conversion (this could be useful for extraction
        # of (meta)data from binary types, like from images or audio):
        #conv = reg.get(type_input_contenttype, type_output_contenttype)
        # if conv:
        #     doc = conv(rev, input_contenttype)
        #     return doc
        # otherwise try via DOM as intermediate format (this is useful if
        # input type is markup, to get rid of the markup):
        #SelfNote: input_conv converts markdown into moin.page (which most likely is a dom-tree
        #input_conv = reg.get(type_input_contenttype, type_moin_document)

        
        # selfNote: some sort of converter cross-ref to other item in the wiki
        #refs_conv = reg.get(type_moin_document, type_moin_document, items='refs')
        #output_conv = reg.get(type_moin_document, type_output_contenttype)
    #     if input_conv and output_conv:
    #         doc = input_conv(rev, input_contenttype)
    #         # We do not convert smileys, includes, macros, links, because
    #         # it does not improve search results or even makes results worse.
    #         # We do run the referenced converter, though, to extract links and
    #         # transclusions.
    #         if is_new:
    #             # we only can modify new, uncommitted revisions, not stored revs
    #             i = Iri(scheme='wiki', authority='', path='/' + item_name)
    #             doc.set(moin_page.page_href, str(i))
    #             refs_conv(doc)
    #             # side effect: we update some metadata:
    #             meta[ITEMLINKS] = refs_conv.get_links()
    #             meta[ITEMTRANSCLUSIONS] = refs_conv.get_transclusions()
    #             meta[EXTERNALLINKS] = refs_conv.get_external_links()
    #         doc = output_conv(doc)
    #         return doc
    #     # no way
    #     raise TypeError("No converter for {0} --> {1}".format(input_contenttype, output_contenttype))
    # except Exception as e:  # catch all exceptions, we don't want to break an indexing run
    #     logging.exception("Exception happened in conversion of item {0!r} rev {1} contenttype {2}:".format(
    #                       item_name, meta.get(REVID, 'new'), meta.get(CONTENTTYPE, '')))
    #     doc = 'ERROR [{0!s}]'.format(e)
    #     return doc
    doc = "doc is simply a string derived from  of input data: which can be markdown; html; images"
    return doc


def storageItem_to_whooshDoc(meta, content, schema, wikiname, backend_name):
    """
    Convert backend metadata/data to a whoosh document.

    :param meta: revision meta from moin backend
    :param content: revision data converted to indexable content
    :param schema: whoosh schema
    :param wikiname: interwikiname of this wiki
    :returns: document to put into whoosh index
    """
    doc = dict([(key, value)
                for key, value in meta.items()
                if key in schema])

    # Don't care for subscriptions for  now 
    # if SUBSCRIPTION_IDS in schema and SUBSCRIPTIONS in meta:
    #     doc[SUBSCRIPTION_IDS], doc[SUBSCRIPTION_PATTERNS] = backend_subscriptions_to_index(meta[SUBSCRIPTIONS])
    for key in [MTIME, PTIME]:
        if key in doc:
            # we have UNIX UTC timestamp (int), whoosh wants datetime
            doc[key] = datetime.datetime.utcfromtimestamp(doc[key])
    doc[NAME_EXACT] = doc[NAME]
    doc[WIKINAME] = wikiname
    doc[CONTENT] = content
    doc[BACKENDNAME] = backend_name
    if CONTENTNGRAM in schema:
        doc[CONTENTNGRAM] = content
    if SUMMARYNGRAM in schema and SUMMARY in meta:
        doc[SUMMARYNGRAM] = meta[SUMMARY]
    if NAMENGRAM in schema and NAME in meta:
        doc[NAMENGRAM] = ' '.join(meta[NAME])
    if doc.get(TAGS, None):
        # global tags uses this to search for items with tags
        doc[HAS_TAG] = True
    if doc.get(NAME, None):
        if doc.get(NAMESPACE, None):
            fullnames = [doc[NAMESPACE] + '/' + x for x in doc[NAME]]
            doc[NAMES] = ' | '.join(fullnames)
        else:
            doc[NAMES] = ' | '.join(doc[NAME])
        doc[NAME_SORT] = doc[NAMES].replace('/', '')
    else:
        doc[NAME_SORT] = ""
    return doc

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

    def index_revision(meta, content, async_=True):
        """
        Index a single revision, add it to all-revs and latest-revs index.

        :param meta: metadata dict
        :param content: preprocessed (filtered) indexable content
        :param async_: if True, use the AsyncWriter, otherwise use normal writer
        """
        #SelfNote: Monal doesn't use backend name; the namespace is the backend name
        backend_name = "default"
        doc = storageItem_to_whooshDoc(meta, content, SCHEMAS[ALL_REVS], wikicfg.WIKINAME, backend_name)
        if async_:
            writer = AsyncWriter(indexes_map[ALL_REVS])
        else:
            writer = indexes_map[ALL_REVS].writer()
        with writer as writer:
            writer.update_document(**doc)  # update, because store_revision() may give us an existing revid
        doc = storageItem_to_whooshDoc(meta, content, SCHEMAS[LATEST_REVS], wikicfg.WIKINAME, backend_name)
        if async_:
            writer = AsyncWriter(indexes_map[LATEST_REVS])
        else:
            writer = indexes_map[LATEST_REVS].writer()
        with writer as writer:
            writer.update_document(**doc)

    def retry_document_search_until_succeed(**kw):
        """
        """
        until = time.time() + INDEXER_TIMEOUT
        while True:
            indexer = document_search(**kw)
            if indexer is not None:
                break
            time.sleep(2)
            if time.time() > until:
                raise KeyError(kw.get('revid', '') + ' - server overload or corrupt index')
        return indexer

    def store_revision(indexItem:IndexQueryAnswer, meta,   data,
                       overwrite=False,
                       action=str(ACTION_SAVE),
                       contenttype_current = None,
                       contenttype_guessed = "text/plain;charset=utf-8",
                       return_meta = True,
                       return_rev = True,
                       storage_revid = None
                       ):

        ct = meta.get(CONTENTTYPE)
        # Don't care much about validation
        #SelfNote: why is id() needed; ignore for now 
        #assert indexItem.id() is not None
        content = indexible_content(meta, data)
        # put stuff in store
        meta[REVID] = storage_revid
        index_revision(meta, content)
        # create a new indexItem
        current = retry_document_search_until_succeed(revid=meta[REVID])
        newIdxItem = IndexQueryAnswer(indexItem.name, current)
        new_revision = Revision.create(newIdxItem, storage_revid)
        return new_revision

            
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

    def create(**query):
        """
        Return IndexQueryAnswer with <name> (may be a new or existing item).
        if query has no matching then the results looks as follows:
        name: 
        current : 
        

        """
        
        # if name.startswith('@itemid/'):
        #     itemid =  name[8:]
        #     #Item(**{ITEMID: name[8:]})
        #     raise ValueError("haven't introduced itemid yes")
        # fqname = split_fqname(name)

        # namespace = fqname.namespace
        # name_exact = fqname.value
        #TODO: Assume document with this name is not in database before
        latest_doc = document_search(**query)
        # print ("result of document_search on query ", query, " is ", latest_doc)
        # if not latest_doc:
        #     latest_doc = {}
        #     for field, value in query.items():
        #         latest_doc[field] = [value] if field in UFIELDS_TYPELIST else value
        #     latest_doc[NAME] = latest_doc[NAME_EXACT] if NAME_EXACT in query else []
        # name = query.get(NAME_EXACT)
        return IndexQueryAnswer(query, latest_doc)

    def save(wikiItem: WikiItem, meta, data=None, names=None, action = ACTION_SAVE, contenttype_guessed=None, comment=None,
              overwrite=False, delete=False, storage_revid=None):
        """
        save an wikiItem; with new meta and data 
        should be called by:
        - rename
        - revert
        - modify 
        - admin
        
        storage_revid: is the uuid we recieve after putting meta and data in object store. Moin where 
        indexing is responsible for storage of meta and data. here indexs assume meta and data is already stored. 
        """

        indexItem = create(**wikiItem.fqcn.query())
        
        currentrev = None
        contenttype_current = None
        #SelfNOte: don't call Revision if indexItem.current doest have a revid
        if indexItem.current.get(REVID, None):
            currentrev = Revision.create(indexItem, CURRENT)
            contenttype_current = currentrev.meta.get(CONTENTTYPE, None)
        #SelfNote: skipping the acl stuff

        assert wikiItem.fqcn.fullname() is not None 
        assert meta.get(NAMESPACE) is  not None 
        if comment is not None:
            meta[COMMENT] = str(comment)

        if currentrev:
            #selfNote: skipping all details about deleted_names
            meta[REV_NUMBER] = currentrev.meta.get(REV_NUMBER, 0) + 1
        else:
            meta[REV_NUMBER]  = 1

        #selfNote: skipping details about PARENTID
        if not overwrite and REVID in meta:
            # we usually want to create a new revision, thus we update parentid and remove the existing REVID
            meta[PARENTID] = currentrev.meta[REVID] if currentrev else meta[REVID]
            del meta[REVID]

        if data is None:
            if currentrev is not None:
                # we don't have (new) data, just copy the old one.
                # a valid usecase of this is to just edit metadata.
                data = currentrev.data
            else:
                data = b''


        if isinstance(data, str):
            # skip the variable business
            #data = self.handle_variables(data, meta)
            charset = meta['contenttype'].split('charset=')[1]
            data = data.encode(charset)

        if isinstance(data, bytes):
            data = BytesIO(data)
                    
        new_revision = store_revision(indexItem, meta, data, overwrite=overwrite, action=str(action), contenttype_current=contenttype_current, contenttype_guessed= contenttype_guessed, storage_revid=storage_revid)
        #SelfNote: closefile is needed if data is not BytesIO. Currently we only have bytesIO
        # if currentrev is not None:
        #     close_file(currentrev.data)
        #close_file(data)

        #close_file(new_meta.revision.data)
        #SelfNote: will think about meta[SIZE] post review 
        return storage_revid, None
        #return storage_revid, new_revision.meta[SIZE]
    
    open()


    indexes.document_search = document_search
    indexes.index_revision = index_revision
    indexes.store_revision = store_revision
    indexes.retry_document_search_until_succeed = retry_document_search_until_succeed
    indexes.indexible_content = indexible_content
    indexes.create = create
    indexes.save = save


def get_storage_revision(fqcn:Name.CompositeName, itemtype=None, contenttype=None, rev_id=CURRENT):
    """
    Get a storage Revision.

    Returns a revision instance. 
    if no item of name fqcn is present then" 
    rev = {name: , item: , revid: }
    """
    #rev_id should not be guessed or overwritten;
    #rev_id = fqcn.value if fqcn.field == REVID else rev_id
    #assert item is None 
    #if item is None:
        #TODO: use protected storage. not up yet
        #Instead use indexes and  return IndexItem 
        #item = flaskg.storage.get_item(**fqname.query)
    item = indexes.create(**fqcn.query())
    # else:
    #     if item.fqname:
    #         fqcn = item.fqcn
    print ("in GSR : item.current:stored-whoosh-doc", item)
    # we need to check if index-search resulted in a hit
    # in moin this is done using ITEMID field. but currently
    # we don't know how ITEMID is getting/initialized used
    # Therefore searching for REVID in the query result (i.e.,
    # item.current)
    
    if not  item.answer:
        # if no such item with given fqcn exists 
        #item = Dummy.Item.create(fqcn)
        # We will use whatever is retured by indexes.create (i.e, create an item)
        rev = Dummy.Rev.create(fqcn, item, itemtype, contenttype)

    else:
        rev = Revision.create(item, rev_id)
        # try:
        #     rev = Revision.create(item, rev_id)
        # except Exception as e:
        #     try:
        #         # Don't act smart -- do whats told 
        #         assert False 
        #         rev = item.get_revision(CURRENT)  # fall back to current revision
        #     except:
        #         raise ValueError("Cannot find current revision of an item...should we fall back to dummy: ", e)
        
        
    return rev
