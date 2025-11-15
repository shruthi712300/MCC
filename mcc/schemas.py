from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List, Union
from . import models

__all__ = ["TokenData", "User"]


class User(BaseModel):
    user_id: int
    user_type: str
    user_info: Union[models.Admin, models.Technician]

    class Config:
        arbitrary_types_allowed = True


class TokenData(BaseModel):
    username: Union[str, None] = None
    id: Union[str,int, None] = None
    user_type: Union[str, None] = None
