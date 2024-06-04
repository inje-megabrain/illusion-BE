from fastapi import FastAPI, status, HTTPException, Form, UploadFile
from typing import List, Optional, Annotated, Dict
from pydantic import BaseModel, HttpUrl, UUID4
import re
import uuid

app = FastAPI()

class PostRequest(BaseModel):
    images: List[str]
    title: str
    description: str
    option: Optional[List[HttpUrl]] = None
    price: int
    averageCompletionDay: Optional[int] = None

class PostResponse(BaseModel):
    images: List[HttpUrl]
    title: str
    description: str
    option: Optional[List[str]] = None
    price: int
    averageCompletionDay: Optional[int] = None

class PreviewPost(BaseModel):
    images: HttpUrl
    title: str
    price: int
    rate: Optional[float] = None
    completionCount: Optional[int] = None
    averageCompletionDay: Optional[int] = None

class TeamRequest(BaseModel):
    title: str
    description: str
    recruitmentStatus: bool = True

class TeamResponse(BaseModel):
    title: str
    description: str
    recruitmentStatus: bool = True

class PreviewTeam(BaseModel):
    title: str
    description: str
    recruitmentStatus: bool

class ReviewRequest(BaseModel):
    #image: List[UploadFile]
    title: str
    description: str
    rate :  float

class ReviewResponse(BaseModel):
    #image: List[UploadFile]
    title: str
    description: str
    rate :  float

class PreviewReview(BaseModel):
    #image: HttpUrl | UploadFile 
    title: str
    description: str
    rate : float
    
class UserRequest(BaseModel):
    id : str
    password : str
    email : str

class UserResponse(BaseModel):
    id : str
    email : str

class ProfileRequest(BaseModel):
    #profileImage: HttpUrl | UploadFile 
    #background_image: HttpUrl | UploadFile
    introduce: str
    nickname: str

class ProfileOutRespone(BaseModel):
    #profileImage: HttpUrl | UploadFile 
    #background_image: HttpUrl | UploadFile
    introduce: str
    nickname: str

@app.get("/")
async def test():
    return "호출됨"

@app.get("/boards/{board_id}/posts", deprecated=False, tags=["게시판"]) #게시판 목록
async def get_posts(page : int = 1):
    posts = [
        PreviewPost(
            images="https://blog.kakaocdn.net/dn/YxTP7/btsytu8PS9l/N269ER2zDdjzw8EUFxSWzK/img.png",
            title="푸바오",
            price=5000,
            rate=3.5,
            completionCount=2,
            averageCompletionDay=1
        ),
        PreviewPost(
            images="https://designbase.co.kr/wp-content/uploads/2022/03/illustrator-advanced-15-overview.jpg",
            title="나만의 작은 일러스트",
            price=7000,
            rate=4,
            completionCount=5,
            averageCompletionDay=1
        ),
        PreviewPost(
            images="https://d2v80xjmx68n4w.cloudfront.net/gigs/fOV7z1701237488.jpg",
            title="캐릭터 일러스트",
            price=50000,
            rate=5,
            completionCount=3,
            averageCompletionDay=10
        ),
        PreviewPost(
            images="https://www.clipstudio.net/wp-content/uploads/2019/08/0033_000.jpg",
            title="게임 일러스트",
            price=100000,
            rate=4,
            completionCount=23,
            averageCompletionDay=30
        ),
        PreviewPost(
            images="https://d2v80xjmx68n4w.cloudfront.net/gigs/FGS081673528026.jpg",
            title="간단하지만 귀여운 일러스트",
            price=10000,
            rate=3,
            completionCount=2,
            averageCompletionDay=7
        ),
        PreviewPost(
            images="https://mblogthumb-phinf.pstatic.net/MjAyMTA3MTRfMzUg/MDAxNjI2MjYyMDc5Nzc3.a2oZYaolOOHvW5rCZDDUJFiRJAvqN_mMnaB_NyJ4HqMg.VS6CekjVsm9_j3sjt3tq4ydl7ZeHzS5BvPhqA89yVNwg.PNG.gkfngkfn414/%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%ED%84%B0_%EA%B7%80%EC%97%AC%EC%9A%B4_%EA%B7%B8%EB%A6%BC%EA%B7%B8%EB%A6%AC%EA%B8%B020.png?type=w800",
            title="우리집 고양이",
            price=5000,
            rate=2,
            completionCount=2,
            averageCompletionDay=1
        ),
        PreviewPost(
            images="https://blog.kakaocdn.net/dn/YxTP7/btsytu8PS9l/N269ER2zDdjzw8EUFxSWzK/img.png",
            title="title",
            price=1000000,
            rate=3.5,
            completionCount=2,
            averageCompletionDay=1
        ),
        PreviewPost(
            images="https://d2v80xjmx68n4w.cloudfront.net/gigs/d3BPj1706541860.jpg",
            title="ai 일러스트",
            price=50000,
            rate=0,
            completionCount=0,
            averageCompletionDay=5
        ),
        PreviewPost(
            images="https://i.pinimg.com/236x/de/a5/11/dea5116a5c02a05423824ff0fa02177d.jpg",
            title="웹툰 일러스트",
            price=70000,
            rate=4.5,
            completionCount=7,
            averageCompletionDay=15
        ),
        PreviewPost(
            images="https://d2v80xjmx68n4w.cloudfront.net/gigs/lHeK11645496339.jpg",
            title="트렌디 하고 예쁜 일러스트",
            price=70000,
            rate=4,
            completionCount=3,
            averageCompletionDay=10
        ),
        ]

    return posts

@app.get("/post", tags=["게시판"]) #게시판 상세 조회
async def get_post(memberId: int = 0):
    post = PostResponse(
        images=[
            "https://img.freepik.com/premium,-vector/cute-dog-illustration_841637-29.jpg",
            "https://png.pngtree.com/png-vector/20230221/ourmid/pngtree-cute-dog-illustration-png-image_6612074.png",
            "https://png.pngtree.com/png-clipart/20230330/original/pngtree-cute-dog-illustration-png-image_9009551.png"
        ],
        title = "title",
        description = "description",
        option = ["수정 가능횟수 3회", "옵션2"],
        price = 35000,
        averageCompletionDay = 5    
    )
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
