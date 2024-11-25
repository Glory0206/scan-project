import os
from app.blank.preprocessing import preprocessing
from app.blank.word_check import find_text_coordinates_easyocr
from app.blank.coord import box_check, crop_image, small_box
from app.blank.blank import is_image_blank

def searching(file_path):
    images = [] # crop된 이미지들을 담는 list
    blanks = []

    image_path = file_path
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    print(file_name)

    preprocess_image = preprocessing(image_path)

    coord_top_left, coord_bottom_right, numbers = find_text_coordinates_easyocr(preprocess_image)

    small_horizontal, small_vertical = small_box(coord_top_left[1], coord_bottom_right[1]) # '문제' 텍스트의 가로, 세로 길이

    horizontal, vertical= box_check(coord_top_left) # 문제란의 가로, 세로 길이

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
    
    return images, numbers, blanks
