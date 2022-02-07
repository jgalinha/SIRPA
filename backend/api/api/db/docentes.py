from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class Docentes(Base):
    """Class to define SQLAlchemy Docentes model

    """
    __tablename__ = "docentes"
    
    id_docente = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String)
    nr_docente = Column(Integer, unique=True)
    id_utilizador = Column(Integer, ForeignKey("utilizadores.id_utilizador"))