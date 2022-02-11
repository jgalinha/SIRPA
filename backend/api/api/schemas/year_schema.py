# -*- coding: utf-8 -*-
"""Curricular year pydantic schema file

This module define the pydantic schema of curricular years data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from pydantic import BaseModel


class YearBase(BaseModel):
    ano: str

    class Config:
        orm_mode = True


class CreateYear(YearBase):
    pass


class UpdateYear(YearBase):
    pass


class ShowYear(YearBase):
    id_ano: int
