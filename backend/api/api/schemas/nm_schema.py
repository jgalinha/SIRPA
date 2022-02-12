# -*- coding: utf-8 -*-
"""N-M relations pydantic schema file

This module define the pydantic schema of n-m relationships data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from datetime import date

from pydantic import BaseModel
from schemas.student_schema import StudentBase
from schemas.teacher_schema import TeacherBase


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


class ShowTeacherInUC(BaseModel):
    id_docente: int
    docente: TeacherBase

    class Config:
        orm_mode = True


class UCSubscriptionBase(BaseModel):
    id_aluno: int
    id_uc: int
    data_inscricao: date

    class Config:
        orm_mode = True


class ShowStudentInUC(BaseModel):
    id_aluno: int
    data_inscricao: date
    aluno: StudentBase

    class Config:
        orm_mode = True


class UCunSubscriptionBase(BaseModel):
    id_aluno: int
    id_uc: int

    class Config:
        orm_mode = True


class CourseSubscriptionBase(BaseModel):
    id_aluno: int
    id_curso: int
    id_ano_curricular: int

    class Config:
        orm_mode = True
