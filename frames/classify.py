import os
import tkinter as tk
from tkinter import ttk
from typing import List

from PIL import Image, ImageTk
import frames.utils as utils

from frames.config import LARGEFONT, IMAGE_WIDTH, NORMALFONT, MEDIUNFONT


class Classify(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.inferred_class: str = 'inferred class'
        self.image_side = int(IMAGE_WIDTH*controller.screen_factor)

        # 0 ------------------------------------------------------------------------------
        self.label_title = ttk.Label(self, text="Classify New Images", font=LARGEFONT)
        self.label_title.grid(row=0, column=0, columnspan=5, padx=0, pady=20)

        # 1 ------------------------------------------------------------------------------
        self.label_col = ttk.Label(self, text="New Images", font=MEDIUNFONT)
        self.label_col.grid(row=1, column=0, padx=0, pady=0)
        self.label_name = ttk.Label(self, text="[image]", font=MEDIUNFONT)
        self.label_name.grid(row=1, column=1, padx=0, pady=0)
        self.label_inf = ttk.Label(self, text="[class]", font=MEDIUNFONT)
        self.label_inf.grid(row=1, column=2, padx=0, pady=0)

        # 2 ------------------------------------------------------------------------------
        images: List[str] = []
        test_dir = '/home/luiz/___classify/classify/test_images'
        for root, dirs, files in os.walk(top=test_dir, topdown=True):
            for name in files:
                images.append(name)
        var = tk.Variable(value=images)
        self.listbox_images = tk.Listbox(self,
                                         listvariable=var,
                                          height=21,
                                         selectmode=tk.SINGLE,
                                         font=NORMALFONT)
        self.listbox_images.bind('<<ListboxSelect>>', self.image_selected)
        self.listbox_images.grid(row=2, rowspan=3, column=0, padx=40, pady=5, ipadx=5, ipady=5, sticky='n')

        self.canvas_new = tk.Canvas(self, height=self.image_side, width=self.image_side, relief='solid')
        image = utils.prepare_image('test_images/dani.png', self.image_side)
        self.img_new = ImageTk.PhotoImage(image)
        self.canvas_new.create_image(0, 0, anchor=tk.NW, image=self.img_new)
        self.canvas_new.grid(row=2, column=1, padx=40, pady=5, ipadx=5, ipady=5)

        self.canvas_cls = tk.Canvas(self, height=self.image_side, width=self.image_side,  relief='solid')
        image = utils.prepare_image('test_images/dani.png', self.image_side)
        self.img_cls = ImageTk.PhotoImage(image)
        self.canvas_cls.create_image(0, 0, anchor=tk.NW, image=self.img_cls)
        self.canvas_cls.grid(row=2, column=2, padx=40, pady=5, ipadx=5, ipady=5)

        # 3 ------------------------------------------------------------------------------
        classes: List[str] = ['class 1', 'class 2', 'class 3', 'class 4', 'class 5', 'class 6']
        self.current_var = tk.StringVar()
        self.combo_change = ttk.Combobox(self, exportselection=False, height=5, state='readonly',
                                         values=classes, textvariable=self.current_var,
                                         justify=tk.CENTER,             width=20, font=NORMALFONT)
        self.combo_change.bind('<<ComboboxSelected>>', self.class_selected)
        self.combo_change.grid(row=3, column=2, padx=0, pady=0)

        # 4 ------------------------------------------------------------------------------
        self.button_accept = ttk.Button(self,
                                        text="accept",
                                        command=lambda: self.accept_inference)
        self.button_accept.grid(row=4, column=2, padx=0, pady=20)

        # 5 ------------------------------------------------------------------------------
        self.button_return = ttk.Button(self,
                                        text="completed",
                                        command=lambda: controller.show_control())
        self.button_return.grid(row=8, column=0, columnspan=5, padx=0, pady=50)

    def image_selected(
            self,
            event
    ) -> None:
        selected_index = self.listbox_images.curselection()
        '''
        INFERENCE
        '''

    def class_selected(
            self,
            event
    ) -> None:
        current_value = self.current_var.get()
        '''
        CHANGE INFERENCE
        '''

    def accept_inference(
            self,
            event
    ) -> None:
        inferred_class = self.inferred_class
        '''
        SHOE INFERRED
        '''





