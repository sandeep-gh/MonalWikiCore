from starlette.applications import Starlette
from moin.constants.keys import CURRENT, NAME_EXACT
from moin.constants.namespaces import NAMESPACE_DEFAULT
from moin.utils.interwiki import url_for_item, split_fqname, CompositeName
import justpy as jp

from moin.signalling import item_displayed, item_modified
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
# from moin.items import (BaseChangeForm, Item, NonExistent, NameNotUniqueError, MissingParentError,
#                         FieldNotUniqueError, get_itemtype_specific_tags, CreateItemForm, find_matches)
from moin.items import Item
from moin import user
from starlette.routing import Router, Route

from MonalWikiCore.webapp.utils.interwiki import url_for_item
from MonalWikiCore.webapp.utils.utils import pre_endpoint_run
from starlette.requests import Request
from starlette.responses import Response

#@jp.SetRoute("/{item_name}", name="frontend.show_item")
#TODO: add decorator to inject path paras
before_request_func = None
def sef_before_request_func(afunc):
    global before_request_func
    before_request_func = afunc
    
    pass
# moving to CustomMiddleware over 
# class CustomMiddleware(GZipMiddleware):
#     async def __call__(self, scope, receive, send) -> None:
#         if before_request_func:
#             before_request_func(scope)
#         await super().__call__(scope, receive, send)

# class CustomMiddleware(SessionMiddleware):
#     async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        
#         await super().__call__(scope, receive, send)


router = Router()
def build_app(before_endpoint):
    app = Starlette(debug=True)

    @app.middleware("http")
    async def before_request_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            #request.state.db = SessionLocal()
            before_endpoint(request)
            response = await call_next(request)
        finally:
            #request.state.db.close()
            pass
        return response
    # app.add_middleware(SessionMiddleware,
    #                    before_request = before_endpoint,
    #                    secret_key = jp.SECRET_KEY )
    app.mount('', router)
    return app

@pre_endpoint_run
def show_item(request):
    print (request.path_params)
    item_name = request.path_params['item_name']
    rev = CURRENT #TODO: we need to figure out how to pass rev
    #TODO: need to inject rev
    fqname = split_fqname(item_name)

    #TODO: no idea why we need this. look at it later
    # item_displayed.send(app._get_current_object(),
    #                     fqname=fqname)
    if not fqname.value and fqname.field == NAME_EXACT:
        fqname = fqname.get_root_fqname()
        return jp.redirect(url_for_item(fqname))
    try:
        item = Item.create(item_name, rev_id=rev)
        user = request['user']
        user.add_trail(item_name)
        item_is_deleted = False #flash_if_item_deleted(item_name, rev, item) #TODO: turn on later
        result = item.do_show(rev, item_is_deleted=item_is_deleted)
    except AccessDenied:
        abort(403)
    except FieldNotUniqueError:
        raise ValueError("uncharted territory")

    print("at show_item for item_name = ", item_name)
    wp = jp.WebPage()
    jp.Span(a=wp, text="ttt")
    return wp


jp.CastAsEndpoint(show_item, "/{item_name}", "show_item", router)
#using name = frontend.show_item because thats moin2.0 computes in url_for_item
#jp.Route("/{item_name}", show_item, name="frontend.show_item") 

# def an_endpoint(request):
#     """

#     """
#     wp = jp.WebPage()
#     return wp
    


#@jp.SetRoute("/", name="frontend.show_root")
def show_root(request):
    cfg = jp.wikiConfig
    # ============ adding a dummy user purely for testing ===========
    #TODO remove this from production
    request['user'] = user.User()

    # ============================= end =============================
    
    item_name = cfg.root_mapping.get(NAMESPACE_DEFAULT, cfg.default_root)
    # return redirect(url_for_item(item_name))
    # print ("what to do item_name = ", item_name)
    # print (jp.app.router.url_path_for("show_item", item_name="HOME"))
    
    target_url = url_for_item(request, item_name,  endpoint_name="show_item")
    print (f"redirecting page to {target_url}")
    return jp.redirect(target_url)

    pass
 

#jp.Route("/", show_root, name="show_root") 
jp.CastAsEndpoint(show_root, "/", "show_root", router)
