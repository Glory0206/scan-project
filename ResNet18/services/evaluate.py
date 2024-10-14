import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from services.model import load_model
from constants import LABELING_PATH

# 모델 평가
def evaluate_model():
    path = LABELING_PATH

    # 데이터 전처리 (훈련과 동일하게)
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    # 테스트 데이터셋 로드
    test_dataset = datasets.ImageFolder(root=path, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # 모델 로드
    model = load_model(num_classes=len(test_dataset.classes))

    # GPU 사용이 가능하다면 모델을 GPU로 옮기기
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    print(f"Accuracy of the model on the test images: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    evaluate_model()
