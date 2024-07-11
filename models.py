from pydantic import BaseModel

from typing import Optional


class User(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
