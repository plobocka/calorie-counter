from datetime import datetime
from tkinter import messagebox
from Views.login_view import LoginWindow
from Views.register_view import RegisterWindow
from Controllers.user_controller import UserController
from Models.database_model import *

class AccountController:
    def __init__(self, master, database_model):
        self.master = master
        self.database_model = database_model

        # Login view
        self.login_view = LoginWindow(master)
        self.login_view.button_register.config(command=self.open_register_window)
        self.login_view.button_login.config(command=self.login)

        # Register
        self.register_view = None

        # User Controller
        self.user_controller = None

    # REGISTER
    def open_register_window(self):
        if self.register_view is None:
            self.register_view = RegisterWindow(self.master)
            self.register_view.protocol('WM_DELETE_WINDOW', self.close_register_window)

            self.register_view.button_register.config(command=self.register_new_user)
            center_window(self.register_view)
        else:
            self.close_register_window()

    def close_register_window(self):
        if self.register_view is not None:
            self.register_view.destroy()
            self.register_view = None

    def register_new_user(self):
        entry_values = self.get_register_entry_values()

        entry_values['weight'] = round(float(entry_values['weight']), 1)
        entry_values['calories'] = int(entry_values['calories'])

        self.database_model.insert_user(entry_values['login'], entry_values['password'], entry_values['email'],
                                        entry_values['calories'])
        user_id = self.database_model.get_user_by_login(entry_values['login'])['user_id']

        current_date = get_current_date()

        self.database_model.insert_weight(user_id, entry_values['weight'], current_date)
        
        self.close_register_window()
       
       
    def get_register_entry_values(self):
        entry_values = {
            'login': self.register_view.entry_login.get(),
            'password': self.register_view.entry_password.get(),
            'email': self.register_view.entry_email.get(),
            'weight': self.register_view.entry_weight.get(),
            'calories': self.register_view.entry_calories.get()
        }
        return entry_values


    # LOGIN
    def login(self):
        login, password = self.get_login_entry_values()
        user = self.database_model.get_user_by_login_and_password(login, password)
        if user is not None:
            self.open_user_window(user)
        else:
            messagebox.showerror("Błąd logowania", "Błędny login lub hasło")
        
    def get_login_entry_values(self):
        # Get login and password from login entries
        login = self.login_view.entry_login.get()
        password = self.login_view.entry_password.get()

        return login, password

    def open_user_window(self, user):
        # Close register window
        if self.register_view is not None:
            self.close_register_window()

        # Hide login window
        self.login_view.withdraw()

        # Create UserController with UserView
        self.user_controller = UserController(self.master, self.database_model, user)
        #self.user_controller.user_view.btn_logout.config(command=self.logout)
        center_window(self.user_controller.user_view)


    def logout(self):
        # Clear UserView and UserController then show login window.
        if self.user_controller.user_view:
            self.user_controller.user_view.destroy()

        if self.user_controller is not None:
            self.user_controller = None

        self.login_view.deiconify()


def center_window(win):
    width=500
    height=500
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(alignstr)

def get_current_date():
        current_date = datetime.now()
        current_date = current_date.strftime("%Y/%m/%d")
        return current_date
