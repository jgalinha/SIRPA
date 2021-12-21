from typing import List, Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    nome_utilizador: str
    email: str
    public_key: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id_utilizador: int
    
    class Config:
        orm_mode = True