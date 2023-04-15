from tkinter import *

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class UserFoodDiaryWindow(ttk.Frame):
    def __init__(self, root, user):
        ttk.Frame.__init__(self, root)
        self.user = user
        
        # main frame
        self.frame_main = Frame(self.master)
        self.frame_main.pack(fill='both', padx=5, pady=5)

        self.create_consumed_products_container()
        self.fill_consumed_products_container()
        self.create_consumed_products_buttons()

    def create_consumed_products_container(self):
        self.frame_products_container = Frame(self.frame_main, relief='groove', bd=2) #relief= 3D effects
        self.frame_products_container.pack(fill='both')
        
        self.canvas_products = Canvas(self.frame_products_container, bd=0, highlightthickness=0, height=300)
        self.scrollbar_products = Scrollbar(self.frame_products_container, orient=VERTICAL,
                                            command=self.canvas_products.yview)

        self.frame_scrollable = Frame(self.canvas_products)
        self.frame_scrollable.bind("<Configure>", lambda e: self.canvas_products.configure(
            scrollregion=self.canvas_products.bbox("all"))
                                   )

        self.canvas_products.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas_products.configure(yscrollcommand=self.scrollbar_products.set)

        self.canvas_products.pack(side="left", fill="both", expand=1)
        self.scrollbar_products.pack(side="right", fill="y")
        
        
    def fill_consumed_products_container(self):
        self.frame_products = Frame(self.frame_scrollable)
        self.frame_products.pack(fill='both', expand=1)

        frame_sizer = Frame(self.frame_products, width=550)
        frame_sizer.pack()

        self.product_selected = tk.IntVar()
        index = 0
        for product in self.user['consumed_products']:
            frame_product = Frame(self.frame_products, relief="ridge", bd=2)
            frame_product.pack(fill="both", padx=2, pady=2)
            frame_product.focus()
            
            # radio button
            frame_radio_button = Frame(frame_product)
            frame_radio_button.grid(row=0, column=0)

            radio_button_product = Radiobutton(frame_radio_button, variable=self.product_selected, value=index)
            radio_button_product.pack(fill="both", padx=5)
            
            # name
            frame_name = Frame(frame_product)
            frame_name.grid(row=0, column=1, padx=2, pady=2)

            label_name = Label(frame_name, text=f"{product['name']}", font=(tkFont.Font(size=10)))
            label_name.pack(padx=5, pady=5)

            # grammage
            frame_grammage = Frame(frame_product)
            frame_grammage.grid(row=0, column=2, padx=2, pady=2)

            label_grammage = Label(frame_grammage, text=f"{product['grammage']} g", font=(tkFont.Font(size=10)))
            label_grammage.pack(padx=5, pady=5)

            # calories
            frame_calories = Frame(frame_product)
            frame_calories.grid(row=0, column=2, padx=2, pady=2)

            frame_center = Frame(frame_calories)
            frame_center.pack()

            label_calories = Label(frame_center, text=f"{product['calories']} kcal", font=(tkFont.Font(size=10)))
            label_calories.pack(padx=5, pady=5)

            index += 1

    def create_consumed_products_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.button_delete_cons_product = tk.Button(self.frame_buttons, text="Usuń produkt z dziennika", font=(tkFont.Font(size=12)))
        self.button_delete_cons_product.pack(side='left', padx=10, pady=10)
        
        self.button_add_product = tk.Button(self.frame_buttons, text="Dodaj produkt", font=(tkFont.Font(size=12)))
        self.button_add_product.pack(side='left', padx=10, pady=10)


    def update_products(self):
        self.frame_products.pack_forget()
        self.frame_products.destroy()
        self.fill_consumed_products_container()


