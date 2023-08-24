from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel


class CategoryBase(CamelModel):
    name: str

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CamelModel):
    name: Optional[str]


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime


class SubcategoryBase(CamelModel):
    category_id: int
    name: str

    class Config:
        orm_mode = True


class SubcategoryCreate(SubcategoryBase):
    pass


class SubcategoryUpdate(CamelModel):
    name: Optional[str]


class Subcategory(SubcategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TagBase(CamelModel):
    subcategory_id: int
    name: str

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    pass


class TagUpdate(CamelModel):
    name: Optional[str]


class Tag(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TagReference(CamelModel):
    id: int


class ResourceBase(CamelModel):
    tag_id: int
    name: Optional[str]
    url: str
    link_text: str

    class Config:
        orm_mode = True


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(CamelModel):
    name: Optional[str]
    url: Optional[str]
    link_text: Optional[str]


class Resource(ResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
