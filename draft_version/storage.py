# Storage
from addict import Dict

def create_sqlite_storage(**kwargs):
    def storage():
        table = "mytable"
        # allocate/init the resource
        def set_item(key, value):
            pass

        def get_item(key):
            pass

        storage.set_item = set_item
        storage.get_item = get_item
        storage.has_item = has_item

    # will allocate/initialize/incarnate the storage
    storage()
    return storage


def init_storage_fs(**kwargs):
    path = "/tmp/monalwiki/content"
    def storage():
        def set_item(key, value):
            pass

        def get_item(key):
            pass

        def has_item(key):
            pass

        storage.set_item = set_item
        storage.get_item = get_item
        storage.has_item = has_item

    storage()
    return storage
    
    #return Dict({'set_item': set_item, 'get_item': get_item, 'has_item': has_item})

def init_storage(storage_type, **kwargs):
    match storage_type:
         case StorageType.sqlite:
             
             return create_storage_sqlite(kwargs)
         case StorageType.fs:
             init_storage_fs()
             return create_storage_sqlite(kwargs)

    
