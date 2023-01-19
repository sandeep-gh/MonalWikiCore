def get_backend(fq_names, namespaces):
    """
    For a given fully-qualified itemname (i.e. something like ns:itemname)
    find the backend it belongs to, the itemname without namespace
    spec and the namespace of the backend.

    :param fq_names: fully-qualified itemnames
    :returns: tuple of (backend name, local item name, namespace)
    """
    fq_name = fq_names[0]
    for namespace, backend_name in namespaces:
        if fq_name.startswith(namespace):
            item_names = [_fq_name[len(namespace):] for _fq_name in fq_names]
            return backend_name, item_names, namespace.rstrip(':')
    raise AssertionError("No backend found for {0!r}. Namespaces: {1!r}".format(fq_name, self.namespaces))

# class PropertiesMixin:
#     """
#     PropertiesMixin offers methods to find out some additional information from meta.
#     """
#     @property
#     def name(self):
#         if self._name and self._name in self.names:
#             name = self._name
#         else:
#             try:
#                 name = self.names[0]
#             except IndexError:
#                 # empty name list, no name:
#                 name = None
#         assert isinstance(name, str) or not name
#         return name

#     @property
#     def namespace(self):
#         return self.meta.get(NAMESPACE, '')

#     def _fqname(self, name=None):
#         """
#         return the fully qualified name including the namespace: NS:NAME
#         """
#         if name is not None:
#             return CompositeName(self.namespace, NAME_EXACT, name)
#         else:
#             return CompositeName(self.namespace, ITEMID, self.meta[ITEMID])

#     @property
#     def fqname(self):
#         """
#         return the fully qualified name including the namespace: NS:NAME
#         """
#         return self._fqname(self.name)

#     @property
#     def fqnames(self):
#         """
#         return the fully qualified names including the namespace: NS:NAME
#         """
#         if self.names:
#             return [self._fqname(name) for name in self.names]
#         else:
#             return [self.fqname]

#     @property
#     def parentnames(self):
#         """
#         Return list of parent names (same order as in names, but no dupes)

#         :return: parent names (list of unicode)
#         """
#         return parent_names(self.names)

#     @property
#     def fqparentnames(self):
#         """
#         return the fully qualified parent names including the namespace: NS:NAME
#         """
#         return [self._fqname(name) for name in self.parentnames]

#     @property
#     def acl(self):
#         return self.meta.get(ACL)

#     @property
#     def ptime(self):
#         dt = self.meta.get(PTIME)
#         if dt is not None:
#             return utctimestamp(dt)

#     @property
#     def names(self):
#         return get_names(self.meta)

#     @property
#     def mtime(self):
#         dt = self.meta.get(MTIME)
#         if dt is not None:
#             return utctimestamp(dt)

        
def parentids(item: Item ):
    # meta for item is item._current
    names = get_names(item._current)
    parentnames = parent_names(names)
    parent_ids = set()
    for parent_name in parentnames:
        rev = indexer._document(idx_name=LATEST_REVS, **{NAME_EXACT: parent_name})
        if rev:
            parent_ids.add(rev[ITEMID])
        return parent_ids


def namespace(item:Item):
    item.meta.get(NAMESPACE, '')
    
def _fqname(item:Item, name=None):
    if name is not None:
        return CompositeName(namespace(item), NAME_EXACT, name)
    else:
        return CompositeName(namespace(item), ITEMID, item.meta[ITEMID])
    pass

def get_fqname(item:Item):
    
def get_fqname(item:Item, name):
    if item.names:
        return [item._fqname(name) for name in item.names]
    else:
        return [item.fqname]

def get_fqname(item_name, field, namespace):
    """
    Compute composite name from item_name, field, namespace
    composite name == [NAMESPACE/][@FIELD/]NAME
    """
    if field and field != NAME_EXACT:
        item_name = '@{0}/{1}'.format(field, item_name)
    if namespace:
        item_name = '{0}/{1}'.format(namespace, item_name)
    return item_name
    
