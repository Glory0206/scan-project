from fastapi import FastAPI
from routers import set_router, train_router, evaluate_router, predict_router

app = FastAPI()

# 각 라우터를 FastAPI 애플리케이션에 등록
app.include_router(set_router.router)
app.include_router(train_router.router)
app.include_router(evaluate_router.router)
app.include_router(predict_router.router)

# 초기 경로
@app.get("/")
def root():
    return {"message": "/set, /train, /evaluate, /predict 중 하나를 선택해 이용해주세요."}
