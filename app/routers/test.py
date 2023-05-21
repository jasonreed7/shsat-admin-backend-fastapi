from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import test_repository

from ..schemas import test as test_schemas

router = APIRouter()


@router.get("/officialTests/", response_model=list[test_schemas.OfficialTest])
def get_official_tests(db: Session = Depends(get_db)):
    return test_repository.get_official_tests(db)
