from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from set import setting

app = FastAPI()

# 단일 이미지 예측 요청을 위한 Pydantic 모델 정의
class PredictRequest(BaseModel):
    file_name: str

@app.post("/set")
def set():
    setting()
    try:
        return {"message": "모든 이미지가 회전되고 저장되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
def train():
    try:
        # train_model()
        return {"message": "모델이 성공적으로 학습되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# train을 한 후 dataset이 비워지기 때문에 set을 다시 한 후 기능을 구현 가능함
# 학습을 하며 epoch마다의 정확도를 띄우기 때문에, 유지할지는 추후 결정
@app.post("/evaluate")
def evaluate():
    try:
        # evaluate_model()
        return {"message": "모델의 정확도를 확인했습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predict():
    try:
        # predict_image()
        return {"message": f"예측을 마칩니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 초기 경로
@app.get("/")
def root():
    return {"message": "/set, /train, /evaluate, /predict 중 하나를 선택해 이용해주세요."}