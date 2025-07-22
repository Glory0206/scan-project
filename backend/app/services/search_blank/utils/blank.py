import cv2
import numpy as np

MIN_NON_WHITE_PIXELS = 400
BLANK_WRITTEN = 'N'
BLANK_EMPTY = 'T'

def is_image_blank(image, number, min_non_white_pixels=MIN_NON_WHITE_PIXELS):
    image = np.array(image)

    # 임계값을 사용하여 이진화 (흰색은 255, 나머지는 0으로 변환)
    _, binary_image = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)

    # 흰색이 아닌(0인) 픽셀의 수를 계산
    non_white_pixels = np.sum(binary_image == 0)

    # 비흰색 픽셀이 일정 수 이상이면 무언가 적혀 있다고 판단
    if non_white_pixels > min_non_white_pixels:
        blank = BLANK_WRITTEN
    else:
        blank = BLANK_EMPTY
    
    return blank