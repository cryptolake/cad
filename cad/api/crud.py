from sqlalchemy.orm import Session

from . import schemas
from .db import models


def get_prompts(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Prompt).offset(skip).limit(limit).all()

def get_prompt(db: Session, prompt_id: int):
    return db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()

def create_prompt(db: Session, prompt: schemas.PromptBase):
    db_prompt = models.Prompt(**prompt.dict())
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_ads(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Ad).offset(skip).limit(limit).all()

def get_ad(db: Session, ad_id: int):
    return db.query(models.Ad).filter(models.Ad.id == ad_id).first()

def create_ad(db: Session, ad: schemas.AdBase, prompt_id: int):
    db_ad = models.Ad(**ad.dict(), prompt_id=prompt_id)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad
