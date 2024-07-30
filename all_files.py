import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import random
import os
from glob import glob

class Resize(object):
    def __init__(self, target_height, target_width):
        self.target_height = target_height
        self.target_width = target_width
    
    def __call__(self, inp):
        img = inp['img']
        h, w = img.shape  # 원본 이미지의 높이와 너비
        
        inp['org_height'] = h
        inp['org_width'] = w
        
        scale_height = self.target_height / h  # 목표 높이와 원본 높이의 비율
        scale_width = self.target_width / w  # 목표 너비와 원본 너비의 비율
        scale = min(scale_height, scale_width)  # 비율 계산
        
        new_h = int(h * scale)
        new_w = int(w * scale)
        
        resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        
        # 목표 크기에 맞게 패딩을 추가
        padded_img = np.ones((self.target_height, self.target_width), dtype=np.uint8) * 255  # 흰색 배경
        y_offset = (self.target_height - new_h) // 2
        x_offset = (self.target_width - new_w) // 2
        
        # 패딩된 이미지에 조정된 이미지 중앙에 배치
        padded_img[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_img
        
        inp['img'] = padded_img
        return inp
    
def process_image(image_path):
    binary_image = preprocess_image(image_path)

    # 텍스트 영역의 윤곽선
    boxes = extract_text_boxes(binary_image)
    
    # 텍스트 영역 크롭 및 리사이즈
    processed_image = crop_and_resize_image(binary_image, boxes)

    # 결과 반전 (흰색 바탕에 검은 글씨)
    inverted_binary = cv2.bitwise_not(processed_image)
    
    return inverted_binary

def preprocess_image(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 이미지를 회색조로 변환
    
    # Bilateral Filtering
    filtered = cv2.bilateralFilter(gray, 24, 75, 75)

    _, binary = cv2.threshold(filtered, 127, 255, cv2.THRESH_BINARY_INV)
    # binary = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    return binary

def extract_text_boxes(binary_image):
    # 텍스트 영역의 윤곽선 찾기
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append((x, y, w, h))
    # print("box", boxes)
    
    return boxes

def box_debug(image, boxes, color=(0, 0, 255), thickness=2):
    image_with_boxes = image.copy()
    for box in boxes:
        x, y, w, h = box
        cv2.rectangle(image_with_boxes, (x, y), (x + w, y + h), color, thickness)
    return image_with_boxes

def crop_and_resize_image(binary_image, boxes):
    if not boxes:
        return binary_image

    # 모든 텍스트 영역을 포함하는 사각형을 계산
    min_x = min(box[0] for box in boxes)
    min_y = min(box[1] for box in boxes)
    max_x = max(box[0] + box[2] for box in boxes)
    max_y = max(box[1] + box[3] for box in boxes)
    
    # 텍스트가 포함된 전체 영역을 크롭
    cropped_image = binary_image[min_y:max_y, min_x:max_x]
    
    # 크롭된 이미지의 높이와 너비
    h, w = cropped_image.shape[:2]
    
    resized_img = cv2.resize(cropped_image, (w, h), interpolation=cv2.INTER_CUBIC)

    return resized_img

def analyze_projection(image, results, ocr):
    if ocr == 0:
        # 텍스트 상자의 좌표를 추출
        text_boxes = [(results['left'][i], results['top'][i], results['width'][i], results['height'][i])
                    for i in range(len(results['text'])) if int(results['conf'][i]) > 0]
    else:
        # 텍스트 상자의 좌표를 추출
        text_boxes = []
        for result in results:
            (top_left, top_right, bottom_right, bottom_left) = result[0]
            x_min, y_min = map(int, top_left)  # 정수로 변환
            x_max, y_max = map(int, bottom_right)  # 정수로 변환
            width = x_max - x_min
            height = y_max - y_min
            text_boxes.append((x_min, y_min, width, height))

    # 빈도 수를 계산할 수 있도록 텍스트 상자의 y 좌표와 x 좌표를 각각 정렬
    vertical_projection = np.zeros(image.shape[1])  # 열 방향
    horizontal_projection = np.zeros(image.shape[0])  # 행 방향

    for (x, y, w, h) in text_boxes:
        vertical_projection[x:x+w] += 1
        horizontal_projection[y:y+h] += 1

    # 최대 빈도 수
    v_max = np.max(vertical_projection)
    h_max = np.max(horizontal_projection)

    # 가로/세로 여부 결정
    if v_max < h_max:
        return True
    elif v_max > h_max:
        return False
    elif v_max == h_max:
        return 'same'

def PrintText(preImage, is_horizontal, original_image_path, ocr):
    if is_horizontal == 'same':
        if ocr == 0:
            result_0 = pytesseract.image_to_data(preImage, lang='eng+kor+math', output_type=Output.DICT)
        else:
            result_0 = reader.readtext(preImage)
        DrawBox(preImage, result_0, ocr)
        return 0

    elif is_horizontal:
        rotated_image_0 = preImage
        rotated_image_180, _ = RotateImage(preImage, 180)

        if ocr == 0:
            result_0 = pytesseract.image_to_data(rotated_image_0, lang='eng+kor+math', output_type=Output.DICT)
            result_180 = pytesseract.image_to_data(rotated_image_180, lang='eng+kor+math', output_type=Output.DICT)
        else:
            result_0 = reader.readtext(rotated_image_0)
            result_180 = reader.readtext(rotated_image_180)

        text_0, box_0 = count_text(result_0, 0, ocr)
        text_180, box_180 = count_text(result_180, 180, ocr)

        if text_0 == text_180:
            if box_0 > box_180:
                DrawBox(rotated_image_0, result_0, ocr)
                rotate_and_save_image(original_image_path, 0)
                return 0
            elif box_0 < box_180:
                DrawBox(rotated_image_180, result_180, ocr)
                rotate_and_save_image(original_image_path, 180)
                return 180
            else:
                print("방향을 인식하지 못했습니다.")
        elif text_0 > text_180:
            DrawBox(rotated_image_0, result_0, ocr)
            rotate_and_save_image(original_image_path, 0)
            return 0
        else:
            DrawBox(rotated_image_180, result_180, ocr)
            rotate_and_save_image(original_image_path, 180)
            return 180

    else:
        rotated_image_90, _ = RotateImage(preImage, 90)
        rotated_image_270, _ = RotateImage(preImage, 270)

        if ocr == 0:
            result_90 = pytesseract.image_to_data(rotated_image_90, lang='eng+kor+math', output_type=Output.DICT)
            result_270 = pytesseract.image_to_data(rotated_image_270, lang='eng+kor+math', output_type=Output.DICT)
        else:
            result_90 = reader.readtext(rotated_image_90)
            result_270 = reader.readtext(rotated_image_270)

        text_90, box_90 = count_text(result_90, 90, ocr)
        text_270, box_270 = count_text(result_270, 270, ocr)

        if text_90 == text_270:
            if box_90 > box_270:
                DrawBox(rotated_image_90, result_90, ocr)
                rotate_and_save_image(original_image_path, 90)
                return 90
            elif box_90 < box_270:
                DrawBox(rotated_image_270, result_270, ocr)
                rotate_and_save_image(original_image_path, 270)
                return 270
            else:
                print("방향을 인식하지 못했습니다.")
        elif text_90 > text_270:
            DrawBox(rotated_image_90, result_90, ocr)
            rotate_and_save_image(original_image_path, 90)
            return 90
        else:
            DrawBox(rotated_image_270, result_270, ocr)
            rotate_and_save_image(original_image_path, 270)
            return 270

def count_text(result, angle, ocr):
    total_count = 0
    confidence_factor = 0

    if ocr == 0:
        box_count = len(result['text'])

        for i in range(box_count):
            if int(result['conf'][i]) > 0:
                text = result['text'][i]
                alnum_hangul_math_count = sum(is_alnum_hangul_math(c) for c in text)
                confidence_factor += int(result['conf'][i]) / 100.0
                total_count += alnum_hangul_math_count
    else:
        box_count = len(result)

        for result in result:
            text = result[1]
            alnum_hangul_math_count = sum(is_alnum_hangul_math(c) for c in text)
            confidence_factor += result[2] / 100.0
            total_count += alnum_hangul_math_count        

    print(f"Angle: {angle}, Total Count: {total_count}, 인식률: {confidence_factor/box_count}")
    return total_count, confidence_factor

def is_alnum_hangul_math(c):
    return (c.isalnum() or
            ('\uAC00' <= c <= '\uD7A3') or  # 한글
            ('\u2200' <= c <= '\u22FF'))  # 수식 기호 (기본 수학 연산)

def RotateImage(image, angle):
    h, w = image.shape[:2]  # 높이, 너비
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
    rotated_img = cv2.warpAffine(image, M, (new_w, new_h), flags=cv2.INTER_LINEAR)
    
    return rotated_img, angle

def rotate_and_save_image(image_path, angle):
    image = cv2.imread(image_path)
    rotated_image, _ = RotateImage(image, angle)
    
    # Save to the 'result' directory
    result_dir = 'result'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        
    file_name = os.path.basename(image_path)
    result_path = os.path.join(result_dir, f"{os.path.splitext(file_name)[0]}.jpg")
    
    cv2.imwrite(result_path, rotated_image)
    print(f"회전된 이미지가 저장되었습니다: {result_path}")

def DrawBox(preImage, results, ocr):
    img_pil = Image.fromarray(cv2.cvtColor(preImage, cv2.COLOR_BGR2RGB))
    font_path = 'Roboto-Black.ttf'  # 글꼴 파일 경로
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img_pil)
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(255, 3), dtype="uint8")

    if ocr == 0:
        for i in range(len(results['text'])):
            if int(results['conf'][i]) > 0:
                x, y, w, h = (results['left'][i], results['top'][i], results['width'][i], results['height'][i])
                color_idx = random.randint(0, 200)
                color = [int(c) for c in COLORS[color_idx]]
                draw.rectangle(((x, y), (x + w, y + h)), outline=tuple(color), width=2)
                draw.text((x, y - 50), str(results['text'][i]), font=font, fill=tuple(color))
    else:
        for result in results:
            bbox, text, _ = result
            (x_min, y_min), (x_max, y_max) = bbox[0], bbox[2]
            color_idx = random.randint(0, 200)
            color = [int(c) for c in COLORS[color_idx]]
            draw.rectangle(((x_min, y_min), (x_max, y_max)), outline=tuple(color), width=2)
            draw.text((x_min, y_min - 50), str(text), font=font, fill=tuple(color))

