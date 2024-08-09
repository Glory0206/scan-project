import os
import easyocr
import torch
import torch.nn as nn
import numpy as np
from PIL import Image

class EasyOCRWithSkew(nn.Module):
    def __init__(self):
        super(EasyOCRWithSkew, self).__init__()
        self.reader = easyocr.Reader(['en'])  # EasyOCR 모델 초기화
        self.fc = nn.Linear(256, 4)  # 피처 벡터의 크기는 256, 출력은 4개의 각도 (0, 90, 180, 270도)

    def forward(self, images):
        image_paths = []  # 임시 이미지 파일 경로를 저장할 리스트
        for idx, image in enumerate(images):
            image_np = image.cpu().numpy().transpose(1, 2, 0) # 텐서를 numpy 배열로 변환하고 (C, H, W)를 (H, W, C)로 변경
            image_np = (image_np * 255).astype(np.uint8)  # Normalize된 이미지를 0-255 범위로 스케일링
            
            if image_np.dtype != np.uint8:
                image_np = image_np.astype(np.uint8)
                
            if len(image_np.shape) == 3 and image_np.shape[2] == 1:
                image_np = np.squeeze(image_np, axis=2)  # 이미지가 단일 채널일 경우 채널 축소

            image_path = f"temp_image_{idx}.jpg"  # 임시 파일 경로 생성
            img_pil = Image.fromarray(image_np)  # numpy 배열을 PIL 이미지로 변환
            img_pil.save(image_path)  # 이미지 파일로 저장
            image_paths.append(image_path)  # 파일 경로 리스트에 추가
        
        ocr_results = [self.reader.readtext(image_path, detail=1) for image_path in image_paths]  # OCR로 텍스트의 각도 검출
        print("각도 : ", ocr_results)
        
        for image_path in image_paths:
            os.remove(image_path)  # 임시 파일 삭제
        
        features = self.extract_features(ocr_results)  # OCR 결과에서 피처 추출
        skew_outputs = self.fc(features)  # 피처를 FC 레이어에 전달하여 각도 예측
        return skew_outputs

    def extract_features(self, ocr_results):
        all_features = []
        for result in ocr_results:
            if not result:
                all_features.append(torch.zeros(256))  # OCR 결과가 없을 경우 기본 피처 벡터 추가
                continue

            angles = []
            for item in result:
                if len(item) != 3:
                    print(f"Unexpected format: {item}")  # 예기치 않은 형식의 결과 출력
                    continue

                box, text, confidence = item
                
                # 박스가 4개의 좌표를 가지고 있는지 확인
                if len(box) != 4:
                    print(f"Box does not have 4 points: {box}")  # 좌표가 4개가 아니면 출력
                    continue

                # 좌표 추출
                x1, y1 = box[0]
                x2, y2 = box[1]
                x3, y3 = box[2]
                x4, y4 = box[3]
                
                # 각도 계산
                angle = self.calculate_angle(x1, y1, x2, y2, x3, y3, x4, y4)
                angles.append(angle)

            if not angles:
                angles = [0]  # 각도가 없을 경우 기본값 추가
                
            avg_angle = np.mean(angles)  # 평균 각도 계산
            features = self.angle_to_features(avg_angle)  # 각도를 피처로 변환
            all_features.append(features)
        
        all_features = torch.stack(all_features)  # 리스트를 텐서로 변환
        return all_features

    def calculate_angle(self, x1, y1, x2, y2, x3, y3, x4, y4):
        dx1 = x2 - x1
        dy1 = y2 - y1
        dx2 = x4 - x3
        dy2 = y4 - y3

        angle1 = np.arctan2(dy1, dx1) * (180 / np.pi)  # 첫 번째 각도 계산
        angle2 = np.arctan2(dy2, dx2) * (180 / np.pi)  # 두 번째 각도 계산

        angle = (angle1 + angle2) / 2  # 평균 각도 계산
        angle = (angle + 360) % 360  # 각도를 0-360 범위로 변환

        # 각도 범위에 맞게 조정
        if (0 <= angle < 45) or (315 <= angle < 360):
            return 0
        elif (45 <= angle < 135):
            return 90
        elif (135 <= angle < 225):
            return 180
        elif (225 <= angle < 315):
            return 270

        return 0

    def angle_to_features(self, angle):
        features = torch.zeros(256)  # 피처 벡터 초기화
        angle_label = int(angle / 90) % 4  # 각도를 0, 90, 180, 270으로 매핑하여 인덱스로 변환
        features[angle_label] = 1  # 해당 인덱스에 1을 설정
        return features
