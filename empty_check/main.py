from fastapi import FastAPI
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

from app.routers.generate_router import router as datasets_router
from app.routers.analyze_router import router as search_router

app = FastAPI()

app.include_router(datasets_router)
app.include_router(search_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "/analyze, /generate"}