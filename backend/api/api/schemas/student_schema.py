# -*- coding: utf-8 -*-
"""Alunos pydantic schema file

This module define the pydantic schema of alunos data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from pydantic import BaseModel
from schemas import user_schema


class StudentBase(BaseModel):
    nome: str
    nr_aluno: int

    class Config:
        orm_mode = True


class CreateStudent(StudentBase):
    utilizador: user_schema.UserCreate


class UpdateStudent(StudentBase):
    pass


class ShowStudent(StudentBase):
    id_aluno: int
    utilizador: user_schema.ShowUser
