from sqlalchemy.orm import Session
from itertools import chain

from . import schemas
from .db import models


def get_prompts(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Prompt).offset(skip).limit(limit).all()

def get_prompt(db: Session, prompt_id: int):
    return db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()

def create_prompt(db: Session, prompt: schemas.PromptBase, user_id: int):
    db_prompt = models.Prompt(**prompt.dict(), user_id=user_id)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_ads(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Ad).offset(skip).limit(limit).all()

def get_ad(db: Session, ad_id: int):
    return db.query(models.Ad).filter(models.Ad.id == ad_id).first()

def create_ad(db: Session, ad: schemas.AdBase,
              prompt_id: int):
    db_ad = models.Ad(**ad.dict(), prompt_id=prompt_id)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

def update_ad(db: Session, id: int, ad: schemas.Ad):
    db_ad = db.query(models.Ad).filter(models.Ad.id == id)
    if db_ad is None:
        return None

    db_ad.update(ad.dict(), synchronize_session='fetch')
    db.commit()
    db.refresh(db_ad)

    return db_ad

def get_image(db: Session, image_id: str):
    return db.query(models.Image).filter(models.Image.uid == image_id).first()

def create_image(db: Session, image: schemas.ImageBase,
                 uid: str, ad_id: int):
    db_image = models.Image(uid=uid,
                            location=image.location,
                            ad_id=ad_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_user(db: Session, username: str | None):
    if username:
        return db.query(models.User).filter(models.User.username == username).first()

def get_user_ads(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    ads = list(chain.from_iterable(map(lambda prompt: prompt.ads, user.prompts)))
    return ads

def is_ad_user(db: Session, user_id: int, ad_id: int):
    pass
