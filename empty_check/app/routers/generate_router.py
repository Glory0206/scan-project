from fastapi import APIRouter, HTTPException, UploadFile, Form
import os

from app.services.datasets import make_dataset

router = APIRouter()

@router.post("/generate")
async def make(file: UploadFile, count: int = Form(...)):
    try:
        # 저장 경로 설정
        storage_dir = os.path.join(os.getcwd(), "storage")
        os.makedirs(storage_dir, exist_ok=True)  # storage 폴더 생성 (이미 있으면 무시)
      
        # 업로드된 파일 저장
        file_path = os.path.join(storage_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
      
        # make_dataset 함수 호출
        make_dataset(file_path, count)

        return {
            "message": f"{count}개의 샘플 데이터가 '{storage_dir}' 경로에 생성되었습니다.",
            "file_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  