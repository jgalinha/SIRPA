# -*- coding: utf-8 -*-
"""Class pydantic schema file

This module define the pydantic schema of classes data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from datetime import date

from pydantic import BaseModel


class ClassBase(BaseModel):
    data: date
    resumo: str
    sumario: str
    sala: str

    class Config:
        orm_mode = True


class CreateClass(ClassBase):
    id_uc: int
    id_docente: int
    id_periodo: int


class UpdateClass(ClassBase):
    pass


class ShowClass(ClassBase):
    id_aula: int
    id_uc: int
    id_docente: int
    id_periodo: int


class CreateQRCodeClass(BaseModel):
    id_aula: int
    id_aluno: int
    password: str

    class Config:
        orm_mode = True
