# -*- coding: utf-8 -*-
"""Alunos router file

This module set the routes for the alunos path of the api

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from typing import Any

from database import get_db
from fastapi import APIRouter, Depends, status
from models import student
from oauth2 import get_current_user
from schemas import student_schema
from sqlalchemy.orm import Session

router = APIRouter(tags=["Alunos"], prefix="/student")

dependencies = [Depends(get_current_user)]


@router.post(
    "/create",
    response_model=student_schema.ShowStudent,
    status_code=status.HTTP_201_CREATED,
    dependencies=dependencies,
)
def create_student(
    request: student_schema.CreateStudent, db: Session = Depends(get_db)
) -> Any:
    return student.create_student(db, request)


@router.get("/list")
def get_students():
    pass


@router.get("{id}")
def get_student_by_id():
    pass


@router.delete(
    "{id}",
    response_model=student_schema.ShowStudent,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def delete_student(id: int, db: Session = Depends(get_db)) -> Any:
    return student.delete_student(db, id_student=id)
