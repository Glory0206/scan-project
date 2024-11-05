from PIL import Image, ExifTags
import os

from constants import EXAM_FOLDER_PATH, LEFT_TO_RIGHT_FOLDER, TOP_TO_BOTTOM_FOLDER, RIGHT_TO_LEFT_FOLDER, BOTTOM_TO_TOP_FOLDER

def setting():
    # 경로 설정
    exam_folder = EXAM_FOLDER_PATH

    # 라벨링 폴더
    left_to_right_folder = LEFT_TO_RIGHT_FOLDER
    top_to_bottom_folder = TOP_TO_BOTTOM_FOLDER
    right_to_left_folder = RIGHT_TO_LEFT_FOLDER
    bottom_to_top_folder = BOTTOM_TO_TOP_FOLDER

    # 디렉토리가 없는 경우 생성(학습 후 데이터를 지우기 때문)
    os.makedirs(left_to_right_folder, exist_ok=True)
    os.makedirs(top_to_bottom_folder, exist_ok=True)
    os.makedirs(right_to_left_folder, exist_ok=True)
    os.makedirs(bottom_to_top_folder, exist_ok=True)

    # 회전 각도 리스트
    angles = [0, 90, 180, 270]

    # EXIF orientation 태그 가져오기
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    # exam 폴더의 모든 이미지 파일에 대해 처리
    for filename in os.listdir(exam_folder):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):  # 이미지 파일만 처리
            file_path = os.path.join(exam_folder, filename)

            # 이미지 열기
            img = Image.open(file_path)

            # EXIF 데이터 : 카메라 제조사 및 모델, 촬영 날짜 및 시간, 노출 시간, 조리개 값, ISO 감도, 초점 거리, 플래시 상태, 해상도 및 이미지 크기, GPS 데이터, 이미지 방향
            # EXIF 데이터 초기화(이미지의 회전 정보 초기화, 데이터 단순화)
            img_exif = img._getexif()
            if img_exif is not None:
                img_exif = dict(img_exif.items())
                orientation_value = img_exif.get(orientation, None)
                if orientation_value == 3:
                    img = img.rotate(180, expand=True)
                elif orientation_value == 6:
                    img = img.rotate(270, expand=True)
                elif orientation_value == 8:
                    img = img.rotate(90, expand=True)

            # 파일 확장자 추출
            file_extension = os.path.splitext(filename)[1]

            # 파일 이름에서 확장자 제거
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
            
            # 각 각도로 이미지 회전 및 저장
            for i, angle in enumerate(angles):
                new_filename = f"{base_filename}_{i * 90}{file_extension}"

                if i == 0:
                    save_path = os.path.join(left_to_right_folder, new_filename)
                elif i == 1:
                    save_path = os.path.join(top_to_bottom_folder, new_filename)
                elif i == 2:
                    save_path = os.path.join(right_to_left_folder, new_filename)
                elif i == 3:
                    save_path = os.path.join(bottom_to_top_folder, new_filename)

                # 이미지 회전 및 저장
                rotated_img = img.rotate(-angle, expand=True)
                rotated_img.save(save_path)