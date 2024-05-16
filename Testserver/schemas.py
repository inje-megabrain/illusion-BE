from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import uuid
from fastapi import UploadFile

class Post(BaseModel):
    postId: int
    title: str
    description: str
    
class PostRequest(Post):
    #images: List[UploadFile]
    option: Optional[List[str]] = None
    price: int
    averageCompletionDay: Optional[int] = None

    class Config:
        orm_mode = True

class PostResponse(PostRequest):
    pass

#미리보기 화면은 database에서 일부부만 출력하는 기능사용해서 만들기
# User 클래스에서 id를 제외한 name, age 열 선택하여 가져오기
#user_data = session.query(User.name, User.age).all()

# Item 클래스에서 id를 제외한 title, description 열 선택하여 가져오기
#item_data = session.query(Item.title, Item.description).all()

# class PreviewPost(BaseModel):
#     #images: List[UploadFile]
#     title: str
#     price: int
#     rate: Optional[float] = None
#     completionCount: Optional[int] = None
#     averageCompletionDay: Optional[int] = None

class TeamRequest(Post):
    recruitmentStatus: bool = True
    class Config:
        orm_mode = True

class TeamResponse(TeamRequest):
    pass

class PreviewTeam(TeamRequest):
    #filther로 description 빼고 가져오기
    pass

class ReviewRequest(Post):
    image: List[UploadFile]
    rate :  float
    class Config:
        orm_mode = True

class ReviewResponse(ReviewRequest):
    pass

class PreviewReview(ReviewRequest):
    pass
    
class UserBase(BaseModel):
    email: str
    id: str
    nickname:  str
class UserCreate(UserBase):
    password : str

class User(UserBase):
    memeber_id: uuid
    profileImage: HttpUrl | UploadFile 
    background_image: HttpUrl | UploadFile
    introduce: str
    class Config:
        orm_mode = True

# class ProfileRequest(BaseModel):
#     #profileImage: HttpUrl | UploadFile 
#     #background_image: HttpUrl | UploadFile
#     introduce: str
#     nickname: str

# class ProfileOutRespone(BaseModel):
#     #profileImage: HttpUrl | UploadFile 
#     #background_image: HttpUrl | UploadFile
#     introduce: str
#     nickname: str