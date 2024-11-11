import easyocr
import cv2

def find_text_coordinates_easyocr(image, temp, target_texts=['문제']):  # '문제' 또는 '문 제'의 정보를 가져오기 위함
    reader = easyocr.Reader(['ko', 'en'])

    results = reader.readtext(image)

    num = 0
    coord_top_left = []
    coord_bottom_right = []

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

            coord_top_left.append(top_left)
            coord_bottom_right.append(bottom_right)

            # 네모박스 그리기
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            num += 1

    if temp == 'F' and coord_top_left and coord_bottom_right:
        coord_top_left.pop(0)
        coord_bottom_right.pop(0)
        num -= 1

    print("1", coord_top_left)
    print("2", coord_bottom_right)

    return coord_top_left, coord_bottom_right, num
