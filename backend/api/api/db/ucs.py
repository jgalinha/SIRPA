from pydoc import classname
from database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date


class Cursos(Base):
    """Cursos SQLAlchemy model

    """
    __tablename__ = "cursos"
    
    id_curso = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome_curso = Column(String, unique=True)
    descricao_curso = Column(String)

    
class InscricoesCursos(Base):
    """Inscricoes Cursos SQLAlchemy model
    """
    __tablename__ = "inscricoes_cursos"

    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), primary_key=True)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"), primary_key=True)
    id_ano_curricular = Column(Integer, ForeignKey("ano_curricular.id_ano"), primary_key=True)

class Semestres(Base):
    """Semestres SQLAlchemy model
    """
    __tablename__ = "semestres"

    id_semestre = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome_semestre = Column(String, unique=True)

class AnoCurricular(Base):
    """Ano Curricular SQLAlchemy model
    """
    __tablename__ = "ano_curricular"
    
    id_ano = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ano = Column(String, unique=True)
    

class Turmas(Base):
    """Turmas SQLAlchemy model
    """
    __tablename__ = "turmas"

    id_turma = Column(Integer, primary_key=True, autoincrement=True, index=True)
    turma = Column(String)

    
class Horarios(Base):
    """Horarios SQLAlchemy model
    """
    __tablename__ = "horarios"

    id_horario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String)
    data_inicio = Column(Date)
    data_fim = Column(Date)
    descricao = Column(String)


class Periodos(Base):
    """Periodos SQLAlchemy model
    """
    __tablename__ = "periodos"

    id_periodo = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_horario = Column(Integer, ForeignKey("horarios.id_horario"))
    dia_semana = Column(String)
    hora_inicio = Column(DateTime)
    hora_fim = Column(DateTime)
    

class UC(Base):
    """Unidade Curricular SQLAlchemy model
    """
    __tablename__ = "uc"

    id_uc = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"))
    nome_uc = Column(String, nullable=False)
    id_semestre = Column(Integer, ForeignKey("semestres.id_semestre"))
    id_ano = Column(Integer, ForeignKey("ano_curricular.id_ano"))
    id_turma = Column(Integer, ForeignKey("turmas.id_turma"))
    id_horario = Column(Integer, ForeignKey("horarios.id_horario"))


class UCDocentes(Base):
    """UC_Docentes SQLAlchemy model
    """
    __tablename__ = "uc_docentes"

    id_uc = Column(Integer, ForeignKey("uc.id_uc"), primary_key=True)
    id_docente = Column(Integer, ForeignKey("docentes.id_docente"), primary_key=True)

    
class InscricoesUC(Base):
    """Inscrições UC SQLAlchemy model
    """
    __tablename__ = "inscricoes_uc"
    
    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), primary_key=True)
    id_uc = Column(Integer, ForeignKey("uc.id_uc"), primary_key=True)
    data_inscricao = Column(Date)

