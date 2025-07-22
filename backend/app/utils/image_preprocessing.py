import cv2
import numpy as np

def preprocess_image(image):
    open_cv_image = np.array(image)
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    return gray_image 