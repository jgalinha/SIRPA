from database import Base
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Aulas(Base):
    """Aulas SQLAlchemy model"""

    __tablename__ = "aulas"

    id_aula = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_uc = Column(Integer, ForeignKey("uc.id_uc"), nullable=False)
    id_docente = Column(Integer, ForeignKey("docentes.id_docente"), nullable=False)
    id_periodo = Column(Integer, ForeignKey("periodos.id_periodo"), nullable=False)
    data = Column(Date, nullable=False)
    resumo = Column(String)
    sumario = Column(String)
    sala = Column(String, nullable=False)

    presencas = relationship("Presencas", back_populates="aula")
    docente = relationship("Docentes", back_populates="aulas")
    uc = relationship("UC", back_populates="aulas")
    periodo = relationship("Periodos", back_populates="aulas")


class Presencas(Base):
    __tablename__ = "presencas"

    id_aula = Column(Integer, ForeignKey("aulas.id_aula"), primary_key=True)
    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), primary_key=True)
    confirmacao = Column(DateTime)

    aula = relationship("Aulas", back_populates="presencas")
    aluno = relationship("Alunos", back_populates="presencas")
