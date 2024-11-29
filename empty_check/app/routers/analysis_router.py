from fastapi import APIRouter, HTTPException, UploadFile
from app.services.search_blank import searching

import os
import base64
import cv2
import shutil
import numpy as np

router = APIRouter()

@router.post("/analysis")
async def make(file: UploadFile):
    try:
        # 업로드된 파일 읽기
        file_bytes = await file.read()

        # numpy 배열로 변환 (파일 바이너리를 OpenCV에서 처리 가능하도록)
        np_array = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="이미지 파일이 유효하지 않습니다.")          
        results, numbers, blanks = searching(image)

        print("results: ",results)
        print("numbers: ",numbers)
        print("blanks: ",blanks)
        
        # 응답 데이터 구조화
        formatted_results = []

        for idx, cropped_image in enumerate(results):
            # 이미지 데이터를 Base64로 변환
            _, buffer = cv2.imencode('.jpg', cropped_image)
            base64_image = base64.b64encode(buffer).decode("utf-8")
            data_uri = f"data:image/jpeg;base64,{base64_image}"
            
            # 구조화된 데이터 추가
            formatted_results.append({
                "areaName": numbers[idx],
                "isBlank": blanks[idx],
                "croppedImage": data_uri
            })
        
        # API 응답 반환
        return {
            "sheetName": file.filename,
            "areas": formatted_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))