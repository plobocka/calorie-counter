from tkinter import *

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class UserProductsWindow(ttk.Frame):
    def __init__(self, root, user):
        ttk.Frame.__init__(self, root)
        self.user = user
        
        # main frame
        self.frame_main = Frame(self.master)
        self.frame_main.pack(fill='both', padx=5, pady=5)

        self.create_search_entry()
        self.create_products_container()
        self.fill_products_container()
        self.create_products_buttons()

    def create_search_entry(self):
        self.label_search_frame = ttk.LabelFrame(self.frame_main, text="Wyszukaj produkt po nazwie")
        self.label_search_frame.pack(fill=tk.BOTH, padx=2, pady=2)

        self.frame_search = ttk.Frame(self.label_search_frame)
        self.frame_search.pack(fill=tk.BOTH, padx=2, pady=2)

        self.entry_search = tk.Entry(self.frame_search, font=(tkFont.Font(size=12)))
        self.entry_search.pack(fill=tk.BOTH, side='left')

        self.button_search = tk.Button(self.frame_search, font=(tkFont.Font(size=12)), text="SZUKAJ")
        self.button_search.pack(fill=tk.BOTH, side='right')

    def create_products_container(self):
        self.frame_products_container = Frame(self.frame_main, relief='groove', bd=2) #relief= 3D effects
        self.frame_products_container.pack(fill='both')
        
        self.canvas_products = Canvas(self.frame_products_container, bd=0, highlightthickness=0, height=250)
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
        
        
    def fill_products_container(self):
        self.frame_products = Frame(self.frame_scrollable)
        self.frame_products.pack(fill='both', expand=1)

        frame_sizer = Frame(self.frame_products, width=550)
        frame_sizer.pack()

        self.product_selected = tk.IntVar()
        index = 0
        for prod_id in self.user['selected_products_ids']:
            product = self.user['products'][f'{prod_id}']
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

            label_name = Label(frame_name, text=f"{product['name']}", font=(tkFont.Font(size=9)))
            label_name.pack(padx=5, pady=5)

            # calories
            frame_calories = Frame(frame_product)
            frame_calories.grid(row=0, column=2, padx=2, pady=2)

            frame_center = Frame(frame_calories)
            frame_center.pack()

            label_calories = Label(frame_center, text=f"{product['calories']} kcal/100g", font=(tkFont.Font(size=10)))
            label_calories.pack(padx=5, pady=5)

            index += 1

    def create_products_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.button_delete_product = tk.Button(self.frame_buttons, text="Usuń produkt", font=(tkFont.Font(size=12)))
        self.button_delete_product.pack(side='left', padx=10, pady=10)
        self.button_add_product = tk.Button(self.frame_buttons, text="Dodaj produkt", font=(tkFont.Font(size=12)))
        self.button_add_product.pack(side='left', padx=10, pady=10)


    def update_products(self):
        self.frame_products.destroy()
        self.fill_products_container()


class AddProductWindow(tk.Toplevel):
    def __init__(self, root, default_name="Nazwa produktu", default_calories=100):
        tk.Toplevel.__init__(self, root)
        self.default_name = default_name
        self.default_calories = default_calories
        self.withdraw()

        self.title('Belly Full - dodaj nowy produkt do bazy')
        self.resizable(False, False)

        self.frame_main = ttk.Frame(self)
        self.frame_main.pack(padx=10, pady=10)

        self.create_entries()
        self.create_buttons()

        center_window(self)
        self.deiconify()


    def create_entries(self):
        # Name
        label_frame = LabelFrame(self.frame_main, text="Nazwa nowego produktu:", font=(tkFont.Font(size=12)))
        label_frame.pack(fill=tk.BOTH, expand=0,  pady=30)

        frame_name = ttk.Frame(label_frame)
        frame_name.pack(fill=tk.BOTH, padx=10, pady=10)

        self.entry_name = tk.Entry(frame_name, font=(tkFont.Font(size=12)))
        self.entry_name.pack(fill=tk.BOTH, padx=10, pady=10)
        self.entry_name.insert(0, f'{self.default_name}')

        # Calories
        label_frame = LabelFrame(self.frame_main, text="Liczba kalorii na 100 gram:", font=(tkFont.Font(size=12)))
        label_frame.pack(fill=tk.BOTH, expand=0, pady=10)

        frame_calories = ttk.Frame(label_frame)
        frame_calories.pack(fill=tk.BOTH, padx=10, pady=10)

        self.entry_calories = tk.Entry(frame_calories, font=(tkFont.Font(size=12)))
        self.entry_calories.pack(fill=tk.BOTH, padx=10, pady=10)
        self.entry_calories.insert(0, f'{self.default_calories}')



    def create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()
    
        self.button_add_product = tk.Button(self.frame_buttons, text="Dodaj produkt", font=(tkFont.Font(size=12)))
        self.button_add_product.pack(side='right', padx=20, pady=20)


def center_window(win):
    width=500
    height=500
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(alignstr)
    