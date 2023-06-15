from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str]


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


class SubcategoryUpdate(BaseModel):
    name: Optional[str]


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


class TagUpdate(BaseModel):
    name: Optional[str]


class Tag(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TagReference(BaseModel):
    id: int


class ResourceBase(BaseModel):
    tag_id: int
    name: Optional[str]
    url: str
    link_text: str

    class Config:
        orm_mode = True


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str]
    url: Optional[str]
    link_text: Optional[str]


class Resource(ResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
