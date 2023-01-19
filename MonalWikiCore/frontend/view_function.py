# this needs to be imported first; else there ends up
# two copies of ofjustpy and breaks the session manager
from MonalWikiCore.frontend.wp_template_components import page_builder, render_nav_bar, render_footer



import justpy as jp
import ofjustpy as oj
import ofjustpy_react as ojr
from . import actions
from addict import Dict
from MonalWikiCore.constant_keys import CURRENT
from MonalWikiCore.constant_keys import ITEMTYPE_NONEXISTENT, ITEMTYPE_DEFAULT
from MonalWikiCore.Name import url_to_compositeName
from MonalWikiCore.wiki import WikiItem
#from MonalWikiCore.wiki.Content import CONTENTTYPE_NONEXISTENT
from ..contenttypes import NonExistent as Content_NonExistent
from tailwind_tags import H,full, bold, bsw, bdr, bold, fz, fw, W, mr, st

app = jp.build_app()
def show_wikiItem_(wikiItem):
    """
    render the content of the wikiItem based on the contenttype 

    """
    def renderer_pagebody(session_manager):
        with session_manager.uictx("body") as bodyCtx:
            _ictx=bodyCtx
            assert  wikiItem.content.contenttype != CONTENTTYPE_NONEXISTENT
            oj.Span_("panel",  text="i am a span:dryrun")
            print("chasing contenttype and data")
            print ("===> contenttype = ", wikiItem.content.contenttype)

            print ("===>  = ", wikiItem.rev.revid)
            
    
    return renderer_pagebody



def modify_wikiItem_(wikiItem):
    """
    render the content of the wikiItem based on the contenttype 

    """
    def renderer_pagebody(session_manager):
        with session_manager.uictx("body") as bodyCtx:
            _ictx=bodyCtx
            
            title_ = oj.Halign_(oj.Span_("itemtitle_body",
                               text=wikiItem.fqcn.fullname(),
                                        pcp=[fz.xl2, fw.bold]
                                        ),
                                key="itemtitle")

            divider_ = oj.Divider_("title_divider")
            commentbox_ = oj.Subsubsection_("comment", "Comment",
                             oj.Textarea_("comment_input", placeholder="enter comments for wiki item here", pcp=[W/full, H/8])
                             )

            contentbox_ = oj.Subsubsection_("content", "Content",
                                            oj.Textarea_("content_input",
                                                         placeholder="enter wiki item content here", pcp=[H/32 ]),
                                            pcp = [mr/st/8]
                             )


            #gm<-- generalmeta
            gm_title_ = oj.Halign_(oj.Span_("gm_title_body",
                                         text="General Meta",
                                         pcp=[fz.lg, fw.bold]
                                        ),
                                align="start",
                                   key="itemtitle",
                                   pcp=[mr/st/8])
            gm_divider_ = oj.Divider_("gm_divider")
            gm_summary_ = oj.Subsubsection_("gm_summary", "Summary",
                                            oj.Textarea_("summary_input", placeholder="enter summary for changes", pcp=[H/8]), pcp=[mr/st/8]
                              )
            gm_tags_ = oj.Subsubsection_("gm_tags", "Tags",
                                         oj.Textarea_("tags_input",
                                                      placeholder="enter tag for content",
                                                      pcp=[H/8]),
                                         pcp=[mr/st/4]

                              )

            def on_submit_btnclick(dbref, msg):
                userinput = Dict()
                userinput.comment = _ictx.comment_input.target.value
                userinput.content = _ictx.content_input.target.value
                userinput.summary_input = _ictx.summary_input.target.value
                userinput.tags = _ictx.tags_input.target.value
                print(userinput)
                print ("====================================")
                pass
            
            submit_ =oj.Halign_(
                oj.Button_("submit", text="Create item (add to wiki)").event_handle(oj.click, on_submit_btnclick),
                pcp=[mr/st/4]
            )
                                

            # panel is what hooks 
            oj.Halign_(
                oj.StackV_("panel_core",
                           cgens=[title_,
                                  divider_,
                                  commentbox_,
                                  contentbox_,
                                  gm_title_,
                                  gm_divider_,
                                  gm_summary_,
                                  gm_tags_,
                                  submit_
                                  ]),
                key="panel",
                pcp=[H/full])
            
    return renderer_pagebody


