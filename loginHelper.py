import sqlite3
import json
import settingsHelper
import api

def isLogged () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("SELECT `value` FROM `settings` WHERE `name` = 'login_hash'")
    results = cursor.fetchall()

    if len(results) > 0 :
        return True
    cursor.close()

    return False

def login (login_hash, user_id) :
    if not isLogged() :
        db = sqlite3.connect('connectify')
        cursor = db.cursor()
        cursor.execute("INSERT INTO `settings`(`name`, `value`) VALUES ('login_hash', '" + login_hash + "')")
        cursor.execute("INSERT INTO `settings`(`name`, `value`) VALUES ('user_id', '" + user_id + "')")
        db.commit()
        cursor.close()

        # Initialize device
        if not settingsHelper.isInitialized() :
            print("Initializing...")
            import platform

            device_name = platform.node()
            ip = '127.0.0.1'

            device_hash_resp = api.post('http://connectify.rf.gd/api/device_hash.php', {
                'login_hash' : get_login_hash(),
                'name' : device_name,
                'ip' : ip
            })

            device_hash = json.loads(device_hash_resp)['hash']
            settingsHelper.deviceInit(device_hash, device_name)

def logout () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("DELETE FROM `settings` WHERE `name` = 'login_hash'")
    cursor.execute("DELETE FROM `settings` WHERE `name` = 'user_id'")
    db.commit()
    cursor.close()

def get_login_hash () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("SELECT `value` FROM `settings` WHERE `name` = 'login_hash'")
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    return result[0]

def get_login_user_id () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("SELECT `value` FROM `settings` WHERE `name` = 'user_id'")
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    return result[0]

def createAll () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE settings(id INTEGER PRIMARY KEY, name TEXT UNIQUE, value TEXT)")
    cursor.close()
    db.commit()
