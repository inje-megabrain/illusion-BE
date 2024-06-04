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
    optionsId = Column(Integer, ForeignKey("options.optionId"))

    imageList = relationship("Image", back_populates="postImage")
    imagesId = Column(Integer, ForeignKey("images.imageId"))

    reviewList = relationship("Review", back_populates="post")

    user = relationship("User", back_populates="postList")
    userId = Column(Integer, ForeignKey("users.memberId"))

    

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

    post = relationship("Post", back_populates="options")

class Review(Base):
    __tablename__ = "reviews"  # 테이블 이름 수정

    reviewPostId = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    rate = Column(Float)

    reviewImageList = relationship("Image", back_populates="reviewImage")
    reviewImagesId = Column(Integer, ForeignKey("images.imageId"))

    post = relationship("Post", back_populates="reviewList")
    postId = Column(Integer, ForeignKey("posts.postId"))

    user = relationship("User", back_populates="reviewList")



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

    imageId = Column(Integer, primary_key=True, index=True)  # 기본 키 추가
    fileName = Column(String, nullable=False)
    filePath = Column(String, nullable=False)

    postImage = relationship("Post", back_populates="imageList")
    reviewImage = relationship("Review", back_populates="reviewImageList")

    user = relationship("User", back_populates="profileImage")


# class PreviewTeamPost(Base):
#     __tablename__ = "preview_team_posts"  # 테이블 이름 수정

#     previewTeamPostId = Column(Integer, primary_key=True, index=True)  # 기본 키 추가
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
    postId = Column(Integer, ForeignKey("posts.postId"))

    reviewList = relationship("Review", back_populates="user")
    reviewPostId = Column(Integer, ForeignKey("reviews.reviewPostId"))

    teamPostList = relationship("TeamPost", back_populates="user")
    teamPostId = Column(Integer, ForeignKey("team_posts.teamPostId"))

    profileImage = relationship("Image", back_populates="user")
    profileImageId = Column(Integer, ForeignKey("images.imageId"))

    backgroudImageId = Column(Integer, ForeignKey("images.imageId"))