# wp_show = page_builder("wp_show_wikiItem",
#                        "Show contents of a wiki item",
#                        lambda request, wikiItem=wikiItem: show_wikiItem_bodygen(request, wikiItem))
            
def wp_nonexistent_wikiItem(request, fqname):
    session_id = request.session_id
    session_manager = oj.get_session_manager(session_id)
    appstate = session_manager.appstate

    # Build href url for each itemtype
    query_str = "?itemtype=default&contenttype=text%2Fcsv%3Bcharset%3Dutf-8&template= HTTP/1.1"
    new_item_url = request.url_for("endpoint_wikiItem", item_name=fqname) + query_str
    print ("new item url = ", new_item_url)
    def panel_builder(session_manager):
        with session_manager.uictx("body") as bodyCtx:
            _ictx = bodyCtx
            aspan_ = oj.Span_("aspan", text=f"Requested item {fqname} does not exists in wiki")
            a_ = oj.Halign_(oj.A_("create ", href=new_item_url,
                                  title=f"Create wiki item {fqname}",
                                  text="create",
                                  pcp=[bold, bsw._, bsw.sm,
                                       bdr.md, bold]))
            oj.Align_(oj.StackV_("panel_core", cgens=[aspan_, a_]), key="panel", pcp=[H/full])
    wp =  page_builder("wp_nonexistent_wikiItem",
                        "Non Existent wiki item",
                        panel_builder
                        )(request)
    wp.session_manager = session_manager
    return wp


def wp_upload_new_csv(request):
    #Assume that session context is already active
    session_id = request.session_id
    session_manager = oj.get_session_manager(session_id)
    appstate = session_manager.appstate

    with oj.sessionctx(session_manager):
        with session_manager.uictx("upload_new_csv") as upload_new_csv_ctx:
            _ictx = upload_new_csv_ctx
            #@Stuff : pass it through state-change-diagram
            def on_click(dbref, msg):
                # collect stuff from front page
                # put it on state
                # let deltas in state take care. of things
                return "/wikiItem_content", {"content ": b"ia m csv content", "comment":"this is commment", "created": "sandeep", "time": "sometime"}
            


            btn_ = oj.Button_("upload_csv_btn", text="Upload").event_handle(oj.click, on_click)

        tlc = oj.Container_("tlc", cgens=[btn_])
        wp_ = oj.WebPage_("basicpage", cgens = [tlc], title="create new csv")
        wp = wp_()
        wp.session_manager = session_manager
    return wp 


def renderhtml_wikiItem(request, wikiItem, session_manager=None):
    """
    build a webpage that shows a wikiItem on the browser. 
    Multiplex/polymorphic based on itemtype/content type 

    wikiItem is of type wikiItemTypes: [Default|NonExistent]
    wikiItem.content is of type Content: [NonExistent| CSV]
    """
    print ("render wikiItem: itemtype= ", wikiItem.itemtype)
    
    
    if wikiItem.itemtype == ITEMTYPE_NONEXISTENT:
        #we assume that user has right to create (see moninwiki/src/items/__init__.py:1455)
        # We should verify parents (whatever that means; and if not then create_new_item.html
        # using modify-select: wtm
        print ("show webpage for nonexists tiem")
        print ("fqcn  = ", wikiItem.fqcn)
        fullname = wikiItem.fqcn.fullname()
        print ("fullname = ", fullname)
        return wp_nonexistent_wikiItem(request, fullname)
        pass
    if wikiItem.itemtype == ITEMTYPE_DEFAULT:
        #print ("render wikiItem: content= ", wikiItem.content.contenttype)
        # return an html response for default item
        # Currently, no good way to telll if we need to upload a new csv or view an existing csv
        # using the revid  condition to determine
        print ("there is rev ", wikiItem.rev.revid)
        if wikiItem.rev.revid == None:
            # There is no content; but the contenttype is defined. 
            # render modify_item.html 
            # 
            #return wp_modify(request, )
            return page_builder("wp_modify_wikiItem",
                        "modify/create a wiki item", modify_wikiItem_(wikiItem)
                                )(request)

        if wikiItem.rev.revid is not  None:
            # this is a fully fledged filled out item : show it.
            print(" i am here ")
            return page_builder("wp_show_wikiItem",
                        "show_wikiItem", show_wikiItem_(wikiItem)
                                )(request)

    assert False
    
