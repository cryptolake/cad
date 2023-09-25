from __future__ import annotations
from typing import List, Optional

from sqlalchemy import String, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)

    brand_name: Mapped[str]
    product_name: Mapped[str] = mapped_column(String(), nullable=True) 
    product_description: Mapped[str]
    parameters: Mapped[str] = mapped_column(String(), nullable=True)

    n: Mapped[int]
    temp: Mapped[float] = mapped_column(Float(), default=1.0)
    max_words: Mapped[int]
    ads: Mapped[List["Ad"]] = relationship(back_populates="prompt")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="prompts")

##
# Ad Image Section
##

class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str]
    headline: Mapped[str]
    short: Mapped[str]

    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"))
    prompt: Mapped["Prompt"] = relationship(back_populates="ads")

    images: Mapped[List["Image"]] = relationship(back_populates="ad")

class Image(Base):
    __tablename__ = "images"

    uid: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    location: Mapped[str]
    ad_id: Mapped[int] = mapped_column(ForeignKey("ads.id"))
    ad: Mapped["Ad"] = relationship(back_populates="images")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str]
    password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(Boolean(), default=False) 

    prompts: Mapped[List["Prompt"]] = relationship(back_populates="user")
