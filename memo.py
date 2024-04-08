from fastapi import FastAPI, status, HTTPException, Form, UploadFile
from typing import List, Optional, Annotated, Dict
from pydantic import BaseModel, HttpUrl, UUID4
import re
import uuid

app = FastAPI()

class PreviewPost(BaseModel):
    #images: List[UploadFile]
    title: str
    price: int
    rate: Optional[float] = None
    completionCount: Optional[int] = None
    averageCompletionDay: Optional[int] = None
    def __init__(self, title, price, rate, completionCount, averageCompletionDay):
        self.title:str
        self.price:int
        self.rate:Optional[float] = None
        self.completionCount:Optional[int] = None
        self.averageCompletionDay:Optional[int] = None

class Post(BaseModel):
    #images: List[UploadFile]
    title: str
    description: str
    option: Optional[List[str]] = None
    price: int
    averageCompletionDay: Optional[int] = None

class Team(BaseModel):
    title: str
    description: str
    recruitmentStatus: bool = True

class PreviewTeam(BaseModel):
    title: str
    description: str
    recruitmentStatus: Optional[bool] = True
    def __init__(self, title, description, recruitmentStatus):
        title:str
        description:str
        recruitmentStatus: Optional[bool] = True

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
    memberId: UUID4

previewPostsData = []
posts  = {}  
previewTeamRecruitmentData = []  
teams = {}
previewReviewsData = [] 
reviews = {}
registed = {}
profiles = {}
baskets  = {}

@app.get("/")
async def test():
    return "호출됨"

@app.get("/posts/list/{page}", deprecated=False, tags=["게시판"]) #게시판 목록 ?????
async def get_posts(page: int):
    previewPosts = []
    cnt = 0
    start = (page - 1) * 10 #1페이지 = 0
    end = page * 10 #1페이지 = 10 
    for writtenOrder in range(start, end):
        previewPosts.append(previewPostsData[writtenOrder])
    # for writtenOrder in range(start, end): #10개의 게시판
    #     memberId = previewPostsData[writtenOrder].keys
    #     previewPosts.append(previewPostsData[writtenOrder].get(memberId))
    #     cnt+=1 아래와 같은 구조 일때 사용
    # previewPostsData = [{memberId : 
    #                       [  ... ], [ ... ]}]

    return previewPosts

@app.get("/post/{memberId}/{written_num}", tags=["게시판"]) #게시판 상세 조회
async def get_post(memberId: str, written_num: int):
    # if not posts[memberId]: #작동을안함 몰?루
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다.")
    post = posts[memberId][written_num]
    return posts

@app.post("/post/create", tags=["게시판"]) #게시판 만들기
async def create_post(post: Post):
    memberId = str(uuid.uuid4())  # 나중에 회원정보에서 자동생성
    newPost = {f"post{len(posts[memberId]) + 1}": post.dict()}  # 새 게시물 생성
    newPreview = {}
    newPreview.update(**post) #나중에 값 더 추가
    previewPostsData.append(newPreview)
    if memberId in posts:
        posts[memberId].append(newPost)
    else:
        posts[memberId] = [newPost]
    return posts  # 나중에 {"message": "게시판 생성 완료"} 등으로 변경 가능

@app.put("/post/{memberId}/{written_num}", tags=["게시판"]) #게시판 수정
async def modify_post(memberId: str, written_num: int, post: Post):
    posts[memberId][written_num] = post.dict() 
    return posts[memberId][written_num]


@app.get("/team_recruitment/posts/{page}", deprecated=False, tags=["팀 모집"])
async def get_team_recruitment_list(page: int):
    
    teamRecruitmentList = []
    start = (page - 1) * 10 #1페이지 = 0
    end = page * 10 #1페이지 = 10 
    for writtenOrder in range(start, end): #10개의 게시판
        teamRecruitmentList.append(previewTeamRecruitmentData[writtenOrder])

    return teamRecruitmentList

@app.post("/team_recruitment/create", tags=["팀 모집"]) 
async def create_team_recruitment(team: Team):
    memberId = str(uuid.uuid4()) 
    newPost = {f"post{len(previewTeamRecruitmentData[memberId]) + 1}": team.dict()}
    newPreview = {}
    newPreview.update(**team)
    previewTeamRecruitmentData.append(newPreview)

    if memberId in teams:
        teams[memberId].append(newPost)
    else:
        teams[memberId] = [newPost]

    return teams

@app.get("/reviews/{page}", tags=["리뷰"])
async def get_reviews(page:int):
    previewReviews=[]
    start = (page-1)*10 
    end = page*10 
    for writtenOrder in range(start, end):
        previewReviews.append(previewPostsData[writtenOrder])
    
    return previewReviews

@app.post("review/create", tags=["리뷰"])
async def create_review(review: Review):
    memberId = str(uuid.uuid4()) 
    newPost = {f"post{len(review[memberId]) + 1}": review.dict()} 
    newPreview = {}
    newPreview.update(**review)
    previewTeamRecruitmentData.append(newPreview)

    if memberId in reviews:
        reviews[memberId].append(newPost)
    else:
        reviews[memberId] = [newPost]
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
    
    memberId = str(uuid.uuid4())
    profiles.update({memberId:[{**profile.dict(), "id":id, "password":password, "email" : email}]})

    return {"message":"회원가입 성공!"}

async def mypage(memberId:str): 
    profile={}
    profile=profiles[memberId]
    return profile

@app.get("/mypage/{memberId}", tags={"마이페이지"})
async def get_mypage(memberId:str):
    return mypage(memberId)

@app.patch("/mypage/image/{memberId}", tags={"마이페이지"})
async def patch_mypage(memberId:str, image_change:HttpUrl | UploadFile):
    profiles.update({memberId : [image_change]})

    return mypage(memberId)

@app.patch("/mypage/background/{memberId}", tags={"마이페이지"})
async def patch_mypage(memberId:str, background_change:HttpUrl | UploadFile):
    profiles.update({memberId:[background_change]})

    return {"message":"배경 이미지 변경이 완료되었습니다."}

@app.patch("/mypage/email/{memberId}", tags={"마이페이지"})
async def patch_mypage(memberId:str, email_change:str):
    profiles.update({memberId:[email_change]})

    return {"message":"이메일 변경이 완료되었습니다."}

#////
@app.patch("/mypage/password/{memberId}", tags={"마이페이지"})
async def patch_mypage(memberId:str, password_change:Annotated[str, Form(min_length=8)]):

    if not re.search(r"[a-z]", password_change):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="소문자가 없습니다.")
    if not re.search(r"[A-Z]", password_change):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="대문자가 없습니다.")
    if not re.search(r"[!@#$%^&*]"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="특수문자가 없습니다.")
    
    profiles.update({memberId:[password_change]})

    return {"message":"비밀번호 변경이 완료되었습니다."}

@app.get("/mypost/list/{memberId}", tags={"마이페이지"})
async def get_mypost_list(memberId:str):
    myposts = previewPosts[memberId]

    return myposts

@app.post("/basket/add/{url}", tags={"마이페이지"})
async def add_basket(memberId:str, url:HttpUrl):
    baskets.update({memberId:[url]})
    return {"message":"게시글을 장바구니에 추가했습니다."}

@app.get("/baskets/{memberId}", tags={"마이페이지"})
async def get_baskets(memberId:str):
    mybaskets = baskets[memberId]

    return mybaskets