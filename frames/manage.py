import os
import tkinter as tk
from tkinter import ttk, CENTER

from classification.classifier import Classifier
from frames.config import LARGEFONT, IMAGE_WIDTH, MEDIUMFONT, WINDOW_WIDTH


class Manage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.button_return = ttk.Button(self,
                                        text="completed",
                                        command=lambda: controller.show_control())
        self.button_return.grid(row=6, column=0, padx=0, pady=30)
