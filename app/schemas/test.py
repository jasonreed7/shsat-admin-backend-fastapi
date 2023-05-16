from datetime import datetime
from pydantic import BaseModel

class OfficialTest(BaseModel):
    id: int
    year: int
    form: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True