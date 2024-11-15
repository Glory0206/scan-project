# preprocessing

import cv2
import numpy as np

def preprocessing(path, dpi=500):
    # PDF 페이지를 이미지로 변환 (한 장만 존재하므로 첫 번째 페이지만 가져옴)
    # page_image = convert_from_path(path, dpi=dpi)[0]

    page_image = cv2.imread(path)

    # 이미지 객체를 OpenCV 형식으로 변환
    open_cv_image = np.array(page_image)
    image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)

    # 90도 회전 (시계 방향)
    # rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    return image
