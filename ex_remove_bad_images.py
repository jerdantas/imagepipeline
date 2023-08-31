import os
import random
from PIL import Image


def count_files(
        input: str
) -> int:

    num = 0
    for i in os.walk(input, topdown=True):
        num += len(i[2])
    return num


def process(
        input: str
) -> int:
    next = 0
    for root, dirs, files in os.walk(top=input, topdown=True):
        for name in files:
            source = os.path.join(root, name)
            image = Image.open(source)
            if len(image.layer) == 3:
                next += 1
            else:
                pass
    return next

import os
import random
from PIL import Image


def count_files(
        input: str
) -> int:

    num = 0
    for i in os.walk(input, topdown=True):
        num += len(i[2])
    return num


def process(
        input: str
) -> (int, int):
    count = 0
    removed = 0
    for root, dirs, files in os.walk(top=input, topdown=True):
        for name in files:
            source = os.path.join(root, name)
            image = Image.open(source)
            if len(image.layer) == 3:
                count += 1
            else:
                removed += 1
                path = os.path.join(root, name)
                print(path)
                os.remove(path)


    return count, removed

count, removed = process(os.getcwd() + '/dddd')
print("count: " + str(count) + "  removed: " + str(removed))


