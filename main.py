from fastapi import FastAPI, Body
from typing import List, Union, Optional
from pydantic import BaseModel

app = FastAPI()
# 클래스 명 파스칼케이스: PacalCase
# 변수 명은 카멜케이스: camelCase
class MiniPost(BaseModel):
    id:int
    title:str
    price:int
    work_day:int
    #images:Union[List[Image], None] = None

class PostPreviewResponse(BaseModel):
    rate: Optional[float] = None
    works:Optional[int] = 0
    def __init__(self, id, rate, completionCount, title, price, comletionTerm):
        self.id=id
        self.rate=rate
        self.completionCount=completionCount
        self.title=title
        self.price=price
        self.completionTerm=comletionTerm


@app.get("/")
def test():
    return '호출됨'

@app.get("/post/list")
def get_posts():
    return MiniPost(1, getTitle())

@app.get("/post/{id}")
def get_post(id:int):
    return recall[id]

@app.post("/post-create")
def create_post(list:List[MiniPost] = Body()):

    return list
