from pydantic import BaseModel

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
