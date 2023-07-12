from __future__ import annotations
from typing import List
import dataclasses

from sqlalchemy import String, ForeignKey, Integer, Float, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite

from .database import Base

@dataclasses.dataclass
class Text:
    font: str
    size: int
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
    

class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str] = mapped_column(String(), nullable=False) 
    headline: Mapped[str] = mapped_column(String(), nullable=False) 
    short_text: Mapped[str] = mapped_column(String(), nullable=False) 

    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"))
    prompt: Mapped["Prompt"] = relationship(back_populates="ads")
    image: Mapped["AdImage"] = relationship(back_populates="ad")

##
# Ad Image Section
##
theme_image_assc = Table("theme_image_assc", Base.metadata,
                         Column("theme_id", Integer, ForeignKey('themes.id')),
                         Column("image_id", Integer, ForeignKey('images.id'))
                         )

adimage_image_assc = Table("adimage_image_assc", Base.metadata,
                         Column("adimage_id", Integer, ForeignKey('adimages.id')),
                         Column("image_id", Integer, ForeignKey('images.id'))
                         )

class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str] = mapped_column(String(), nullable=False) 
    size: Mapped[int] = mapped_column(Integer(), nullable=False)

class Theme(Base):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True)
    headline: Mapped[Text] = composite(mapped_column("h_font"),
                                       mapped_column("h_size"),
                                       mapped_column("h_x"),
                                       mapped_column("h_y"))
    short_text: Mapped[Text] = composite(mapped_column("s_font"),
                                       mapped_column("s_size"),
                                       mapped_column("s_x"),
                                       mapped_column("s_y"))
    adimages: Mapped[List["AdImage"]] = relationship(back_populates="theme")
    image: Mapped["Image"] = relationship(secondary=theme_image_assc)

class AdImage(Base):
    __tablename__ = "adimages"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped["Image"] = relationship(secondary=adimage_image_assc)
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"))
    theme: Mapped["Theme"] = relationship(back_populates="adimages")
    ad_id: Mapped[int] = mapped_column(ForeignKey("ads.id"))
    ad: Mapped["Ad"] = relationship(back_populates="adimage")
