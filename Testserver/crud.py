from sqlalchemy.orm import Session
import models
import schemas

# 게시판 목록
def get_preview_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

# 게시판 상세 조회
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.postId == post_id).first()

# 리뷰 게시판 목록
def get_preview_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Review).offset(skip).limit(limit).all()

# 리뷰 게시판
def get_review(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Review.postId == post_id).first()

# 팀 게시판 목록
def get_teams(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.TeamPost).offset(skip).limit(limit).all()

# 팀 게시판
def get_team_post(db: Session, post_id: int):
    return db.query(models.TeamPost).filter(models.TeamPost.teamPostId == post_id).first()

# 게시판 만들기
def create_post(db: Session, post: schemas.PostRequest):
    db_post = models.Post(
        title = post.title,
        description = post.description,
        price = post.price,
        averageCompletionDay = post.averageCompletionDay,
        optionList = post.option,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# 팀 게시판 만들기
def create_team_post(db: Session, team: schemas.TeamRequest):
    db_team = models.TeamPost(
        title = team.title,
        description = team.description,
        recruitmentStatus = team.recruitmentStatus,
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

# 리뷰 게시판 만들기
def create_review(db: Session, review: schemas.ReviewRequest):
    db_review = models.Review(
        title = review.title,
        description = review.description,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# 회원가입
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 중복확인
def get_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()