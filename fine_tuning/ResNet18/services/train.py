import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn as nn
import shutil
import os
from services.model import initialize_model, save_model

# 모델 훈련
def train_model(num_epochs=12):

    path = 'data_files/dataset'

    # 데이터 전처리
    transform = transforms.Compose([
        transforms.Resize((128, 128)),  # 이미지 크기 조정
        transforms.ToTensor(),  # 이미지를 텐서로 변환
        transforms.Normalize((0.5,), (0.5,))  # 정규화
    ])

    # 데이터셋 로드
    train_dataset = datasets.ImageFolder(root=path, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # 모델 초기화
    num_classes = len(train_dataset.classes)  # 폴더의 클래스 수를 기준으로
    model = initialize_model(num_classes) # ResNet-18 호출과 fine-tuning

    # GPU 사용이 가능하다면 모델을 GPU로 옮기기
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    # 손실 함수와 옵티마이저 정의
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001) # 학습률

    model.train()
    for epoch in range(num_epochs):
        running_loss = 0.0 # 현재 epock 동안의 손실값
        correct = 0 # 결과가 일치하는 이미지 개수
        total = 0 # 전체 이미지 개수
        
        # 학습 데이터 불러와 이미지와 라벨로 분류
        for images, labels in train_loader:
            # 이미지와 라벨 데이터를 GPU 또는 CPU 장치로 이동
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad() # 이전 미분값 초기화
            outputs = model(images) # 모델에 이미지를 입력해 예측 결과를 얻어옴
            loss = criterion(outputs, labels) # 예측 결과와 실제 라벨을 비교하여 손실 계산
            loss.backward() # 손실에 대한 미분 계산
            optimizer.step() # 모델의 가중치 업데이트

            running_loss += loss.item()

            # 정확도 계산
            _, predicted = torch.max(outputs.data, 1) # 각 이미지에 대해 예측된 최대 확률값
            total += labels.size(0) # 현재 batch의 전체 이미지 수를 더함
            correct += (predicted == labels).sum().item() # 에측이 맞은 이미지 개수

        epoch_loss = running_loss / len(train_loader)
        epoch_accuracy = 100 * correct / total

        # epoch, 손실률, 정확성 출력
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.2f}%")

    # 모델 저장
    save_model(model)

    # dataset 폴더 삭제(model 생성 후 학습을 위한 데이터 삭제)
    if os.path.exists('data_files/dataset'):
        shutil.rmtree('data_files/dataset/left_to_right')
        shutil.rmtree('data_files/dataset/top_to_bottom')
        shutil.rmtree('data_files/dataset/right_to_left')
        shutil.rmtree('data_files/dataset/bottom_to_top')

if __name__ == "__main__":
    train_model()
