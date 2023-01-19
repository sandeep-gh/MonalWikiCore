import justpy as jp
import ofjustpy as oj
import ofjustpy_react as ojr
from . import actions
from addict import Dict
from tailwind_tags import H,full, bold, bsw, bdr, bold, fz, fw, W, mr, st
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware



SECRET_KEY="Pls use a good professional secret key"
csrf_cookie_name = "csrftoken"
csrf_secret='shhshh' #should this be signed by cookie signer??
ui_app_trmap_iter = [
    ]


app = jp.build_app()

def on_input_change(dbref, msg):
    #traceback.print_stack(file=sys.stdout)
    print (msg)
    pass

def on_submit_click(dbref, msg):
    #print (msg)

                #stop_validation = self._run_validation_chain(data, chain)
    # print(dbref.spathMap)
    # for cpath, cbref in dbref.spathMap.items():
    print ("form on_submit called")
    #     print (cpath, cbref)
    pass
    
def wp_register_user(request):
    session_id = request.session_id
    session_manager = oj.get_session_manager(session_id)
    appstate = session_manager.appstate

    # This is only a bandaid fix
    # session manager should come from
    # middleware
    request.session_manager = session_manager
    with oj.sessionctx(session_manager):
        btn_ = oj.Button_("mybtn", text="Submit", type="submit")
        
        username_input_ = oj.LabeledInput_("username",
                                           "Username",
                                           "username",

                                           data_validators = [oj.validator.InputRequired()
                                                              ]
                                           ).event_handle(oj.change,
                                                          on_input_change
                                                          )
        email_input_ = oj.LabeledInput_("email",
                                        "Email",
                                        "Email",
                                        data_validators = [oj.validator.Email()
                                                           ]
                                        ).event_handle(oj.change,
                                                       on_input_change
                                                       )
        password_ = oj.LabeledInput_("password",
                                     "password",
                                     "Enter Password",
                                     data_validators=[oj.validator.InputRequired()
                                                      ]
                                     ).event_handle(oj.change,
                                                    on_input_change
                                                    )

        confirm_password_ = oj.LabeledInput_("confirm_password",
                                             "confirm_password",
                                             "Confirm Password",
                                             data_validators=[oj.validator.InputRequired(),
                                                              oj.validator.EqualTo(password_.spath)
                                                              ]
                                             ).event_handle(oj.change,
                                                            on_input_change
                                                            )

        all_inputs_ = oj.StackV_("all_inputs",
                                 cgens = [username_input_,
                                          email_input_,
                                          password_,
                                          confirm_password_
                                          ]
                                 )
        target_ = oj.Form_("myform",
                           all_inputs_
                           , btn_,
                           stubStore = session_manager.stubStore
                           ).event_handle(oj.submit,
                                        on_submit_click
                                          )

        
        wp = oj.WebPage_("wp_root",
                         cgens= [target_],
                         WPtype=ojr.WebPage,
                         ui_app_trmap_iter = ui_app_trmap_iter,
                         session_manager = session_manager,
                         template_file='svelte.html',
                         action_module = actions,
                         display_url = "register_user", 
                         title="The root page for wiki")()
        wp.session_manager = session_manager
        wp.use_websockets = False 
        #request.session[csrf_cookie_name] =  csrf_secret
        # using justpy cookie managment
        wp.cookies[csrf_cookie_name] =  csrf_secret
    return wp    
    
app.add_jproute("/register_user", wp_register_user)

