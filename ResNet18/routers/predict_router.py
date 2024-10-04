from fastapi import APIRouter, HTTPException
from services.predict import predict_image

router = APIRouter()

@router.post("/predict")
def predict_image_route():
    try:
        predict_image()
        return {"message": "예측을 마칩니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))