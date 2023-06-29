#!/usr/bin/env python3
from pydantic import BaseModel

class AdBase(BaseModel):
    text: str
    # images: bytes

class Ad(AdBase):
    id: int
    prompt_id: int

    class Config:
        orm_mode = True


class PromptBase(BaseModel):
    name: str
    description: str
    parameters: str
    link: str | None = None
    n: int
    temp: float | None = None
    max_words: int

class Prompt(PromptBase):
    id: int
    ads: list[Ad] = []

    class Config:
        orm_mode = True
