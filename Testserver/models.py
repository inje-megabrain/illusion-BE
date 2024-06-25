from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class Post(Base):
    __tablename__ = "posts"

    postId = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    averageCompletionDay = Column(Integer, nullable=True)

    optionList = relationship("Option", back_populates="post")
    imageList = relationship("Image", back_populates="postImage")
    reviewList = relationship("Review", back_populates="post")

    user = relationship("User", back_populates="postList")
    memberId = Column(Integer, ForeignKey("users.memberId"))

    

# class PreviewPost(Base):
#     __tablename__ = "preview_posts"

#     previewPostId = Column(Integer, primary_key=True, index=True)  # 기본 키 추가
#     title = Column(String, index=True)
#     price = Column(Integer)
#     averageCompletionDay = Column(Integer, nullable=True)
#     imagelist = relationship("Image", back_populates="previewPostImages")

class Option(Base):
    __tablename__ = "options"

    optionId = Column(Integer, primary_key=True, index=True)  # 기본 키 추가
    listOption = Column(String, nullable=True)

    postId = Column(Integer, ForeignKey("post.postId"))
    post = relationship("Post", back_populates="optionList", foreign_keys=[postId])

class Review(Base):
    __tablename__ = "reviews"  # 테이블 이름 수정

    reviewPostId = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    rate = Column(Float)

    reviewImageList = relationship("Image", back_populates="reviewImage")

    postId = Column(Integer, ForeignKey("posts.postId"))
    post = relationship("Post", back_populates="reviewList", foreign_keys=[postId])

    memberId = Column(Integer, ForeignKey("user.memberId"))
    user = relationship("User", back_populates="reviewList", foreign_keys=[memberId])



# class PreviewReview(Base):
#     __tablename__ = "preview_reviews"  # 테이블 이름 수정

#     previewReviewPostId = Column(Integer, primary_key=True, index=True)  # 기본 키 추가
#     title = Column(String, index=True)
#     rate = Column(Float)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     review = relationship("User", back_populates="reviews")
#     reviewImages = relationship("Image", back_populates="reviewImage")

class Image(Base):
    __tablename__ = "images"

    imageId = Column(Integer, primary_key=True, index=True) 
    fileName = Column(String, nullable=False)
    filePath = Column(String, nullable=False)

    postId = Column(Integer, ForeignKey("postImage.postId"))
    postImage = relationship("Post", back_populates="imageList", foreign_keys=[postId])

    reviewPostId = Column(Integer, ForeignKey("reviewImage.reviewPostId"))
    reviewImage = relationship("Review", back_populates="reviewImageList", foreign_keys=[reviewPostId])
    

    profileImageId = Column(Integer, ForeignKey("user.memberId"))
    backgroudImageId = Column(Integer, ForeignKey("user.memberId"))
    user = relationship("User", back_populates="profileImage", foreign_keys=[profileImageId])



# class PreviewTeamPost(Base):
#     __tablename__ = "preview_team_posts"  # 테이블 이름 수정

#     previewTeamPostId = Column(Integer, primary_key=True, index=True) 
#     title = Column(String, index=True)
#     recruitmentStatus = Column(Boolean)

class TeamPost(Base):
    __tablename__ = "team_posts"

    teamPostId = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    recruitmentStatus = Column(Boolean)

    user = relationship("User", back_populates="teamPostList")
    userId = Column(Integer, ForeignKey("users.memberId"))

class User(Base):
    __tablename__ = "users"

    memberId = Column(String, primary_key=True, index=True)
    id = Column(Integer, index=True)
    email = Column(String, unique=True, index=True)
    nickname = Column(String, index=True)
    hashedPassword = Column(String)
    introduce = Column(String)
    
    postList = relationship("Post", back_populates="user")
    reviewList = relationship("Review", back_populates="user")
    teamPostList = relationship("TeamPost", back_populates="user")
    profileImage = relationship("Image", back_populates="user")