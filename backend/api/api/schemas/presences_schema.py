# -*- coding: utf-8 -*-
"""Presence pydantic schema file

This module define the pydantic schema of precenses data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from time import time

from pydantic import BaseModel


class PresenceBase(BaseModel):
    confirmacao: time

    class Config:
        orm_mode = True


class CreatePresence(PresenceBase):
    id_aula: int
    id_aluno: int


class UpdatePresence(PresenceBase):
    pass


class ShowPresence(PresenceBase):
    id_aula: int
    id_aluno: int
