from sqlalchemy.orm import Session

from fastapi import status, HTTPException
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

def get_user_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user(db: Session, username: str | None):
    if username:
        return db.query(models.User).filter(models.User.username == username).first()

def get_user_ads(db: Session, user_id: int, skip: int, limit: int):
    user = get_user_id(db=db, user_id=user_id)
    if not user:
        return None
    return db.query(models.Ad).filter(models.Ad.prompt.in_(user.prompts)).offset(skip).limit(limit).all()

def get_user_ad(db: Session, user_id: int, ad_id: int):
    user = get_user_id(db=db, user_id=user_id)
    if not user:
        return None
    ad = get_ad(db=db, ad_id=ad_id)
    if not ad:
        return None
    if ad.prompt in user.prompts:
        return ad

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ad does not belong to user"
    )

def get_user_prompts(db: Session, user_id: int, skip: int = 0, limit: int = 0):
    return db.query(models.User.prompts).filter(models.User.id == user_id)\
                                .offset(skip).limit(limit).all()

def get_user_prompt(db: Session, user_id: int, prompt_id: int):
    prompt = db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()
    if not prompt:
        return None

    if prompt.user_id == user_id:
        return prompt

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Prompt does not belong to the user"
    )
