"""
The index shows list of all the items in the wiki (in pagination manner) 
and option to create new item
"""
from MonalWikiCore.frontend.wp_template_components import page_builder, render_nav_bar, render_footer
import justpy as jp
from addict import Dict
import ofjustpy_extn as ojx
import ofjustpy as oj

from starlette.testclient import TestClient

from tailwind_tags import mr, sb

def wp_index_bodygen(session_manager):
    
    with session_manager.uictx("body") as bodyCtx:
        _ictx=bodyCtx
        # Put title right in center top 
        oj.Title_("pagetitle", "Global Index")
        
        # A horizontal marker line 
        oj.Divider_("bodyFooterDivider", pcp=[mr/sb/4])
        def on_actionbtn_click(dbref, msg):
            pass

        #Select All  Download  Delete  Destroy  Filter  Namespace  New Item
         
        actionbtns_ = oj.Halign_(
            oj.StackH_("actionbtns", cgens  = [
            oj.Button_("selectall", text="Select all").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("download", text="Download").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("delete", text="Delete").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("destory", text="Destroy").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("filter", text="Filter").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("namespace", text="Namespace").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("newitem", text="New Item").event_handle(oj.click, on_actionbtn_click),
            ]
                       ),
            "start")

        indexbtns_ = oj.Halign_(
            oj.StackH_("indexbtns", cgens  = [
            oj.Button_("showall", text="Show all all").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("letterA", text="A").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("letterB", text="B").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("letterC", text="C").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("letterD", text="D").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("letterE", text="E").event_handle(oj.click, on_actionbtn_click),
            oj.Button_("letterF", text="F").event_handle(oj.click, on_actionbtn_click),
            ]
                       ),
            )

        #A table without header 
        #TODO: build a paginated table after revising justpy
        values = [["Home", "7",  "1", 	"169.254.84.26", 	"2022-08-27 01:59:10z"],
                  ["alphas",	"11", 	"1",	"169.254.84.26", 	"2022-08-27 01:46:49z"],
                  ]
        
        ojx.Table_("itemtbl", values, add_cbox=True)
        oj.StackV_("panel",
                   cgens = [_ictx.pagetitle, _ictx.bodyFooterDivider, actionbtns_, indexbtns_, _ictx.itemtbl])

wp_index = page_builder("wp_index", "An index page",  wp_index_bodygen)

jp.CastAsEndpoint(wp_index, "/", "wp_index")
app = jp.app
# client = TestClient(app)

# response = client.get('/') 

