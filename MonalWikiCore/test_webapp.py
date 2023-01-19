"""
top level app for devel purposes; we need session_manager and session context to be pypassed/fastshippedhtml/render functitons 
"""
import os
import logging
if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)


    

from MonalWikiCore.frontend import view_function
from starlette.testclient import TestClient
import justpy as jp 


from io import BytesIO
import os

from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from MonalWikiCore.engine.storage_routing import storage_routing
from MonalWikiCore.constant_keys import NAME, NAMESPACE
from MonalWikiCore.engine import indexes

storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"

# initialize storage 
storage_routing(NAMESPACES, storage_base_dir)

# initialize indexes  
indexes.indexes(storage_base_dir)
app = jp.app
client = TestClient(app)
response = client.get('/Home?itemtype=default&contenttype=text%2Fcsv%3Bcharset%3Dutf-8&template= HTTP/1.1')
response = client.get('/Home')
