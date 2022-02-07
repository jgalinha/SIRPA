from pydantic import BaseModel

class DocenteBase(BaseModel):
    """DocenteBase Pydantic model
    """
    id_docente: int
    nome: str