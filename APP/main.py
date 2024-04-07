from fastapi import FastAPI, status, HTTPException, Form, UploadFile
from typing import List, Optional, Dict, Annotated
from pydantic import BaseModel, HttpUrl, UUID4
import re
import uuid

app = FastAPI()

class MiniPost(BaseModel):
    #images: List[UploadFile]
    title: str
    price: int
    rate: Optional[float] = None
    completionCount: Optional[int] = None
    completionTerm: Optional[int] = None

class Post(BaseModel):
    #images: List[UploadFile]
    title: str
    description: str
    option: Optional[List[str]] = None
    price: int
    completionTerm: Optional[int] = None

class Team(BaseModel):
    title: str
    description: str
    recruitmentStatus: bool = True

class Review(BaseModel):
    title: str
    description: str

class ProfileIn(BaseModel):
    #image: HttpUrl | UploadFile 
    #background_image: HttpUrl | UploadFile
    introduce: str
    nickname: str

class ProfileOut(BaseModel):
    #image: HttpUrl | UploadFile 
    background_image: HttpUrl | UploadFile
    introduce: str
    nickname: str
    id: str
    email: str
    password: str
    member_code: UUID4

previewPosts = {}
posts  = {}  
teams = {}        
reviews = {}
registed = {}
profiles = {}
baskets  = {}

@app.get("/")
async def test():
    return "호출됨"

async def get_minipost(page: int):
    miniPosts = {}
    start = (page - 1) * 10 #1페이지 = 0
    end = page * 10 #1페이지 = 10 
    for writtenOrder in range(start, end): #10개의 게시판
        miniPosts[writtenOrder] = previewPosts.get(str(writtenOrder)) 
    return miniPosts

@app.get("/posts/list/{page}", deprecated=False, tags=["게시판"]) #게시판 목록 ?????
async def get_posts(page: int):
    miniPosts = await get_minipost(page)
    return miniPosts

@app.get("/post/{member_code}/{written_num}", tags=["게시판"]) #게시판 상세 조회
async def get_post(member_code: str, written_num: int):
    # if not posts[member_code]: #작동을안함 몰?루
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다.")
    post = posts[member_code][written_num]
    return posts

@app.post("/post/create", tags=["게시판"]) #게시판 만들기
async def create_post(post: Post):
    member_code = str(uuid.uuid4())  # 나중에 회원정보에서 자동생성
    new_post = {f"post{len(posts[member_code]) + 1}": post.dict()}  # 새 게시물 생성
    if member_code in posts:
        posts[member_code].append(new_post)
    else:
        posts[member_code] = [new_post]
    return posts  # 나중에 {"message": "게시판 생성 완료"} 등으로 변경 가능

@app.put("/post/{member_code}/{written_num}", tags=["게시판"]) #게시판 수정
async def modify_post(member_code: str, written_num: int, post: Post):
    posts[member_code][written_num] = post.dict() 
    return posts[member_code][written_num]

async def get_team_recruitment_list(page: int):
    miniPosts = {}
    start = (page - 1) * 10 #1페이지 = 0
    end = page * 10 #1페이지 = 10 
    for writtenOrder in range(start, end): #10개의 게시판
        miniPosts[writtenOrder] = previewPosts.get(str(writtenOrder)) 
    return miniPosts

@app.get("/team_recruitment/posts/{page}", deprecated=True, tags=["팀 모집"])
async def get_teams_recruitment(page: int):
    teams = await get_team_recruitment_list(page)
    return teams

@app.post("/team_recruitment/create", tags=["팀 모집"]) 
async def create_team_recruitment(team: Team):
    member_code = str(uuid.uuid4()) 
    new_post = {f"post{len(teams[member_code]) + 1}": team.dict()} 
    if member_code in teams:
        teams[member_code].append(new_post)
    else:
        teams[member_code] = [new_post]
    return teams

async def get_reviews(page: int):
    review={}
    start = (page-1)*10 
    end = page*10 
    for writtenOrder in range(start, end):
        reviews.update(reviews.get(writtenOrder))

@app.get("/reviews/{page}", tags=["리뷰"])
async def get_reviews(page:int):
    pages = await get_reviews(page)

@app.post("review/create", tags=["리뷰"])
async def create_review(review: Review):
    member_code = str(uuid.uuid4()) 
    new_post = {f"post{len(review[member_code]) + 1}": review.dict()} 
    if member_code in reviews:
        reviews[member_code].append(new_post)
    else:
        reviews[member_code] = [new_post]
    return reviews

@app.post("/login/") #로그인
async def get_login(id:Annotated[str, Form()], password:Annotated[str, Form()]):
    if registed.get(id):
        registed.get(id) == password
        return #status.HTTP_200_OK  나중에 메인화면 부르기
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="아이디 비밀번호가 틀렸습니다.")
    
@app.post("/signup/", status_code=status.HTTP_201_CREATED) #회원가입
async def get_signup(profile:ProfileIn = Form(),
                     id:str = Form(min_length=8), 
                     password:str = Form(min_length=8), 
                     email:str = Form(), 
): #중복 체크는 db에서 unique로
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="소문자가 없습니다.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="대문자가 없습니다.")
    if not re.search(r"[!@#$%^&*]", password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="특수문자가 없습니다.")
    
    member_code = str(uuid.uuid4())
    profiles.update({member_code:[{**profile.dict(), "id":id, "password":password, "email" : email}]})

    return {"message":"회원가입 성공!"}

async def mypage(member_code:str): 
    profile={}
    profile=profiles[member_code]
    return profile

@app.get("/mypage/{member_code}", tags={"마이페이지"})
async def get_mypage(member_code:str):
    return mypage(member_code)

@app.patch("/mypage/image/{member_code}", tags={"마이페이지"})
async def patch_mypage(member_code:str, image_change:HttpUrl | UploadFile):
    profiles.update({member_code : [image_change]})

    return mypage(member_code)

@app.patch("/mypage/background/{member_code}", tags={"마이페이지"})
async def patch_mypage(member_code:str, background_change:HttpUrl | UploadFile):
    profiles.update({member_code:[background_change]})

    return {"message":"배경 이미지 변경이 완료되었습니다."}

@app.patch("/mypage/email/{member_code}", tags={"마이페이지"})
async def patch_mypage(member_code:str, email_change:str):
    profiles.update({member_code:[email_change]})

    return {"message":"이메일 변경이 완료되었습니다."}

#////
@app.patch("/mypage/password/{member_code}", tags={"마이페이지"})
async def patch_mypage(member_code:str, password_change:Annotated[str, Form(min_length=8)]):

    if not re.search(r"[a-z]", password_change):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="소문자가 없습니다.")
    if not re.search(r"[A-Z]", password_change):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="대문자가 없습니다.")
    if not re.search(r"[!@#$%^&*]"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="특수문자가 없습니다.")
    
    profiles.update({member_code:[password_change]})

    return {"message":"비밀번호 변경이 완료되었습니다."}

@app.get("/mypost/list/{member_code}", tags={"마이페이지"})
async def get_mypost_list(member_code:str):
    myposts = previewPosts[member_code]

    return myposts

@app.post("/basket/add/{url}", tags={"마이페이지"})
async def add_basket(member_code:str, url:HttpUrl):
    baskets.update({member_code:[url]})
    return {"message":"게시글을 장바구니에 추가했습니다."}

@app.get("/baskets/{member_code}", tags={"마이페이지"})
async def get_baskets(member_code:str):
    mybaskets = baskets[member_code]

    return mybaskets