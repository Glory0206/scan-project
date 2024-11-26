from fastapi import APIRouter, HTTPException, UploadFile, Form
import os
import shutil

from app.services.datasets import make_dataset

router = APIRouter()

@router.post("/generate")
async def make(file: UploadFile, count: int = Form(...)):
    # 저장 경로 설정
    temp = os.path.join("temp")
    storage = os.path.join("storage")

    try:
        os.makedirs(temp, exist_ok=True)
        os.makedirs(storage, exist_ok=True)
      
        # 업로드된 파일 저장
        file_path = os.path.join(temp, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("업로드 파일",file_path)
      
        # make_dataset 함수 호출
        make_dataset(file_path, count)

        return {
            "message": f"{count}개의 샘플 데이터가 '{temp}' 경로에 생성되었습니다.",
            "file_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 작업 완료 후 temp 폴더 삭제
        if os.path.exists(temp):
            shutil.rmtree(temp)
            print(f"임시 폴더 '{temp}'가 삭제되었습니다.")