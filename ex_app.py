import tkinter as tk
from tkinter import ttk
from os import path

from frames.classify import Classify
from frames.detect import Detect
from frames.config import NORMALFONT, WINDOW_WIDTH, WINDOW_HEIGHT
from frames.control import Control
from frames.manage import Manage
from frames.review import Review
from frames.test import Test
from frames.train import Train


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        container = tk.Frame(self)

        self.style = ttk.Style(self)
        self.style.theme_use('alt')
        self.style = ttk.Style(self)
        self.style.configure(style='TLabel', font=NORMALFONT)
        self.style.configure(style='TButton', font=NORMALFONT)
        self.style.configure(style='TLabelFrame', font=NORMALFONT)
        self.style.configure(style='TLabel', font=NORMALFONT)
        self.style.configure(style='TRadiobutton', font=NORMALFONT)
        self.style.configure(style='TEntry', font=NORMALFONT)
        self.style.configure(style='TCombobox', font=NORMALFONT)
        self.style.configure(style='TListbox', font=NORMALFONT)

        self.title('Video Analytics - Model building and updating pipeline')
        self.screen_factor = 1.0
        if self.winfo_screenwidth() < WINDOW_WIDTH:
            self.screen_factor = 1600./self.winfo_screenwidth()
        window_width = int(WINDOW_WIDTH*self.screen_factor)
        window_height = int(WINDOW_HEIGHT*self.screen_factor)
        self.geometry(f'{window_width}x{window_height}')
        self.resizable(width=False, height=False)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(index=0, weight=1)
        container.grid_columnconfigure(index=0, weight=1)

        self.frames = {}
        for page in (Control, Detect, Classify, Train, Manage, Review, Test):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_control()

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

    def show_control(self):
        frame = self.frames[Control]
        frame.tkraise()


if __name__ == '__main__':
    app = tkinterApp()
    app.mainloop()
