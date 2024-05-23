from sqlalchemy.orm import Session
import models
import schemas

def get_preview_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PreviewPost).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.postId == post_id).first()
#.join() 
def get_preview_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PreviewReview).offset(skip).limit(limit).all()

def get_review(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Review.postId == post_id).first()

def get_teams(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PreviewTeamPost).offset(skip).limit(limit).all()

def get_team_post(db: Session, post_id: int):
    return db.query(models.TeamPost).filter(models.TeamPost.postId == post_id).first()

def create_post(db: Session, post: schemas.PostRequest):
    db_post = models.Post(post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def create_team_post(db: Session, team: schemas.TeamRequest):
    db_team = models.TeamPost(team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def create_review(db: Session, review: schemas.ReviewRequest):
    db_review = models.Review(review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review



# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user