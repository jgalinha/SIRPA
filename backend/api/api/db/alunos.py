from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from db.aulas import Presencas

class Alunos(Base):
    __tablename__ = "alunos"
    
    id_aluno = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_utilizador = Column(Integer, ForeignKey("utilizadores.id_utilizador"), nullable=False)
    nome = Column(String, nullable=False)
    nr_aluno = Column(Integer, unique=True, nullable=False)

    presencas = relationship("Presencas", back_populates="aluno")
    inscricoes_cursos = relationship("InscricoesCursos", back_populates="aluno")
    inscricoes_ucs = relationship("InscricoesUC", back_populates="aluno")
    utilizador = relationship("User", back_populates="aluno")