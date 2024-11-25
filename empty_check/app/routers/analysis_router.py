from fastapi import APIRouter, HTTPException, UploadFile
from app.services.search_blank import searching

import os
import base64
import cv2
import shutil

router = APIRouter()

@router.post("/analysis")
async def make(file: UploadFile):
    # 저장 경로 설정
    temp = os.path.join("temp")

    try:
        os.makedirs(temp, exist_ok=True)
      
        # 업로드된 파일 저장
        file_path = os.path.join(temp, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        results, numbers, blanks = searching(file_path)

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
    
    finally:
        # 작업 완료 후 temp 폴더 삭제
        if os.path.exists(temp):
            shutil.rmtree(temp)
            print(f"임시 폴더 '{temp}'가 삭제되었습니다.")
