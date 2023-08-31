import os
import tkinter as tk
from tkinter import ttk, CENTER

from classification.classifier import Classifier
from frames.config import LARGEFONT, IMAGE_WIDTH, MEDIUMFONT, WINDOW_WIDTH


class Train(tk.Frame):
    def __init__(self, parent, controller):

        super().__init__(parent)
        self.controller = controller

        class_count = 0
        image_count = 0
        root_dir = os.getcwd()
        self.train_dir = os.path.join(root_dir, 'dddd/train')       # PARAMETER
        for root, dirs, files in os.walk(top=self.train_dir, topdown=True):
            for dir in dirs:
                class_count += 1
        for root, dirs, files in os.walk(top=self.train_dir, topdown=True):
            for name in files:
                image_count += 1

        frame = ttk.Frame(      self)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # 0 ------------------------------------------------------------------------------
        self.label_title = ttk.Label(frame, text="Train Model", font=LARGEFONT)
        self.label_title.grid(row=0, column=0, padx=0, pady=100)
        self.label_title.columnconfigure(0, minsize=WINDOW_WIDTH)

        # 1 ------------------------------------------------------------------------------
        self.label_col = ttk.Label(frame, text="Train Images", font=MEDIUMFONT)
        self.label_col.grid(row=1, column=0, padx=0, pady=0)

        # 2 ------------------------------------------------------------------------------
        self.label_name = ttk.Label(frame, text="class count: " + str(class_count), font=MEDIUMFONT)
        self.label_name.grid(row=2, column=0, padx=0, pady=0)

        # 3 ------------------------------------------------------------------------------
        self.label_name = ttk.Label(frame, text="image count: " + str(image_count), font=MEDIUMFONT)
        self.label_name.grid(row=3, column=0, padx=0, pady=0)

        # 4 ------------------------------------------------------------------------------
        self.button_start = ttk.Button(frame,
                                        text="start training",
                                        command=lambda: self.start_training)
        self.button_start.grid(row=4, column=0, padx=0, pady=80)

        # 5 ------------------------------------------------------------------------------
        self.label_name = ttk.Label(frame, text="", font=MEDIUMFONT)
        self.label_name.grid(row=5, column=0, padx=0, pady=30)

        # 6 ------------------------------------------------------------------------------
        self.button_return = ttk.Button(frame,
                                        text="completed",
                                        command=lambda: controller.show_control())
        self.button_return.grid(row=6, column=0, padx=0, pady=30)

    def start_training(
            self,
            event
    ) -> None:
        self.label_name["text"] = "training..."


