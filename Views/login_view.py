from tkinter import *

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class LoginWindow(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.withdraw()

        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Logowanie')

        self.resizable(width=False, height=False)

        self.frame_login = ttk.Frame(self)
        self.frame_login.pack()

        center_window(self)

        self.create_components(self.frame_login)

        self.deiconify()

    def create_components(self, frame):
        self.label_title = tk.Label(frame, font=(tkFont.Font(size=25)), text="belly full")
        self.label_title.pack(fill=tk.BOTH, padx=10, pady=40)

        self.entry_login = tk.Entry(frame, font=(tkFont.Font(size=12)), name="login", justify="center")
        self.entry_login.pack(fill=tk.BOTH, padx=20, pady=20)

        self.entry_password=tk.Entry(frame, font=(tkFont.Font(size=12)), show="*",  name="hasło", justify="center")
        self.entry_password.pack(fill=tk.BOTH, padx=20, pady=20)

        self.button_register=tk.Button(frame, font=(tkFont.Font(size=12)), text="Zarejestruj się")
        self.button_register.pack(side='left')

        self.button_login=tk.Button(frame, font=(tkFont.Font(size=12)), text="Zaloguj się")
        self.button_login.pack(side='right')


def center_window(win):
    width=500
    height=500
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(alignstr)