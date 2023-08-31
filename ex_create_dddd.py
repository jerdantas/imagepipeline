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
        input: str,
        output: str,
        count: int,
        max: int = 100
) -> int:
    next = 0
    for root, dirs, files in os.walk(top=input, topdown=True):
        for name in files:
            source = os.path.join(root, name)
            image = Image.open(source)
            if len(image.layer) == 3:
                next += 1
                if next > max:
                    break
                count += 1
                current = str(count).zfill(5)

                # ----- train split
                train_path = output + '/train/' + current
                os.mkdir(train_path)
                train_path = train_path + '/'
                image.save(train_path + current + '.jpg')
                for i in range(5):
                    image.\
                        rotate(random.randrange(start=1, stop=359)).\
                        save(train_path + current + '-' + str(i) +'.jpg')

                # ----- validation split
                validation_path = output + '/validation/' + current
                os.mkdir(validation_path)
                validation_path = validation_path + '/'
                for i in range(2):
                    image.\
                        rotate(random.randrange(start=1, stop=359)).\
                        save(validation_path + current + '-' + str(i) +'.jpg')

                # ----- test split
                test_path = output + '/test/' + current
                os.mkdir(test_path)
                test_path = test_path + '/'
                for i in range(2):
                    image.\
                        rotate(random.randrange(start=1, stop=359)).\
                        save(test_path + current + '-' + str(i) +'.jpg')
    return count


count = 0
input = os.getcwd() + '/images'
output = os.getcwd() + '/dddd'
count = process(input + '/ds_cards/train/king of diamonds', output, count, max=200)
count = process(input + '/ds_cards/train/queen of diamonds', output, count, max=200)
count = process(input + '/ds_cards/train/four of diamonds', output, count, max=200)
count = process(input + '/ds_cards/train/four of hearts', output, count, max=200)
count = process(input + '/ds_cards/train/ten of diamonds', output, count, max=200)
print('end ', str(count))