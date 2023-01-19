
# create new user

import ofjustpy as oj
import justpy as jp
from starlette.testclient import TestClient
from starlette.responses import HTMLResponse

login_page_html = """
<html>
<div class="form-style">
    <input class="input-field-style" type="text" id="username" name="username" placeholder="Username"> <br/>
    <input class="input-field-style" type="password" id="password" name="password" placeholder="Password"> <br/>
    <input class="input-field-style" type="password" id="reenterpassword" name="reenterpassword" placeholder="Enter Password again"> <br/>
    <input type="button" value="Create New Account" onclick="create_account()"/>
</div>

<script type="text/javascript">
  function create_account() {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var reenterpassword = document.getElementById('reenterpassword').value;
var xhr = new XMLHttpRequest();
xhr.open("GET", "/login", true, "san", "que");
xhr.setRequestHeader("Authorization", "Basic "+btoa(username+':'+password));
xhr.withCredentials = true;
xhr.send();

  }
</script>
</html>
"""

#show form on frontend to
#the get credentials and post them to server-side-logic
async def get_loginCredentials(request):
    response = HTMLResponse(login_page_html)
    return response

def launcher(request):
    session_id = "abc"
    session_manager = oj.get_session_manager(session_id)
    with oj.sessionctx(session_manager):
        with session_manager.uictx("register_user") as _ictx:
            oj.Container_("tlc", cgens=[])
            wp_ = oj.WebPage_("basicpage", cgens = [_ictx.tlc], title="register new user")
            wp = wp_()
            wp.session_manager = session_manager
    return wp

# routes = [
#     Route('/', get_loginCredentials),
#     Route("/login", verify_loginCredentials, methods=['POST', 'GET']),
#     Route("/loggedinhomepage", recieve_loggedUser)
# ]

jp.CastAsEndpoint(get_loginCredentials, "/getLoginCredentials", "getLoginCredentials")
#jp.CastAsEndpoint(launcher, "/", "basicPage")
app = jp.app            

# client = TestClient(app)
# response = client.get('/getLoginCredentials')

