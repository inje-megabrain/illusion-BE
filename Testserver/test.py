from fastapi import FastAPI, status, HTTPException, Form, UploadFile, Depends
from typing import List, Optional, Annotated, Dict
from pydantic import BaseModel, HttpUrl
import re
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schemas


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def test():
    return "호출됨"

#게시판 목록
@app.get("/posts", response_model= list[schemas.Post], deprecated=False, tags=["게시판"]) 
async def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_users(db, skip=skip, limit=limit)
    return posts

#게시판 상세 조회
@app.get("/post/{post_id}", tags=["게시판"]) 
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

#게시판 만들기
@app.post("/post", tags=["게시판"]) 
async def create_post(post : schemas.PostRequest, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post = post)
    # post = crud.get_post(db, post.PostID)
    # return post

#게시판 수정
@app.put("/post/re", tags=["게시판"]) 
async def modify_post(post: schemas.PostResponse, db: Session = Depends(get_db)):
    existing_post = crud.get_post(db, post.postId)
    if existing_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # 수정 로직 추가 필요
    return existing_post
    
#팀 모집 게시판 목록
@app.get("/team/posts", response_model= list[schemas.TeamResponse],deprecated=False, tags=["팀 모집"]) 
async def get_team_recruitment_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip, limit=limit)
    return teams

#팀 모집 게시판 만들기
@app.post("/team", tags=["팀 모집"]) 
async def create_team_recruitment(team: schemas.TeamRequest, db: Session = Depends(get_db)):
    return crud.create_team_post(db=db, team=team)

#리뷰 게시판 목록
@app.get("/review/posts", response_model=list[schemas.ReviewResponse],tags=["리뷰"]) 
async def get_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = crud.get_preview_reviews(db=db, skip=skip, limit=limit)
    return reviews

#리뷰 게시판 상세 조회
@app.get("/review/post/{post_id}", tags=["리뷰"])
async def get_review(post_id: int, db: Session = Depends(get_db)):
    review = crud.get_review(db=db, post_id=post_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

 #리뷰 게시판 만들기
@app.post("/review", tags=["리뷰"])
async def create_review(review: schemas.ReviewRequest, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)

# @app.post("/login/") #로그인
# async def get_login(id:Annotated[str, Form()], password:Annotated[str, Form()]):
#     if registed.get(id):
#         registed.get(id) == password
#         return #status.HTTP_200_OK  나중에 메인화면 부르기
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="아이디 비밀번호가 틀렸습니다.")
    
@app.post("/signup/", response_model=schemas.UserCreate,status_code=status.HTTP_201_CREATED) #회원가입
async def get_signup(
                     user: schemas.UserCreate,
                     db: Session = Depends(get_db)
):
    db_user = crud.get_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    #비번 제약걸기
    # if not re.search(r"[a-z]", user.password):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="소문자가 없습니다.")
    # if not re.search(r"[A-Z]", user.password):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="대문자가 없습니다.")
    # if not re.search(r"[!@#$%^&*]", user.password):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="특수문자가 없습니다.")
    
    return crud.create_user(db=db, user=user)

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
