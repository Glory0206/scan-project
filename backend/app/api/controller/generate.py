from fastapi import APIRouter, HTTPException, UploadFile, Form
from fastapi.responses import StreamingResponse
import io
from pathlib import Path
import zipfile
import cv2
import numpy as np

from app.services.make_dataset.service import make_dataset

router = APIRouter()

@router.post("/generate")
async def make(file: UploadFile, count: int = Form(...)):
    try:
        # 업로드된 파일 읽기
        file_bytes = await file.read()

        # numpy 배열로 변환 (파일 바이너리를 OpenCV에서 처리 가능하도록)
        np_array = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="이미지 파일이 유효하지 않습니다.")      
          
        filename_stem = Path(file.filename).stem
        # 데이터 생성(zip)
        result_files = make_dataset(image, count, filename_stem)

        zip_stream = io.BytesIO() # 메모리상에 존재하는 이진 파일 객체
        with zipfile.ZipFile(zip_stream, "w") as zip_file: # 쓰기 모드로 zip 파일 열기
            for filename, file_buffer in result_files:
                zip_file.writestr(filename, file_buffer.getvalue()) # 파일명을 지정해서 문자열 혹은 바이트 데이터를 zip 내부에 직접 작성

        zip_stream.seek(0) # zip_stream의 포인터를 처음 위치(0)으로 이동, 처음부터 읽기 위해서
    
        # StreamingResponse: FastAPI의 비동기 스트리밍 응답 클래스
        # 대용량 파일이나 메모리에 생성된 데이터를 한 번에 메모리에 올리지 않고 클라이언트로 점진적으로 보낼 수 있음
        return StreamingResponse(
            zip_stream,
            media_type="application/x-zip-compressed",
            headers={
                "Content-Disposition": f'attachment; filename="{filename_stem}_dataset.zip"'
            }
        )    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))