from sqlalchemy.orm import Session

from . import schemas
from .db import models
from dataclasses import dataclass


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

def create_ad(db: Session, ad: schemas.AdBase,
              prompt_id: int, theme_id: int, image_loc: str):
    db_ad = models.Ad(**ad.dict(), prompt_id=prompt_id,
                      theme_id=theme_id, image_loc=image_loc)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

def get_themes(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Theme).offset(skip).limit(limit).all()

def get_theme(db: Session, theme_id: int):
    return db.query(models.Theme).filter(models.Theme.id == theme_id).first()

@dataclass
class Text:
    font: str
    size: int
    color: str
    x: int
    y: int

def create_theme(db: Session, theme: schemas.ThemeBase):
    theme_dict = theme.dict()
    theme_dict.update({
            "headline": Text(**theme_dict['headline']),
            "short": Text(**theme_dict['short'])
    })
    db_theme = models.Theme(**theme_dict)
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme

def get_image(db: Session, image_id: str):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

def create_image(db: Session, image: schemas.ImageBase, image_hash: str):
    db_image = models.Image(id=image_hash,
                            location=image.location, size=image.size)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
