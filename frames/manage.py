import tkinter as tk
from tkinter import ttk
from frames.config import LARGEFONT


class Manage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Images", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        button_return = ttk.Button(self,
                                   text="Options",
                                   command=lambda: controller.show_control())
        button_return.grid(row=2, column=1, padx=10, pady=10)


