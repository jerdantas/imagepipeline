import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import glob
from typing import List

from detection.detector import Detector
from detection.analyse import Alarm, Box, NonCompliance
import viz_utils
from frames.config import LARGEFONT, DETECT_IMAGE_WIDTH, NORMALFONT, MEDIUMFONT, SMALLFONT

category_index = {
    0: {'id': 0, 'name': 'eye-glass'},
    1: {'id': 1, 'name': 'face-shield'},
    2: {'id': 2, 'name': 'glove'},
    3: {'id': 3, 'name': 'helmet'},
    4: {'id': 4, 'name': 'mask'},
    5: {'id': 5, 'name': 'person'},
    6: {'id': 6, 'name': 'safety-shoe'}
}


class Detect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.model = Detector(threshold=0.5)
        self.image_side = int(DETECT_IMAGE_WIDTH * controller.screen_factor)

        root_dir = os.getcwd()
        self.images = [f for f in glob.glob(os.path.join(root_dir, 'imgs2detect', '*.png'))]
        self.images.sort()
        self.img_names = [os.path.split(f)[-1] for f in self.images]

        self.img_new = None
        self.img_res = None
        self.classlist = tk.StringVar()

        # 0 ------------------------------------------------------------------------------
        self.label_title = ttk.Label(self, text="Object Detection", font=LARGEFONT)
        self.label_title.grid(row=0, column=0, columnspan=3, padx=0, pady=20)

        # 1 ------------------------------------------------------------------------------
        self.label_col = ttk.Label(self, text="Source Image", font=MEDIUMFONT)
        self.label_col.grid(row=1, column=1, padx=0, pady=0)
        self.label_inf = ttk.Label(self, text="Detected Objects", font=MEDIUMFONT)
        self.label_inf.grid(row=1, column=2, padx=0, pady=0)

        # 2 ------------------------------------------------------------------------------
        var = tk.Variable(value=self.img_names)
        self.listbox_images = tk.Listbox(self,
                                         listvariable=var,
                                         height=21,
                                         selectmode=tk.SINGLE,
                                         font=NORMALFONT)
        self.listbox_images.bind('<<ListboxSelect>>', self.image_selected)
        self.listbox_images.grid(row=2, rowspan=3, column=0, padx=40, pady=5, ipadx=5, ipady=5, sticky='n')
        self.canvas_src = tk.Canvas(self, height=self.image_side, width=self.image_side, relief='solid')
        self.canvas_src.grid(row=2, column=1, padx=40, pady=5)
        self.canvas_res = tk.Canvas(self, height=self.image_side, width=self.image_side, relief='solid')
        self.canvas_res.grid(row=2, column=2, padx=0, pady=0)

        # 3 ------------------------------------------------------------------------------
        self.label_name = ttk.Label(self, text="[image]", font=MEDIUMFONT)
        self.label_name.grid(row=3, column=1, padx=0, pady=0)

        self.classes_label = WrappingLabel(self, height=8, width=56, justify=tk.LEFT,
                                           font=SMALLFONT)
        self.classes_label.grid(row=3, column=2, padx=0, pady=0, ipadx=0, ipady=0)
        self.classes_label.configure(textvariable=self.classlist)

        # 4 ------------------------------------------------------------------------------
        self.button_return = ttk.Button(self,
                                        text="Return",
                                        command=lambda: controller.show_control())
        self.button_return.grid(row=4, column=0, columnspan=3, padx=0, pady=50)

    def image_selected(self, event) -> None:
        # show selected image
        selected_index = self.listbox_images.curselection()[0]
        self.label_name['text'] = self.img_names[selected_index]
        src_image = Image.open(self.images[selected_index])

        det_image, result = self.model.infer(src_image)
        bboxes, classes, scores = get_box_info(result)

        alarm = Alarm()

        i = 0
        while i < len(bboxes):
            box = Box(list(bboxes[i]), src_image.height, src_image.width, normalized=True)
            cls = int(classes[i])
            score = float(scores[i])

            if alarm.add_target(category_index[cls]['name'], cls, box, score) >= 0:
                i += 1
            else:
                # Target has been discarded
                bboxes = np.delete(bboxes, i, 0)
                classes = np.delete(classes, i, 0)
                scores = np.delete(scores, i, 0)

        problems: List[NonCompliance] = alarm.get_alarms()
        reason_list = []
        for prob in problems:
            t = ''
            if prob.target_id is not None:
                t = f'{prob.category_name}-{prob.target_id}: '
            t += prob.reason
            reason_list += [t]

        reason = ' \n'.join([p for p in reason_list])
        self.classlist.set(reason)

        image = adjust_image(src_image, self.image_side)
        self.img_new = ImageTk.PhotoImage(image)
        self.canvas_src.create_image(self.image_side / 2, self.image_side / 2,
                                     anchor=tk.CENTER, image=self.img_new)

        image = adjust_image(det_image, self.image_side)
        viz_utils.visualize_boxes_and_labels_on_image_array(image, bboxes, classes, scores,
                                                            category_index,
                                                            use_normalized_coordinates=True,
                                                            max_boxes_to_draw=20,
                                                            min_score_thresh=0.2,
                                                            line_thickness=2,
                                                            skip_labels=False,
                                                            skip_scores=False)

        self.img_res = ImageTk.PhotoImage(image)
        self.canvas_res.create_image(self.image_side / 2, self.image_side / 2,
                                     anchor=tk.CENTER, image=self.img_res)


def adjust_image(image: Image, side: int) -> Image:
    try:
        image_factor = min(side / image.width, side / image.height)
        if image_factor != 1.0:
            image = image.resize((int(image.width * image_factor), int(image.height * image_factor)))
    except Exception() as ex:
        pass
    return image


def get_box_info(boxes):
    classes = boxes['class']
    scores = boxes['score']
    bboxes = boxes['bbox']

    return np.array(bboxes), np.array(classes), np.array(scores)


class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))
