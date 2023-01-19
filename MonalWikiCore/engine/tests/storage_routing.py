from io import BytesIO
import os

from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from MonalWikiCore.engine.storage_routing import storage_routing
from MonalWikiCore.constant_keys import NAME, NAMESPACE

storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"

storage_routing(NAMESPACES, storage_base_dir)
revid_or_metaid = storage_routing.namespace_storage_map['users'].store({NAME: 'test'}, b'this is test string')
print("revid_or_metaid = ", revid_or_metaid)
