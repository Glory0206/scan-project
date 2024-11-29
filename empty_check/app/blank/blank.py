import cv2
import numpy as np

def is_image_blank(image, number, min_non_white_pixels=300):
    blanks = []
    image = np.array(image)

    # 임계값을 사용하여 이진화 (흰색은 255, 나머지는 0으로 변환)
    _, binary_image = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)

    # 흰색이 아닌(0인) 픽셀의 수를 계산
    non_white_pixels = np.sum(binary_image == 0)

    # 비흰색 픽셀이 일정 수 이상이면 무언가 적혀 있다고 판단
    if non_white_pixels > min_non_white_pixels:
        blanks.append("N")
        print(f"해당 논술용지의 {number}번은 작성 완료 되었습니다.")
        print(f"{number}번 문제의 픽셀: ",non_white_pixels)
    else:
        blanks.append("T")
        print(f"해당 논술용지의 {number}번 문제는 공백 상태입니다.")
        print(f"{number}번 문제의 픽셀: ",non_white_pixels)
        
    return blanks