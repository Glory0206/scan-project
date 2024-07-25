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
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # 이미지를 회색조로
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Otsu's Binarization
    _, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)

    return binary

def PrintText(preImage, is_horizontal, original_image_path):
    if is_horizontal:
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
    h, w = preImage.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
    
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    
    # new width and height calculations for arbitrary angles
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    # If angle is 90 or 270, swap width and height
    if angle in [90, 270]:
        new_w, new_h = h, w
    
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    
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

def analyze_projection(image):
    vertical_projection = np.sum(image, axis=0) # 각 열의 픽셀 값의 합
    horizontal_projection = np.sum(image, axis=1) # 각 행의 픽셀 값의 합
    v_max = np.max(vertical_projection) # 크기가 가장 큰 열의 값
    h_max = np.max(horizontal_projection) # 크기가 가장 큰 행의 값

    print("v",v_max)
    print("h",h_max)

    return v_max <= h_max

def get_osd_orientation(edged):
    # pytesseract로부터 반환된 텍스트 방향(OSD) 가져오기
    orientation = pytesseract.image_to_osd(edged)
    print(orientation)

    # 문자열에서 각도 추출
    angle_start_idx = orientation.find('Rotate: ') + len('Rotate: ')
    angle_end_idx = orientation.find('\n', angle_start_idx)
    rotation_angle = int(orientation[angle_start_idx:angle_end_idx])
    print(rotation_angle)

def find_text_contours(image, results):    
    text_contours = []
    # 각 텍스트 블록에 대해 반복
    for i in range(len(results['text'])):
        x = results['left'][i]    # 텍스트 블록의 왼쪽 상단 x 좌표
        y = results['top'][i]     # 텍스트 블록의 왼쪽 상단 y 좌표
        w = results['width'][i]   # 텍스트 블록의 너비
        h = results['height'][i]  # 텍스트 블록의 높이
        
        # 인식 신뢰도(confidence)가 0보다 큰 경우에만 처리
        if int(results['conf'][i]) > 0:
            roi = image[y:y+h, x:x+w]  # 이미지에서 텍스트 블록의 ROI 추출
            contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # 각 외곽선의 좌표를 전체 이미지 좌표로 변환하여 리스트에 추가
            for cnt in contours:
                cnt[:, 0, 0] += x  # ROI에서 전체 이미지 좌표로 x 좌표 변환
                cnt[:, 0, 1] += y  # ROI에서 전체 이미지 좌표로 y 좌표 변환
                text_contours.append(cnt)
    
    return text_contours

if __name__ == "__main__":
    image_path = 'exam/exam54.jpg'

    pre_image = preprocess_image(image_path)

    # Tesseract OCR를 사용하여 이미지에서 텍스트 인식
    custom_config = r'--oem 3 --psm 6'
    results = pytesseract.image_to_data(pre_image, output_type=pytesseract.Output.DICT, config=custom_config, lang='eng+kor+math')

    is_horizontal = analyze_projection(pre_image)
    print("가로입니까? : ", is_horizontal)

    contours = find_text_contours(pre_image, results)

    # Uncomment if you need to use OSD orientation
    # get_osd_orientation(preImage)

    PrintText(pre_image, is_horizontal, image_path)
