import requests
import json
from tendo import singleton
import win32gui, win32con

import loginHelper
import api

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

#hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(hide , win32con.SW_HIDE)

#me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD = True)

# Routes
@app.route("/")
def index():
    if loginHelper.isLogged() :
        total_copies = json.loads(api.post('http://connectify.rf.gd/api/user_stats.php', { 'login_hash' : loginHelper.get_login_hash(), 'stat' : 'num_total_copies' }))['result']
        total_devices = json.loads(api.post('http://connectify.rf.gd/api/user_stats.php', { 'login_hash' : loginHelper.get_login_hash(), 'stat' : 'num_devices' }))['result']
        return render_template('index.html', name = "index", total_copies = total_copies, total_devices = total_devices)
    else :
        return render_template('login.html', name = "login")

@app.route("/logout/")
def logout () :
    loginHelper.logout()
    return redirect("/")

@app.route("/login_submittion", methods = [ 'POST' ])
def login_submittion () :
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        api_login_response = api.post("http://connectify.rf.gd/api/login.php", { 'email' : email, 'password' : password })
        if (api_login_response) :
            json_parsed = json.loads(api_login_response)
            login_error = ""
            if json_parsed['success'] :
                loginHelper.login(json_parsed['login_hash'])
                return redirect("/")
            else :
                if json_parsed['empty_fields'] :
                    login_error = "empty_fields"
                elif not json_parsed['email_exists'] :
                    login_error = "email_doesnt_exist"
                else :
                    login_error = "wrong_password"

                return redirect("/?loginerror=" + login_error)

    return "not logged"

@app.route("/copies/")
def copies () :
    if loginHelper.isLogged ():
        copies = json.loads(api.post('http://connectify.rf.gd/api/get_copies.php', { 'login_hash' : loginHelper.get_login_hash() }))['copies']
        return render_template('copies.html', name = "copies", copies = copies)
    else :
        return redirect('/')

@app.route("/groups/")
def groups () :
    if loginHelper.isLogged ():
        copies = json.loads(api.post('http://connectify.rf.gd/api/get_copies.php', { 'login_hash' : loginHelper.get_login_hash() }))['copies']
        return render_template('copies.html', name = "groups", copies = copies)
    else :
        return redirect('/')

@app.route("/settings/", defaults = { 'tab' : 'general' })
@app.route("/settings/<tab>/")
def settings (tab) :
    if loginHelper.isLogged ():
        return render_template('settings.html', name = "settings", tab = tab)
    else :
        return redirect('/')

@app.route("/copy/<id>/delete/")
def delete_copy (id) :
    response = api.post('http://connectify.rf.gd/api/copy_options.php', { 'login_hash' : loginHelper.get_login_hash(), 'copy_id' : id, 'action' : 'delete'})
    return response


# Template filters
@app.template_filter('make_caps')
def caps(text):
    """Convert a string to all caps."""
    return text.upper()

# # # # # # # # # # # # # # #
if __name__ == "__main__":
   app.run()

def run(self):
    #self.init_routes()
    self.socketio.run(self.app, host='127.0.0.1', port=4444)