"""Start the local Flask demo after checking its database connection."""
import socket
import sys
import threading
import time
import urllib.request
import webbrowser

from mysql.connector import Error
from kiem_tra_database import check_database, friendly_error
from app import app

URL = 'http://127.0.0.1:5000/login'


def port_in_use():
    with socket.socket() as sock:
        sock.settimeout(1)
        return sock.connect_ex(('127.0.0.1', 5000)) == 0


def open_when_ready():
    for _ in range(50):
        try:
            with urllib.request.urlopen(URL, timeout=1) as response:
                if response.status == 200:
                    webbrowser.open(URL)
                    return
        except OSError:
            time.sleep(.2)


if __name__ == '__main__':
    try:
        check_database()
    except (Error, KeyError, ValueError, RuntimeError) as err:
        print(friendly_error(err))
        sys.exit(1)
    if port_in_use():
        print('Cong 5000 dang duoc su dung. Neu da mo web, vao ' + URL)
        print('Neu can khoi dong lai, dung cua so web cu bang Ctrl+C truoc.')
        webbrowser.open(URL)
        sys.exit(0)
    print('\nMo web tai: ' + URL)
    print('Giu cua so nay mo trong luc dung web. Nhan Ctrl+C de dung.\n')
    threading.Thread(target=open_when_ready, daemon=True).start()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
