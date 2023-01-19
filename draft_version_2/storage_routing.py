"""
should perform the same functions as storage/middleware/routing.py

this routes storage of meta data to the right store. 
"""

from wikicfg import STORAGETYPE, STORAGEARGS
from storage import  create_storage
from constant_keys import NAME, BACKENDNAME, NAMESPACE
# in moin; mappings are created and passed to the Backend instance;
# this implementation; instantiates the instance right here.

def _get_backend(fq_names, namespaces):
    """
    For a given fully-qualified itemname (i.e. something like ns:itemname)
    find the backend it belongs to, the itemname without namespace
    spec and the namespace of the backend.

    :param fq_names: fully-qualified itemnames
    :returns: tuple of (backend name, local item name, namespace)
    """
    fq_name = fq_names[0]

    for namespace in namespaces:
        #we assume backend_name is same as namespace
        if fq_name.startswith(namespace):
            item_names = [_fq_name[len(namespace):] for _fq_name in fq_names]
            return item_names, namespace.rstrip(':')
    raise AssertionError("No backend found for {fq_name}. Namespaces: {namespaces}")
    
def storage_routing(namespaces, storage_base_dir):
    namespace_storage_map = {}
    for namespace in namespaces:
        namespace_storage_map[namespace] = create_storage(f"{storage_base_dir}/{namespace}")
        
    def store(meta, data):
        namespace = meta.get(NAMESPACE)
        if namespace is None:
            # if there is no NAMESPACE in metadata, we assume that the NAME
            # is fully qualified and determine the namespace from it:
            fq_names = meta[NAME]
            assert isinstance(fq_names, list)
            if fq_names:
                item_names, namespace = _get_backend(fq_names)
                # side effect: update the metadata with namespace and short item name (no ns)
                meta[NAMESPACE] = namespace
                meta[NAME] = item_names
            else:
                raise ValueError('can not determine namespace: empty NAME list, no NAMESPACE metadata present')
        else:
            if namespace:
                namespace += ':'  # needed for _get_backend
                _, namespace = _get_backend([namespace], namespaces)
        namespace_storage_manager = namespace_storage_map[namespace]


        revid = namespace_storage_manager.store(meta, data)

        # add the BACKENDNAME after storing, so it gets only into
        # the index, but not in stored metadata:
        meta[BACKENDNAME] = backend_name
        return backend_name, revid
    
    

    storage_routing.store = store
    storage_routing.namespace_storage_map = namespace_storage_map
    #storage_routing.get_item = get_item 
    
