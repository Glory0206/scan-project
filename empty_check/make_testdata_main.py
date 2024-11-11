from testdata.function.random_rotate import random_rotate
from function.word_check import find_text_coordinates_easyocr
from testdata.function.write import write
from testdata.function.preprocessing import preprocess_image
from function.coord import box_check

pdf_path = 'dataset/original_data/삼육대2_B.pdf'
print(pdf_path[22:])

# 앞면, 뒷면 구분
if 'F' in pdf_path[22 :]:
    temp = 'F'
else:
    temp = 'B'

images = random_rotate(pdf_path)

preprocess_images = []

for i in range(len(images)):
    preprocess_images.append(preprocess_image(images[i]))

coord_top_left, coord_bottom_right, num_of_ploblems = find_text_coordinates_easyocr(preprocess_images[0], temp)
print("문제의 개수",num_of_ploblems)

for i in range(len(preprocess_images)):
    horizontal, vertical, pass_text = box_check(coord_top_left)

    write(images[i], coord_top_left, horizontal, vertical, num_of_ploblems, i)