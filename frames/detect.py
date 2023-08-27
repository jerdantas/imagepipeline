import os
import tkinter as tk
from tkinter import ttk
from typing import List

from PIL import ImageTk
import frames.utils as utils
from classification.classifier import Classifier

from frames.config import LARGEFONT, IMAGE_WIDTH, NORMALFONT, MEDIUNFONT

global root_dir


class Detect(tk.Frame):
    def __init__(self, parent, controller):

        super().__init__(parent)
        self.controller = controller
