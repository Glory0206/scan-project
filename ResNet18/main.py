from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

# 각 라우터에서 APIRouter 객체 가져오기
from routers.set_router import router as set_router
from routers.train_router import router as train_router
from routers.evaluate_router import router as evaluate_router
from routers.predict_router import router as predict_router
from routers.upload_router import router as upload_router

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React 웹의 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(set_router)
app.include_router(train_router)
app.include_router(evaluate_router)
app.include_router(predict_router)
app.include_router(upload_router)

# 초기 경로
@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "/train, /evaluate, /predict 중 하나를 url의 뒤에 붙여 기능을 이용해주세요."}
