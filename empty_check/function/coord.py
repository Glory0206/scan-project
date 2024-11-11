# coord

from PIL import Image
import cv2
import numpy as np

def box_check(coord_top_left, pass_text=True): # 첫 문제의 가로, 세로 길이
    if abs(coord_top_left[0][1] - coord_top_left[1][1]) < 100: # [문제] 외에 인식된 경우를 넘기기 위함
        x1, y1 = coord_top_left[0][0], coord_top_left[0][1]
        x2, y2 = coord_top_left[1][0], coord_top_left[2][1]
        pass_text = True
    else:
        x1, y1 = coord_top_left[1][0], coord_top_left[1][1]
        x2, y2 = coord_top_left[2][0], coord_top_left[3][1]
        pass_text = False

    horizontal = x2 - x1 # 가로 길이
    vertical = y2 - y1 # 세로 길이

    return horizontal, vertical, pass_text

def crop_image(preprocess_image, coord_top_left, horizontal, vertical, i):
    image = Image.fromarray(preprocess_image)
    
    x1, y1 = coord_top_left[i]
    x2 = x1 + horizontal
    y2 = y1 + vertical

    # 이미지 자르기
    cropped_image = image.crop((x1, y1, x2, y2))
    cropped_image_np = np.array(cropped_image)

    cv2.imwrite(f"cropped_resized_image{i}.jpg", cropped_image_np)

    return cropped_image