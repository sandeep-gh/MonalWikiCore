class ProtectingMiddleware:
    from .indexing import parent_names

    def __init__(self, indexer, user, acl_mapping):
        """
        This object is created at the start of a transaction. It is accessed via flaskg.storage.

        :param indexer: indexing middleware instance
        :param user: a User instance (used for checking permissions)
        :param acl_mapping: list of (name_prefix, acls) tuples, longest prefix first, '' last
                            acls = dict with before, default, after, hierarchic entries
        """
        self.indexer = indexer
        self.user = user
        self.acl_mapping = acl_mapping
        self.valid_rights = ACL_RIGHTS_CONTENTS
        # The ProtectingMiddleware exists just 1 request long, but might have
        # to parse and evaluate huge amounts of ACLs. We avoid doing same stuff
        # again and again by using some fresh lru caches for each PMW instance.
        lru_cache_decorator = lru_cache(PARSE_CACHE)
        self.parse_acl = lru_cache_decorator(self._parse_acl)
        lru_cache_decorator = lru_cache(EVAL_CACHE)
        self.eval_acl = lru_cache_decorator(self._eval_acl)
        lru_cache_decorator = lru_cache(LOOKUP_CACHE)
        self.get_acls = lru_cache_decorator(self._get_acls)
        lru_cache_decorator = lru_cache(ACL_CACHE)
        self.allows = lru_cache_decorator(self._allows)
        # placeholder to show we are passing meta data around without affecting lru caches
        self.meta = None

    def _clear_acl_cache(self):
        # if we have modified the backend somehow so ACL lookup is influenced,
        # this functions need to get called, so it clears the ACL cache.
        # ACL lookups afterwards will fetch fresh info from the lower layers.
        self.get_acls.cache_clear()

    def _get_configured_acls(self, fqname):
        """
        for a fully-qualified itemname (namespace:name), get the acl configuration
        for that (part of the) namespace.

        :param fqname: fully qualified itemname
        :returns: acl configuration (acl dict from the acl_mapping)
        """
        for namespace, acls in self.acl_mapping:
            if namespace == fqname.namespace:
                return acls
        else:
            if fqname.namespace == NAMESPACE_ALL:
                # prevent traceback, /+index/all page has several links to /+index/all
                return {'default': 'All:', 'hierarchic': False, 'after': '', 'before': ''}
            raise ValueError('No acl_mapping entry found for item {0!r}'.format(fqname))

    def _get_acls(self, itemid=None, fqname=None):
        """
        return a list of (alternatively valid) effective acls for the item
        identified via itemid or fqname.
        this can be a list just containing the item's own acl (as only alternative),
        or a list with None, indicating no acl was found (in non-hierarchic mode).
        if hierarchic acl mode is enabled, a list of all valid parent acls will
        be returned.
        All lists are without considering before/default/after acls.
        """
        if itemid is not None:
            q = {ITEMID: itemid}
        elif fqname is not None:
            # itemid might be None for new, not yet stored items,
            # but we have fqname then
            q = fqname.query
        else:
            raise ValueError("need itemid or fqname")
        item = self.get_item(**q)
        acl = item.acl
        fqname = item.fqname
        if acl is not None:
            return [acl, ]
        acl_cfg = self._get_configured_acls(fqname)
        if acl_cfg['hierarchic']:
            # check parent(s), recursively
            parentids = item.parentids
            if parentids:
                acl_list = []
                for parentid in parentids:
                    pacls = self.get_acls(parentid, None)
                    acl_list.extend(pacls)
                return acl_list
        return [None, ]

    def _parse_acl(self, acl, default=''):
        return AccessControlList([acl, ], default=default, valid=self.valid_rights)

    def _eval_acl(self, acl, default_acl, user_name, right):
        aclobj = self.parse_acl(acl, default_acl)
        return aclobj.may(user_name, right)

    def query_parser(self, default_fields, idx_name=LATEST_REVS):
        return self.indexer.query_parser(default_fields, idx_name=idx_name)

    def search(self, q, idx_name=LATEST_REVS, **kw):
        for rev in self.indexer.search(q, idx_name, **kw):
            rev = ProtectedRevision(self, rev)
            if rev.allows(READ) or rev.allows(PUBREAD):
                yield rev

    def search_page(self, q, idx_name=LATEST_REVS, pagenum=1, pagelen=10, **kw):
        for rev in self.indexer.search_page(q, idx_name, pagenum, pagelen, **kw):
            rev = ProtectedRevision(self, rev)
            if rev.allows(READ) or rev.allows(PUBREAD):
                yield rev

    def search_meta(self, q, idx_name=LATEST_REVS, **kw):
        """
        Yield an item's metadata, skipping any items where read permission is denied.

        The intended use of this method is to return the current rev metadata for all
        of the items in namespace subject to query restrictions. This is useful for reports
        such as Global Index, Global Tags, Wanted Items, Orphaned Items, etc.
        """
        for meta in self.indexer.search_meta(q, idx_name, **kw):
            meta[FQNAMES] = gen_fqnames(meta)
            result = self.may_read_rev(meta)
            if result:
                yield meta

    def may_read_rev(self, meta):
        """
        Return true if user may read item revision represented by whoosh index hit.
        Called by ajaxsearch template, others.
        """
        from .indexing import parent_names
        self.meta = meta
        self.fqnames = gen_fqnames(meta)
        may_read = self.allows(tuple(self.user.name), meta.get(ACL, None), tuple(parent_names(meta[NAME])), meta[NAMESPACE], READ)
        return may_read

    def full_acls(self):
        """
        iterator over all alternatively possible full acls for this item,
        including before/default/after acl.
        """
        fqname = self.fqnames[0]
        itemid = self.meta[ITEMID]
        acl_cfg = self._get_configured_acls(fqname)
        before_acl = acl_cfg['before']
        after_acl = acl_cfg['after']
        for item_acl in self.get_acls(itemid, fqname):
            if item_acl is None:
                item_acl = acl_cfg['default']
            yield ' '.join([before_acl, item_acl, after_acl])

    def _allows(self, user_names, acls, parentnames, namespace, right):
        """
        Check if usernames may have <right> access on this item.

        :param right: the right to check
        :param user_names: user names to use for permissions check (default is to
                          use the user names doing the current request)
        :rtype: bool
        :returns: True if you have permission or False
        """
        acl_cfg = self._get_configured_acls(self.fqnames[0])
        for user_name in user_names:
            for full_acl in self.full_acls():
                allowed = self.eval_acl(full_acl, acl_cfg['default'], user_name, right)
                if allowed and pchecker(right, allowed, self.meta):
                    return True
        return False

    def search_meta_page(self, q, idx_name=LATEST_REVS, pagenum=None, pagelen=None, **kw):
        """
        Yield a revision's metadata, skipping any items where read permission is denied.

        The intended use of this method is to return the rev metadata for a pagefull of
        the items in the namespace subject to query restrictions. This is useful for reports
        such as My Changes, Item History, etc.

        Save processing time by avoiding a full ACL check when the answer will be the same as the last.

        Note that ALCs are checked after whoosh returns a pagefull of items. It is possible that
        the results shown to the user will have fewer revisions than expected.
        """
        # import here to avoid circular import error
        from .indexing import parent_names

        for meta in self.indexer.search_meta_page(q, idx_name=idx_name, pagenum=pagenum, pagelen=pagelen, **kw):
            self.meta = meta
            self.fqnames = gen_fqnames(meta)
            result = self.allows(tuple(self.user.name), meta.get(ACL, None), tuple(parent_names(meta[NAME])), meta[NAMESPACE], READ)
            if result:
                yield meta

    def search_results_size(self, q, idx_name=ALL_REVS, **kw):
        return self.indexer.search_results_size(q, idx_name, **kw)

    def documents(self, idx_name=LATEST_REVS, **kw):
        for rev in self.indexer.documents(idx_name, **kw):
            rev = ProtectedRevision(self, rev)
            if rev.allows(READ) or rev.allows(PUBREAD):
                yield rev

    def document(self, idx_name=LATEST_REVS, **kw):
        rev = self.indexer.document(idx_name, **kw)
        if rev:
            rev = ProtectedRevision(self, rev)
            if rev.allows(READ) or rev.allows(PUBREAD):
                return rev

    def has_item(self, name):
        return self.indexer.has_item(name)

    def __getitem__(self, name):
        item = self.indexer[name]
        return ProtectedItem(self, item)

    def get_item(self, **query):
        item = self.indexer.get_item(**query)
        return ProtectedItem(self, item)

    def create_item(self, **query):
        item = self.indexer.create_item(**query)
        return ProtectedItem(self, item)

    def existing_item(self, **query):
        item = self.indexer.existing_item(**query)
        return ProtectedItem(self, item)

    def may(self, fqname, capability, usernames=None):
        if usernames is not None and isinstance(usernames, (bytes, str)):
            # we got a single username (maybe bytes), make a list of str:
            if isinstance(usernames, bytes):
                usernames = usernames.decode('utf-8')
            usernames = [usernames, ]
        # TODO Make sure that fqname must be a CompositeName class instance, not unicode or list.
        fqname = fqname[0] if isinstance(fqname, list) else fqname
        if isinstance(fqname, str):
            fqname = split_fqname(fqname)
        item = self.get_item(**fqname.query)
        allowed = item.allows(capability, user_names=usernames)
        return allowed
