import time
import sys
import os
import json
import pyperclip
import requests
import threading
import win32gui, win32con
from tendo import singleton
import atexit
import subprocess

import tray
import notifications
from subprocess import call

import api
import loginHelper
import settingsHelper

#hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(hide , win32con.SW_HIDE)

me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

# Run webapp
try :
    pass
    #p = subprocess.Popen("webapp.exe")
except FileNotFoundError as e :
    print("Webapp application wasn't found.")
    raise SystemExit
    sys.exit(0)

# Run tray service
try :
    threading.Thread(target=tray.run).start() # Tray service
    threading.Thread(target=notifications.balloon_tip, args=("Connectify", "Local server is running.")).start() # Startup popup
except Exception as e :
    print(e)

sys.path.append(os.path.abspath("SO_site-packages"))

# Copies detector
def copiesDetector () :
    recent_value = pyperclip.paste().strip()
    while True:
        if loginHelper.isLogged() :
            tmp_value = pyperclip.paste().strip()
            if tmp_value != recent_value and tmp_value != "" and recent_value != "":
                recent_value = tmp_value.strip()
                api.post("http://connectify.rf.gd/api/copy.php", { 'login_hash': loginHelper.get_login_hash(), 'copy': recent_value, 'device_hash' : settingsHelper.getDeviceHash() })
        time.sleep(0.5)
threading.Thread(target=copiesDetector).start()

# Initialize device
if not settingsHelper.isInitialized() :
    print("Initializing...")
    import platform

    device_name = platform.node()
    ip = '127.0.0.1'

    device_hash_resp = api.post('http://connectify.rf.gd/api/device_hash.php', {
        'login_hash' : loginHelper.get_login_hash(),
        'name' : device_name,
        'ip' : ip
    })

    device_hash = json.loads(device_hash_resp)['hash']
    settingsHelper.deviceInit(device_hash, device_name)

def exit_handler() :
    pass
    #p.terminate()

atexit.register(exit_handler)