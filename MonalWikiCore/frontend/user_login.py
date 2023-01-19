import justpy as jp
import ofjustpy as oj
import ofjustpy_react as ojr
from . import actions
from addict import Dict
from tailwind_tags import H,full, bold, bsw, bdr, bold, fz, fw, W, mr, st



ui_app_trmap_iter = [
    ]

app = jp.build_app()

def wp_register_user(request):
    session_id = request.session_id
    session_manager = oj.get_session_manager(session_id)
    appstate = session_manager.appstate

    # This is only a bandaid fix
    # session manager should come from
    # middleware
    request.session_manager = session_manager
    with oj.sessionctx(session_manager):
        aspan_ = oj.Span_("aspan", text="this should turn into a login page"
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
    return wp    
    
app.add_jproute("/register", wp_register_user)
