import easyocr
import cv2
import re

def find_text_coordinates_easyocr(image, target_texts=['[', ']']):  # '[]' 안에 있는 '문제'의 정보를 가져오기 위함
    reader = easyocr.Reader(['ko', 'en'])

    results = reader.readtext(image)

    coord_top_left = []
    coord_bottom_right = []
    numbers = []

    # 인식된 텍스트와 각 텍스트의 좌표 출력
    print("전체 인식된 한글 텍스트 및 좌표:")
    for (bbox, text, prob) in results:
        # bbox는 네 개의 꼭지점 좌표를 포함 (좌상단, 우상단, 우하단, 좌하단)

        # 공백을 제거하고 '문제' 텍스트의 좌표 찾기
        clean_text = text.replace(" ", "")
        
        if any(target in clean_text for target in target_texts):
            # 텍스트의 좌상단, 우하단 좌표를 사용하여 사각형 그리기
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            print(f"'{text}' 텍스트의 좌표: 좌상단 {top_left}, 우하단 {bottom_right}")

            number = re.findall(r'\d+', text)  # 숫자를 모두 찾기

            if number:
                if len(number) == 1:
                    numbers.append(number)
                    coord_top_left.append(top_left)
                    coord_bottom_right.append(bottom_right)

            # 네모박스 그리기
            # cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    print("문제들: ",numbers)

    return coord_top_left, coord_bottom_right, numbers