def process_and_rotate_images(input_folder, select_ocr):
    image_paths = glob(os.path.join(input_folder, '*.jpg')) + glob(os.path.join(input_folder, '*.png'))

    for image_path in image_paths:
        print(f"Processing {image_path}...")
        # 텍스트에 대해 윤곽선을 잡은 후 해장 부분 crop, resize
        processed_image = process_image(image_path)

        if select_ocr == 0:
            results = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT, config=custom_config, lang='eng+kor+math')

        elif select_ocr == 1:
            # EasyOCR를 사용하여 이미지에서 텍스트 인식
            results = reader.readtext(processed_image)
        
        is_horizontal = analyze_projection(processed_image, results, select_ocr)
        print("가로입니까? : ", is_horizontal)
        
        angle = PrintText(processed_image, is_horizontal, image_path, select_ocr)
        print(f"회전 각도: {angle}")

if __name__ == "__main__":
    input_folder = 'exam'

    print("Tesseract : 0   EasyOCR : 1")
    select_ocr = int(input("OCR : "))

    if select_ocr == 0:
        import pytesseract
        from pytesseract import Output
        # Path
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # Tesseract OCR를 사용하여 이미지에서 텍스트 인식
        custom_config = r'--oem 3 --psm 6'
    elif select_ocr == 1:
        import easyocr

        reader = easyocr.Reader(['en', 'ko'])  # 사용할 언어 설정

    process_and_rotate_images(input_folder, select_ocr)
