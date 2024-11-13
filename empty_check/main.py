# main

import os
from function.preprocessing import preprocessing
from function.word_check import find_text_coordinates_easyocr
from function.coord import box_check, crop_image, small_box
from function.blank import is_image_blank

images = [] # crop된 이미지들을 담는 list

image_path = 'dataset/test_datas/Sahmyook2_F_4.jpg'
file_name = os.path.splitext(os.path.basename(image_path))[0]
print(file_name)

# 앞면, 뒷면 구분
if 'F' in file_name:
    temp = 'F'
else:
    temp = 'B'

preprocess_image = preprocessing(image_path)

coord_top_left, coord_bottom_right, numbers = find_text_coordinates_easyocr(preprocess_image, temp)

small_horizontal, small_vertical = small_box(coord_top_left[1], coord_bottom_right[1]) # '문제' 텍스트의 가로, 세로 길이

horizontal, vertical= box_check(coord_top_left) # 문제란의 가로, 세로 길이

# 길이 조정
horizontal -= small_horizontal
vertical -= small_vertical

for i in range(len(coord_top_left)):
    cropped_image = crop_image(preprocess_image, coord_top_left, coord_bottom_right, horizontal, vertical, i)
    images.append(cropped_image)

for i in range(len(images)):
    is_image_blank(images[i], numbers[i])