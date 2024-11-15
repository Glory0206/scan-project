# coord

from PIL import Image
import cv2
import numpy as np

def box_check(coord_top_left): # 첫 문제의 가로, 세로 길이
    if abs(coord_top_left[0][1] - coord_top_left[1][1]) < 100: # [문제] 외에 인식된 경우를 넘기기 위함
        x1, y1 = coord_top_left[0][0], coord_top_left[0][1]
        x2, y2 = coord_top_left[1][0], coord_top_left[2][1]
    else:
        x1, y1 = coord_top_left[1][0], coord_top_left[1][1]
        x2, y2 = coord_top_left[2][0], coord_top_left[3][1]

    horizontal = x2 - x1 # 가로 길이
    vertical = y2 - y1 # 세로 길이

    return horizontal, vertical

def small_box(coord_top_left, coord_bottom_right):
    horizontal = coord_bottom_right[0] - coord_top_left[0]
    vertical = coord_bottom_right[1] - coord_top_left[1]

    return horizontal, vertical

def crop_image(preprocess_image, coord_top_left, coord_bottom_right, horizontal, vertical, i, alpha=20):
    masked_image = cv2.rectangle(preprocess_image, coord_top_left[i], coord_bottom_right[i], (255, 255, 255), thickness=cv2.FILLED)
    image = Image.fromarray(masked_image)
    # image = Image.fromarray(preprocess_image)
    
    x1, y1 = coord_top_left[i]
    y1 += alpha
    x2 = x1 + horizontal
    y2 = y1 + vertical - alpha

    # 이미지 자르기
    cropped_image = image.crop((x1, y1, x2, y2))
    cropped_image_np = np.array(cropped_image)

    cv2.imwrite(f"cropped_resized_image{i}.jpg", cropped_image_np)

    return cropped_image
