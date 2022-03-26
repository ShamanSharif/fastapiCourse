from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Test(BaseModel):
    name: str
    content: str
    published: bool = True
    report: Optional[int] = None


@app.get('/')
def health_check():
    return {"message": "API health check OK"}


@app.post('/test')
def test_post(test: Test):
    return test.dict()
