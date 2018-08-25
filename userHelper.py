import sqlite3
import json
import loginHelper
import api

def get_user_details () :
    if loginHelper.isLogged () :
        return json.loads(api.post('http://localhost:8080/connectify-server/api/get_user_details.php', { 'login_hash' : loginHelper.get_login_hash(), 'info' : 'all', 'req_user_id' : loginHelper.get_login_user_id() }))['details']
    return None