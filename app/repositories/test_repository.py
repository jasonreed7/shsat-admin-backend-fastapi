from sqlalchemy.orm import Session

from ..models import test as test_models


def get_official_tests(db: Session):
    return db.query(test_models.OfficialTest).all()
