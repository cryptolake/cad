#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles


from . import gen_ai, schemas, crud
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

@app.post("/api/ads", response_model=list[schemas.Ad])
def create_ad(prompt: schemas.PromptBase, db: Session = Depends(get_db)):
    db_prompt = crud.create_prompt(db=db, prompt=prompt)
    ads = gen_ai.generate_ad(**prompt.dict())
    if ads is None:
        raise HTTPException(status_code=500,
                            detail="There was a problem generating you ad.")
    db_ads = [crud.create_ad(db=db, ad=schemas.AdBase(**ad),
                                     prompt_id=db_prompt.id) for ad in ads]
    return db_ads

@app.get("/api/ads", response_model=list[schemas.Ad])
def get_ads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ads = crud.get_ads(db=db, skip=skip, limit=limit)
    return ads


@app.get("/api/ads/{ad_id}", response_model=schemas.Ad)
def get_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = crud.get_ad(db=db, ad_id=ad_id)
    if ad is None:
        raise HTTPException(status_code=404,
                            detail="Ad not found")
    return ad

@app.get("/api/prompts", response_model=list[schemas.Prompt])
def get_prompts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prompts = crud.get_prompts(db=db, skip=skip, limit=limit)
    return prompts


@app.get("/api/prompts/{prompt_id}", response_model=schemas.Prompt)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = crud.get_prompt(db=db, prompt_id=prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404,
                            detail="Prompt not found")
    return prompt
