import os
import torch
from PIL import Image, ExifTags
from torchvision import transforms
from typing import Optional, List
from services.model import load_model

def correct_orientation(image):
    """이미지의 EXIF 데이터를 확인하여 회전된 이미지를 정방향으로 조정."""
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif: Optional[dict] = image._getexif()
        if exif is not None:
            orientation: Optional[int] = exif.get(orientation)
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass  # EXIF 데이터가 없거나 오류 발생 시 아무 작업도 하지 않음
    return image

def predict_image(image, model, device):
    """이미지의 방향을 예측."""
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    image = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(image)
        _, predicted_direction = torch.max(output.data, 1)
    
    classes = ['bottom_to_top', 'left_to_right', 'right_to_left', 'top_to_bottom']
    return classes[predicted_direction.item()]

def adjust_images_in_folder(folder_path, model):
    """폴더 내 모든 이미지를 예측하여 회전 및 저장."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()

    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path).convert('RGB')

            # EXIF 데이터 기반 이미지 회전 정정
            image = correct_orientation(image)

            # 방향 예측
            predicted_direction = predict_image(image, model, device)
            print(f"{filename}: Predicted {predicted_direction}")

            # 예측된 방향에 따라 이미지 회전
            if predicted_direction == 'right_to_left':
                rotated_image = image.rotate(-180, expand=True)
            elif predicted_direction == 'top_to_bottom':
                rotated_image = image.rotate(-270, expand=True)
            elif predicted_direction == 'bottom_to_top':
                rotated_image = image.rotate(-90, expand=True)
            else:
                rotated_image = image  # 'left_to_right'

            # 원래 파일에 덮어쓰기
            rotated_image.save(image_path)
            print(f"{filename}: Adjusted and saved.")

if __name__ == "__main__":
    folder_path = 'data_files/test_data'  # 이미지가 있는 폴더 경로
    model = load_model(num_classes=4)  # 모델을 불러올 때 클래스 수를 설정
    adjust_images_in_folder(folder_path, model)
