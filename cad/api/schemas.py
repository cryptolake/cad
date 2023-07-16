#!/usr/bin/env python3
from pydantic import BaseModel
import dataclasses

class AdBase(BaseModel):
    text: str
    short: str
    headline: str

class Ad(AdBase):
    id: int
    prompt_id: int
    theme_id: int
    image_loc: str

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

class TextBase(BaseModel):
    font: str
    size: int
    x: int
    y: int
    color: str

class Text(TextBase):
    class Config:
        orm_mode = True

class ThemeBase(BaseModel):
    headline: TextBase
    short: TextBase
    image_loc: str

class Theme(ThemeBase):
    headline: Text
    short: Text
    id: int
    ads: list[Ad]

    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    location: str
    size: int

class Image(ImageBase):
    id: str

    class Config:
        orm_mode = True

