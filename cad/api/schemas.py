#!/usr/bin/env python3
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    disabled: bool | None = None

class UserInDB(User):
    password: str

    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    location: str

class Image(ImageBase):
    uid: str
    ad_id: int

    class Config:
        orm_mode = True

class AdBase(BaseModel):
    text: str
    short: str
    headline: str

class Ad(AdBase):
    id: int
    prompt_id: int
    images: list[Image] = []

    class Config:
        orm_mode = True

class PromptBase(BaseModel):
    brand_name: str
    product_name: str | None = None
    product_description: str
    parameters: str
    n: int
    temp: float | None = None
    max_words: int

class Prompt(PromptBase):
    id: int
    ads: list[Ad] = []

    class Config:
        orm_mode = True

