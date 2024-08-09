# main.py
import torch
from train import train_model
# from utils import preprocess_image

def main():
    # 모델 학습 호출
    train_model()
    
    # 모델 로드
    from model import EasyOCRWithSkew
    model = EasyOCRWithSkew()
    model.load_state_dict(torch.load('model.pth'))
    model.eval()  # 모델을 평가 모드로 설정

if __name__ == "__main__":
    main()
