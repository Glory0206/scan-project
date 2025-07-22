# Python 베이스 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 생성 및 이동
WORKDIR /app

# OpenCV 등 이미지 처리에 필요한 라이브러리 설치
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# 의존성 파일 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 