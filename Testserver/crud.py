from sqlalchemy.orm import Session
import models
import schemas

def get_preview_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PreviewPost).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(models.Post).join().filter(models.Post.postId == post_id).first()

def get_preview_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PreviewReview).offset(skip).limit(limit).all()

def get_review(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Review.postId == post_id).first()




def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
