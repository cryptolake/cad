#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException, Depends, UploadFile
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from . import gen_ai, schemas, crud, img_ops
from .db import models, database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/generate_ads", response_model=list[schemas.Ad])
async def generate_ads(theme_id: int, prompt: schemas.PromptBase,
                       db: Session = Depends(get_db)):
    db_prompt = crud.create_prompt(db=db, prompt=prompt)
    db_theme = crud.get_theme(db=db, theme_id=theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404,
                            detail="Theme non existant")

    ads = gen_ai.generate_ad(**prompt.dict())
    if ads is None:
        raise HTTPException(status_code=500,
                            detail="There was a problem generating the ad.")
    ad_imgs = [
        img_ops.save_image(
            img_ops.create_image(image_loc=db_theme.image_loc,
                                headline=db_theme.headline,
                                short=db_theme.short,
                                headline_text=ad['headline'],
                                short_text=ad['short'] ))[1] for ad in ads
    ]
    db_ads = [crud.create_ad(db=db, ad=schemas.AdBase(**ad),
                                     prompt_id=db_prompt.id,
                                     theme_id=db_theme.id,
                                     image_loc=img_loc) for ad, img_loc in zip(ads, ad_imgs)]
    return db_ads

# @app.post("/api/ads", response_model=schemas.Ad)
# async def create_ad(ad: schemas.AdBase, prompt_id: int,
#               theme_id: int, image_loc: str, db: Session = Depends(get_db)):
#     db_ad = crud.create_ad(db=db, ad=ad, prompt_id=prompt_id,
#                         theme_id=theme_id, image_loc=image_loc)
#     if db_ad is None:
#         raise HTTPException(status_code=500,
#                             detail="There was a problem creating the ad.")
        
#     return db_ad

@app.get("/api/ads", response_model=list[schemas.Ad])
async def get_ads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ads = crud.get_ads(db=db, skip=skip, limit=limit)
    return ads


@app.get("/api/ads/{ad_id}", response_model=schemas.Ad)
async def get_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = crud.get_ad(db=db, ad_id=ad_id)
    if ad is None:
        raise HTTPException(status_code=404,
                            detail="Ad not found")
    return ad

@app.post("/api/themes", response_model=schemas.Theme)
async def create_theme(theme: schemas.ThemeBase,
                 db: Session = Depends(get_db)):
    db_theme = crud.create_theme(db=db, theme=theme)
    return db_theme

@app.get("/api/themes", response_model=list[schemas.Theme])
async def get_themes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    themes = crud.get_themes(db=db, skip=skip, limit=limit)
    return themes


@app.get("/api/themes/{theme_id}", response_model=schemas.Theme)
async def get_theme(theme_id: int, db: Session = Depends(get_db)):
    theme = crud.get_theme(db=db, theme_id=theme_id)
    if theme is None:
        raise HTTPException(status_code=404,
                            detail="Theme not found")
    return theme

@app.post("/api/prompts", response_model=list[schemas.Prompt])
async def create_prompt(prompt: schemas.PromptBase, db: Session = Depends(get_db)):
    db_prompt = crud.create_prompt(db=db, prompt=prompt)
    return db_prompt

@app.get("/api/prompts", response_model=list[schemas.Prompt])
async def get_prompts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prompts = crud.get_prompts(db=db, skip=skip, limit=limit)
    return prompts


@app.get("/api/prompts/{prompt_id}", response_model=schemas.Prompt)
async def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = crud.get_prompt(db=db, prompt_id=prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404,
                            detail="Prompt not found")
    return prompt

@app.post("/api/upload_image", response_model=schemas.Image)
async def upload_image(image: UploadFile, db: Session = Depends(get_db)):

    image_bytes = await image.read()
    image_hash = img_ops.get_hash(image_bytes)

    image_search = crud.get_image(db=db, image_id=image_hash)

    if image_search  is not None:
        return image_search

    _, image_path, image_size = img_ops.save_image(image_bytes)

    image_scheme = schemas.ImageBase(location=image_path,
                                     size=image_size)

    image_db = crud.create_image(db=db, image=image_scheme,
                                 image_hash=image_hash)

    return image_db
