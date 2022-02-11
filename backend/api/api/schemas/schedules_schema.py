# -*- coding: utf-8 -*-
"""Schedules pydantic schema file

This module define the pydantic schema of schedules data

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from datetime import time

from pydantic import BaseModel


class ScheduleBase(BaseModel):
    dia_semana: int
    hora_inicio: time
    hora_fim: time

    class Config:
        orm_mode = True


class CreateSchedule(ScheduleBase):
    id_uc: int


class UpdateSchedule(ScheduleBase):
    pass


class ShowSchedule(ScheduleBase):
    id_periodo: int
    id_uc: int
