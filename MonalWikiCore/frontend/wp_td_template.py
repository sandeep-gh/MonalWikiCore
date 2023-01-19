import justpy as jp
from addict import Dict
import ofjustpy as oj
from starlette.testclient import TestClient
from MonalWikiCore.frontend.wp_template_components import page_builder, render_nav_bar, render_footer


def builder_pagebody(session_manager):
    with session_manager.uictx("body") as bodyCtx:
        oj.Span_("panel",  text="i am a span:dryrun")

wp_td = page_builder("wp_td", "a test drive",  builder_pagebody)

jp.CastAsEndpoint(wp_td, "/", "test_drive")
app = jp.app
#client = TestClient(app)

#response = client.get('/') 
