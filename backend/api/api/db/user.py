# -*- coding: utf-8 -*-
"""User SQLAlchemy schema file 

This module represents the SQLAlchemy schema for the user tables

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    """User SQLAlchemy model"""

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
