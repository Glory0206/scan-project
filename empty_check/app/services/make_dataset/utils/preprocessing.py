import cv2
import numpy as np

def preprocess_image(page_image):
    # gray Scale 적용
    open_cv_image = np.array(page_image)
    image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)

    return image