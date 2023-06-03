from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.question import question_tag_table


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )


class Subcategory(Base):
    __tablename__ = "subcategory"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategory.id"))
    name: Mapped[str]
    resources: Mapped[List["Resource"]] = relationship(back_populates="tag")
    questions: Mapped[List["Question"]] = relationship(  # noqa: F821
        secondary=question_tag_table, back_populates="tags"
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )


class Resource(Base):
    __tablename__ = "resource"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"))
    tag: Mapped["Tag"] = relationship(back_populates="resources")
    name: Mapped[Optional[str]]
    url: Mapped[str]
    link_text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
