import socket
import pyautogui as pg

host = 'phone ip'
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    data = s.recv(1024).decode()
    print(data)
    print('pg' in data)
    if not data:
        break
    if data not in ['←', '↓', '↑', '→', 'ESC'] or 'pg' not in data:
        pg.press(data)
        if 'pg' in data:
            eval(data)
    else:
        if data == '↑':
            pg.press('up')
        if data == '↓':
            pg.press('down')
        if data == '←':
            pg.press('left')
        if data == '→':
            pg.press('right')
        if data == 'ESC':
            pg.hotkey('alt', 'f4')
        
s.close()
