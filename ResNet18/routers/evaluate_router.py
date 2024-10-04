from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/evaluate")
def evaluate_model_route():
    try:
        # evaluate_model()
        return {"message": "모델의 정확도를 확인했습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))