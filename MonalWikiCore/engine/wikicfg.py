from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from wiki_system_params import StorageType
from addict import Dict
config = Config(".env")
BACKEND_DATADIR_BASE=config("BACKEND_DATADIR_BASE", default="./")
WIKINAME=config("WIKINAME", default=None)
NAMESPACES =  config('NAMESPACES', cast=CommaSeparatedStrings)
STORAGETYPE = getattr(StorageType, config('STORAGE_TYPE', default="fs"))
STORAGEARGS = Dict([_.split(":") for _ in config('STORAGE_ARGS', default=[], cast=CommaSeparatedStrings)])
