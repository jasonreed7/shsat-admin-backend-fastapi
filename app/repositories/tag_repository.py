from sqlalchemy import select
from app.models import tag as tag_models
from app.schemas import tag as tag_schemas
from app.database import SessionLocal


def get_categories(db: SessionLocal) -> list[tag_models.Category]:
    stmt = select(tag_models.Category).order_by(tag_models.Category.name)
    result = db.scalars(stmt).all()
    return result