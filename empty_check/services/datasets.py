from testdata.function.random_rotate import random_rotate
from function.word_check import find_text_coordinates_easyocr
from testdata.function.write import write
from testdata.function.preprocessing import preprocess_image
from function.coord import box_check, small_box
import os

def make_dataset():
    path = 'dataset/original_data/Sahmyook1_B.jpg'
    file_name = os.path.splitext(os.path.basename(path))[0]
    print(file_name)

    images = random_rotate(path)

    preprocess_images = []

    for i in range(len(images)):
        preprocess_images.append(preprocess_image(images[i]))

    coord_top_left, coord_bottom_right, numbers = find_text_coordinates_easyocr(preprocess_images[0])
    num_of_problems = len(numbers)

    horizontal, vertical = box_check(coord_top_left)

    small_horizontal, small_vertical = small_box(coord_top_left[0], coord_bottom_right[0])

    horizontal -= small_horizontal
    vertical -= small_vertical

    print("문제의 개수",num_of_problems)

    for i in range(len(preprocess_images)):
        write(images[i], file_name, coord_top_left, horizontal, vertical, num_of_problems, i)