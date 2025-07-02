# preprocessing

import cv2
import numpy as np

def preprocessing(image, dpi=500):
    # 이미지 객체를 OpenCV 형식으로 변환
    open_cv_image = np.array(image)
    image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)

    return image
