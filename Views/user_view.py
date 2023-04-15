from tkinter import *

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from Views.user_products_view import UserProductsWindow
from Views.user_food_diary_view import UserFoodDiaryWindow

class UserWindow(tk.Toplevel):
    def __init__(self, root, user):
        tk.Toplevel.__init__(self, root)
        self.user = user
        self.withdraw()
        

        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Belly full')

        self.resizable(width=False, height=False)

        # main frame
        self.frame_user = ttk.Frame(self)
        self.frame_user.pack()
        # top frame
        self.frame_user_top = ttk.Frame(self.frame_user)
        self.frame_user_top.pack()
        #top frame first row 
        self.frame_user_first_row = ttk.Frame(self.frame_user_top)
        self.frame_user_first_row.pack(expand=True, fill=tk.BOTH, pady=5)
        # top frame second row
        self.frame_user_second_row = ttk.Frame(self.frame_user_top)
        self.frame_user_second_row.pack(expand=True, fill=tk.BOTH, pady=5)
        # bottom frame
        self.frame_user_bottom = ttk.Frame(self.frame_user)
        self.frame_user_bottom.pack(fill=tk.BOTH, pady=10)

        self.create_components()
        self.create_tabs()

        center_window(self)
        self.deiconify()

    def create_components(self):
        # 1st row
        self.button_next_date=tk.Button(self.frame_user_first_row, font=(tkFont.Font(size=12)), text=">")
        self.button_next_date.pack(side='right')

        self.button_set_date=tk.Button(self.frame_user_first_row, font=(tkFont.Font(size=12)), text=f"{self.user['current_date']}")
        self.button_set_date.pack(side='right')

        self.button_prev_date=tk.Button(self.frame_user_first_row, font=(tkFont.Font(size=12)), text="<")
        self.button_prev_date.pack(side='right')

        self.button_date_today=tk.Button(self.frame_user_first_row, font=(tkFont.Font(size=12)), text="DZIŚ")
        self.button_date_today.pack(side='right')

        self.label_weight_at_date = tk.Label(self.frame_user_first_row, font=(tkFont.Font(size=10)), text=f"Waga: {self.user['current_date_weight']['weight_value']} kg")
        self.label_weight_at_date.pack(side='left', padx=5, pady=5)
        
        self.button_set_weight=tk.Button(self.frame_user_first_row, font=(tkFont.Font(size=8)), text="Zmień wagę")
        self.button_set_weight.pack(side='left')

        # 2nd row
        self.label_calories_left = tk.Label(self.frame_user_second_row, font=(tkFont.Font(size=10)), text=f"Pozostało: {self.user['calories_left']} kcal")
        self.label_calories_left.pack(side='right', padx=5, pady=5)

        self.label_calories_consumed = tk.Label(self.frame_user_second_row, font=(tkFont.Font(size=10)), text=f"Spożyto: {self.user['calories_consumed']} kcal")
        self.label_calories_consumed.pack(side='left', padx=5, pady=5)

        self.button_set_calories_intake=tk.Button(self.frame_user_second_row, font=(tkFont.Font(size=8)), text="Zmień zapotrzebowanie")
        self.button_set_calories_intake.pack(side='right', padx=10)
  
        
    def update_user_status_view(self):
        self.button_set_date.configure(text=f"{self.user['current_date']}")
        self.label_weight_at_date.configure(text=f"Waga: {self.user['current_date_weight']['weight_value']} kg")
        self.label_calories_consumed.configure(text=f"Spożyto: {self.user['calories_consumed']} kcal")
        self.label_calories_left.configure(text=f"Pozostało: {self.user['calories_left']} kcal")

    def create_tabs(self):
        self.tabs = ttk.Notebook(self.frame_user_bottom)
        self.tab_products = ttk.Frame(self.tabs)
        self.tab_food_diary = ttk.Frame(self.tabs)
        
        self.tabs.add(self.tab_food_diary, text="Spożyte produkty")
        self.tabs.add(self.tab_products, text="Wszystkie produkty")
        
        self.tabs.pack()
        
        self.user_food_diary_view = UserFoodDiaryWindow(self.tab_food_diary, self.user)
        self.user_food_diary_view.pack()
        self.user_products_view = UserProductsWindow(self.tab_products, self.user)
        self.user_products_view.pack()

    def update_weight(self):
        self.label_weight_at_date.configure(text=f"Waga: {self.user['current_date_weight']['weight_value']} kg")

        
class SetWeightWindow(tk.Toplevel):
    def __init__(self, root, current_weight):
        tk.Toplevel.__init__(self, root)
        self.current_weight = current_weight
        self.withdraw()

        self.title('Belly Full zmiana wagi')
        self.resizable(False, False)

        self.frame_set_weight = ttk.Frame(self)
        self.frame_set_weight.pack(fill=tk.BOTH, padx=10, pady=10)

        self.create_entries()
        self.create_buttons()

        center_window(self)
        self.deiconify()

    def create_entries(self):
        self.label_frame = ttk.LabelFrame(self.frame_set_weight, text="Podaj wagę:")
        self.label_frame.pack(expand=0, pady=40)

        self.frame_weight = ttk.Frame(self.label_frame)
        self.frame_weight.pack(fill=tk.BOTH, padx=10, pady=10)

        self.entry_weight = tk.Entry(self.frame_weight, font=(tkFont.Font(size=10)))
        self.entry_weight.pack(padx=10, pady=10)
        self.entry_weight.insert(0, f'{self.current_weight}')

    def create_buttons(self):
        self.button_set_weight = tk.Button(self.frame_set_weight, text="Aktualizuj", width=20, font=(tkFont.Font(size=12)))
        self.button_set_weight.pack(side='right', padx=20, pady=20)

class SetCaloriesIntakeWindow(tk.Toplevel):
    def __init__(self, root, current_calories_intake):
        tk.Toplevel.__init__(self, root)
        self.current_calories_intake = current_calories_intake
        self.withdraw()

        self.title('Belly Full zmiana zapotrzebowania kalorycznego')
        self.resizable(False, False)

        self.frame_set_calories_intake = ttk.Frame(self)
        self.frame_set_calories_intake.pack(fill=tk.BOTH, padx=10, pady=10)

        self.create_entries()
        self.create_buttons()

        center_window(self)
        self.deiconify()

    def create_entries(self):
        self.label_frame = ttk.LabelFrame(self.frame_set_calories_intake, text="Podaj zapotrzebowanie kaloryczne:")
        self.label_frame.pack(expand=0, pady=40)

        self.frame_calories = ttk.Frame(self.label_frame)
        self.frame_calories.pack(padx=10, pady=10)

        self.entry_calories_intake = tk.Entry(self.frame_calories, font=(tkFont.Font(size=10)))
        self.entry_calories_intake.pack(padx=10, pady=10)
        self.entry_calories_intake.insert(0, f'{self.current_calories_intake}')

    def create_buttons(self):
        self.button_set_calories_intake = tk.Button(self.frame_set_calories_intake, text="Aktualizuj", width=20, font=(tkFont.Font(size=12)))
        self.button_set_calories_intake.pack(side='right', padx=20, pady=20)

def center_window(win):
    width=500
    height=500
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(alignstr)