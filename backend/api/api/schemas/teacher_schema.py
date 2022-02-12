# -*- coding: utf-8 -*-
"""Teacher pydantic schema file

This module define the pydantic schema of teacher data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from pydantic import BaseModel
from schemas import user_schema


class TeacherBase(BaseModel):
    nome: str
    nr_docente: int

    class Config:
        orm_mode = True


class CreateTeacher(TeacherBase):
    utilizador: user_schema.UserCreate


class UpdateTeacher(TeacherBase):
    pass


class ShowTeacher(TeacherBase):
    id_docente: int
    utilizador: user_schema.ShowUser


class Teacher(TeacherBase):
    id_docente: int
