from fastapi import FastAPI
from typing import Dict

from app.routers.datasets_router import router as datasets_router

app = FastAPI()

app.include_router(datasets_router)

@app.get("/")
def root() -> Dict[str, str]:
  return {"message": "/datasets, /blank"}