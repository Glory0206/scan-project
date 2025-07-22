from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.search_blank.service import searching
from typing import List

import base64
import cv2
import numpy as np
import logging

router = APIRouter()

@router.post("/analyze")
async def analyze_images(images: List[UploadFile] = File(...)):
    try:
        # 업로드된 파일이 없을 때
        if not images or len(images) == 0:
            raise HTTPException(status_code=422, detail="이미지 파일이 첨부되지 않았습니다.")
        response_data = []
        
        for img in images:
            # 업로드된 파일 읽기
            file_bytes = await img.read()
            if not file_bytes:
                raise HTTPException(status_code=422, detail=f"{img.filename} 파일이 비어 있습니다.")

            # numpy 배열로 변환 (파일 바이너리를 OpenCV에서 처리 가능하도록)
            np_array = np.frombuffer(file_bytes, np.uint8)
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            if image is None:
                raise HTTPException(status_code=400, detail=f"{img.filename}는(은) 유효한 이미지 파일이 아닙니다.")    
            try:
                images_list, numbers, blanks = searching(image)
            except Exception as e:
                logging.exception(f"이미지 분석 중 오류 발생: {img.filename}")
                raise HTTPException(status_code=500, detail=f"{img.filename} 분석 중 오류가 발생했습니다. 관리자에게 문의해 주세요.")
            # 응답 데이터 구조화
            formatted_results = []

            for idx, cropped_image in enumerate(images_list):
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
            
            response_data.append({
                "sheetName": img.filename,
                "areas": formatted_results
            })
        
        # API 응답 반환
        return {"results": response_data}
    except HTTPException as e:
        raise
    except Exception as e:
        # 로그 남기기
        logging.exception("/analyze API 서버 내부 오류 발생")
        raise HTTPException(status_code=500, detail="서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")