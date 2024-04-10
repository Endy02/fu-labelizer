import tkinter as tk
import customtkinter as ctk
from fulabelizer.interfaces.dashboard import Dashboard

class Labelizer():
    def __init__(self):
        self.window = self.init_window()
        self.dashboard = Dashboard(window=self.window)

    def init_window(self):
        try:
            window = ctk.CTk()
            #getting screen width and height of display
            width= window.winfo_screenwidth()
            height= window.winfo_screenheight()
            #setting tkinter window size
            window.geometry("%dx%d" % (width, height))

            window.grid_rowconfigure(0, weight=1)
            window.grid_columnconfigure(2, weight=1)

            window.title("Fu Labelizer")
            window.resizable(width=True, height=True)
            nav_menu = self.nav_menu(window=window)

            window.config(menu=nav_menu)

            return window
        except Exception as e:
            raise e
    
    def nav_menu(self, window):
        try:
            # Creating Menubar 
            menubar = tk.Menu(window) 
            
            # Adding File Menu
            file = tk.Menu(menubar, tearoff = 0) 
            menubar.add_cascade(label ='File', menu = file)
            file.add_command(label="Open Folder")
            file.add_command(label="Close")  

            # Adding Edit Menu
            edit = tk.Menu(menubar, tearoff = 0) 
            menubar.add_cascade(label ='Edit', menu = edit)
            edit.add_command(label="Rectangle")
            edit.add_command(label="Rectangle")

            return menubar
        except Exception as e:
            raise e


    def launch(self):
        try:
            self.dashboard.create()
            self.window.mainloop()
        except Exception as e:
            raise e