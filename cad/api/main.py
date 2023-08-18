#!/usr/bin/env python3

from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, UploadFile, status

from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import gen_ai, schemas, crud, auth, ACCESS_TOKEN_EXPIRE_MINUTES
from .db import models, database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/generate_ads", response_model=schemas.Prompt)
async def generate_ads(prompt: schemas.PromptBase,
                       token: Annotated[str, Depends(oauth2_scheme)],
                       db: Session = Depends(get_db)):

    try:
        user = await auth.get_current_user(db=db, token=token)
    except Exception as e:
        raise e

    db_prompt = crud.create_prompt(db=db, prompt=prompt, user_id=user.id)

    ads = gen_ai.generate_ad(**prompt.dict())
    if ads is None:
        raise HTTPException(status_code=500,
                            detail="There was a problem generating the ad.")
    for ad in ads:
        crud.create_ad(db=db, ad=schemas.AdBase(**ad),
                       prompt_id=db_prompt.id)
    db_prompt = crud.get_prompt(db=db, prompt_id=db_prompt.id)
    return db_prompt

@app.get("/api/ads", response_model=list[schemas.Ad])
async def get_ads(
        token: Annotated[str, Depends(oauth2_scheme)],
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)):

    ads = crud.get_ads(db=db, skip=skip, limit=limit)
    return ads

@app.get("/api/ads/{id}", response_model=schemas.Ad)
async def get_ad(id: int,
                 token: Annotated[str, Depends(oauth2_scheme)],
                 db: Session = Depends(get_db)):
    ad = crud.get_ad(db=db, ad_id=id)
    if ad is None:
        raise HTTPException(status_code=404,
                            detail="Ad not found")
    return ad

@app.patch("/api/ads/{id}", response_model=schemas.Ad)
async def update_ads(data: schemas.Ad,
                     id: int,
                     token: Annotated[str, Depends(oauth2_scheme)],
                     db: Session = Depends(get_db)):
    ad = crud.get_ad(db=db, ad_id=id)
    if ad is None:
        raise HTTPException(status_code=404,
                            detail="Ad not found")
    ad_model = schemas.Ad(**ad.__dict__)
    update_data = data.dict(exclude_unset=True)
    updated_ad = ad_model.copy(update=update_data)
    
    ad = crud.update_ad(db=db, ad=updated_ad, id=id)

    return ad

@app.post("/api/prompts", response_model=list[schemas.Prompt])
async def create_prompt(prompt: schemas.PromptBase,
                        token: Annotated[str, Depends(oauth2_scheme)],
                        db: Session = Depends(get_db)):
    try:
        user = await auth.get_current_user(db=db, token=token)
    except Exception as e:
        raise e
    db_prompt = crud.create_prompt(db=db, prompt=prompt, user_id=user.id)
    return db_prompt


@app.get("/api/prompts/{prompt_id}", response_model=schemas.Prompt)
async def get_prompt(prompt_id: int,
                     token: Annotated[str, Depends(oauth2_scheme)],
                     db: Session = Depends(get_db)):
    prompt = crud.get_prompt(db=db, prompt_id=prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404,
                            detail="Prompt not found")
    return prompt

# @app.post("/api/upload_image", response_model=schemas.Image)
# async def upload_image(ad_id: int, image: UploadFile, db: Session = Depends(get_db)):

#     image_bytes = await image.read()
#     image_hash = img_ops.get_hash(image_bytes)

#     image_search = crud.get_image(db=db, image_id=image_hash)

#     if image_search  is not None:
#         return image_search

#     _, image_path, image_size = img_ops.save_image(image_bytes)

#     image_scheme = schemas.ImageBase(location=image_path,
#                                      size=image_size)

#     image_db = crud.create_image(db=db, image=image_scheme,
#                                  image_hash=image_hash, ad_id=ad_id)

#     return image_db


@app.post("/api/images", response_model=list[schemas.Image])
async def create_image(image: schemas.ImageBase,
                       uid: str,
                       token: Annotated[str, Depends(oauth2_scheme)],
                       ad_id: int,
                       db: Session = Depends(get_db)):
    db_image = crud.create_image(db=db, image=image,
                                 uid=uid, ad_id=ad_id)
    if db_image is None:
        raise HTTPException(status_code=404,
                            detail="Image not created")

    return db_image

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = auth.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
