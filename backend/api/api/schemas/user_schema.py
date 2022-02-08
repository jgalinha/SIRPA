from pydantic import BaseModel


class UserBase(BaseModel):
    nome_utilizador: str
    email: str

class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True

class ShowUser(UserBase):
    id_utilizador: int
    public_key: str

    class Config:
        orm_mode = True
