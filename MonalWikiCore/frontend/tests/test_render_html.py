
from io import BytesIO
import os

from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from MonalWikiCore.engine.storage_routing import storage_routing
from MonalWikiCore.engine.indexes import indexes

from MonalWikiCore.constant_keys import NAME, NAMESPACE, NAME_EXACT, NAMESPACE_DEFAULT, CURRENT, CONTENTTYPE
from MonalWikiCore.Name import CompositeName
from MonalWikiCore.wiki import WikiItem, wikiItemTypes
from MonalWikiCore.frontend.view_function import endpoint_wikiItem, renderhtml_wikiItem
from starlette.testclient import TestClient

import justpy as jp 

storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"
# storage backend 
storage_routing(NAMESPACES, storage_base_dir)
# init indexes 
indexes(storage_base_dir)

app = jp.app
client = TestClient(app)

# show webpage of nonexistent item with unkown itemtype and contenttype
#response = client.get('/Home')

# show webpage of nonexistent item with known itemtype and contenttype 
response = client.get('/Home?itemtype=default&contenttype=text%2Fcsv%3Bcharset%3Dutf-8&template= HTTP/1.1')


