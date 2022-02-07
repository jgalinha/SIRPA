from pydoc import classname
from tkinter.tix import Balloon
from database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date, null
from sqlalchemy.orm import relationship


class Cursos(Base):
    """Cursos SQLAlchemy model

    """
    __tablename__ = "cursos"
    
    id_curso = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome_curso = Column(String, unique=True, nullable=False)
    descricao_curso = Column(String)

    ucs = relationship("UC", back_populates="curso")
    inscricoes_cursos = relationship("InscricoesCursos", back_populates="curso")

    
class InscricoesCursos(Base):
    """Inscricoes Cursos SQLAlchemy model
    """
    __tablename__ = "inscricoes_cursos"

    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), primary_key=True)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"), primary_key=True)
    id_ano_curricular = Column(Integer, ForeignKey("ano_curricular.id_ano"), primary_key=True)

    ano_curricular = relationship("AnoCurricular", back_populates="inscricoes_cursos")
    curso = relationship("Cursos", back_populates="inscricoes_cursos")
    aluno = relationship("Alunos", back_populates="inscricoes_cursos")


class Semestres(Base):
    """Semestres SQLAlchemy model
    """
    __tablename__ = "semestres"

    id_semestre = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_ano_curricular = Column(Integer, ForeignKey("ano_curricular.id_ano"), nullable=False)
    nome_semestre = Column(String, unique=True, nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)

    ano_curricular = relationship("AnoCurricular", back_populates="semestres")
    ucs = relationship("SemestresUC", back_populates="semestre")

class AnoCurricular(Base):
    """Ano Curricular SQLAlchemy model
    """
    __tablename__ = "ano_curricular"
    
    id_ano = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ano = Column(String, unique=True, nullable=False)

    inscricoes_cursos = relationship("InscricoesCursos", back_populates="ano_curricular")
    semestres = relationship("Semestres", back_populates="ano_curricular")
    

class Periodos(Base):
    """Periodos SQLAlchemy model
    """
    __tablename__ = "periodos"

    id_periodo = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_uc = Column(Integer, ForeignKey("uc.id_uc"), nullable=False)
    dia_semana = Column(String, nullable=False)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fim = Column(DateTime, nullable=False)

    aulas = relationship("Aulas", back_populates="periodo")
    uc = relationship("UC", back_populates="periodos")
    

class UC(Base):
    """Unidade Curricular SQLAlchemy model
    """
    __tablename__ = "uc"

    id_uc = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"), nullable=False)
    nome_uc = Column(String, nullable=False)
    descricao = Column(String)

    aulas = relationship("Aulas", back_populates="uc") 
    curso = relationship("Cursos", back_populates="ucs")
    docentes = relationship("UCDocentes", back_populates="uc")
    periodos = relationship("Periodos", back_populates="uc")
    inscricoes = relationship("InscricoesUC", back_populates="uc")

    semestres = relationship("SemestresUC", back_populates="uc")


class SemestresUC(Base):
    __tablename__ = "semestres_uc"

    id_uc = Column(Integer, ForeignKey("uc.id_uc"), primary_key=True)
    id_semestre = Column(Integer, ForeignKey("semestres.id_semestre"), primary_key=True)

    uc = relationship("UC", back_populates="semestres")
    semestre = relationship("Semestres", back_populates="ucs")


class UCDocentes(Base):
    """UC_Docentes SQLAlchemy model
    """
    __tablename__ = "uc_docentes"

    id_uc = Column(Integer, ForeignKey("uc.id_uc"), primary_key=True)
    id_docente = Column(Integer, ForeignKey("docentes.id_docente"), primary_key=True)

    docente = relationship("Docentes", back_populates="ucs")
    uc = relationship("UC", back_populates="docentes")

    
class InscricoesUC(Base):
    """Inscricoes UC SQLAlchemy model
    """
    __tablename__ = "inscricoes_uc"
    
    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), primary_key=True)
    id_uc = Column(Integer, ForeignKey("uc.id_uc"), primary_key=True)
    data_inscricao = Column(Date)

    aluno = relationship("Alunos", back_populates="inscricoes_ucs")
    uc = relationship("UC", back_populates="inscricoes")

