#train.py
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import SkewDataset, transform
from model import EasyOCRWithSkew

# 각도를 모델의 출력 라벨로 변환하는 함수
def convert_angle_to_label(angle):
    if angle == 0:
        return 0  # 각도가 0도인 경우, 라벨 0을 반환
    elif angle == 90:
        return 1  # 각도가 90도인 경우, 라벨 1을 반환
    elif angle == 180:
        return 2  # 각도가 180도인 경우, 라벨 2를 반환
    elif angle == 270:
        return 3  # 각도가 270도인 경우, 라벨 3을 반환
    else:
        raise ValueError(f"Unexpected angle: {angle}")  # 예상치 못한 각도 값이 들어온 경우 오류 발생

def train_model():
    image_paths = ['fine_tuning/exam/exam1_0.jpg', 'fine_tuning/exam/exam1_1.jpg', 'fine_tuning/exam/exam1_2.jpg', 'fine_tuning/exam/exam1_3.jpg',
                   'fine_tuning/exam/exam2_0.jpg', 'fine_tuning/exam/exam2_1.jpg', 'fine_tuning/exam/exam2_2.jpg', 'fine_tuning/exam/exam2_3.jpg',
                   'fine_tuning/exam/exam3_0.jpg', 'fine_tuning/exam/exam3_1.jpg', 'fine_tuning/exam/exam3_2.jpg', 'fine_tuning/exam/exam3_3.jpg',
                   'fine_tuning/exam/exam4_0.jpg', 'fine_tuning/exam/exam4_1.jpg', 'fine_tuning/exam/exam4_2.jpg', 'fine_tuning/exam/exam4_3.jpg',
                   'fine_tuning/exam/exam5_0.jpg', 'fine_tuning/exam/exam5_1.jpg', 'fine_tuning/exam/exam5_2.jpg', 'fine_tuning/exam/exam5_3.jpg',
                   'fine_tuning/exam/exam6_0.jpg', 'fine_tuning/exam/exam6_1.jpg', 'fine_tuning/exam/exam6_2.jpg', 'fine_tuning/exam/exam6_3.jpg',
                   'fine_tuning/exam/exam7_0.jpg', 'fine_tuning/exam/exam7_1.jpg', 'fine_tuning/exam/exam7_2.jpg', 'fine_tuning/exam/exam7_3.jpg',
                   'fine_tuning/exam/exam8_0.jpg', 'fine_tuning/exam/exam8_1.jpg', 'fine_tuning/exam/exam8_2.jpg', 'fine_tuning/exam/exam8_3.jpg'
                  ]
    
    angles = [0, 90, 180, 270,
              0, 90, 180, 270,
              0, 90, 180, 270,
              0, 90, 180, 270,
              0, 90, 180, 270,
              0, 90, 180, 270,
              0, 90, 180, 270,
              0, 90, 180, 270,
             ]

    # 데이터셋 객체 생성 및 데이터 로더 설정
    dataset = SkewDataset(image_paths, angles, transform=transform)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    # 모델, 손실 함수 및 옵티마이저 초기화
    model = EasyOCRWithSkew()
    criterion = nn.CrossEntropyLoss() # CrossEntropyLoss는 분류 문제에 적합
    optimizer = optim.Adam(model.parameters(), lr=0.001) # Adam 옵티마이저 사용

    num_epochs = 10  # 총 10 에폭 동안 학습
    for epoch in range(num_epochs):
        model.train()  # 모델을 학습 모드로 설정
        running_loss = 0.0  # 에폭별로 손실을 기록하기 위한 변수
        correct = 0  # 올바르게 예측된 샘플 수
        total = 0  # 총 샘플 수

        # 데이터 로더를 통해 배치 단위로 데이터를 처리
        for images, angles in dataloader:
            images = images.float()  # 이미지 텐서를 float 형식으로 변환
            angles = angles.tolist()  # 각도 라벨을 리스트 형식으로 변환

            # 각도를 모델의 출력 라벨로 변환
            angle_labels = [convert_angle_to_label(angle) for angle in angles]
            angle_tensor = torch.tensor(angle_labels, dtype=torch.long)  # 라벨을 텐서로 변환

            # 배치 크기 일치 확인
            if len(angle_tensor) != images.size(0):
                print(f"Mismatch between batch sizes: images ({images.size(0)}) vs labels ({len(angle_tensor)})")
                continue

            optimizer.zero_grad()  # 옵티마이저의 기울기를 0으로 초기화
            outputs = model(images)  # 모델을 통해 예측값 생성

            loss = criterion(outputs, angle_tensor)  # 손실 계산
            loss.backward()  # 손실을 기준으로 기울기 계산
            optimizer.step()  # 옵티마이저를 통해 파라미터 업데이트

            # 정확도 계산
            _, predicted = torch.max(outputs.data, 1)  # 예측된 클래스 얻기
            total += angle_tensor.size(0)  # 총 샘플 수 업데이트
            correct += (predicted == angle_tensor).sum().item()  # 올바르게 예측된 샘플 수 업데이트

            running_loss += loss.item()  # 에폭별 손실 기록

        avg_loss = running_loss / len(dataloader)  # 평균 손실 계산
        accuracy = 100 * correct / total  # 정확도 계산
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")

        # 디버깅을 위한 추가 출력
        print(f"Predicted: {predicted}")
        print(f"Ground Truth: {angle_tensor}")

    torch.save(model.state_dict(), 'model.pth')

if __name__ == "__main__":
    train_model()
