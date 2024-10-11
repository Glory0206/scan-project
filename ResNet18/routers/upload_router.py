from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path

router = APIRouter()

UPLOAD_DIRECTORY = "uploads"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_images(files: list[UploadFile] = File(...)):
    try:
        uploaded_files = []
        
        # 업로드된 각 파일 처리
        for file in files:
            file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_files.append(file.filename)
        
        return {"message": "Files uploaded successfully", "files": uploaded_files}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")
