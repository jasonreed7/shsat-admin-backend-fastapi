from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime


class SubcategoryBase(BaseModel):
    category_id: int
    name: str

    class Config:
        orm_mode = True


class SubcategoryCreate(SubcategoryBase):
    pass


class Subcategory(SubcategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TagBase(BaseModel):
    subcategory_id: int
    name: str

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ResourceBase(BaseModel):
    tag_id: int
    name: Optional[str]
    url: str
    link_text: str

    class Config:
        orm_mode = True


class ResourceCreate(ResourceBase):
    pass


class Resource(ResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
