from fastapi import FastAPI
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import router as api_router

app = FastAPI()

app.include_router(api_router)

origins = [
    "http://localhost:3000",  # 로컬 프론트엔드 주소
    "http://localhost:5173",
    "https://glory-scan-f.onrender.com",
]

app.add_middleware(
    CORSMiddleware,

    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "/analyze, /generate"}