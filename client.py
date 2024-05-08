import socket
import threading
import tkinter as tk
import pyautogui as pg

host = '0.0.0.0' 
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print(f'Waiting on port {port}...')

conn = None


def send_message(message):
    if conn:
        conn.sendall(message.encode())

def on_button_click(event):
    x = event.x
    y = event.y
    send_message(f"pg.moveTo({x*16}, {y*7.45})")
    print(f'Clicked at {x}, {y}.')

def start_tkinter_app():
    root = tk.Tk()
    root.title('Mobile keyboard')

    keyboard_frame = tk.Frame(root)
    keyboard_frame.pack()

    buttons = [
        'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
        'Z', 'X', 'C', 'V', 'B', 'N', 'M'
    ]

    row = 0
    column = 0

    for button_text in buttons:
        button = tk.Button(keyboard_frame, text=button_text, width=2, height=2,
                           command=lambda text=button_text: send_message(text))
        button.grid(row=row, column=column)

        column += 1
        if column > 9:
            column = 0
            row += 1

    special_buttons = ['SPACE', 'ENTER', 'BACKSPACE', 'ESC']
    for special in special_buttons:
        button = tk.Button(keyboard_frame, text=special, width=3, height=2,
                           command=lambda text=special: send_message(text))
        button.grid(row=row, column=column)

        column += 1

    arrow_frame = tk.Frame(root)
    arrow_frame.pack(side=tk.BOTTOM)

    arrow_buttons = ['←', '↓', '↑', '→', 'WIN', 'TAB', '+', '-']
    for arrow in arrow_buttons:
        button = tk.Button(arrow_frame, text=arrow, width=2, height=2,
                           command=lambda text=arrow: send_message(text))
        button.pack(side=tk.LEFT, padx=5, pady=5)
    
    button = tk.Button(root, text="Click me", width=16, height=9)
    button.bind("<Button-1>", on_button_click)
    button.pack()

    def close_connection():
        global conn
        if conn:
            conn.close()
            conn = None
        s.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_connection)
    root.mainloop()



def start_server():
    global conn
    conn, addr = s.accept()
    print(f"Połączono z {addr}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Otrzymano wiadomość: {data}")

    conn.close()


tkinter_thread = threading.Thread(target=start_tkinter_app)
server_thread = threading.Thread(target=start_server)

tkinter_thread.start()
server_thread.start()
