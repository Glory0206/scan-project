from fastapi import APIRouter, HTTPException
from services.train import train_model

router = APIRouter()

@router.post("/train")
def train_model_route():
    try:
        train_model()
        return {"message": "모델이 성공적으로 학습되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))