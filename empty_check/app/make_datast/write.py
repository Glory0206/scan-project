import cv2
import random

def write_problem(image, file_name, coord_top_left, horizontal, vertical, num_of_problems, num):
    for i in range(num_of_problems):
        use = random.randint(0, 1)  # 0 또는 1(답안을 적을지 말지 체크)
        
        if use == 1:
            # 좌상단 좌표와 우하단 좌표를 분리
            x1, y1 = coord_top_left[i][0] + horizontal, coord_top_left[i][1] + vertical

            # 가운데 좌표 계산
            center_x = (coord_top_left[i][0] + x1) // 2
            center_y = (coord_top_left[i][1] + y1) // 2

            # 이미지에 텍스트 작성
            texts = ["Hello\n2025", "2a + 3y", "a - d - c", "Glory\n2001", "Succes in not final,\nfailure is not fatal", "1", "105 / 3 = 35"]
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2
            font_color = (0, 0, 0)  # (B, G, R)
            thickness = 5

            random_text = texts[random.randint(0, len(texts) - 1)]

            # 텍스트를 줄바꿈 문자 기준으로 분할
            lines = random_text.split('\n')

            # 각 줄을 순차적으로 작성
            # y_offset은 중심에서부터 시작하여 텍스트 높이만큼 조정
            text_height = cv2.getTextSize(lines[0], font, font_scale, thickness)[0][1]
            y_offset = center_y - (len(lines) - 1) * (text_height // 2)

            for line in lines:
                # 텍스트 크기 계산
                text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
                text_width, text_height = text_size

                # 텍스트가 문제의 가운데에 오도록 x 좌표 조정
                adjusted_x = center_x - (text_width // 2)

                # 각 줄의 y 좌표는 y_offset부터 시작해서 줄 간격만큼 증가
                cv2.putText(image, line, (adjusted_x, y_offset), font, font_scale, font_color, thickness, cv2.LINE_AA)
                y_offset += text_height + 30  # 줄 간격을 적절히 조정(30 픽셀)

    # 이미지 저장
    cv2.imwrite(f"storage/{file_name}_{num}.jpg", image)

def write_sign(preprocess_image, sign_box):
    use = random.randint(0, 1)
    if use == 1:
        top_left = sign_box[0]
        bottom_right = sign_box[1]

        x1, y1 = top_left[0] + 165, top_left[1]
        x2, y2 = bottom_right[0] + 330, bottom_right[1] + 38    

        # 중심 좌표 계산
        center_x = x1 + (x2 - x1) // 2
        center_y = y1 + (y2 - y1) // 2

        # 텍스트 추가할 이미지 복사
        image_with_text = preprocess_image.copy()

        # 텍스트 추가
        texts = ["Glory", "David", "Sebastian", "Milk", "Richard"]
        random_number = random.randint(0,len(texts)-1)
        text = texts[random_number]
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0, 0, 0)
        thickness = 2

        # 중심 좌표 기준으로 텍스트 삽입 (좌상단 좌표로 변환)
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = center_x - text_size[0] // 2  # 텍스트 가로 중심
        text_y = center_y + text_size[1] // 2  # 텍스트 세로 중심

        cv2.putText(image_with_text, text, (text_x, text_y), font, font_scale, font_color, thickness)

        return image_with_text
    else:
        return preprocess_image