from fastapi import APIRouter, HTTPException, UploadFile, Form
import os
import cv2
import numpy as np
import shutil

from app.services.datasets import make_dataset

router = APIRouter()

@router.post("/generate")
async def make(file: UploadFile, count: int = Form(...)):
    storage = os.path.join("storage")

    try:
        os.makedirs(storage, exist_ok=True)

        # 업로드된 파일 읽기
        file_bytes = await file.read()

        # numpy 배열로 변환 (파일 바이너리를 OpenCV에서 처리 가능하도록)
        np_array = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="이미지 파일이 유효하지 않습니다.")      
          
        # make_dataset 함수 호출
        make_dataset(image, count, file.filename)

        return {
            "message": f"{count}개의 샘플 데이터가 생성되었습니다.",
            "file_path": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))