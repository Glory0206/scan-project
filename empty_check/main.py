from fastapi import FastAPI
from typing import Dict

from app.routers.generate_router import router as datasets_router
from app.routers.analysis_router import router as search_router

app = FastAPI()

app.include_router(datasets_router)
app.include_router(search_router)

@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "/analysis, /generate"}