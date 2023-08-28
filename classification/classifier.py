import os
from time import time
import torch
from PIL import Image
from transformers import ViTImageProcessor, ViTForImageClassification


class Classifier:
    
    def __init__(self):
        model_name = 'vit-base-bbbb/checkpoint-600'                                   # PARAMETER
        self.processor = ViTImageProcessor.from_pretrained(model_name)
        self.model = ViTForImageClassification.from_pretrained(model_name)

    def predict(
            self,
            file_path: str
    ) -> str:
            class_name: str = ''
            try:
                image = Image.open(file_path)
                start = time()
                inputs = self.processor(images=image, return_tensors="pt")
                outputs = self.model(**inputs)
                duration = (time() - start) * 1000
                logits = outputs.logits
                predicted_class_idx = logits.argmax(-1).item()
                smt = logits.softmax(-1)
                sm = smt[0,predicted_class_idx]
                n = smt.shape[1]
                sec = 0.0
                for i in range(n):
                    if i != predicted_class_idx and smt[0,i] > sec:
                        sec = smt[0,i]
                if sm * 0.5 > sec or sm >= 0.01:
                    class_name = self.model.config.id2label[predicted_class_idx]
                else:
                    class_name = '[unknown]'
            except Exception() as ex:
                pass
            return class_name
