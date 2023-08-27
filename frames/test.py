import os
import tkinter as tk
from tkinter import ttk
from typing import List

from PIL import Image, ImageTk
import frames.utils as utils

from frames.config import LARGEFONT, IMAGE_WIDTH


class Test(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.image_side = int(IMAGE_WIDTH*controller.screen_factor)

        self.label_title = ttk.Label(self, text="Mettrics Using Test Dataset", font=LARGEFONT)
        self.label_title.grid(row=0, column=0, columnspan=5, padx=0, pady=20)

        images: List[str] = []
        test_dir = '/home/luiz/___classify/classify/test_images'