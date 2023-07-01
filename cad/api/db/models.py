from __future__ import annotations
from typing import List

from sqlalchemy import String, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)

    brand_name: Mapped[str] = mapped_column(String(), nullable=False) 
    product_name: Mapped[str] = mapped_column(String(), nullable=True) 
    product_description: Mapped[str] = mapped_column(String(), nullable=False)
    parameters: Mapped[str] = mapped_column(String(), nullable=True)

    n: Mapped[int] = mapped_column(Integer(), nullable=False)
    temp: Mapped[float] = mapped_column(Float(), default=1.0)
    max_words: Mapped[int] = mapped_column(Integer(), nullable=False)
    ads: Mapped[List["Ad"]] = relationship(back_populates="prompt")
    

class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str] = mapped_column(String(), nullable=False) 
    headline: Mapped[str] = mapped_column(String(), nullable=False) 
    short_text: Mapped[str] = mapped_column(String(), nullable=False) 

    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"))
    prompt: Mapped["Prompt"] = relationship(back_populates="ads")
