from keys import WIKINAME, NAMESPACE, NAME, NAMES, NAME_SORT, NAME_OLD, REVID, REV_NUMBER, BACKENDNAME, MTIME, ITEMTYPE, CONTENTTYPE, TAGS, HAS_TAG, LANGUAGE, USERID, ADDRESS, HOSTNAME, SIZE, ACTION, COMMENT,SUMMARY, DATAID, TRASH, CONTENT
from keys import ITEMID, ITEMLINKS, ITEMTRANSCLUSIONS , ACL, CONTENTNGRAM, SUMMARYNGRAM, NAMENGRAM, EMAIL, MAILTO_AUTHOR, DISABLED, LOCALE, SUBSCRIPTION_IDS, SUBSCRIPTION_PATTERNS, PTIME
INDEXES = [LATEST_REVS, ALL_REVS, ]


class IndexingMiddleware:
    def __init__(self, index_engine,  backend, wiki_name=None, acl_rights_contents=[], **kw):
        """
        index_engine: is already up and running 
        """

        #create or open index
        self.indexes = await index_engine.open_indexes(INDEXES)
        self.backend = backend
        self.wikiname = wiki_name
   
        self.schemas = {}  # existing schemas

        # field_boosts favor hits on names, tags, summary, comment, content, namengram, summaryngram, and contentngram respectively
        # when query_parser default search includes [NAMES, NAMENGRAM, TAGS, SUMMARY, SUMMARYNGRAM, CONTENT, CONTENTNGRAM, COMMENT].
        # Note *NGRAMS are only present in latest_revs index, see below
        common_fields = {
            # wikiname so we can have a shared index in a wiki farm, always check this!
            WIKINAME: ID(stored=True),
            # namespace, so we can have different namespaces within a wiki, always check this!
            NAMESPACE: ID(stored=True),
            # since name is a list whoosh will think it is a list of tokens see #364
            # we store list of names, but do not use for searching
            NAME: TEXT(stored=True),
            # string created by joining list of Name strings, we use NAMES for searching
            NAMES: TEXT(stored=True, multitoken_query="or", analyzer=item_name_analyzer(), field_boost=30.0),
            # names without slashes, slashes cause strange sort sequences
            NAME_SORT: TEXT(stored=True),
            # unmodified NAME from metadata - use this for precise lookup by the code.
            # also needed for wildcard search, so the original string as well as the query
            # (with the wildcard) is not cut into pieces.
            NAME_EXACT: ID(field_boost=1.0),
            # history and mychanges views show old name for deleted items
            NAME_OLD: TEXT(stored=True),
            # revision id (aka meta id)
            REVID: ID(unique=True, stored=True),
            # sequential revision number for humans: 1, 2, 3...
            REV_NUMBER: NUMERIC(stored=True),
            # parent revision id
            PARENTID: ID(stored=True),
            # backend name (which backend is this rev stored in?)
            BACKENDNAME: ID(stored=True),
            # MTIME from revision metadata (converted to UTC datetime)
            MTIME: DATETIME(stored=True),
            # ITEMTYPE from metadata, always matched exactly hence ID
            ITEMTYPE: ID(stored=True),
            # tokenized CONTENTTYPE from metadata
            CONTENTTYPE: TEXT(stored=True, multitoken_query="and", analyzer=MimeTokenizer()),
            # unmodified list of TAGS from metadata
            TAGS: KEYWORD(stored=True, commas=True, scorable=True, field_boost=30.0),
            # search on HAS_TAG improves response time of global tags
            # https://whoosh.readthedocs.io/en/latest/api/query.html?highlight=#whoosh.query.Every
            HAS_TAG: BOOLEAN(stored=False),
            LANGUAGE: ID(stored=True),
            # USERID from metadata
            USERID: ID(stored=True),
            # ADDRESS from metadata
            ADDRESS: ID(stored=True),
            # HOSTNAME from metadata
            HOSTNAME: ID(stored=True),
            # SIZE from metadata
            SIZE: NUMERIC(stored=True),
            # ACTION from metadata
            ACTION: ID(stored=True),
            # tokenized COMMENT from metadata
            COMMENT: TEXT(stored=True, field_boost=30.0),
            # SUMMARY from metadata
            SUMMARY: TEXT(stored=True, field_boost=10.0),
            # DATAID from metadata
            DATAID: ID(stored=True),
            # TRASH from metadata
            TRASH: BOOLEAN(stored=True),
            # data (content), converted to text/plain and tokenized
            CONTENT: TEXT(stored=True, spelling=True),
        }

        latest_revs_fields = {
            # ITEMID from metadata - as there is only latest rev of same item here, it is unique
            ITEMID: ID(unique=True, stored=True),
            # unmodified list of ITEMLINKS from metadata
            ITEMLINKS: ID(stored=True),
            # unmodified list of ITEMTRANSCLUSIONS from metadata
            ITEMTRANSCLUSIONS: ID(stored=True),
            # tokenized ACL from metadata
            ACL: TEXT(analyzer=AclTokenizer(acl_rights_contents), multitoken_query="and", stored=True),
            # index ngrams of words, field_boosts favor hits on name and summary over content
            CONTENTNGRAM: NGRAMWORDS(minsize=3, maxsize=6, queryor=True, field_boost=0.01),
            SUMMARYNGRAM: NGRAMWORDS(minsize=3, maxsize=6, queryor=True, field_boost=1.0),
            NAMENGRAM: NGRAMWORDS(minsize=3, maxsize=6, queryor=True, field_boost=1.0),
        }
        latest_revs_fields.update(**common_fields)

        userprofile_fields = {
            # Note: email (if given) should be unique, but we might
            # have lots of empty values if it is not given and thus it is NOT
            # unique overall! Wrongly declaring it unique would lead to whoosh
            # killing other users from index when update_document() is called!
            EMAIL: ID(stored=True),
            MAILTO_AUTHOR: BOOLEAN(stored=True),
            DISABLED: BOOLEAN(stored=True),
            LOCALE: ID(stored=True),
            SUBSCRIPTION_IDS: ID(),
            SUBSCRIPTION_PATTERNS: ID(),
        }
        latest_revs_fields.update(**userprofile_fields)

        blog_entry_fields = {
            # blog publish time from metadata (converted to UTC datetime)
            PTIME: DATETIME(stored=True),
        }
        latest_revs_fields.update(**blog_entry_fields)

        all_revs_fields = {
            ITEMID: ID(stored=True),
        }
        all_revs_fields.update(**common_fields)

        # Meilisearch doesn't care for schema or dynamic fields


    def index_revision(self, meta, content, backend_name, async_=True):
        """
        Index a single revision, add it to all-revs and latest-revs index.

        :param meta: metadata dict
        :param content: preprocessed (filtered) indexable content
        :param async_: if True, use the AsyncWriter, otherwise use normal writer
        """
        doc = backend_to_index(meta, content, self.schemas[ALL_REVS], self.wikiname, backend_name)
        if async_:
            writer = AsyncWriter(self.ix[ALL_REVS])
        else:
            writer = self.ix[ALL_REVS].writer()
        with writer as writer:
            writer.update_document(**doc)  # update, because store_revision() may give us an existing revid
        doc = backend_to_index(meta, content, self.schemas[LATEST_REVS], self.wikiname, backend_name)
        if async_:
            writer = AsyncWriter(self.ix[LATEST_REVS])
        else:
            writer = self.ix[LATEST_REVS].writer()
        with writer as writer:
            writer.update_document(**doc)

    def remove_revision(self, revid, async_=True):
        """
        Remove a single revision from indexes.
        """
        if async_:
            writer = AsyncWriter(self.ix[ALL_REVS])
        else:
            writer = self.ix[ALL_REVS].writer()
        with writer as writer:
            writer.delete_by_term(REVID, revid)
        if async_:
            writer = AsyncWriter(self.ix[LATEST_REVS])
        else:
            writer = self.ix[LATEST_REVS].writer()
        with writer as writer:
            # find out itemid related to the revid we want to remove:
            with self.ix[LATEST_REVS].searcher() as searcher:
                docnum_remove = searcher.document_number(revid=revid)
                if docnum_remove is not None:
                    itemid = searcher.stored_fields(docnum_remove)[ITEMID]
            if docnum_remove is not None:
                # we are removing a revid that is in latest revs index
                latest_backends_revids = self._find_latest_backends_revids(self.ix[ALL_REVS], Term(ITEMID, itemid))
                if latest_backends_revids:
                    # we have a latest revision, just update the document in the index:
                    assert len(latest_backends_revids) == 1  # this item must have only one latest revision
                    latest_backend_revid = latest_backends_revids[0]
                    # we must fetch from backend because schema for LATEST_REVS is different than for ALL_REVS
                    # (and we can't be sure we have all fields stored, too)
                    meta, _ = self.backend.retrieve(*latest_backend_revid)
                    # we only use meta (not data), because we do not want to transform data->content again (this
                    # is potentially expensive) as we already have the transformed content stored in ALL_REVS index:
                    with self.ix[ALL_REVS].searcher() as searcher:
                        doc = searcher.document(revid=latest_backend_revid[1])
                        content = doc[CONTENT]
                    doc = backend_to_index(meta, content, self.schemas[LATEST_REVS], self.wikiname,
                                           backend_name=latest_backend_revid[0])
                    writer.update_document(**doc)
                else:
                    # this is no revision left in this item that could be the new "latest rev", just kill the rev
                    writer.delete_document(docnum_remove)

    def _modify_index(self, index, schema, wikiname, revids, mode='add', procs=1, limitmb=256):
        """
        modify index contents - add, update, delete the indexed documents for all given revids

        Note: mode == 'add' is faster but you need to make sure to not create duplicate
              documents in the index.
        """
        with index.writer(procs=procs, limitmb=limitmb) as writer:
            for backend_name, revid in revids:
                if mode in ['add', 'update', ]:
                    meta, data = self.backend.retrieve(backend_name, revid)
                    content = convert_to_indexable(meta, data, is_new=False)
                    doc = backend_to_index(meta, content, schema, wikiname, backend_name)
                if mode == 'update':
                    writer.update_document(**doc)
                elif mode == 'add':
                    writer.add_document(**doc)
                elif mode == 'delete':
                    writer.delete_by_term(REVID, revid)
                else:
                    raise ValueError("mode must be 'update', 'add' or 'delete', not '{0}'".format(mode))

    def _find_latest_backends_revids(self, index, query=None):
        """
        find the latest revision identifiers using the all-revs index

        :param index: an up-to-date and open ALL_REVS index
        :param query: query to search only specific revisions (optional, default: all items/revisions)
        :returns: a list of tuples (backend name, latest revid)
        """
        if query is None:
            query = Every()
        with index.searcher() as searcher:
            result = searcher.search(query, groupedby=ITEMID, sortedby=FieldFacet(MTIME, reverse=True))
            by_item = result.groups(ITEMID)
            # values in v list are in same relative order as in results, so latest MTIME is first:
            latest_backends_revids = [(searcher.stored_fields(v[0])[BACKENDNAME],
                                      searcher.stored_fields(v[0])[REVID])
                                      for v in by_item.values()]
        return latest_backends_revids

    def rebuild(self, tmp=False, procs=1, limitmb=256):
        """
        Add all items/revisions from the backends of this wiki to the index
        (which is expected to have no items/revisions from this wiki yet).

        Note: index might be shared by multiple wikis, so it is:
              create, rebuild wiki1, rebuild wiki2, ...
              create (tmp), rebuild wiki1, rebuild wiki2, ..., move
        """
        storage = self.get_storage(tmp)
        index = storage.open_index(ALL_REVS)
        try:
            # build an index of all we have (so we know what we have)
            all_revids = self.backend  # the backend is an iterator over all revids
            self._modify_index(index, self.schemas[ALL_REVS], self.wikiname, all_revids, 'add', procs, limitmb)
            latest_backends_revids = self._find_latest_backends_revids(index)
        finally:
            index.close()

        # now build the index of the latest revisions:
        index = storage.open_index(LATEST_REVS)
        try:
            self._modify_index(index, self.schemas[LATEST_REVS], self.wikiname, latest_backends_revids, 'add',
                               procs, limitmb)
        finally:
            index.close()

    def update(self, tmp=False):
        """
        Make sure index reflects current backend state, add missing stuff, remove outdated stuff.

        This is intended to be used:
        * after a full rebuild that was done at tmp location
        * after wiki is made read-only or taken offline
        * after the index was moved to the normal index location

        Reason: new revisions that were created after the rebuild started might be missing in new index.

        :returns: index changed (bool)
        """
        storage = self.get_storage(tmp)
        index_all = storage.open_index(ALL_REVS)
        try:
            # NOTE: self.backend iterator gives (backend_name, revid) tuples, which is NOT
            # the same as (name, revid), thus we do the set operations just on the revids.
            # first update ALL_REVS index:
            revids_backends = dict((revid, backend_name) for backend_name, revid in self.backend)
            backend_revids = set(revids_backends)
            with index_all.searcher() as searcher:
                ix_revids_backends = dict((doc[REVID], doc[BACKENDNAME]) for doc in searcher.all_stored_fields())
            revids_backends.update(ix_revids_backends)  # this is needed for stuff that was deleted from storage
            ix_revids = set(ix_revids_backends)
            add_revids = backend_revids - ix_revids
            del_revids = ix_revids - backend_revids
            changed = add_revids or del_revids
            add_revids = [(revids_backends[revid], revid) for revid in add_revids]
            del_revids = [(revids_backends[revid], revid) for revid in del_revids]
            self._modify_index(index_all, self.schemas[ALL_REVS], self.wikiname, add_revids, 'add')
            self._modify_index(index_all, self.schemas[ALL_REVS], self.wikiname, del_revids, 'delete')

            backend_latest_backends_revids = set(self._find_latest_backends_revids(index_all))
        finally:
            index_all.close()
        index_latest = storage.open_index(LATEST_REVS)
        try:
            # now update LATEST_REVS index:
            with index_latest.searcher() as searcher:
                ix_revids = set(doc[REVID] for doc in searcher.all_stored_fields())
            backend_latest_revids = set(revid for name, revid in backend_latest_backends_revids)
            upd_revids = backend_latest_revids - ix_revids
            upd_revids = [(revids_backends[revid], revid) for revid in upd_revids]
            self._modify_index(index_latest, self.schemas[LATEST_REVS], self.wikiname, upd_revids, 'update')
            self._modify_index(index_latest, self.schemas[LATEST_REVS], self.wikiname, del_revids, 'delete')
        finally:
            index_latest.close()
        return changed

    def optimize_backend(self):
        """
        Optimize backend / collect garbage to safe space:

        * deleted items: destroy them? use a deleted_max_age?
        * user profiles: only keep latest revision?
        * normal wiki items: keep by max_revisions_count / max_age
        * deduplicate data (determine dataids with same hash, fix references to point to one of them)
        * remove unreferenced dataids (destroyed revisions, deduplicated stuff)
        """
        # TODO

    def optimize_index(self, tmp=False):
        """
        Optimize whoosh index.
        """
        storage = self.get_storage(tmp)
        for name in INDEXES:
            ix = storage.open_index(name)
            try:
                ix.optimize()
            finally:
                ix.close()

    def dump(self, tmp=False, idx_name=LATEST_REVS):
        """
        Yield key/value tuple lists for all documents in the indexes, fields sorted.
        """
        storage = self.get_storage(tmp)
        ix = storage.open_index(idx_name)
        try:
            with ix.searcher() as searcher:
                for doc in searcher.all_stored_fields():
                    name = doc.pop(NAME, "")
                    content = doc.pop(CONTENT, "")
                    yield [(NAME, name), ] + sorted(doc.items()) + [(CONTENT, content), ]
        finally:
            ix.close()

    def query_parser(self, default_fields, idx_name=LATEST_REVS):
        """
        Build a query parser for a list of default fields.
        """
        schema = self.schemas[idx_name]
        if len(default_fields) > 1:
            qp = MultifieldParser(default_fields, schema=schema)
        elif len(default_fields) == 1:
            qp = QueryParser(default_fields[0], schema=schema)
        else:
            raise ValueError("default_fields list must at least contain one field name")
        qp.add_plugin(RegexPlugin())

        def userid_pseudo_field_factory(fieldname):
            """generate a translator function, that searches for the userid
               in the given fieldname when provided with the username
            """
            def userid_pseudo_field(node):
                username = node.text
                users = user.search_users(**{NAME_EXACT: username})
                if users:
                    userid = users[0].meta[ITEMID]
                    node = WordNode(userid)
                    node.set_fieldname(fieldname)
                    return node
                return node
            return userid_pseudo_field
        qp.add_plugin(PseudoFieldPlugin(dict(
            # username:JoeDoe searches for revisions modified by JoeDoe
            username=userid_pseudo_field_factory(USERID),
            # assigned:JoeDoe searches for tickets assigned to JoeDoe
            assigned=userid_pseudo_field_factory(ASSIGNED_TO),
        )))
        return qp

    def search(self, q, idx_name=LATEST_REVS, **kw):
        """
        Search with query q, yield Revisions.
        """
        with self.ix[idx_name].searcher() as searcher:
            # Note: callers must consume everything we yield, so the for loop
            # ends and the "with" is left to close the index files.
            for hit in searcher.search(q, **kw):
                doc = hit.fields()
                latest_doc = doc if idx_name == LATEST_REVS else None
                item = Item(self, latest_doc=latest_doc, itemid=doc[ITEMID])
                yield item.get_revision(doc[REVID], doc=doc)

    def search_page(self, q, idx_name=LATEST_REVS, pagenum=1, pagelen=10, **kw):
        """
        Same as search, but with paging support.
        """
        with self.ix[idx_name].searcher() as searcher:
            # Note: callers must consume everything we yield, so the for loop
            # ends and the "with" is left to close the index files.
            for hit in searcher.search_page(q, pagenum, pagelen=pagelen, **kw):
                doc = hit.fields()
                latest_doc = doc if idx_name == LATEST_REVS else None
                item = Item(self, latest_doc=latest_doc, itemid=doc[ITEMID])
                yield item.get_revision(doc[REVID], doc=doc)

    def search_meta(self, q, idx_name=LATEST_REVS, **kw):
        """
        Search with query q, yield Revision metadata from index.
        """
        with self.ix[idx_name].searcher() as searcher:
            # Note: callers must consume everything we yield, so the for loop
            # ends and the "with" is left to close the index files.
            for hit in searcher.search(q, **kw):
                meta = hit.fields()
                yield meta

    def search_meta_page(self, q, idx_name=LATEST_REVS, pagenum=1, pagelen=10, **kw):
        """
        Same as search_meta, but with paging support.
        """
        with self.ix[idx_name].searcher() as searcher:
            # Note: callers must consume everything we yield, so the for loop
            # ends and the "with" is left to close the index files.
            for hit in searcher.search_page(q, pagenum, pagelen=pagelen, **kw):
                meta = hit.fields()
                yield meta

    def search_results_size(self, q, idx_name=ALL_REVS, **kw):
        """
        Return the number of matching revisions.
        """
        with self.ix[idx_name].searcher() as searcher:
            return len(searcher.search(q, **kw))

    def documents(self, idx_name=LATEST_REVS, **kw):
        """
        Yield Revisions matching the kw args.
        """
        for doc in self._documents(idx_name, **kw):
            latest_doc = doc if idx_name == LATEST_REVS else None
            item = Item(self, latest_doc=latest_doc, itemid=doc[ITEMID])
            yield item.get_revision(doc[REVID], doc=doc)

    def _documents(self, idx_name=LATEST_REVS, **kw):
        """
        Yield documents matching the kw args (internal use only).

        If no kw args are given, this yields all documents.
        """
        with self.ix[idx_name].searcher() as searcher:
            # Note: callers must consume everything we yield, so the for loop
            # ends and the "with" is left to close the index files.
            for doc in searcher.documents(**kw):
                yield doc

    def document(self, idx_name=LATEST_REVS, **kw):
        """
        Return a Revision matching the kw args.
        """
        doc = self._document(idx_name, **kw)
        if doc:
            latest_doc = doc if idx_name == LATEST_REVS else None
            item = Item(self, latest_doc=latest_doc, itemid=doc[ITEMID])
            return item.get_revision(doc[REVID], doc=doc)

    def _document(self, idx_name=LATEST_REVS, **kw):
        """
        Return a document matching the kw args (internal use only).
        """
        with self.ix[idx_name].searcher() as searcher:
            return searcher.document(**kw)

    def has_item(self, name):
        # TODO: Add fqname support to this method
        item = self[name]
        return bool(item)

    def __getitem__(self, name):
        """
        Return item with <name> (may be a new or existing item).
        """
        if name.startswith('@itemid/'):
            return Item(self, **{ITEMID: name[8:]})
        fqname = split_fqname(name)
        return Item(self, **{NAME_EXACT: fqname.value, NAMESPACE: fqname.namespace})

    def get_item(self, **query):
        """
        Return item identified by the query (may be a new or existing item).

        :kwargs query: e.g. name_exact="Foo" or itemid="..." or ...
                     (must be a unique fieldname=value for the latest-revs index)
        """
        return Item(self, **query)

    def create_item(self, **query):
        """
        Return item identified by the query (must be a new item).

        :kwargs query: e.g. name_exact="Foo" or itemid="..." or ...
                     (must be a unique fieldname=value for the latest-revs index)
        """
        return Item.create(self, **query)

    def existing_item(self, **query):
        """
        Return item identified by query (must be an existing item).

        :kwargs query: e.g. name_exact="Foo" or itemid="..." or ...
                     (must be a unique fieldname=value for the latest-revs index)
        """
        return Item.existing(self, **query)

