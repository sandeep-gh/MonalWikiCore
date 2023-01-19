from MonalWikiCore.frontend.register_user import wp_register_user, app
from addict import Dict


# from starlette.testclient import TestClient
# # client = TestClient(app)
# # response = client.get('/')
# request = Dict()
# request.session_id = "abc"
# wp = wp_register_user(request)
# _sm = wp.session_manager
# _ss = _sm.stubStore
# #print(_ss.labeldinput_input)
# _ss.username_input.target.value = "dssdf"
# _ss.email_input.target.value = "spoofemail@monallabsy.in"
# _ss.password_input.target.value = "mypass1"
# _ss.confirm_password_input.target.value = "mypass1"
# #print(_ss.keys())
# msg = None
# _ss.myform.target.on_submit(msg)
app.add_jproute("/register", wp_register_user)
