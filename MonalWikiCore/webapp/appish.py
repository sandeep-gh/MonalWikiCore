import logging
from moin.constants.keys import CURRENT
import justpy as jp
import importlib
import os
from frontend import frontend
from moin.storage.middleware import protecting, indexing, routing
# justpy already loads <run_dir>/justpy.env as config
from starlette.testclient import TestClient
from addict import Dict
from moin import user
from moin.utils.clock import Clock
from moin.themes import setup_jinja_env, themed_error
from MonalWikiCore.webapp import auth
from moin.constants.misc import ANON
from starlette.datastructures import Headers
# from moin.constants.keys import CURRENT
# from moin.constants.namespaces import NAMESPACE_DEFAULT
# from MonalWikiCore.webapp.utils.interwiki import url_for_item
def setup_user(request):
    """
    Try to retrieve a valid user object from the request, be it
    either through the session or through a login.
    """
    # init some stuff for auth processing:
    appctx = app.ctx 
    appctx._login_multistage = None
    appctx._login_multistage_name = None
    appctx._login_messages = []
    session = request['session']

    # first try setting up from session
    try:
        userobj = auth.setup_from_session()
    except KeyError:
        # error caused due to invalid cookie, recreating session
        session.clear()
        userobj = auth.setup_from_session()

    # then handle login/logout forms
    form = request.values.to_dict()
    if 'login_submit' in form:
        # this is a real form, submitted by POST
        userobj = auth.handle_login(userobj, **form)
    elif 'logout_submit' in form:
        # currently just a GET link
        userobj = auth.handle_logout(userobj)
    else:
        userobj = auth.handle_request(userobj)

    # if we still have no user obj, create a dummy:
    if not userobj:
        userobj = user.User(name=ANON, auth_method='invalid')
    # if we have a valid user we store it in the session
    if userobj.valid:
        request_session = session
        request_session['user.itemid'] = userobj.itemid
        request_session['user.trusted'] = userobj.trusted
        request_session['user.auth_method'] = userobj.auth_method
        request_session['user.auth_attribs'] = userobj.auth_attribs
        request_session['user.session_token'] = userobj.get_session_token()
    return userobj


def before_wiki(request):
    """
    Setup environment for wiki requests, start timers.
    """
    logging.debug("running before_wiki ", scope)
    session = request['session']
    appctx = app.ctx
    appctx.clock = Clock()
    appctx.clock.start('total')
    appctx.clock.start('init')
    try:
        appctx.unprotected_storage = app.storage

        appctx.user = setup_user(request)
        appctx.storage = protecting.ProtectingMiddleware(app.storage, appctx.user, app.cfg.acl_mapping)

        appctx.dicts = app.cfg.dicts()
        appctx.groups = app.cfg.groups()

        appctx.content_lang = app.cfg.language_default
        appctx.current_lang = app.cfg.language_default

        setup_jinja_env()

        # request.user_agent == '' if this is pytest
        appctx.add_lineno_attr = headers.user_agent and appctx.user.edit_on_doubleclick
    finally:
        appctx.clock.stop('init')

    # if return value is not None, it is the final response


def load_wikicfg():
    wikicfg_fp = jp.config('MONALWIKICONFIGPATH', default='./wikiconfig.py')
    modulename = os.path.basename(wikicfg_fp)[:-3]
    moduledir = os.path.dirname(wikicfg_fp)
    spec = importlib.util.spec_from_file_location("WikiConfigModule", wikicfg_fp)
    wikicfg_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wikicfg_module)

    return wikicfg_module.Config

#print(wikicfg_fp)
Config = load_wikicfg()
#TODO: make sure wikiConfig has secrets set

setattr(jp, "wikiConfig", Config())
app = jp.app

frontend_app = frontend.build_app(before_wiki)
app.mount(path="", app=frontend_app, name="frontend")
#
#from moin.apps.frontend import frontend
#frontend.before_request(before_wiki)
# frontend.teardown_request(teardown_wiki)
# app.register_blueprint(frontend)
# from moin.apps.admin import admin
# admin.before_request(before_wiki)
# admin.teardown_request(teardown_wiki)
# app.register_blueprint(admin, url_prefix='/+admin')
# from moin.apps.feed import feed
# feed.before_request(before_wiki)
# feed.teardown_request(teardown_wiki)
# app.register_blueprint(feed, url_prefix='/+feed')
# from moin.apps.misc import misc
# misc.before_request(before_wiki)
# misc.teardown_request(teardown_wiki)
# app.register_blueprint(misc, url_prefix='/+misc')
# from moin.apps.serve import serve
# app.register_blueprint(serve, url_prefix='/+serve')
# clock.stop('create_app register')
# clock.start('create_app flask-cache')
# # the 'simple' caching uses a dict and is not thread safe according to the docs.
# cache = Cache(config={'CACHE_TYPE': 'simple'})
# cache.init_app(app)
# app.cache = cache
# clock.stop('create_app flask-cache')
# # init storage
# clock.start('create_app init backends')
# init_backends(app)
# clock.stop('create_app init backends')
# clock.start('create_app flask-babel')
# i18n_init(app)
# clock.stop('create_app flask-babel')
# # configure templates
# clock.start('create_app flask-theme')
# setup_themes(app)
# if app.cfg.template_dirs:
#     app.jinja_env.loader = ChoiceLoader([
#         FileSystemLoader(app.cfg.template_dirs),
#         app.jinja_env.loader,
#     ])
# app.register_error_handler(403, themed_error)
# clock.stop('create_app flask-theme')
# clock.stop('create_app total')
# del clock
#return app

#cfg = jp.wikiConfig
# item_name = cfg.root_mapping.get(NAMESPACE_DEFAULT, cfg.default_root)
# print("n = ", NAMESPACE_DEFAULT)
# print (cfg.default_root)
# print (item_name)
    


print (app.router)
client = TestClient(app)
response = client.get('/')
#frontend.show_root(None)
#print(jp.wikiConfig)
#jp.justpy(frontend.show_root)
