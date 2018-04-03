import sqlite3

def isInitialized () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("SELECT `value` FROM `settings` WHERE `name` = 'initialized'")
    results = cursor.fetchall()

    if len(results) > 0 :
        return True
    cursor.close()

    return False

def deviceInit (device_hash, device_name) :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("INSERT INTO `settings`(`name`, `value`) VALUES ('initialized', 'true')")
    cursor.execute("INSERT INTO `settings`(`name`, `value`) VALUES ('device_hash', '" + device_hash + "')")
    cursor.execute("INSERT INTO `settings`(`name`, `value`) VALUES ('device_name', '" + device_name + "')")
    db.commit()
    cursor.close()

def uninitialize () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("DELETE FROM `settings` WHERE `name` = 'initialized'")
    cursor.execute("DELETE FROM `settings` WHERE `name` = 'device_hash'")
    cursor.execute("DELETE FROM `settings` WHERE `name` = 'device_name'")
    db.commit()
    cursor.close()

def getDeviceHash () :
    db = sqlite3.connect('connectify')
    cursor = db.cursor()
    cursor.execute("SELECT `value` FROM `settings` WHERE `name` = 'device_hash'")
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    return result[0]