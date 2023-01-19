from .keys import NAMESPACE, NAME
from utilshelpermisc import get_backend
def instantiate_backend(**kwargs):
    """
    allocate/init/instantiate a backend 
    """

    def backend():
        namespaces = None #TODO: fill this up
        backends = None #TODO: fill this up 
        def retrieve(backend_name, revid):

            pass

        def store(meta, data):
            namespace = meta.get_item(NAMESPACE)
            if namespace is None:

                fq_names = meta.get_item(NAME)
                assert isinstance(fq_names, list)
                if fq_names:
                    backend_name, item_names, namespace = get_backend(fq_names, namespaces)
                    meta.set_item(NAMESPACE, namespace)
                    meta.set_item(NAME, item_names)
                else:
                raise ValueError('can not determine namespace: empty NAME list, no NAMESPACE metadata present')
            else:
                if namespace:
                    namespace += ':'  # needed for _get_backend
                backend_name, _, _ = get_backend([namespace], namespaces)
            backend = backends[backend_name]
            if not isinstance(backend, MutableBackendBase):
                raise TypeError('backend {0} is readonly!'.format(backend_name))

            revid = backend.store(meta, data)

            # add the BACKENDNAME after storing, so it gets only into
            # the index, but not in stored metadata:
            meta.set_item(BACKENDNAME, backend_name)
            return backend_name, revid        



        backend.retrieve = retrieve
        backend.store = store

    backend()
    return backend


