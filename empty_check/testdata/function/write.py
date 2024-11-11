import cv2
import random

def write(image, coord_top_left, horizontal, vertical, num_of_problems, num):
    for i in range(num_of_problems):
        use = random.randint(0, 1) # 0 또는 1(답안을 적을지 말지 체크)
        
        if use == 1:
            # 좌상단 좌표와 우하단 좌표를 분리
            x1, y1 = coord_top_left[i][0] + horizontal, coord_top_left[i][1] + vertical

            # 가운데 좌표 계산
            center_x = (coord_top_left[i][0] + x1) // 2
            center_y = (coord_top_left[i][1] + y1) // 2

            # 이미지에 텍스트 작성
            texts = ["Hello 2025", "2a + 3y", "a - d - c", "1/2", "Glory"]
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 8
            color = (0, 0, 0)  # (B, G, R)
            thickness = 5

            random_text = texts[random.randint(0, len(texts) - 1)]

            # 텍스트의 크기 계산
            text_size = cv2.getTextSize(random_text, font, font_scale, thickness)[0]
            text_width, text_height = text_size

            # 텍스트가 문제의 가운데에 오도록 조정
            adjusted_x = center_x - (text_width // 2)
            adjusted_y = center_y + (text_height // 2)

            # 텍스트 작성 (조정된 좌표에 작성)
            cv2.putText(image, random_text, (adjusted_x, adjusted_y), font, font_scale, color, thickness, cv2.LINE_AA)


    # 이미지 저장
    cv2.imwrite(f"output_image{num}.jpg", image)