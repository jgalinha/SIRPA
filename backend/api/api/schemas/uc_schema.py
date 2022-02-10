# -*- coding: utf-8 -*-
"""UC pydantic schema file

This module define the pydantic schema of ucs data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from pydantic import BaseModel
from schemas import courses_schema


class UCBase(BaseModel):
    nome_uc: str
    descricao: str

    class Config:
        orm_mode = True


class CreateUC(UCBase):
    id_curso: int

    class Config:
        orm_mode = True


class ShowUC(UCBase):
    id_uc: int

    curso: courses_schema.ShowCourse

    class Config:
        orm_mode = True


class UpdateUC(UCBase):
    class Config:
        orm_mode = True
