import torch
from PIL import Image
from torchvision import transforms
from services.model import load_model

def predict_image():

    path = r"C:\Users\dmb07223\OneDrive - 진학사\바탕 화면\Seo\project\its_glory\fine_tuning\ResNet18\test_data\1.jpg"

    # 이미지 전처리 (훈련과 동일하게)
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    # 모델 로드
    model = load_model(num_classes=4)  # 클래스 수를 맞춰 설정
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()

    image = Image.open(path)
    image = transform(image).unsqueeze(0).to(device)
    
    output = model(image)
    _, predicted_direction = torch.max(output.data, 1)
    
    # 예측된 방향 출력
    classes = ['bottom_to_top', 'left_to_right', 'right_to_left', 'top_to_bottom']
    print(f"Predicted Direction: {classes[predicted_direction.item()]}")