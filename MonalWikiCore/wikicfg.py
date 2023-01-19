from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from .system_params import StorageType
from addict import Dict
from MonalWikiCore.constant_keys import NAMESPACE_DEFAULT
import os
config = Config(".env")
BACKEND_DATADIR_BASE=config("BACKEND_DATADIR_BASE", default="./")
WIKINAME=config("WIKINAME", default=None)

WIKI_DATADIR = os.path.join(BACKEND_DATADIR_BASE, WIKINAME)
NAMESPACES =  [_ for _ in config('NAMESPACES', cast=CommaSeparatedStrings)] + [NAMESPACE_DEFAULT]
                                                                  
STORAGETYPE = getattr(StorageType, config('STORAGE_TYPE', default="fs"))
STORAGEARGS = Dict([_.split(":") for _ in config('STORAGE_ARGS', default=[], cast=CommaSeparatedStrings)])


ADMIN_DB_SQLALCHEMY_URL = "sqlite:///" + os.path.join(WIKI_DATADIR, "/admin.db")
