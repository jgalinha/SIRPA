# -*- coding: utf-8 -*-
"""Semester pydantic schema file

This module define the pydantic schema of semester data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from datetime import date

from pydantic import BaseModel


class SemesterBase(BaseModel):
    nome_semestre: str
    data_inicio: date
    data_fim: date

    class Config:
        orm_mode = True


class CreateSemester(SemesterBase):
    id_ano_curricular: int


class UpdateSemester(SemesterBase):
    pass


class ShowSemester(SemesterBase):
    id_semestre: id
