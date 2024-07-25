import numpy as np
import random
import cv2
import pytesseract
from pytesseract import Output
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

# Path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    image = cv2.imread(image, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 이미지를 회색조로 변환

    # Bilateral Filtering
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    _, binary = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return binary

def PrintText(preImage, is_horizontal, original_image_path):
    if is_horizontal == 'same':
        result_0 = pytesseract.image_to_data(pre_image, lang='eng+kor+math', output_type=Output.DICT)
        DrawBox(preImage, result_0)

    elif is_horizontal:
        rotated_image_0 = preImage
        rotated_image_180, _ = RotateImage(preImage, 180)

        result_0 = pytesseract.image_to_data(rotated_image_0, lang='eng+kor+math', output_type=Output.DICT)
        result_180 = pytesseract.image_to_data(rotated_image_180, lang='eng+kor+math', output_type=Output.DICT)

        text_0, box_0 = count_text(result_0, 0)
        text_180, box_180 = count_text(result_180, 180)

        if text_0 == text_180:
            if box_0 > box_180:
                DrawBox(rotated_image_0, result_0)
            elif box_0 < box_180:
                DrawBox(rotated_image_180, result_180)
            else:
                print(0)
                print("방향을 인식하지 못했습니다.")
        elif text_0 > text_180:
            DrawBox(rotated_image_0, result_0)
        else:
            DrawBox(rotated_image_180, result_180)

    else:
        rotated_image_90, _ = RotateImage(preImage, 90)
        rotated_image_270, _ = RotateImage(preImage, 270)

        result_90 = pytesseract.image_to_data(rotated_image_90, lang='eng+kor+math', output_type=Output.DICT)
        result_270 = pytesseract.image_to_data(rotated_image_270, lang='eng+kor+math', output_type=Output.DICT)

        text_90, box_90 = count_text(result_90, 90)
        text_270, box_270 = count_text(result_270, 270)

        if text_90 == text_270:
            if box_90 > box_270:
                DrawBox(rotated_image_90, result_90)
            elif box_90 < box_270:
                DrawBox(rotated_image_270, result_270)
            else:
                print("방향을 인식하지 못했습니다.")
        elif text_90 > text_270:
            DrawBox(rotated_image_90, result_90)
        else:
            DrawBox(rotated_image_270, result_270)

def count_text(result, angle):
    total_count = 0
    confidence_factor = 0
    box_count = len(result['text'])

    for i in range(box_count):
        if int(result['conf'][i]) > 0:
            text = result['text'][i]
            alnum_hangul_math_count = sum(is_alnum_hangul_math(c) for c in text)
            confidence_factor += int(result['conf'][i]) / 100.0
            total_count += alnum_hangul_math_count

    print(f"Angle: {angle}, Total Count: {total_count}, 인식률: {confidence_factor/box_count}")
    return total_count, confidence_factor

def is_alnum_hangul_math(c):
    return (c.isalnum() or
            ('\uAC00' <= c <= '\uD7A3') or  # 한글
            ('\u2200' <= c <= '\u22FF'))  # 수식 기호 (기본 수학 연산)

def RotateImage(preImage, angle):
    h, w = preImage.shape[:2]  # 높이, 너비
    center = (w / 2, h / 2)  # 중점
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)  # angle이 음수 : 시계 방향, angle이 양수 : 반시계 방향

    # 회전 후 이미지의 크기 계산    
    cos = np.abs(M[0, 0])  # cos(theta)
    sin = np.abs(M[0, 1])  # sin(theta)
    
    # new width and height calculations for arbitrary angles
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    # 각도가 90 또는 270일 경우, 가로, 세로 길이를 바꿔줌
    if angle in [90, 270]:
        new_w, new_h = h, w
    
    # 회전 후에도 모든 픽셀을 포함할 수 있도록 이미지 크기 조정
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    # 보간 방법 선택: cv2.INTER_LINEAR 또는 cv2.INTER_CUBIC 사용    
    rotated_img = cv2.warpAffine(preImage, M, (new_w, new_h), flags=cv2.INTER_LINEAR)
    
    return rotated_img, angle

def DrawBox(preImage, result):
    img_pil = Image.fromarray(cv2.cvtColor(preImage, cv2.COLOR_BGR2RGB))
    font_path = 'Roboto-Black.ttf'
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img_pil)
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(255, 3), dtype="uint8")

    for i in range(len(result['text'])):
        if int(result['conf'][i]) > 0:
            x, y, w, h = (result['left'][i], result['top'][i], result['width'][i], result['height'][i])
            color_idx = random.randint(0, 200)
            color = [int(c) for c in COLORS[color_idx]]
            draw.rectangle(((x, y), (x + w, y + h)), outline=tuple(color), width=2)
            draw.text((x, y - 50), str(result['text'][i]), font=font, fill=tuple(color))

    plt.figure(figsize=(12, 12))
    plt.imshow(img_pil)
    plt.axis('off')
    plt.show()

def analyze_projection(image, results):
    # 텍스트 상자의 좌표를 추출
    text_boxes = [(results['left'][i], results['top'][i], results['width'][i], results['height'][i])
                  for i in range(len(results['text'])) if int(results['conf'][i]) > 0]

    # 신뢰도 수집
    confidences = [int(results['conf'][i]) for i in range(len(results['text'])) if int(results['conf'][i]) > 0]
    average_confidence = np.mean(confidences) if confidences else 0

    print("텍스트 상자 좌표:", text_boxes)
    print("신뢰도 리스트:", confidences)
    print("평균 신뢰도:", average_confidence)

    # 빈도 수를 계산할 수 있도록 텍스트 상자의 y 좌표와 x 좌표를 각각 정렬
    vertical_projection = np.zeros(image.shape[1])  # 열 방향
    horizontal_projection = np.zeros(image.shape[0])  # 행 방향

    for (x, y, w, h) in text_boxes:
        vertical_projection[x:x+w] += 1
        horizontal_projection[y:y+h] += 1

    # 최대 빈도 수
    v_max = np.max(vertical_projection)
    h_max = np.max(horizontal_projection)

    print("v", v_max)
    print("h", h_max)

    # 가로/세로 여부 결정
    if v_max < h_max:
        return True
    elif v_max > h_max:
        return False
    elif v_max == h_max:
        return 'same'

if __name__ == "__main__":
    image_path = 'exam/exam62.jpg'

    pre_image = preprocess_image(image_path)

    # Tesseract OCR를 사용하여 이미지에서 텍스트 인식
    custom_config = r'--oem 3 --psm 6'
    results = pytesseract.image_to_data(pre_image, output_type=pytesseract.Output.DICT, config=custom_config, lang='eng+kor+math')

    is_horizontal = analyze_projection(pre_image, results)
    print("가로입니까? : ", is_horizontal)

    PrintText(pre_image, is_horizontal, image_path)
