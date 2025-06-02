import cv2
import random
import numpy as np

def random_rotate(image, count):
    images = []

    # 이미지 객체를 OpenCV 형식으로 변환
    open_cv_image = np.array(image)
    for i in range(count): # 생성할 이미지 개수

        # 회전 방향
        direction = random.choice([-1, 1])
        # 회전 정도
        angle = random.uniform(0.1, 0.5)

        angle *= direction
        print("회전 각도",angle)

        # 이미지의 중심 좌표 계산
        (h, w) = open_cv_image.shape[:2]
        center = (w // 2, h // 2)

        # 회전 행렬 생성
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        # 이미지 회전
        rotated_image = cv2.warpAffine(open_cv_image, rotation_matrix, (w, h))

        # 90도 회전 (시계 방향)
        rotated_image = cv2.rotate(rotated_image, cv2.ROTATE_90_CLOCKWISE)
        images.append(rotated_image)
        
    return(images)
