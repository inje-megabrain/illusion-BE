from fastapi import FastAPI, status, HTTPException, Form, UploadFile
from typing import List, Optional, Annotated, Dict
from pydantic import BaseModel, HttpUrl, UUID4
import re
import uuid
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schemas


app = FastAPI()

@app.get("/")
async def test():
    return "호출됨"

@app.get("/boards/{board_id}/posts", deprecated=False, tags=["게시판"]) #게시판 목록
async def get_posts(page : int = 1):
    posts = PreviewPost(
        title="title",
        price=35000,
        rate=0,
        completionCount=0,
        averageCompletionDay=0
    )

    print(page)
    return posts

@app.get("/post", tags=["게시판"]) #게시판 상세 조회
async def get_post(memberId: int = 0):
    post = PostResponse(
        title = "title",
        description = "description",
        option = ["option1", "option2"],
        price = 350000,
        averageCompletionDay = 10    
    )
    print(memberId)
    return post

@app.post("/boards/{board_id}/post", tags=["게시판"]) #게시판 만들기
async def create_post(post : PostRequest, memberId: int = 0):
    print(memberId)
    return "게시판 생성 완료"

@app.put("/post", tags=["게시판"]) #게시판 수정
async def modify_post(post: PostRequest, memberId: int = 0):
    print(memberId)
    return "수정 완료"


@app.get("/team/posts", deprecated=False, tags=["팀 모집"]) #팀 모집 게시판
async def get_team_recruitment_list(page: int = 0):
    teams = PreviewTeam(
        title = "제목",
        description = "설명",
        recruitmentStatus = True
    )
    print(page)
    return teams

@app.post("/team/post", tags=["팀 모집"]) #팀 모집 게시판 만들기
async def create_team_recruitment(team: TeamRequest, memberId: int = 0):
    print(memberId)
    return "팀 게시판 생성 완료"

@app.get("/reviews", tags=["리뷰"]) #리뷰 게시판
async def get_reviews(page : int = 1):
    review = ReviewResponse(
        title = "제목",
        description= "설명",
        rate= 1.5,
    )
    print(page)
    return review

@app.post("/post/{post_id}/review", tags=["리뷰"]) #리뷰 만들기
async def create_review(review: ReviewRequest, memberId: int = 0):
    print(memberId)
    return "리뷰 게시판 생성 완료"

# @app.post("/login/") #로그인
# async def get_login(id:Annotated[str, Form()], password:Annotated[str, Form()]):
#     if registed.get(id):
#         registed.get(id) == password
#         return #status.HTTP_200_OK  나중에 메인화면 부르기
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="아이디 비밀번호가 틀렸습니다.")
    
# @app.post("/signup/", status_code=status.HTTP_201_CREATED) #회원가입
# async def get_signup(profile:ProfileIn = Form(),
#                      id:str = Form(min_length=8), 
#                      password:str = Form(min_length=8), 
#                      email:str = Form(), 
# ): #중복 체크는 db에서 unique로
#     if not re.search(r"[a-z]", password):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="소문자가 없습니다.")
#     if not re.search(r"[A-Z]", password):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="대문자가 없습니다.")
#     if not re.search(r"[!@#$%^&*]", password):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="특수문자가 없습니다.")
    
#     memberId = str(uuid.uuid4())
#     profiles.update({memberId:[{**profile.dict(), "id":id, "password":password, "email" : email}]})

#     return {"message":"회원가입 성공!"}

# @app.get("/mypage/{memberId}", tags={"마이페이지"})
# async def get_mypage(memberId:str):

# @app.patch("/mypage/image/{memberId}", tags={"마이페이지"})
# async def patch_mypage(memberId:str, image_change:HttpUrl | UploadFile):

# @app.patch("/mypage/background/{memberId}", tags={"마이페이지"})
# async def patch_mypage(memberId:str, background_change:HttpUrl | UploadFile):

#     return {"message":"배경 이미지 변경이 완료되었습니다."}

# @app.patch("/mypage/email/{memberId}", tags={"마이페이지"})
# async def patch_mypage(email_change:str):
#     return {"message":"이메일 변경이 완료되었습니다."}

# @app.patch("/mypage/password/{memberId}", tags={"마이페이지"})
# async def patch_mypage(memberId:str, password_change:Annotated[str, Form(min_length=8)]):
#     return {"message":"비밀번호 변경이 완료되었습니다."}

# @app.get("/mypost/list/{memberId}", tags={"마이페이지"})
# async def get_mypost_list(memberId:str):


# @app.post("/basket/add/{url}", tags={"마이페이지"})
# async def add_basket(memberId:str, url:HttpUrl):
#     return {"message":"게시글을 장바구니에 추가했습니다."}

# @app.get("/baskets/{memberId}", tags={"마이페이지"})
# async def get_baskets(memberId:str):
