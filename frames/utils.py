import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def prepare_image(url: str,
                  side: int
) -> Image:
    image = None
    try:
        image = Image.open(url)
        image_factor = 1.0
        if image.width > image.height:
            if image.width > side:
                image_factor = side / image.width
        else:
            if image.height > side:
                image_factor = side / image.height
        if image_factor != 1.0:
            image = image.resize((int(image.width * image_factor), int(image.height * image_factor)))
    except Exception() as ex:
        pass
    return image
