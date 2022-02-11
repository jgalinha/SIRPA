# -*- coding: utf-8 -*-
"""N-M relations pydantic schema file

This module define the pydantic schema of n-m relationships data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from datetime import date
from tkinter.tix import Tree

from pydantic import BaseModel


class SemesterUCBase(BaseModel):
    id_uc: int
    id_semestre: int

    class Config:
        orm_mode = True


class TeacherUCBase(BaseModel):
    id_uc: int
    id_docente: int

    class Config:
        orm_mode = True


class UCSubscriptionBase(BaseModel):
    id_aluno: int
    id_uc: int
    data_incricao: date

    class Config:
        orm_mode = True


class CourseSubscriptionBase(BaseModel):
    id_aluno: int
    id_curso: int
    id_ano_curricular: int

    class Config:
        orm_mode = True
