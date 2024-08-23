import torch
import torchvision.models as models
import torch.nn as nn

def initialize_model(num_classes):
    # Pretrained ResNet18 모델 로드
    model = models.resnet18(weights='IMAGENET1K_V1')
    
    # 마지막 fully connected layer를 수정하여 새로운 레이어 추가
    num_ftrs = model.fc.in_features

    # ReLU 활성화 함수를 추가한 새로운 신경망 구조
    model.fc = nn.Sequential(
        nn.Linear(num_ftrs, 512),
        nn.ReLU(),  # ReLU 활성화
        nn.Linear(512, 256),
        nn.ReLU(),  # ReLU 활성화
        nn.Linear(256, num_classes)
    )
    
    return model

# 모델 저장
def save_model(model, path='model.pth'):
    torch.save(model.state_dict(), path)

# 모델 불러오기
def load_model(path='model.pth', num_classes=4):
    model = initialize_model(num_classes)
    model.load_state_dict(torch.load(path))
    return model
