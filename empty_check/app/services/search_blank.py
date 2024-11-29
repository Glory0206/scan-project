import os
from app.blank.preprocessing import preprocessing
from app.blank.find_text import find_texts
from app.blank.coord import problem_box_check, crop_image, small_box
from app.blank.blank import is_image_blank
from app.blank.numbering import sorting

def searching(image):
    images = [] # crop된 이미지들을 담는 list
    blanks = []

    preprocess_image = preprocessing(image)

    coord_top_left, coord_bottom_right, numbers = find_texts(preprocess_image)

    small_horizontal, small_vertical = small_box(coord_top_left[1], coord_bottom_right[1]) # '문제' 텍스트의 가로, 세로 길이

    horizontal, vertical= problem_box_check(coord_top_left) # 문제란의 가로, 세로 길이

    # 길이 조정
    horizontal -= small_horizontal
    vertical -= small_vertical

    problems_count = len(coord_top_left)

    for i in range(problems_count):
        cropped_image = crop_image(preprocess_image, coord_top_left, coord_bottom_right, horizontal, vertical, i)
        images.append(cropped_image)

    for i in range(len(images)):
        blank = is_image_blank(images[i], numbers[i])
        blanks.append(blank)

    numbers_list, blanks_list = sorting(numbers, blanks)
    
    return images, numbers_list, blanks_list
