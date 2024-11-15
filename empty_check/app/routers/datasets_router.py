from fastapi import APIRouter, HTTPException
from services.datasets import make_dataset

router = APIRouter()

@router.post("/datasets")
def make():
  try:
    make_dataset()
    return {"message": "데이터셋이 생성되었습니다."}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))