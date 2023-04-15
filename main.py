import tkinter as tk

from Controllers.main_controller import MainController

if __name__ == '__main__':
    print("start belly full")
    root = tk.Tk()
    root.withdraw()
    app = MainController(root)
    root.mainloop()
    