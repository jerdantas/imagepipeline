import tkinter as tk
from tkinter import ttk
from typing import List

from frames.classify import Classify
from frames.config import LARGEFONT, MEDIUNFONT, NORMALFONT
from frames.review import Review
from frames.test import Test


class Control(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        # 0 ------------------------------------------------------------------------------
        label_title = ttk.Label(self, text="Image Handling Pipeline", font=LARGEFONT)
        label_title.grid(row=0, column=0, columnspan=4, padx=0, pady=50)

        # 1 ------------------------------------------------------------------------------
        label_project = ttk.Label(self, text="Project:", font=MEDIUNFONT)
        label_project.grid(row=1, column=0, sticky='W', padx=50, pady=100)
        projects: List[str] = ['classification', 'object detection']
        self.project_var = tk.StringVar()
        self.combo_project = ttk.Combobox(self, exportselection=False, height=5, state='readonly',
                                          values=projects, textvariable=self.project_var,
                                          justify=tk.CENTER,             width=20, font=NORMALFONT)
        self.combo_project.grid(row=1, column=1, sticky='W', columnspan=3, padx=0, pady=0)
        self.combo_project.bind('<<ComboboxSelected>>', self.project_selected)
        self.combo_project.grid(row=1, column=1, padx=0, pady=0)

        # 2 ------------------------------------------------------------------------------
        label_class = ttk.Label(self, text="Classify", font=MEDIUNFONT)
        label_class.grid(row=2, column=0, sticky='W', padx=50, pady=20)
        button_class = ttk.Button(self, text="classify new images",
                                 command=lambda: controller.show_frame(Classify))
        button_class.grid(row=2, column=1, sticky='W', padx=50, pady=20)
        class_comment = ttk.Label(self, text="submit new images to VA Image Classifier", font=NORMALFONT)
        class_comment.grid(row=2, column=2, sticky='W', padx=50, pady=20)

        # 3 ------------------------------------------------------------------------------
        label_review = ttk.Label(self, text="Review", font=MEDIUNFONT)
        label_review.grid(row=3, column=0, padx=50, pady=20, sticky='W')
        button_review = ttk.Button(self, text="review classes",
                                 command=lambda: controller.show_frame(Review))
        button_review.grid(row=3, column=1, sticky='W',  padx=50, pady=20)
        review_comment = ttk.Label(self, text="review and update classes assigned to existing images", font=NORMALFONT)
        review_comment.grid(row=3, column=2, sticky='W', padx=50, pady=20)

        # 4 ------------------------------------------------------------------------------
        label_train = ttk.Label(self, text="Train", font=MEDIUNFONT)
        label_train.grid(row=4, column=0, padx=50, pady=20, sticky='W')
        button_train = ttk.Button(self, text="train model",
                                 command=lambda: controller.show_frame(Review))
        button_train.grid(row=4, column=1, sticky='W',  padx=50, pady=20)
        train_comment = ttk.Label(self, text="train model using existing images", font=NORMALFONT)
        train_comment.grid(row=4, column=2, sticky='W', padx=50, pady=20)

        # 5 ------------------------------------------------------------------------------
        label_test = ttk.Label(self, text="Test", font=MEDIUNFONT)
        label_test.grid(row=5, column=0, padx=50, pady=20, sticky='W')
        button_test = ttk.Button(self, text="test",
                                 command=lambda: controller.show_frame(Test))
        button_test.grid(row=5, column=1, sticky='W',  padx=50, pady=20)
        test_comment = ttk.Label(self, text="calculate current metrics using test dataset", font=NORMALFONT)
        test_comment.grid(row=5, column=2, sticky='W', padx=50, pady=20)

        # 2 ------------------------------------------------------------------------------
        label_manage = ttk.Label(self, text="Manage", font=MEDIUNFONT)
        label_manage.grid(row=6, column=0, padx=50, pady=20, sticky='W')
        button_manage = ttk.Button(self, text="manage images",
                                 command=lambda: controller.show_frame(Review))
        button_manage.grid(row=6, column=1, sticky='W',  padx=50, pady=20)
        manage_comment = ttk.Label(self, text="add new images and remove existing messages", font=NORMALFONT)
        manage_comment.grid(row=6, column=2, sticky='W', padx=50, pady=20)


    def project_selected(
            self,
            event
    ) -> None:
        current_value = self.project_var.get()
        '''
        CHANGE PROJECT
        '''

