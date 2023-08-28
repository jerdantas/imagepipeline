import os
from PIL import Image
from typing import List

import torch
from ultralytics import YOLO
from ultralytics.engine.results import Results


class Detector:
    def __init__(self, threshold):
        self.threshold = threshold
        root_dir = os.getcwd()
        model = os.path.join(root_dir, 'detection/model', 'best.pt')

        # Load detect model
        self.interpreter = YOLO(model)
        input_shape = (1, 640, 640, 3)

        n, self.frameHeight, self.frameWidth, c = input_shape

    '''
    Examine the image to detect objects
    :return: frame, boxes
    '''
    def infer(self, frame: Image) -> [Image, dict]:
        ih, iw = frame.size
        if (ih, iw) != (self.frameHeight, self.frameWidth):
            image = frame.resize((self.frameHeight, self.frameWidth))
        else:
            image = frame

        # run model
        results: List[Results] = self.interpreter.predict(image, imgsz=640,
                                                          conf=0.2, verbose=False,
                                                          show=False, save=False)

        # get results
        # boxlist, catlist, scorelist
        result = results[0]
        boxlist = result.boxes.xyxyn
        catlist = result.boxes.cls
        scorelist = result.boxes.conf

        num_detections = result.boxes.shape[0]

        num_detections = min(20, num_detections)

        # detection_classes should be ints.
        catlist = catlist.to(torch.int32)

        # box val must be inverted, xyxy to yxyx
        boxlist = invert(boxlist)

        boxes = collect_box(boxlist[:num_detections],
                            (catlist[:num_detections]).tolist(),
                            scorelist[:num_detections].tolist(),
                            self.threshold)

        return frame, boxes


def invert(boxlist):
    bl = []
    for box in boxlist:
        a = box.tolist()
        bl.append([a[1], a[0], a[3], a[2]])
    return bl


def collect_box(boxlist, catlist, scorelist, threshold):
    bl = []
    cl = []
    sl = []
    for i in range(len(boxlist)):
        if scorelist[i] >= threshold:
            bl.append(boxlist[i])
            cl.append(catlist[i])
            sl.append(scorelist[i])

    box_list = {'class': cl, 'score': sl, 'bbox': bl}
    return box_list
