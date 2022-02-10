from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Docentes(Base):
    """Class to define SQLAlchemy Docentes model"""

    __tablename__ = "docentes"

    id_docente = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String, nullable=False)
    nr_docente = Column(Integer, unique=True, nullable=False)
    id_utilizador = Column(
        Integer, ForeignKey("utilizadores.id_utilizador"), nullable=False
    )

    aulas = relationship("Aulas", back_populates="docente")
    ucs = relationship("UCDocentes", back_populates="docente")
    utilizador = relationship("User", back_populates="docente")


class NaoDocentes(Base):
    """NaoDocentes SQLAlchemy model"""

    __tablename__ = "nao_docentes"

    id_nao_docente = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String, nullable=False)
    nr_nao_docente = Column(Integer, unique=True, nullable=False)
    id_utilizador = Column(
        Integer, ForeignKey("utilizadores.id_utilizador"), nullable=False
    )

    utilizador = relationship("User", back_populates="nao_docente")
