# we are not making any distinction between storage and backend
# Storage
from addict import Dict


import os
import base64
import zlib

import os

from sqlite3 import connect, Row
from .crypto import make_uuid
from ..constant_keys import REVID, DATAID, SIZE, HASH_ALGORITHM
from .utils import serialize, deserialize
from ..wikicfg import STORAGETYPE, STORAGEARGS
from ..system_params import StorageType

def create_sqlite_db(db_filepath):
    conn = connect(db_filepath)
    conn.row_factory = Row
    def db_manager(**kwargs):
        """
        creates a database file and returns a tbl_storage function.
        tbl_storage manages tables within the databe 

        returns 
        """
        def get_tbl_manager(tblname):
            def tbl_manager():
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
                    return value 


                def drop_table():
                    conn.execute(f'drop table {tblname}')


                tbl_manager.set_item = set_item
                tbl_manager.get_item = get_item
                tbl_manager.drop_table = drop_table
            tbl_manager()
            return tbl_manager
        def commit():
            print ("commit db on path = ", db_filepath)
            conn.commit()
        db_manager.commit = commit
        db_manager.get_tbl_manager = get_tbl_manager
    db_manager()
    return db_manager

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
    db_managers = []
    metatbl_manager = None
    datatbl_manager = None
    match storage_type:
         case StorageType.sqlite:
             nmd_storage = storage_args.get("NMDStorage", "db")
             if nmd_storage == "db":
                 #"meta" and "store" should be its own db
                 meta_db_filepath = f"{storage_base_dir}/.meta.db"
                 meta_db_manager = create_sqlite_db(meta_db_filepath)
                 metatbl_manager = meta_db_manager.get_tbl_manager("store")
                 data_db_filepath = f"{storage_base_dir}/.data.db"
                 data_db_manager = create_sqlite_db(data_db_filepath)
                 datatbl_manager = data_db_manager.get_tbl_manager("store")
                 db_managers = [meta_db_manager, data_db_manager]

             if nmd_storage == "tbl":
                 #"meta" and "store" are stored  tables in single db
                 db_filepath = f"{storage_base_dir}/.db"
                 db_manager= create_sqlite_db(db_filepath)
                 metatbl_manager = db_manager.get_tbl_manager("meta")
                 datatbl_manager = db_manager.get_tbl_manager("data")
                 db_managers = [db_manager]
                 
             pass
             #return create_storage_sqlite(kwargs)
         case StorageType.fs:
             pass
         
             #return create_storage_fs(kwargs)

    assert datatbl_manager is not None
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
            return metaid

        def store(meta, data):
            """
                Store info consisting of meta and data on to the metatbl and datatbl
            """
            # if DATAID not in meta:
            #     tfw = TrackingFileWrapper(data, hash_method=HASH_ALGORITHM)
            #     dataid = make_uuid()
            #     # we 
            #     datatbl_manager.set_item(dataid,  tfw.read())
            #     meta[DATAID] = dataid
            #     # check whether size and hash are consistent:
            #     size_expected = meta.get(SIZE)
            #     size_real = tfw.size
            #     if size_expected is not None and size_expected != size_real:
            #         raise ValueError("computed data size ({0}) does not match data size declared in metadata ({1})".format(
            #                          size_real, size_expected))
            #     meta[SIZE] = size_real
            #     hash_expected = meta.get(HASH_ALGORITHM)
            #     hash_real = tfw.hash.hexdigest()
            #     if hash_expected is not None and hash_expected != hash_real:
            #         raise ValueError("computed data hash ({0}) does not match data hash declared in metadata ({1})".format(
            #                          hash_real, hash_expected))
            #     meta[HASH_ALGORITHM] = hash_real
            # else:
            #     dataid = meta[DATAID]
            # we will just asume stuff is correct if you pass it with a data id
            dataid = make_uuid()
            meta[DATAID] = dataid
            try:
                datatbl_manager.get_item(dataid)
            except:
                datatbl_manager.set_item(dataid, data)

            # sems we don't need this 
            # if dataid not in data_store:
            #     datatbl_manager.set_item(dataid, data)
            # if something goes wrong below, the data shall be purged by a garbage collection
            metaid = store_meta(meta)
            return metaid
        
        
        def retrieve(metaid):
            """
                Store info consisting of meta and data on to the metatbl and datatbl
            """
            meta = deserialize(metatbl_manager.get_item(metaid))
            dataid = meta[DATAID]
            data = datatbl_manager.get_item(dataid)
            return meta, data
        
        def commit():
            for db_manager in db_managers:
                db_manager.commit()
        store_manager.store_meta = store_meta
        store_manager.store = store
        store_manager.retrieve = retrieve
        store_manager.datatbl_manager = datatbl_manager
        store_manager.commit = commit
    store_manager()
    
    return store_manager


