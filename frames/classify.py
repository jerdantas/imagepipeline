import os
import tkinter as tk
from tkinter import ttk
from typing import List

from PIL import Image, ImageTk
import frames.utils as utils
from classification.classifier import Classifier

from frames.config import LARGEFONT, IMAGE_WIDTH, NORMALFONT, MEDIUNFONT


class Classify(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.predictor = Classifier()
        self.inferred_class: str = 'inferred class'
        self.image_side = int(IMAGE_WIDTH*controller.screen_factor)

        self.classes: List[str] = []
        train_dir = '/home/luiz/___imagepipeline/imagepipeline/bbbb/train'       # PARAMETER
        for root, dirs, files in os.walk(top=train_dir, topdown=True):
            for dir in dirs:
                self.classes.append(dir)

        self.new_images: List[str] = []
        self.new_files: List[str] = []
        new_dir = '/home/luiz/___imagepipeline/imagepipeline/bbbb/test'          # PARAMETER
        for root, dirs, files in os.walk(top=new_dir, topdown=True):
            for name in files:
                self.new_images.append(name)
                self.new_files.append(os.path.join(root, name))
        self.train_dir = '/home/luiz/___imagepipeline/imagepipeline/bbbb/train'          # PARAMETER

        # 0 ------------------------------------------------------------------------------
        self.label_title = ttk.Label(self, text="Classify New Images", font=LARGEFONT)
        self.label_title.grid(row=0, column=0, columnspan=5, padx=0, pady=20)

        # 1 ------------------------------------------------------------------------------
        self.label_col = ttk.Label(self, text="New Images", font=MEDIUNFONT)
        self.label_col.grid(row=1, column=0, padx=0, pady=0)
        # self.label_name = ttk.Label(self, text="[image]", font=MEDIUNFONT)
        # self.label_name.grid(row=1, column=1, padx=0, pady=0)
        self.label_inf = ttk.Label(self, text="Classification", font=MEDIUNFONT)
        self.label_inf.grid(row=1, column=2, padx=0, pady=0)

        # 2 ------------------------------------------------------------------------------
        var = tk.Variable(value=self.new_images)
        self.listbox_images = tk.Listbox(self,
                                         listvariable=var,
                                          height=21,
                                         selectmode=tk.SINGLE,
                                         font=NORMALFONT)
        self.listbox_images.bind('<<ListboxSelect>>', self.image_selected)
        self.listbox_images.grid(row=2, rowspan=3, column=0, padx=40, pady=5, ipadx=5, ipady=5, sticky='n')
        self.canvas_new = tk.Canvas(self, height=self.image_side, width=self.image_side, relief='solid')
        self.canvas_new.grid(row=2, column=1, padx=40, pady=5, ipadx=5, ipady=5)
        self.canvas_cls = tk.Canvas(self, height=self.image_side, width=self.image_side,  relief='solid')
        self.canvas_cls.grid(row=2, column=2, padx=40, pady=5, ipadx=5, ipady=5)

        # 3 ------------------------------------------------------------------------------
        self.label_name = ttk.Label(self, text="[image]", font=MEDIUNFONT)
        self.label_name.grid(row=3, column=1, padx=0, pady=0)

        # 4 ------------------------------------------------------------------------------
        classes: List[str] = self.classes
        self.current_var = tk.StringVar()
        self.combo_change = ttk.Combobox(self, exportselection=False, height=5, state='readonly',
                                         values=classes, textvariable=self.current_var,
                                         justify=tk.CENTER,             width=20, font=NORMALFONT)
        self.combo_change.bind('<<ComboboxSelected>>', self.class_selected)
        self.combo_change.grid(row=4, column=2, padx=0, pady=0)

        # 5 ------------------------------------------------------------------------------
        self.button_accept = ttk.Button(self,
                                        text="accept",
                                        command=lambda: self.accept_inference)
        self.button_accept.grid(row=5, column=2, padx=0, pady=20)

        # 6 ------------------------------------------------------------------------------
        self.button_return = ttk.Button(self,
                                        text="completed",
                                        command=lambda: controller.show_control())
        self.button_return.grid(row=6, column=0, columnspan=5, padx=0, pady=50)

    def image_selected(
            self,
            event
    ) -> None:

        # show selected image
        selected_index = self.listbox_images.curselection()[0]
        self.label_name['text'] = self.new_images[selected_index]
        image = utils.prepare_image(self.new_files[selected_index], self.image_side)
        self.img_new = ImageTk.PhotoImage(image)
        self.canvas_new.create_image(self.image_side/2, self.image_side/2, anchor=tk.CENTER, image=self.img_new)

        # classify and show similar image
        image_class = self.predictor.predict(self.new_files[selected_index])
        similar_dir = os.path.join(self.train_dir, image_class)
        if os.path.exists(similar_dir):
            similar_images = os.listdir(similar_dir)
            if len(similar_images) > 0:
                similar_image = utils.prepare_image(os.path.join(similar_dir, similar_images[0]), self.image_side)
                self.img_cls = ImageTk.PhotoImage(similar_image)
                self.canvas_cls.create_image(self.image_side / 2, self.image_side / 2, anchor=tk.CENTER, image=self.img_cls)
                self.combo_change.set(image_class)
        else:
            self.canvas_cls.delete('all')
            self.combo_change.set('')



    def class_selected(
            self,
            event
    ) -> None:
        image_class = self.current_var.get()
        similar_dir = os.path.join(self.train_dir, image_class)
        if os.path.exists(similar_dir):
            similar_images = os.listdir(similar_dir)
            if len(similar_images) > 0:
                similar_image = utils.prepare_image(os.path.join(similar_dir, similar_images[0]), self.image_side)
                self.img_cls = ImageTk.PhotoImage(similar_image)
                self.canvas_cls.create_image(self.image_side / 2, self.image_side / 2, anchor=tk.CENTER, image=self.img_cls)
                self.combo_change.set(image_class)

    def accept_inference(
            self,
            event
    ) -> None:
        inferred_class = self.inferred_class
        '''
        SHOE INFERRED
        '''





