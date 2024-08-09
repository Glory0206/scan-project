# dataset.py
import cv2
import numpy as np
# import matplotlib.pyplot as plt
from torch.utils.data import Dataset
from torchvision import transforms

def process_image(image_path):
    binary_image = preprocess_image(image_path)

    # 텍스트 영역의 윤곽선
    boxes = extract_text_boxes(binary_image)
    
    # 텍스트 영역 크롭 및 리사이즈
    processed_image = crop_and_resize_image(binary_image, boxes)
    
    return processed_image

def preprocess_image(image):
    # 이미지 읽기
    # image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 이미지를 회색조로 변환
    
    # Bilateral Filtering
    filtered = cv2.bilateralFilter(gray, 25, 75, 75)

    _, binary = cv2.threshold(filtered, 127, 255, cv2.THRESH_BINARY_INV)

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

class SkewDataset(Dataset):
    def __init__(self, image_paths, angles, transform=None):
        self.image_paths = image_paths
        self.angles = angles
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = cv2.imread(self.image_paths[idx])
        angle = self.angles[idx]

        # Apply preprocessing
        image = process_image(image)

        if self.transform:
            image = self.transform(image)

        return image, angle

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((1440, 1440)),
    transforms.ToTensor(),
])