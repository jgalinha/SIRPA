# -*- coding: utf-8 -*-
"""Courses pydantic schema file

This module define the pydantic schema of courses data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from pydantic import BaseModel


class CourseBase(BaseModel):
    nome_curso: str
    descricao_curso: str


class CreateCourse(CourseBase):
    pass


class ShowCourse(CourseBase):
    id_curso: int

    class Config:
        orm_mode = True


class UpdateCourse(CourseBase):
    class Config:
        orm_mode = True
