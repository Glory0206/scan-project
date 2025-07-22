from fastapi import FastAPI
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import router as api_router

app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"], # React 프론트 연결
    allow_origins=["*"], # 모든 도메인 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "/analyze, /generate"}