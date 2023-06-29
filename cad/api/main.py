#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from .db.database import SessionLocal
from .gen_ai import generate_ad
from .schemas import Prompt

app = FastAPI()

@app.post("/api/ads/")
def create_ad(prompt: Prompt):
    ads = generate_ad(**prompt.__dict__)
    if ads is None:
        raise HTTPException(status_code=500,
                            detail="There was a problem generating you ad.")
    return ads

@app.get("/api/ads/")
def get_ad():
    pass


@app.get("/api/prompts/")
def get_prompt():
    pass
