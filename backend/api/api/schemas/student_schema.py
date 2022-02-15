# -*- coding: utf-8 -*-
"""Alunos pydantic schema file

This module define the pydantic schema of alunos data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from datetime import date, time
from typing import List

from pydantic import BaseModel, validator
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


class TodayClasses(BaseModel):
    id_aula: int
    id_docente: int
    data: date
    resumo: str
    sala: str

    class Config:
        orm_mode = True


class TodaySchedules(BaseModel):
    id_periodo: int
    dia_semana: int
    hora_inicio: time
    hora_fim: time

    aulas: List[TodayClasses]

    class Config:
        orm_mode = True

    @validator("aulas")
    def ensure_aulas(cls, v):
        for aula in v:
            if aula.data <= date.today():
                return v


class TodayUC(BaseModel):
    nome_uc: str

    periodos: List[TodaySchedules]

    class Config:
        orm_mode = True

    @validator("periodos")
    def ensure_peridos(cls, v):
        for periodo in v:
            if periodo.aulas:
                return v


class TodayUCSubscrition(BaseModel):
    id_uc: int
    data_inscricao: date
    uc: TodayUC

    class Config:
        orm_mode = True

    @validator("uc")
    def ensure_uc(cls, v):
        if v.periodos:
            return v


class TodayStudent(StudentBase):
    id_aluno: int
    inscricoes_ucs: List[TodayUCSubscrition]

    @validator("inscricoes_ucs")
    def ensure_inscricoes(cls, v):
        for uc in v:
            if uc.uc:
                return v
