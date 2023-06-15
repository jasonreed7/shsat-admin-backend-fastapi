from fastapi import APIRouter, Depends

from app.database import SessionLocal, get_db
from app.repositories import tag_repository
from app.schemas import tag as tag_schemas

router = APIRouter()


@router.get("/categories")
def get_categories(db: SessionLocal = Depends(get_db)) -> list[tag_schemas.Category]:
    return tag_repository.get_categories(db)


@router.get("/subcategories")
def get_subcategories(
    db: SessionLocal = Depends(get_db),
) -> list[tag_schemas.Subcategory]:
    return tag_repository.get_subcategories(db)


@router.get("/tags")
def get_tags(db: SessionLocal = Depends(get_db)) -> list[tag_schemas.Tag]:
    return tag_repository.get_tags(db)


@router.get("/resources")
def get_resources(db: SessionLocal = Depends(get_db)) -> list[tag_schemas.Resource]:
    return tag_repository.get_resources(db)


@router.post("/category")
def create_category(
    category: tag_schemas.CategoryCreate, db: SessionLocal = Depends(get_db)
) -> tag_schemas.Category:
    return tag_repository.create_category(db, category)


@router.patch("/category/{category_id}")
def update_category(
    category_id: int,
    category_data: tag_schemas.CategoryUpdate,
    db: SessionLocal = Depends(get_db),
) -> tag_schemas.Category:
    return tag_repository.update_category(db, category_id, category_data)


@router.post("/subcategory")
def create_subcategory(
    subcategory: tag_schemas.SubcategoryCreate, db: SessionLocal = Depends(get_db)
) -> tag_schemas.Subcategory:
    return tag_repository.create_subcategory(db, subcategory)


@router.patch("/subcategory/{subcategory_id}")
def update_subcategory(
    subcategory_id: int,
    subcategory_data: tag_schemas.SubcategoryUpdate,
    db: SessionLocal = Depends(get_db),
) -> tag_schemas.Subcategory:
    return tag_repository.update_subcategory(db, subcategory_id, subcategory_data)


@router.post("/tag")
def create_tag(
    tag: tag_schemas.TagCreate, db: SessionLocal = Depends(get_db)
) -> tag_schemas.Tag:
    return tag_repository.create_tag(db, tag)


@router.patch("/tag/{tag_id}")
def update_tag(
    tag_id: int, tag_data: tag_schemas.TagUpdate, db: SessionLocal = Depends(get_db)
) -> tag_schemas.Tag:
    return tag_repository.update_tag(db, tag_id, tag_data)


@router.post("/resource")
def create_resource(
    resource: tag_schemas.ResourceCreate, db: SessionLocal = Depends(get_db)
) -> tag_schemas.Resource:
    return tag_repository.create_resource(db, resource)


@router.patch("/resource/{resource_id}")
def update_resource(
    resource_id: int,
    resource_data: tag_schemas.ResourceUpdate,
    db: SessionLocal = Depends(get_db),
) -> tag_schemas.Resource:
    return tag_repository.update_resource(db, resource_id, resource_data)
