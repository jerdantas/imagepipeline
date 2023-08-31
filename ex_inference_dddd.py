import os
from time import time
import torch
from PIL import Image
from transformers import ViTImageProcessor, ViTForImageClassification

processor = ViTImageProcessor.from_pretrained('vit-base-dddd/checkpoint-300')
model = ViTForImageClassification.from_pretrained('vit-base-dddd/checkpoint-300')

root_dir = os.getcwd()
test_dir = os.path.join(root_dir, 'dddd/test')

error_count = 0
test_count = 0
for root, dirs, files in os.walk(top=test_dir, topdown=True):
    if test_count > 4000:
        break
    for name in files:
        file_name = os.path.join(root, name)
        image = Image.open(file_name)

        # ----- inference --------------------------------------
        # ------------------------------------------------------
        start = time()
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        duration = (time() - start) * 1000
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        class_name = model.config.id2label[predicted_class_idx]
        # -------------------------------------------------------
        # smt = logits.softmax(-1)
        # sm = smt[0, predicted_class_idx]
        # n = smt.shape[1]
        # sec = 0.0
        # for i in range(n):
        #     if i != predicted_class_idx and smt[0, i] > sec:
        #         sec = smt[0, i]
        # if sm * 0.5 > sec or sm >= 0.01:
        #     class_name = model.config.id2label[predicted_class_idx]
        # else:
        #     class_name = '[unknown]'
        # -------------------------------------------------------
        if file_name.find(class_name) != -1:
            error = ''
        else:
            error_count += 1
            error = str(error_count)
        print("Class:", class_name,
              "   ", file_name, "   ", error,
              "   ", str(duration))
        test_count += 1
        if test_count > 4000:
            break
        # ------------------------------------------------------
print('test_count = ', str(test_count))
print('Error count  = ', str(error_count))
print('accuracy = ', str((test_count - error_count)/test_count))
print(torch.cuda.is_available())
print(torch.cuda.is_initialized())
