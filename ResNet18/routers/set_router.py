from fastapi import APIRouter, HTTPException
from services.set import setting

router = APIRouter()

@router.post("/set")
def set_images():
    try:
        setting()
        return {"message": "모든 이미지가 회전되고 저장되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))