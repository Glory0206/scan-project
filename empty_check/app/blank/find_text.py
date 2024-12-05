import easyocr
import cv2
import re

def find_texts(image, target_texts=['[', ']']):  # '[]' 안에 있는 '문제'의 정보를 가져오기 위함
    reader = easyocr.Reader(['ko', 'en'])

    results = reader.readtext(image)

    coord_top_left = []
    coord_bottom_right = []
    sign_box = []

    # 인식된 텍스트와 각 텍스트의 좌표 출력
    print("전체 인식된 한글 텍스트 및 좌표:")

    for (bbox, text, prob) in results:
        # bbox는 네 개의 꼭지점 좌표를 포함 (좌상단, 우상단, 우하단, 좌하단)

        # 공백을 제거하고 '문제' 텍스트의 좌표 찾기
        clean_text = text.replace(" ", "")
        # print("인식 문자: ",text)
        
        if any(target in clean_text for target in target_texts):
            # 텍스트의 좌상단, 우하단 좌표를 사용하여 사각형 그리기
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            print(f"'{text}' 텍스트의 좌표: 좌상단 {top_left}, 우하단 {bottom_right}")

            number = re.findall(r'\d+', text)  # 숫자를 모두 찾기

            if number:
                if len(number) == 1:
                    coord_top_left.append(top_left)
                    coord_bottom_right.append(bottom_right)
            elif '문' in text or '제' in text:
                    coord_top_left.append(top_left)
                    coord_bottom_right.append(bottom_right)
        elif any(char in clean_text for char in ['감', '독']):
            if sign_box == []:
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                sign_box = [top_left, bottom_right]

            print(f"'감독 관련 텍스트: {text}'의 좌표: 좌상단 {top_left}, 우하단 {bottom_right}")

            # 네모박스 그리기
            # cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    numbers = refind(image, coord_top_left, coord_bottom_right)

    return coord_top_left, coord_bottom_right, numbers, sign_box
    
def refind(image, coord_top_left, coord_bottom_right):
    reader = easyocr.Reader(['ko', 'en'])
    
    numbers = []  # 숫자를 저장할 리스트
    
    print("\n잘라낸 영역 재분석 결과:")
    for i, (top_left, bottom_right) in enumerate(zip(coord_top_left, coord_bottom_right)):
        x1, y1 = top_left
        x2, y2 = bottom_right
        
        x1 += 10
        x2 -= 9

        # 이미지 자르기
        cropped_image = image[y1:y2, x1:x2]

        # 전처리: 이진화 (Thresholding)
        _, binary = cv2.threshold(cropped_image, 10, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # 전처리된 이미지를 저장
        preprocessed_path = f"preprocessed_cropped_{i + 1}.jpg"
        # cv2.imwrite(preprocessed_path, binary)
        # print(f"박스 {i + 1}: 전처리된 이미지가 '{preprocessed_path}'에 저장되었습니다.")

        # EasyOCR로 다시 인식
        reanalyzed_results = reader.readtext(binary)

        print(f"박스 {i + 1}:")
        for (bbox, re_text, re_prob) in reanalyzed_results:
            print(f"  재인식 문자: '{re_text}', 정확도: {re_prob:.2f}")
            
            # 텍스트에서 숫자 추출
            detected_numbers = re.findall(r'\d+', re_text)
            if detected_numbers:
                numbers.extend(detected_numbers)  # 숫자를 리스트에 추가

        # 전처리된 이미지 보기
        # cv2.imshow(f"박스 {i + 1} (전처리)", binary)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
    return numbers