import os
from app.blank.preprocessing import preprocessing
from app.blank.find_text import find_texts
from app.blank.coord import problem_box_check, crop_problems_image, small_box, crop_sign_image
from app.blank.blank import is_image_blank
from app.blank.numbering import sorting

def searching(reader, image):
    masked_images = [] # crop된 이미지들을 담는 list
    origin_images = []
    blanks = []

    preprocess_image = preprocessing(image)

    coord_top_left, coord_bottom_right, numbers, sign_box = find_texts(reader, preprocess_image)

    small_horizontal, small_vertical = small_box(coord_top_left[1], coord_bottom_right[1]) # '문제' 텍스트의 가로, 세로 길이

    horizontal, vertical= problem_box_check(coord_top_left) # 문제란의 가로, 세로 길이

    # 길이 조정
    horizontal -= small_horizontal
    vertical -= small_vertical

    problems_count = len(coord_top_left)

    if sign_box != []:
        sign_image, origin_sign_image = crop_sign_image(image, preprocess_image, sign_box)
        masked_images.append(sign_image)
        origin_images.append(origin_sign_image)
        numbers.insert(0, '감독관 확인')

    for i in range(problems_count):
        masked_cropped_image, cropped_origin_image = crop_problems_image(image, preprocess_image, coord_top_left, coord_bottom_right, horizontal, vertical, i)
        masked_images.append(masked_cropped_image)
        origin_images.append(cropped_origin_image)

    for i in range(len(masked_images)):
        blank = is_image_blank(masked_images[i], numbers[i])
        blanks.append(blank)

    numbers_list, blanks_list, images_list = sorting(numbers, blanks, origin_images)
    
    return images_list, numbers_list, blanks_list
