# we are not making any distinction between storage and backend
# Storage
from addict import Dict

from aenum import Enum
import os
import base64
import zlib

import os

from sqlite3 import connect, Row
class StorageType(Enum):
    sqlite = "sqlite"
    fs = "fs"

def create_sqlite_storage(db_filepath,  **kwargs):
    """
    creates a database file and returns a tbl_storage function.
    tbl_storage manages tables within the databe 

    returns 
    """
    db_path = os.path.dirname(db_filepath)
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    conn = connect(db_filepath)
    print (f"created database at {db_filepath}")
    conn.row_factory = Row
    def tbl_storage(tblname):
        conn.execute(f'create table {tblname} (key text primary key, value blob)')
        print (f"creating table {tblname}")
        def storage():
            # allocate/init the resource
            def set_item(tblname, key, value):
                value = base64.b64encode(value).decode()  # a str in base64 encoding
                conn.execute(f'insert into  {tblname} values ({key}, {value})')
                pass

            def get_item(tblname, key):
                rows = list(conn.execute(f"select value from {tblname} where key=?", (key,)))
                if not rows:
                    raise KeyError(key)
                value = str(rows[0]['value'])  # a str in base64 encoding
                value = base64.b64decode(value.encode())            
                pass
            storage.set_item = set_item
            storage.get_item = get_item
        def drop_table(tblname):
            conn.execute(f'drop table {tblname}')
        tbl_storage.drop_table = drop_table

        storage()
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

def create_storage(storage_base_dir, storage_type, storage_args, **kwargs):
    """
    create meta and data store for namespace 
    """
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
             return metatbl_manager, datatbl_manager
                 
             #return create_storage_sqlite(kwargs)
         case StorageType.fs:
             pass
         
             #return create_storage_fs(kwargs)

    

         
