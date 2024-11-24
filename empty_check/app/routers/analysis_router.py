from fastapi import APIRouter, HTTPException, UploadFile
from app.services.search_blank import searching

import os
import base64

router = APIRouter()

@router.post("/analysis")
async def make(file: UploadFile):
    try:
        storage_dir = os.path.join(os.getcwd(), "storage")
        os.makedirs(storage_dir, exist_ok=True)
        file_path = os.path.join(storage_dir, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        results, numbers, blanks = searching(file_path)
        
        # 응답 데이터 구조화
        formatted_results = []

        for idx, cropped_image in enumerate(results):
            # 이미지 데이터를 Base64로 변환
            base64_image = base64.b64encode(cropped_image).decode("utf-8")
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