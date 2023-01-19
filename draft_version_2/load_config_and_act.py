from wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from storage_routing import storage_routing
from constant_keys import NAME, NAMESPACE
from io import BytesIO
import os
storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"

# after invocation storage_routing is both function and a class instance (kind-of-like global-static class instance. it has member store(meta, data) and stuff
storage_routing(NAMESPACES, storage_base_dir)
storage_routing.namespace_storage_map['users'].store({NAME: 'test'}, BytesIO(b''))


#print (storage_routing.namespace_storage_map['users'].store)

# ################# MOIN stuff to generate met and item ##################
# from io import BytesIO
# import hashlib
# #from whoosh.query import Term

# #from flask import g as flaskg

# from moin.constants.keys import (NAME, NAME_EXACT, SIZE, ITEMID, REVID, DATAID,
#                                  HASH_ALGORITHM, CONTENT, COMMENT, LATEST_REVS,
#                                  ALL_REVS, NAMESPACE, NAMERE, NAMEPREFIX,
#                                  CONTENTTYPE, ITEMTYPE, ITEMLINKS, REV_NUMBER)

# from moin.constants.namespaces import NAMESPACE_USERS

# from moin.utils.interwiki import split_fqname

# from moin.config.default import DefaultConfig as Config
# #from flask import current_app as app
# from flask import Flask, request, session
# from moin.storage.middleware import protecting, indexing, routing

# #from moin import create_app
# app = Flask('moin')

# flask_config_file = "/tmp/wetfeet/wikiconfig.py"
# app.config.from_pyfile(flask_config_file)
# Config = app.config.get('MOINCFG')
# Config.secrets = app.config.get('SECRET_KEY')
# cfg = Config()
# app.cfg = cfg
# router = routing.Backend(cfg.namespace_mapping, cfg.backend_mapping)

# router.open()
# imw = indexing.IndexingMiddleware(cfg.index_storage, router,
#                                                    wiki_name=cfg.interwikiname,
#                                                    acl_rights_contents=cfg.acl_rights_contents)

# imw.open()
# item_name = 'foo'
# data = b'bar'
# newdata = b'baz'


# with app.app_context():
#     item = imw[item_name]
#     print (item)
    
#     #store({NAME: 'test'}, BytesIO(b''))
# #config = app.config

# #     app.config.from_pyfile(flask_config_file)
# #     Config = app.config.get('MOINCFG')
# #     cfg = Config()
#     # router = routing.Backend(cfg.namespace_mapping, cfg.backend_mapping)
#     # router.open()

#     # imw = indexing.IndexingMiddleware(cfg.index_storage, app.router,
#     #                                               wiki_name=cfg.interwikiname,
#     #                                               acl_rights_contents=cfg.acl_rights_contents)
