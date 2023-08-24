from datetime import datetime

from fastapi_camelcase import CamelModel


class OfficialTest(CamelModel):
    id: int
    year: int
    form: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
