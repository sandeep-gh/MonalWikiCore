from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from storage import StorageType, create_storage
from addict import Dict
import os
#import indexes
from whoosh.filedb.filestore import FileStorage
from constant_keys import LATEST_REVS, ALL_REVS
from IndexSchema import latest_revisions_schema, all_revisions_schema

import sys
config = Config(".env")
BACKEND_DATADIR_BASE=config("BACKEND_DATADIR_BASE", default="./")
WIKINAME=config("WIKINAME", default=None)

storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"
index_dir = f"{storage_base_dir}/whoosh"
try:
    os.mkdir(index_dir)
except:
    print("index already exists...aborting")
    sys.exit()
    pass
index_store = FileStorage(index_dir)
INDEXES = [LATEST_REVS, ALL_REVS, ]
schemas = {}  # existing schemas
schemas[ALL_REVS] = all_revisions_schema
schemas[LATEST_REVS] = latest_revisions_schema
        
for name in INDEXES:
    index_store.create_index(schemas[name], indexname=name)
            
#indexes.indexes(storage_base_dir)
