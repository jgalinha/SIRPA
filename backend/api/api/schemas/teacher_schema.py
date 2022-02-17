# -*- coding: utf-8 -*-
"""Teacher pydantic schema file

This module define the pydantic schema of teacher data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from datetime import date, datetime, time
from typing import List

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


class TodayTeacherStudent(BaseModel):
    nome: str
    nr_aluno: str

    class Config:
        orm_mode = True


class TodayTeacherPresences(BaseModel):
    id_aluno: int
    confirmacao: datetime

    aluno: TodayTeacherStudent

    class Config:
        orm_mode = True


class TodayTeacherCourse(BaseModel):
    id_curso: int
    nome_curso: str

    class Config:
        orm_mode = True


class TodayTeacherUC(BaseModel):
    id_uc: int
    nome_uc: str

    curso: TodayTeacherCourse

    class Config:
        orm_mode = True


class TodayTeacherSchedule(BaseModel):
    id_periodo: int
    dia_semana: int
    hora_inicio: time
    hora_fim: time

    class Config:
        orm_mode = True


class TodayTeacherClasses(BaseModel):
    id_aula: int
    data: date
    resumo: str
    sumario: str
    sala: str

    presencas: List[TodayTeacherPresences]
    uc: TodayTeacherUC
    periodo: TodayTeacherSchedule

    class Config:
        orm_mode = True


class TodayTeacher(TeacherBase):
    id_docente: int

    aulas: List[TodayTeacherClasses]

    class Config:
        orm_mode: True
