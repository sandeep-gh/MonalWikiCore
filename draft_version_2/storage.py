# we are not making any distinction between storage and backend
# Storage
from addict import Dict

from utils_helper_misc import serialize
import os
import base64
import zlib

import os
from wikicfg import STORAGETYPE, STORAGEARGS
from wiki_system_params import StorageType
from sqlite3 import connect, Row
from trackingFileWrapper import TrackingFileWrapper
from crypto import make_uuid
from constant_keys import REVID, DATAID, SIZE, HASH_ALGORITHM

def create_sqlite_storage(db_filepath,  **kwargs):
    """
    creates a database file and returns a tbl_storage function.
    tbl_storage manages tables within the databe 

    returns 
    """
    conn = connect(db_filepath)
    conn.row_factory = Row
    def tbl_storage(tblname):
        def storage():
            # allocate/init the resource
            def set_item(key, value):
                value = base64.b64encode(value).decode()  # a str in base64 encoding
                conn.execute(f"""insert into  {tblname} values ("{key}", "{value}")""")
                pass

            def get_item(key):
                rows = list(conn.execute(f"select value from {tblname} where key=?", (key,)))
                if not rows:
                    raise KeyError(key)
                value = str(rows[0]['value'])  # a str in base64 encoding
                value = base64.b64decode(value.encode())            
                pass

            def drop_table():
                conn.execute(f'drop table {tblname}')            
            storage.set_item = set_item
            storage.get_item = get_item
            storage.drop_table = drop_table
        storage()
        return storage
    # will allocate/initialize/incarnate the storage
    
    return tbl_storage


def create_fs_storage(data_dir, **kwargs):
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

def create_storage(storage_base_dir, storage_type=STORAGETYPE, storage_args=STORAGEARGS, **kwargs):
    """
    create meta and data store for namespace. 
    """
    metatbl_manager = None
    datatbl_manager = None
    match storage_type:
         case StorageType.sqlite:
             nmd_storage = storage_args.get("NMDStorage", "db")
             if nmd_storage == "db":
                 #"meta" and "store" should be its own db
                 meta_db_filepath = f"{storage_base_dir}/.meta.db"
                 meta_db = create_sqlite_storage(meta_db_filepath)
                 metatbl_manager = meta_db("store")
                 data_db_filepath = f"{storage_base_dir}/.data.db"
                 data_db = create_sqlite_storage(data_db_filepath)
                 datatbl_manager = data_db("store")

             if nmd_storage == "tbl":
                 #"meta" and "store" are stored  tables in single db
                 db_filepath = f"{storage_base_dir}/.db"
                 db_tbl_manager = create_sqlite_storage(db_filepath)
                 metatbl_manager = db_tbl_manager("meta")
                 datatbl_manager = db_tbl_manager("data")
                 
             pass
             #return create_storage_sqlite(kwargs)
         case StorageType.fs:
             pass
         
             #return create_storage_fs(kwargs)

    def store_manager():
        def store_meta(meta):
            if REVID not in meta:
            # Item.clear_revision calls us with REVID already present
                meta[REVID] = make_uuid()
            metaid = meta[REVID]
            meta = serialize(meta)
            # XXX Idea: we could check the type the store wants from us:
            # if it is a str/bytes (BytesStore), just use meta "as is",
            # if it is a file (FileStore), wrap it into BytesIO and give that to the store.
            metatbl_manager.set_item(metaid, meta)

        def store(meta, data):
            """
                Store info consisting of meta and data on to the metatbl and datatbl
            """
            if DATAID not in meta:
                tfw = TrackingFileWrapper(data, hash_method=HASH_ALGORITHM)
                dataid = make_uuid()
                # we 
                datatbl_manager.set_item(dataid,  tfw.read())
                meta[DATAID] = dataid
                # check whether size and hash are consistent:
                size_expected = meta.get(SIZE)
                size_real = tfw.size
                if size_expected is not None and size_expected != size_real:
                    raise ValueError("computed data size ({0}) does not match data size declared in metadata ({1})".format(
                                     size_real, size_expected))
                meta[SIZE] = size_real
                hash_expected = meta.get(HASH_ALGORITHM)
                hash_real = tfw.hash.hexdigest()
                if hash_expected is not None and hash_expected != hash_real:
                    raise ValueError("computed data hash ({0}) does not match data hash declared in metadata ({1})".format(
                                     hash_real, hash_expected))
                meta[HASH_ALGORITHM] = hash_real
            else:
                dataid = meta[DATAID]
                # we will just asume stuff is correct if you pass it with a data id
                try:
                    datatbl_manager.get_item(dataid)
                except:
                    datatbl_manager.set_item(data)

                if dataid not in data_store:
                    self.data_store[dataid] = data
            # if something goes wrong below, the data shall be purged by a garbage collection
            metaid = store_meta(meta)
            return metaid       
        

        
        store_manager.store_meta = store_meta
        store_manager.store = store
    store_manager()
    
    return store_manager


