from typing import List, Optional
from pydantic import BaseModel, validator


class User(BaseModel):
    nome_utilizador: str
    email: str
    password: str


class ShowUser(BaseModel):
    id_utilizador: int
    nome_utilizador: str
    email: str

    class Config:
        orm_mode = True
