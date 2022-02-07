from pydantic import BaseModel

class AlunoBase(BaseModel):
    nome: str
    nr_aluno: int