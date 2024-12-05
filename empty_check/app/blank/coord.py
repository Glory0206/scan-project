# coord

from PIL import Image
import cv2
import numpy as np

def problem_box_check(coord_top_left): # 첫 문제의 가로, 세로 길이
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

def crop_problems_image(rgb_image, preprocess_image, coord_top_left, coord_bottom_right, horizontal, vertical, i, alpha=20):
    # 마스킹 처리된 이미지 생성
    masked_image = cv2.rectangle(preprocess_image.copy(), coord_top_left[i], coord_bottom_right[i], (255, 255, 255), thickness=cv2.FILLED)
    image = Image.fromarray(masked_image)
    
    # 원본 이미지를 Pillow로 변환
    origin_image = Image.fromarray(rgb_image)

    # 크롭 영역 설정
    x1, y1 = coord_top_left[i]
    y1 += alpha
    x2 = x1 + horizontal
    y2 = y1 + vertical - alpha

    # 마스킹된 이미지 크롭
    cropped_masked_image = image.crop((x1, y1, x2, y2))
    cropped_masked_image_np = np.array(cropped_masked_image)

    origin_x1, origin_y1 = coord_top_left[i]
    origin_x2, origin_y2 = x2, y2

    # 원본 이미지 크롭
    cropped_original_image = origin_image.crop((origin_x1, origin_y1, origin_x2, origin_y2))
    cropped_original_image_np = np.array(cropped_original_image)

    return cropped_masked_image_np, cropped_original_image_np


def crop_sign_image(rgb_image, preprocess_image, sign_box):
    image = Image.fromarray(preprocess_image)
    rgb_image = Image.fromarray(rgb_image)

    top_left = sign_box[0]
    bottom_right = sign_box[1]

    x1, y1 = top_left[0] + 165 ,top_left[1]
    x2, y2 = bottom_right[0] + 330, bottom_right[1] + 38

    image_with_box = preprocess_image.copy()
    #cv2.rectangle(image_with_box, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #cv2.imwrite("image_with_box.jpg", image_with_box)

    cropped_image = image.crop((x1, y1, x2, y2))
    cropped_image_np = np.array(cropped_image)
    
    origin_x1, origin_y1 = top_left
    origin_x2, origin_y2 = x2, y2
    
    cropped_origin_image = rgb_image.crop((origin_x1, origin_y1, origin_x2, origin_y2))
    origin_image_np = np.array(cropped_origin_image)

    #cv2.imwrite(f"sign_image.jpg", cropped_image_np)

    return cropped_image_np, origin_image_np