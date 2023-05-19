from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class OfficialTest(Base):
    __tablename__ = 'official_test'

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    form: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())