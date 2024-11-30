from app.make_datast.random_rotate import random_rotate
from app.blank.find_text import find_texts
from app.make_datast.write import write
from app.make_datast.preprocessing import preprocess_image
from app.blank.coord import problem_box_check, small_box
import os

def make_dataset(image, count, file_name):
    images = random_rotate(image, count)

    preprocess_images = []

    for i in range(len(images)):
        preprocess_images.append(preprocess_image(images[i]))

    coord_top_left, coord_bottom_right, numbers, sign_box = find_texts(preprocess_images[0])
    num_of_problems = len(numbers)

    horizontal, vertical = problem_box_check(coord_top_left)

    small_horizontal, small_vertical = small_box(coord_top_left[0], coord_bottom_right[0])

    horizontal -= small_horizontal
    vertical -= small_vertical

    print("문제의 개수",num_of_problems)

    for i in range(len(preprocess_images)):
        write(images[i], file_name, coord_top_left, horizontal, vertical, num_of_problems, i)
        