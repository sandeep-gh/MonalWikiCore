from .storage import init_storage
from .systemdesign import StorageType
from aenum import Dict
from .keys import DATAID
def init_backend(**kwargs):
    # For now hardwire meta to sqlite storage
    # and
    # data to file storage

    backend_runtime = Dict()
    meta_store = backend_runtime.storage.meta_store  = init_storage(StorageType.sqlite)
    data_store = backend_runtime.storage.data_store = init_storage(StorageType.fs)
    
    def store(meta, data):
        if not meta.has_item(DATAID):
            tfw = TrackingFileWrapper(data, hash_method=HASH_ALGORITHM)
            dataid = make_uuid()
            data_store.add_item(dataid, tfw)
            meta.add_item(DATAID, dataid)
            # check whether size and hash are consistent:
            size_expected = meta.get_item(SIZE)
        
        
        
