import tkinter as tk
from tkinter import ttk


class Dashboard():
    def __init__(self, window):
        self.window = window

    def create(self):
        try:
            content = ttk.Frame(self.window, padding=(3,3,12,12))
            frame = ttk.Frame(content, borderwidth=3, relief="sunken", width=50, height=50)
            namelbl = ttk.Label(content, text="Name")
            name = ttk.Entry(content)

            onevar = tk.BooleanVar()
            twovar = tk.BooleanVar()
            threevar = tk.BooleanVar()

            onevar.set(True)
            twovar.set(False)
            threevar.set(True)

            one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
            two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
            three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
            ok = ttk.Button(content, text="Okay")
            cancel = ttk.Button(content, text="Cancel")

            content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
            frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
            namelbl.grid(column=3, row=0, columnspan=2, sticky=(tk.N, tk.W), padx=5)
            name.grid(column=3, row=1, columnspan=2, sticky=(tk.N,tk.E,tk.W), pady=5, padx=5)
            one.grid(column=0, row=3)
            two.grid(column=1, row=3)
            three.grid(column=2, row=3)
            ok.grid(column=3, row=3)
            cancel.grid(column=4, row=3)

            self.window.columnconfigure(0, weight=1)
            self.window.rowconfigure(0, weight=1)
            content.columnconfigure(0, weight=3)
            content.columnconfigure(1, weight=3)
            content.columnconfigure(2, weight=3)
            content.columnconfigure(3, weight=1)
            content.columnconfigure(4, weight=1)
            content.rowconfigure(1, weight=1)
            
        except Exception as e:
            raise e