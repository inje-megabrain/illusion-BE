from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Post(Base):
    __tablename__ = "posts"

    postId = Column(Integer, unique=True, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    averageCompletionDay = Column(Integer, nullable=True)
    options = relationship("Option", back_populates="post")
    imagelist = relationship("Image", back_populates="postImages")
    post = relationship("User", back_populates="posts")

    user_id = relationship()

class PreviewPost(Base):
    __tablename__ = "preview_posts"

    title = Column(String, index=True)
    price = Column(Integer)
    averageCompletionDay = Column(Integer, nullable=True)
    imagelist = relationship("Image", back_populates="postImages")

class Option(Base):
    __tablename__ = "options"

    listOption = Column(String, nullable=True)

    post = relationship("Post", back_populates="options")

class Review(Base):
    __tablename__ = "review"
    
    reviewPostId = Column(Integer, unique=True, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    rate = Column(float)

    review = relationship("User", back_populates= "reviews")
    reviewImages = relationship("Image", back_populates="reviewImage")

class PreviewReview(Base):
    __tablename__ = "review"
    
    reviewPostId = Column(Integer, unique=True, primary_key=True)
    title = Column(String, index=True)
    rate = Column(float)

    review = relationship("User", back_populates= "reviews")
    reviewImages = relationship("Image", back_populates="reviewImage")

class Image(Base):
    __tablename__ = "images"

    fileName = Column(String, nullable=False)
    filePath = Column(String, nullable=False)

    reviewImageId = Column(Integer, ForeignKey("reviews.id"))
    reviewImage = relationship("Review", back_populates= "reviewImages")

    profileImageId = Column(Integer, ForeignKey("users.id"))
    profileImage = relationship("User", back_populates="profileImages")

    backgroundImageId = Column(Integer, ForeignKey("users.id"))
    backgroundImage = relationship("User", back_populates="backgroundImages")

    postImagesId = Column(Integer, ForeignKey("posts.id"))
    postImages = relationship("Post", back_populates="imagelist")

    previewPostImagesId = Column(Integer, ForeignKey("posts.id"))
    previewPostImages = relationship("PreviewPost", back_populates="imagelist")

class PreviewTeamPost(Base):
    __tablename__ = "teams"

    postId = Column(String, index=True, primary_key=True)
    title = Column(String, index=True)
    recruitmentStatus = Column(Boolean)

class TeamPost(PreviewTeamPost):
    __tablename__ = "team_post"
    description = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nickname = Column(String, index=True)
    hashedPassword = Column(String)
    memberId = Column(String, index=True)
    introduce = Column(String)

    profileImages = relationship("Image", back_populates="profileImage")
    backgroundImages = relationship("Image", back_populates="backgroundImage")
    reviews = relationship("Review", back_populates="review")
    posts = relationship("Post", back_populates="post")