class AddConsumedProductWindow(tk.Toplevel):
    def __init__(self, root, user_products, user_products_ids, default_radio=0, default_grammage=100):
        tk.Toplevel.__init__(self, root)
        self.user_products = user_products
        self.user_products_ids = user_products_ids
        self.default_radio = default_radio
        self.default_grammage = default_grammage
        self.withdraw()

        self.title("Belly Full - dodaj produkt do dzisiejszego dziennika")
        self.resizable(False, False)

        self.frame_main = ttk.Frame(self)
        self.frame_main.pack(padx=5, pady=5)

        self.create_box_search()
        self.create_products_container()
        self.fill_products_container(self.user_products_ids)
        self.create_grammage_entry()
        self.create_buttons()

        center_window(self)
        self.deiconify()


    def create_box_search(self):
        self.label_search_frame = ttk.LabelFrame(self.frame_main, text="Wyszukaj produkt po nazwie")
        self.label_search_frame.pack(fill=tk.BOTH, padx=2, pady=2)

        self.frame_search = ttk.Frame(self.label_search_frame)
        self.frame_search.pack(fill=tk.BOTH, padx=2, pady=2)

        self.entry_search = tk.Entry(self.frame_search, font=(tkFont.Font(size=12)))
        self.entry_search.pack(fill=tk.BOTH, side='left')

        self.button_search = tk.Button(self.frame_search, font=(tkFont.Font(size=12)), text="SZUKAJ")
        self.button_search.pack(fill=tk.BOTH, side='right') #fill?


    def create_products_container(self):
        self.frame_products_container = Frame(self.frame_main, relief="groove", bd=2)
        self.frame_products_container.pack(fill="both")

        self.canvas_products = Canvas(self.frame_products_container, bd=0, highlightthickness=0, height=300)
        self.scrollbar_products = Scrollbar(self.frame_products_container, orient=VERTICAL,
                                            command=self.canvas_products.yview)

        self.frame_scrollable = Frame(self.canvas_products)
        self.frame_scrollable.bind("<Configure>", lambda e: self.canvas_products.configure(
            scrollregion=self.canvas_products.bbox("all"))
                                   )

        self.canvas_products.create_window((0, 0), window=self.frame_scrollable, anchor="nw") #where text is positioned relative to a reference point; northwest 
        self.canvas_products.configure(yscrollcommand=self.scrollbar_products.set)

        self.canvas_products.pack(side="left", fill="both", expand=1)
        self.scrollbar_products.pack(side="right", fill="y")

    def fill_products_container(self, products_ids):
        self.frame_products = Frame(self.frame_scrollable)
        self.frame_products.pack(fill='both', expand=1)

        frame_sizer = Frame(self.frame_products, width=550)
        frame_sizer.pack()

        self.product_selected = tk.IntVar(value=self.default_radio)
        index = 0
        for product_id in products_ids:
            frame_product = Frame(self.frame_products, relief="ridge", bd=2)
            frame_product.pack(fill="both", padx=2, pady=2)
            frame_product.focus()
            
            # radio button
            frame_radio_button = Frame(frame_product)
            frame_radio_button.grid(row=0, column=0)

            radio_button_product = Radiobutton(frame_radio_button, variable=self.product_selected, value=index)
            radio_button_product.pack(fill="both", padx=5)
            
            # name
            frame_name = Frame(frame_product)
            frame_name.grid(row=0, column=1, padx=2, pady=2)

            label_name = Label(frame_name, text=f"{self.user_products[f'{product_id}']['name']}", font=(tkFont.Font(size=12)))
            label_name.pack(padx=5, pady=5)

            # calories
            frame_calories = Frame(frame_product)
            frame_calories.grid(row=0, column=2, padx=2, pady=2)

            frame_center = Frame(frame_calories)
            frame_center.pack()

            label_calories = Label(frame_center, text=f"{self.user_products[f'{product_id}']['calories']} kcal/100g", font=(tkFont.Font(size=12)))
            label_calories.pack(padx=5, pady=5)

            index += 1

    def create_grammage_entry(self):
        self.label_frame = ttk.LabelFrame(self.frame_main, text="Waga produktu w gramach:")
        self.label_frame.pack(fill=tk.BOTH, expand=1, pady=5)

        self.frame_grammage = ttk.Frame(self.label_frame)
        self.frame_grammage.pack(fill=tk.BOTH, padx=5, pady=5)

        self.entry_grammage = tk.Entry(self.frame_grammage, font=(tkFont.Font(size=12)))
        self.entry_grammage.pack(fill=tk.BOTH, padx=5, pady=5)
        self.entry_grammage.insert(0, f'{self.default_grammage}')

    def create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.button_back = tk.Button(self.frame_buttons, text="Powrót", font=(tkFont.Font(size=12)))
        self.button_back.pack(side='left', padx=5, pady=5)

        self.button_add_product = tk.Button(self.frame_buttons, text="Wybierz", font=(tkFont.Font(size=12)))
        self.button_add_product.pack(side='left', pady=5)

    def update_products_list(self, products_ids):
        self.frame_products.pack_forget()
        self.frame_products.destroy()
        self.fill_products_container(products_ids)

def center_window(win):
    width=500
    height=500
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(alignstr)
    
