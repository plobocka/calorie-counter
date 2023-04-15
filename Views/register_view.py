from logging.handlers import RotatingFileHandler
from tkinter import *

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class RegisterWindow(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.withdraw()

        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Rejestracja')

        self.resizable(width=False, height=False)

        self.frame_register = ttk.Frame(self)
        self.frame_register.pack()

        center_window(self)

        self.create_components(self.frame_register)

        self.deiconify()

    def create_components(self, frame):
        self.label_title = tk.Label(frame, font=(tkFont.Font(size=25)), text="belly full")
        self.label_title.pack(fill=tk.BOTH, padx=10, pady=30)

        self.label_login = tk.Label(frame, font=(tkFont.Font(size=12)), text="login")
        self.label_login.pack(fill=tk.BOTH)
        self.entry_login = tk.Entry(frame, font=(tkFont.Font(size=12)), name="login", justify="center")
        self.entry_login.pack(fill=tk.BOTH, padx=5, pady=5)

        self.label_password = tk.Label(frame, font=(tkFont.Font(size=12)), text="hasło")
        self.label_password.pack(fill=tk.BOTH)
        self.entry_password=tk.Entry(frame, font=(tkFont.Font(size=12)), show="*",  name="hasło", justify="center")
        self.entry_password.pack(fill=tk.BOTH, padx=5, pady=5)


        self.label_email = tk.Label(frame, font=(tkFont.Font(size=12)), text="email")
        self.label_email.pack(fill=tk.BOTH)
        self.entry_email = tk.Entry(frame, font=(tkFont.Font(size=12)), name="email", justify="center")
        self.entry_email.pack(fill=tk.BOTH, padx=5, pady=5)

        self.label_weight = tk.Label(frame, font=(tkFont.Font(size=12)), text="waga")
        self.label_weight.pack(fill=tk.BOTH)
        self.entry_weight = tk.Entry(frame, font=(tkFont.Font(size=12)), name="waga", justify="center")
        self.entry_weight.pack(fill=tk.BOTH, padx=5, pady=5)

        self.label_calories = tk.Label(frame, font=(tkFont.Font(size=12)), text="zapotrzebowanie kaloryczne")
        self.label_calories.pack(fill=tk.BOTH)
        self.entry_calories = tk.Entry(frame, font=(tkFont.Font(size=12)), name="zapotrzebowanie kaloryczne", justify="center")
        self.entry_calories.pack(fill=tk.BOTH, padx=5, pady=5)

        self.button_register=tk.Button(frame, font=(tkFont.Font(size=12)), text="Zarejestruj się")
        self.button_register.pack()


def center_window(win):
    width=500
    height=500
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(alignstr)