from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    """User SQLAlchemy model
    """
    __tablename__ = "utilizadores"
    
    id_utilizador = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_utilizador = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    private_key = Column(String, nullable=False)
    public_key = Column(String, nullable=False)

    docente = relationship("Docentes", back_populates="utilizador")
    nao_docente = relationship("NaoDocentes", back_populates="utilizador")
    aluno = relationship("Alunos", back_populates="utilizador")