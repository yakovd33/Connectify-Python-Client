import sqlite3

def isLogged () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("SELECT `value` FROM `settings` WHERE `name` = 'login_hash'")
    results = cursor.fetchall()

    if len(results) > 0 :
        return True
    cursor.close()

    return False

def login (login_hash) :
    if not isLogged() :
        db = sqlite3.connect('connectify')
        cursor = db.cursor()
        cursor.execute("INSERT INTO `settings`(`name`, `value`) VALUES ('login_hash', '" + login_hash + "')")
        db.commit()
        cursor.close()

def logout () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("DELETE FROM `settings` WHERE `name` = 'login_hash'")
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

def createAll () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE settings(id INTEGER PRIMARY KEY, name TEXT UNIQUE, value TEXT)")
    cursor.close()
    db.commit()
