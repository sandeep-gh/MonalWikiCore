"""
describes all components (nav-bar, footer,  etc) that form the pieces of a webpage on the wiki 
"""



import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
  
import justpy as jp
import ofjustpy as oj
import ofjustpy_react as ojr
from tailwind_tags import fw, fc, fz, gray, pd, y, ji, jc, text, mr, sb, ppos, bottom, container, H, screen 

def page_builder(page_key, title, builder_pagebody):

    def view_function(request):
        session_manager = oj.get_session_manager(request.session_id)
        stubStore = session_manager.stubStore
        with oj.sessionctx(session_manager):
            with session_manager.uictx("tlctx") as tlctx:
                _ictx = tlctx
                render_nav_bar(session_manager)
                builder_pagebody(session_manager)
                render_footer(session_manager)
                oj.Container_("tlc", cgens= [tlctx.topper.panel, _ictx.body.panel, tlctx.footer.panel], pcp=[H/screen])
                wp_ = oj.WebPage_(page_key, cgens = [_ictx.tlc], title=title)

                wp = wp_()
        wp.session_manager = session_manager
        return wp
    return view_function


def render_nav_bar(session_manager):
    with session_manager.uictx("topper") as navbarCtx:
        _ctx = navbarCtx
        # a box placed at the  right end
        top_level_nav_ = oj.StackH_("anchors",
                                              cgens = [
                                                  oj.Span_("navtitle", text="Navigation", pcp=[fw.bold]), 
                                                  oj.A_("history", href="#", text="History"),
                                                  oj.A_("index", href="#", text="Index"),
                                                  oj.A_("tags", href="#", text="Tags"),
                                                  oj.A_("user", href="#", text="User"),
                                              ]
                                               )
        
        
        page_trail_  = oj.StackH_("pagetrail",
                                              cgens = [
                                                  oj.Span_("title", text="Page Trail", pcp =[fw.bold])
                                              ]
                                               )

        item_nav_  = oj.StackH_("itemviews",
                                              cgens = [
                                                  oj.Span_("itemview", text="Item views", pcp=[fw.bold]),
                                                  oj.A_("show", href="#", text="modify"),
                                                  oj.A_("history", href="#", text="history"),
                                                  oj.A_("Download", href="#", text="download"),
                                                  oj.A_("delete", href="#", text="delete"),
                                                  oj.A_("subitems", href="#", text="subitems"),
                                                  oj.A_("discussion", href="#", text="discussion"),
                                                  oj.A_("rename", href="#", text="rename"),
                                                  oj.A_("highlight", href="#", text="highlight"),
                                                  oj.A_("meta", href="#", text="Meta"),
                                                  oj.A_("sitemap", href="#", text="Site Map"),
                                                  oj.A_("similar", href="#", text="Similar")
                                              ]
                                               )        
        
        navpanel_ = oj.Halign_(oj.StackV_("navpanel",
                                          cgens = [top_level_nav_, page_trail_, item_nav_]),
                               "end")
        

        #oj.Halign_(oj.Span_("dummySpan", text="i am a dummy span", pcp=[bg/pink/2])),
        cgens = [
            oj.A_("HomeAnchor", pcp=[fc/gray/9, fz.xl, fw.extrabold],
                  href="#", text="PutWikiTitleHere"),

             navpanel_
        ]
        abox_ = oj.StackH_("abox", cgens = cgens, pcp=[pd/y/4,  ji.center, jc.between])
        oj.Nav_("panel", cgens=[abox_])

        
def render_footer(session_manager):
    with session_manager.uictx("footer") as footerbodyCtx:
        _ictx = footerbodyCtx
        oj.Prose_("aboutcontent",
                  text= "MyWiki Powered by MonalWiki Engine", pcp=[fz.sm, text/gray/600, pd/y/2])

        oj.Subsection_("about", "About", _ictx.aboutcontent)

        oj.StackG_("linkouthref", num_cols=3, cgens = [
            oj.A_("pypower", text="Python Power", href="#"), 
            oj.A_("Licensed", text="GPL Licensed", href="#"),
            oj.A_("ShreeLabs", text="Developed by Shree Labs ", href="#")
        ])
        oj.Subsection_("linkout", "", _ictx.linkouthref)
        
        oj.Footer_("footer", cgens=[oj.Divider_("bodyFooterDivider", pcp=[mr/sb/4]),
                                    oj.StackH_("boxcontainer", cgens= [_ictx.about, _ictx.linkout]
                                        )
                                    ]
                   
                   )
        # place it at the bottom
        oj.StackH_("panel", cgens = [_ictx.footer],
                   pcp=[ppos.absolute, bottom/0, container]
                   )

        
