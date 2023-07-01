#!/usr/bin/env python3
from pydantic import BaseModel

class AdBase(BaseModel):
    text: str
    short_text: str
    headline: str
    # image: bytes

class Ad(AdBase):
    id: int
    prompt_id: int

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