# all urls for /<itemname> will arrive here; if an item with the itemname exists -- its content
# will be rendered based on its itemtyp/contenttype; if itemname does not exists then choice
# will be given to select the itemtype/contenttype 
def endpoint_wikiItem(request, rev = CURRENT, item_name =None):
    print ("show_wikiItem invoked: with rev, itemName", rev, item_name)
    print ("query_params = ", request.query_params._dict)
    itemtype = request.query_params._dict.get('itemtype', ITEMTYPE_NONEXISTENT)
    contenttype = request.query_params._dict.get('contenttype', None)
    fqcn = url_to_compositeName(item_name)
    wikiItem = WikiItem.create(fqcn, rev_id=rev, itemtype = itemtype, contenttype=contenttype)
    return renderhtml_wikiItem(request, wikiItem)


# def modify_wikiitem(request, item_name=None):
#     """
#     if wikiitem with name = item_name; then show its various content for edititng;
#     else create the item  (including choice for content type markdown/csv/etc). 
    
#     """
#     itemtype = request.path_params['itemtype'] #do not resort to default item type;
#     contenttype = request.path_params['contenttype'] #contenttype path params is mandatory
#     item = Item.create(item_name, itemtype=itemtype, contenttype=contenttype)
#     ret = item.do_modify()
#     return ret 

#jp.CastAsEndpoint(endpoint_wikiItem, "/{rev}/{item_name}", "show_wikiItem")
#jp.CastAsEndpoint(endpoint_wikiItem, "/{item_name}", "show_wikiItem")
app.add_jproute("/{rev}/{item_name}", endpoint_wikiItem, "endpoint_wikiItem")
app.add_jproute("/{item_name}", endpoint_wikiItem, "endpoint_wikiItem")



# def modify_select_itemtype(fqname:CompositeName):
#     """
#     show an href to csv item creating link; but first lets create csv-item-create-page
#     """
#     # oj.Title_("Item not found, create it now")
#     # content_ = oj.Prose_("prose", "item {fqname.fullname} does not exists; Create  it now")
    
#     # oj.Subsection_("heading", "Item not found, create it now?", content_)

    
#     pass


ui_app_trmap_iter = [
    ]

def wp_root(request):
    """
    
    """
    session_id = request.session_id
    session_manager = oj.get_session_manager(session_id)
    appstate = session_manager.appstate

    # This is only a bandaid fix
    # session manager should come from
    # middleware jj
    request.session_manager = session_manager
    with oj.sessionctx(session_manager):
        aspan_ = oj.Span_("aspan", text="dummy text"
                 )
        cgens = [aspan_]
        wp = oj.WebPage_("wp_root",
                         cgens= cgens,
                         WPtype=ojr.WebPage,
                         ui_app_trmap_iter = ui_app_trmap_iter,
                         session_manager = session_manager,
                         template_file='svelte.html',
                         action_module = actions,
                         title="The root page for wiki")()
        wp.session_manager = session_manager
        wp.redirect = "/Home"
    return wp




#jp.CastAsEndpoint(wp_root, "/", "endpoint_root")
#jp.Route("/", wp_root)

app.add_jproute("/", wp_root, "root")
