# SCAN IMAGE - Image OCR and Preprocessing Pipeline
이 프로젝트는 이미지에서 텍스트를 추출하고 이미지의 방향을 판별하는 파이프라인을 구현합니다.

이 과정에는 이미지 전처리, 텍스트 영역 검출, Crop 및 Resize, 텍스트 인식(OCR)이 포함됩니다.

## 주요 기능
- 이미지 전처리(GrayScale, Bilateral Filtering, Binarization)
- 텍스트 영역 검출
- 텍스트 영역 Crop 및 Resize
- OCR을 통한 텍스트 인식(Tesseract와 EasyOCR 지원)
---

## 가상환경 설정
Miniforge3를 사용하여 가상환경을 구성한다.
### 가상환경 생성(Python == 3.10.14)
    **conda create --name '생성 환경 이름' python=3.10**
### 가상환경 활성화
    **conda activate '생성 환경 이름'**
### 가상환경 정상 진입 확인
    **conda info --envs**
---

## 환경 설정(Package 설치)
### OpenCV-python == 4.10.0.84
    **pip install opencv-python**

### Pillow == 10.4.0
    **conda install pillow**

### Matplotlib == 9.9.1
    **conda install matplotlib**

### Tesseract == 0.3.10
    **pip install pytesseract**

### EasyOCR == 1.7.1
    **pip install easyocr**

### DownGrade
    **numpy == 1.26.4**

    **ninja == 1.10.2**

    **torch == 2.0.0**

    **torchvision == 0.15.1**
---

## 실행 방법
1. main.py를 실행합니다.
2. 하나의 파일에 대해 실행할지, 폴더 내의 모든 파일에 대해 실행할지 숫자를 입력해 선택합니다.
3. 하나의 파일에 대해 실행 시, 답안의 번호를 입력 후 OCR을 선택합니다.
4. 폴더 내의 모든 파일에 대해 실행 시, OCR을 선택합니다.