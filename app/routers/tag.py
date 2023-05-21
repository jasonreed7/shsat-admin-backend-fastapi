from fastapi import APIRouter, Depends

from app.database import SessionLocal, get_db
from app.repositories import tag_repository
from app.schemas import tag as tag_schemas


router = APIRouter()


@router.get("/categories")
def get_categories(db: SessionLocal = Depends(get_db)) -> list[tag_schemas.Category]:
    return tag_repository.get_categories(db)

@router.get("/subcategories")
def get_subcategories(db: SessionLocal = Depends(get_db)) -> list[tag_schemas.Subcategory]:
    return tag_repository.get_subcategories(db)

@router.get("/tags")
def get_tags(db: SessionLocal = Depends(get_db)) -> list[tag_schemas.Tag]:
    return tag_repository.get_tags(db)

@router.get("/resources")
def get_resources(db: SessionLocal = Depends(get_db)) -> list[tag_schemas.Resource]:
    return tag_repository.get_resources(db)


@router.post("/category")
def create_category(category: tag_schemas.CategoryCreate, db: SessionLocal = Depends(get_db)) -> tag_schemas.Category:
    return tag_repository.create_category(db, category)

@router.post("/subcategory")
def create_subcategory(subcategory: tag_schemas.SubcategoryCreate, db: SessionLocal = Depends(get_db)) -> tag_schemas.Subcategory:
    return tag_repository.create_subcategory(db, subcategory)

@router.post("/tag")
def create_tag(tag: tag_schemas.TagCreate, db: SessionLocal = Depends(get_db)) -> tag_schemas.Tag:
    return tag_repository.create_tag(db, tag)

@router.post("/resource")
def create_resource(resource: tag_schemas.ResourceCreate, db: SessionLocal = Depends(get_db)) -> tag_schemas.Resource:
    return tag_repository.create_resource(db, resource)