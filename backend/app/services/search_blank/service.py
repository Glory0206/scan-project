from app.utils.image_preprocessing import preprocess_image
from app.utils.find_text import find_texts
from app.utils.coord import problem_box_check, crop_problems_image, small_box, crop_sign_image
from app.services.search_blank.utils.blank import is_image_blank
from app.services.search_blank.utils.numbering import sorting
import base64
import cv2

CHECK_SUPERVISOR = '감독관 확인'

# 템플릿 추출 함수 (요청 당 1회 호출)
def extract_template_info(template_image):
    preprocessed_image = preprocess_image(template_image)

    # 텍스트 찾기
    coord_top_left, coord_bottom_right, numbers, sign_box = find_texts(preprocessed_image)

    # 박스 크기 계산
    small_horizontal, small_vertical = small_box(coord_top_left[1], coord_bottom_right[1])
    horizontal, vertical = problem_box_check(coord_top_left)

    # 길이 조정
    horizontal -= small_horizontal
    vertical -= small_vertical

    problems_count = len(coord_top_left)

    # 추출된 템플릿 정보를 딕셔너리로 반환
    template_info = {
        "coord_top_left": coord_top_left,
        "coord_bottom_right": coord_bottom_right,
        "numbers": numbers,
        "sign_box": sign_box,
        "horizontal": horizontal,
        "vertical": vertical,
        "problems_count": problems_count
    }
    return template_info

# 템플릿 적용 분석 함수 (이미지 당 1회 호출)
def analyze_image_with_template(image, template_info):
    masked_images = []
    origin_images = []
    blanks = []

    # 원본 이미지 전처리 (크롭을 위해 필요)
    preprocessed_image = preprocess_image(image)

    # 템플릿 정보 언패킹
    coord_top_left = template_info["coord_top_left"]
    coord_bottom_right = template_info["coord_bottom_right"]
    sign_box = template_info["sign_box"]
    horizontal = template_info["horizontal"]
    vertical = template_info["vertical"]
    problems_count = template_info["problems_count"]
    
    # numbers 리스트는 insert로 수정되므로, 원본을 건드리지 않게 복사해서 사용
    numbers = list(template_info["numbers"]) 

    # 감독관 서명란 크롭
    if sign_box:
        sign_image, origin_sign_image = crop_sign_image(image, preprocessed_image, sign_box)
        masked_images.append(sign_image)
        origin_images.append(origin_sign_image)
        numbers.insert(0, CHECK_SUPERVISOR)

    # 문제란 크롭
    for i in range(problems_count):
        masked_cropped_image, cropped_origin_image = crop_problems_image(
            image, preprocessed_image, coord_top_left, coord_bottom_right, horizontal, vertical, i
        )
        masked_images.append(masked_cropped_image)
        origin_images.append(cropped_origin_image)

    # 빈칸 여부 확인
    for i in range(len(masked_images)):
        blank = is_image_blank(masked_images[i], numbers[i])
        blanks.append(blank)

    # 정렬
    numbers_list, blanks_list, images_list = sorting(numbers, blanks, origin_images)
    
    return images_list, numbers_list, blanks_list

# 응답 포맷팅 헬퍼 함수
def format_analysis_results(images_list, numbers_list, blanks_list):
    formatted_results = []
    for idx, cropped_image in enumerate(images_list):
        # 이미지 데이터를 Base64로 변환
        _, buffer = cv2.imencode('.jpg', cropped_image)
        base64_image = base64.b64encode(buffer).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{base64_image}"
        
        # 구조화된 데이터 추가
        formatted_results.append({
            "areaName": numbers_list[idx],
            "isBlank": blanks_list[idx],
            "croppedImage": data_uri
        })
    return formatted_results