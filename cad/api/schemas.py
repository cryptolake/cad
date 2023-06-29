#!/usr/bin/env python3
from pydantic import BaseModel

class Prompt(BaseModel):
    name: str
    description: str
    parameters: str
    n: int
    max_words: int
    temp: float | None = None
    link: str | None = None

class Ad(BaseModel):
    text: str
    # images: bytes
