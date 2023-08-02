from __future__ import annotations
from typing import List
import dataclasses

from sqlalchemy import String, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite

from .database import Base

@dataclasses.dataclass
class Text:
    font: str
    size: int
    color: str
    x: int
    y: int

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

##
# Ad Image Section
##

class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str] = mapped_column(String(), nullable=False) 
    headline: Mapped[str] = mapped_column(String(), nullable=False) 
    short: Mapped[str] = mapped_column(String(), nullable=False) 

    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"))
    prompt: Mapped["Prompt"] = relationship(back_populates="ads")

    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"))
    theme: Mapped["Theme"] = relationship(back_populates="ads")

    image_loc: Mapped[str] = mapped_column(String(), nullable=False) 

class Image(Base):
    __tablename__ = "images"

    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    location: Mapped[str] = mapped_column(String(), nullable=False) 
    size: Mapped[int] = mapped_column(Integer(), nullable=False)

class Theme(Base):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True)
    headline: Mapped[Text] = composite(mapped_column("h_font"),
                                       mapped_column("h_size"),
                                       mapped_column("h_color"),
                                       mapped_column("h_x"),
                                       mapped_column("h_y"))
    short: Mapped[Text] = composite(mapped_column("s_font"),
                                       mapped_column("s_size"),
                                       mapped_column("s_color"),
                                       mapped_column("s_x"),
                                       mapped_column("s_y"))

    ads: Mapped[List["Ad"]] = relationship(back_populates="theme")

    image_loc: Mapped[str] = mapped_column(String(), nullable=False) 
