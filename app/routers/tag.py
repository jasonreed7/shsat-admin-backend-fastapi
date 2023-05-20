from fastapi import APIRouter, Depends

from app.database import SessionLocal, get_db
from app.repositories import tag_repository
from app.schemas import tag as tag_schemas


router = APIRouter()


@router.get("/categories")
def get_categories(db: SessionLocal = Depends(get_db)) -> list[tag_schemas.Category]:
    return tag_repository.get_categories(db)
