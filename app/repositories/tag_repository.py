from fastapi import HTTPException
from sqlalchemy import select

from app.database import SessionLocal
from app.models import tag as tag_models
from app.schemas import tag as tag_schemas


def get_categories(db: SessionLocal) -> list[tag_models.Category]:
    stmt = select(tag_models.Category).order_by(tag_models.Category.name)
    result = db.scalars(stmt).all()
    return result


def get_subcategories(db: SessionLocal) -> list[tag_models.Subcategory]:
    stmt = select(tag_models.Subcategory).order_by(tag_models.Subcategory.name)
    result = db.scalars(stmt).all()
    return result


def get_tags(db: SessionLocal) -> list[tag_models.Tag]:
    stmt = select(tag_models.Tag).order_by(tag_models.Tag.name)
    result = db.scalars(stmt).all()
    return result


def get_resources(db: SessionLocal) -> list[tag_models.Resource]:
    stmt = select(tag_models.Resource).order_by(tag_models.Resource.id)
    result = db.scalars(stmt).all()
    return result


def create_category(
    db: SessionLocal, category: tag_schemas.CategoryCreate
) -> tag_models.Category:
    category_model = tag_models.Category(name=category.name)

    db.add(category_model)
    db.commit()

    return category_model


def create_subcategory(
    db: SessionLocal, subcategory: tag_schemas.SubcategoryCreate
) -> tag_models.Subcategory:
    subcategory_model = tag_models.Subcategory(
        category_id=subcategory.category_id, name=subcategory.name
    )

    db.add(subcategory_model)
    db.commit()

    return subcategory_model


def create_tag(db: SessionLocal, tag: tag_schemas.TagCreate) -> tag_models.Tag:
    tag_model = tag_models.Tag(subcategory_id=tag.subcategory_id, name=tag.name)

    db.add(tag_model)
    db.commit()

    return tag_model


def create_resource(
    db: SessionLocal, resource: tag_schemas.ResourceCreate
) -> tag_models.Resource:
    resource_model = tag_models.Resource(
        tag_id=resource.tag_id,
        name=resource.name,
        url=resource.url,
        link_text=resource.link_text,
    )

    db.add(resource_model)
    db.commit()

    return resource_model


def update_category(
    db: SessionLocal, category_id: int, category_update: tag_schemas.CategoryUpdate
) -> tag_models.Category:
    category_model = db.get(tag_models.Category, category_id)
    if not category_model:
        raise HTTPException(400, f"Passage not found, id: {category_id}")
    category_data = category_update.dict(exclude_unset=True)
    for key, value in category_data.items():
        setattr(category_model, key, value)

    db.add(category_model)

    db.commit()
    return category_model


def update_subcategory(
    db: SessionLocal,
    subcategory_id: int,
    subcategory_update: tag_schemas.SubcategoryUpdate,
) -> tag_models.Subcategory:
    subcategory_model = db.get(tag_models.Subcategory, subcategory_id)
    if not subcategory_model:
        raise HTTPException(400, f"Passage not found, id: {subcategory_id}")
    subcategory_data = subcategory_update.dict(exclude_unset=True)
    for key, value in subcategory_data.items():
        setattr(subcategory_model, key, value)

    db.add(subcategory_model)

    db.commit()
    return subcategory_model


def update_tag(
    db: SessionLocal, tag_id: int, tag_update: tag_schemas.TagUpdate
) -> tag_models.Tag:
    tag_model = db.get(tag_models.Tag, tag_id)
    if not tag_model:
        raise HTTPException(400, f"Passage not found, id: {tag_id}")
    tag_data = tag_update.dict(exclude_unset=True)
    for key, value in tag_data.items():
        setattr(tag_model, key, value)

    db.add(tag_model)

    db.commit()
    return tag_model


def update_resource(
    db: SessionLocal, resource_id: int, resource_update: tag_schemas.ResourceUpdate
) -> tag_models.Resource:
    resource_model = db.get(tag_models.Resource, resource_id)
    if not resource_model:
        raise HTTPException(400, f"Passage not found, id: {resource_id}")
    resource_data = resource_update.dict(exclude_unset=True)
    for key, value in resource_data.items():
        setattr(resource_model, key, value)

    db.add(resource_model)

    db.commit()
    return resource_model
