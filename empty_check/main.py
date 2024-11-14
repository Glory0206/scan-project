from fastapi import FastAPI

from services.datasets import make_dataset
from services.search_blank import searching

app = FastAPI()

temp = int(input("0: 데이터셋 생성\n1: 공백 확인\n\n입력: "))

if temp == 0:
    make_dataset()
elif temp == 1:
    searching()