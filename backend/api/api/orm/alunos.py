from sqlalchemy import Column, ForeignKey, Integer
from database import Base

class Alunos(Base):
    __tablename__ = "alunos"
    
    id_aluno = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_utilizador = Column(Integer, ForeignKey("utilizadores.id_utilizador"))
    nr_aluno = Column(Integer, unique=True)