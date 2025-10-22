from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.search_blank.service import extract_template_info, analyze_image_with_template, format_analysis_results
from typing import List

import cv2
import numpy as np
import logging

router = APIRouter()

@router.post("/analyze")
async def analyze_images(images: List[UploadFile] = File(...)):
    try:
        # 1. 업로드된 파일이 없을 때
        if not images:
            raise HTTPException(status_code=422, detail="이미지 파일이 첨부되지 않았습니다.")
        
        response_data = []
        template_info = None # 템플릿 정보를 저장할 변수

        # 첫 번째 이미지로 템플릿 추출
        first_img = images[0]
        try:
            file_bytes = await first_img.read()
            if not file_bytes:
                raise HTTPException(status_code=422, detail=f"{first_img.filename} 파일이 비어 있습니다.")

            np_array = np.frombuffer(file_bytes, np.uint8)
            template_cv_image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            if template_cv_image is None:
                raise HTTPException(status_code=400, detail=f"{first_img.filename}는(은) 유효한 이미지 파일이 아닙니다.")
            
            # 템플릿 추출
            template_info = extract_template_info(template_cv_image)

            # 첫 번째 이미지 분석 (템플릿 추출에 사용한 이미지 재사용)
            images_list, numbers, blanks = analyze_image_with_template(template_cv_image, template_info)
            
            # 결과 포맷팅 및 추가
            formatted_results = format_analysis_results(images_list, numbers, blanks)
            response_data.append({
                "sheetName": first_img.filename,
                "areas": formatted_results
            })

        except Exception as e:
            logging.exception(f"템플릿 추출 또는 첫 이미지 분석 중 오류 발생: {first_img.filename}")
            # 템플릿(첫 이미지) 분석 실패 시, 500 오류 발생
            raise HTTPException(status_code=500, detail=f"{first_img.filename} 분석 중 오류가 발생했습니다. (기준 템플릿 오류)")

        # 나머지 이미지들은 템플릿을 적용하여 분석 ---
        for img in images[1:]: # 두 번째 이미지부터 순회
            try:
                file_bytes = await img.read()
                if not file_bytes:
                     # 비어있는 파일은 로그만 남기고 건너뛸 수 있습니다.
                    logging.warning(f"{img.filename} 파일이 비어 있습니다.")
                    continue # 혹은 오류로 처리

                np_array = np.frombuffer(file_bytes, np.uint8)
                image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

                if image is None:
                    logging.warning(f"{img.filename}는(은) 유효한 이미지 파일이 아닙니다.")
                    continue # 혹은 오류로 처리
                
                # 템플릿 적용하여 분석
                images_list, numbers, blanks = analyze_image_with_template(image, template_info)
                
                formatted_results = format_analysis_results(images_list, numbers, blanks)
                response_data.append({
                    "sheetName": img.filename,
                    "areas": formatted_results
                })
            
            except Exception as e:
                # 개별 이미지 분석 실패 시, 로그만 남기고 다음 이미지로 넘어감
                logging.exception(f"이미지 분석 중 오류 발생: {img.filename}")
                continue

        # 4. 최종 응답 반환
        return {"results": response_data}

    except HTTPException as e:
        raise # HTTPException은 그대로 전달
    except Exception as e:
        logging.exception("/analyze API 서버 내부 오류 발생")
        raise HTTPException(status_code=500, detail="서버 내부 오류가 발생했습니다.")