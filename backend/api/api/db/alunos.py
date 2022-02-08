# -*- coding: utf-8 -*-
"""Alunos SQLAlchemy schema file 

This module represents the SQLAlchemy schema for the students tables

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from database import Base

# trunk-ignore(flake8/F401)
from db.aulas import Presencas
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Alunos(Base):
    """Alunos SQLAlchemy model

    Attributes:
        id_aluno (int): student id
        id_utilizador (int): user id
        nome (str): student name
        nr_aluno (int): student school number
    """

    __tablename__ = "alunos"

    id_aluno = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_utilizador = Column(
        Integer, ForeignKey("utilizadores.id_utilizador"), nullable=False
    )
    nome = Column(String, nullable=False)
    nr_aluno = Column(Integer, unique=True, nullable=False)

    presencas = relationship("Presencas", back_populates="aluno")
    inscricoes_cursos = relationship("InscricoesCursos", back_populates="aluno")
    inscricoes_ucs = relationship("InscricoesUC", back_populates="aluno")
    utilizador = relationship("User", back_populates="aluno")
