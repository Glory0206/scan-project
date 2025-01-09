from app.make_datast.random_rotate import random_rotate
from app.blank.find_text import find_texts
from app.make_datast.write import write_problem, write_sign
from app.make_datast.preprocessing import preprocess_image
from app.blank.coord import problem_box_check, small_box
import os

def make_dataset(reader, image, count, file_name):
    images = random_rotate(image, count)

    preprocess_images = []

    for i in range(len(images)):
        preprocess_images.append(preprocess_image(images[i]))

    coord_top_left, coord_bottom_right, numbers, sign_box = find_texts(reader, preprocess_images[0])
    num_of_problems = len(numbers)

    horizontal, vertical = problem_box_check(coord_top_left)

    small_horizontal, small_vertical = small_box(coord_top_left[0], coord_bottom_right[0])

    horizontal -= small_horizontal
    vertical -= small_vertical

    print("문제의 개수",num_of_problems)

    if sign_box == []:
        for i in range(len(preprocess_images)):
            write_problem(images[i], file_name, coord_top_left, horizontal, vertical, num_of_problems, i)
    else:
        sign_written_image = []

        for i in range(len(preprocess_images)):
            sign_written_image = write_sign(images[i], sign_box)
            write_problem(sign_written_image, file_name, coord_top_left, horizontal, vertical, num_of_problems, i)
