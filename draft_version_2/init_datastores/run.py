from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from storage import StorageType, create_storage
from addict import Dict
import os
import indexes

config = Config(".env")
BACKEND_DATADIR_BASE=config("BACKEND_DATADIR_BASE", default="./")
WIKINAME=config("WIKINAME", default=None)
NAMESPACES =  config('NAMESPACES', cast=CommaSeparatedStrings)
STORAGETYPE = getattr(StorageType, config('STORAGE_TYPE', default="fs"))
STORAGEARGS = Dict([_.split(":") for _ in config('STORAGE_ARGS', default=[], cast=CommaSeparatedStrings)])
#print(BACKEND_DATADIR_BASE)
#print(NAMESPACES)
print (STORAGEARGS)
def build_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

build_dir(BACKEND_DATADIR_BASE)
build_dir(f"{BACKEND_DATADIR_BASE}/{WIKINAME}")
def build_namespace_storage(namespace):
    storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}/{namespace}"
    build_dir(storage_base_dir)

    # data_store_path = f"{BACKEND_DATADIR_BASE}/{namespace}/data"
    # meta_store_path = f"{BACKEND_DATADIR_BASE}/{namespace}/meta"
    # storage_builder = get_storage_builder(STORAGE_TYPE)
    # storage_builder(data_store_uri)
    # storage_builder(meta_store_uri)
    create_storage(storage_base_dir,  STORAGETYPE, STORAGEARGS)
    pass

    
for namespace in NAMESPACES:
    build_namespace_storage(namespace)


