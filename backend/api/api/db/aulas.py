from database import Base
from sqlalchemy import Column, Date, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Aulas(Base):
    """Aulas SQLAlchemy model
    """
    __tablename__ = "aulas"

    id_aula = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_uc = Column(Integer, ForeignKey("uc.id_uc"))
    id_docente = Column(Integer, ForeignKey("docentes.id_docente"))
    id_periodo = Column(Integer, ForeignKey("periodos.id_periodo"))
    data = Column(Date, nullable=False)
    resumo = Column(String)
    sumario = Column(String)
    sala = Column(Integer)

    presencas = relationship("Presencas")


class Presencas(Base):
    __tablename__ = "presencas"

    id_aula = Column(Integer, ForeignKey("aulas.id_aula"), primary_key=True)
    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), primary_key=True)
    confirmacao = Column(DateTime)

