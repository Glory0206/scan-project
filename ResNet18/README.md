# 손글씨 방향 인식 프로젝트(회전)
이 프로젝트는 ResNet-18 모델을 파인튜닝하여 이미지 속 손글씨의 방향을 인식하여 사용자가 편하게 볼 수 있는 각도(0도)로 회전시킵니다.

이 프로젝트는 이미지의 텍스트 방향을 인식하기 위한 학습, 모델의 정확도 확인, 특정 사진에 대한 텍스트 방향 반환(출력), 한 폴더 내의 모든 사진에 대해 회전 적용 기능을 제공합니다.

## 주요 기능
- 훈련 : 주어진 데이터셋을 사용하여 모델(ResNet-18)을 학습합니다.
- 평가 : 학습된 모델의 정확도를 확인합니다.
- 예측 : 새로운 이미지의 텍스트 방향을 예측합니다.
- 이미지 회전 : 이미지의 텍스트 방향을 인식하여 텍스트 방향이 '왼쪽 -> 오른쪽'이 되도록 회전시킵니다.
---

## 가상환경 설정
Miniforge3를 사용하여 가상환경을 구성한다.
### 가상환경 생성(Python == 3.10.14)
    conda create --name '생성 환경 이름' python=3.10
### 가상환경 활성화
    conda activate '생성 환경 이름'
### 가상환경 정상 진입 확인
    conda info --envs
---

## 환경 설정(Package 설치)
### torch == 2.4.0
    pip install torch

### torchvision == 0.19.0
    pip install torchvision

### Pillow == 10.4.0
    pip install pillow

### fastapi == 0.112.1
    pip install fastapi

### uvicorn == 0.30.6
    pip install uvicorn

---

## 사용 방법
1. exam 폴더 내 이미지들의 텍스트 방향을 모두 왼쪽 -> 오른쪽으로 통일합니다.
2. fastapi를 통해 set을 실행하여 exam 폴더의 모든 이미지에 대해 0, 90, 180, 270도 회전하여 dataset 폴더 내의 left_to_right, top_to_bottom, right_to_left, bottom_to_top 폴더들에 저장합니다.
3. fastapi를 통해 train(모델 학습), evaluate(모델 정확도 확인), predict(이미지 예측) 중 사용하고자 하는 기능을 입력해 실행합니다.(train을 한 후 dataset이 초기화되기 때문에 이를 인지하고 사용해야합니다.)
4. image_rotation.py를 실행하여 학습된 모델을 통해 경로에 있는 모든 이미지들에 대해 회전을 적용합니다.