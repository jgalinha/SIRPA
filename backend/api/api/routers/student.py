# -*- coding: utf-8 -*-
"""Alunos router file

This module set the routes for the alunos path of the api

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from typing import Any, List

from database import get_db
from fastapi import APIRouter, Depends, status
from models import student
from oauth2 import get_current_user
from schemas import student_schema
from sqlalchemy.orm import Session

router = APIRouter(tags=["Alunos"], prefix="/student")

dependencies = [Depends(get_current_user)]


@router.get(
    "/number/{number}",
    response_model=student_schema.ShowStudent,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_student_by_number(number: int, db: Session = Depends(get_db)) -> Any:
    return student.get_student_by_number(db, student_nr=number)


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


@router.get(
    "/list",
    response_model=List[student_schema.ShowStudent],
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_students(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    return student.get_students(db, skip=skip, limit=limit)


@router.get(
    "/{id}",
    response_model=student_schema.ShowStudent,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_student_by_id(id: int, db: Session = Depends(get_db)) -> Any:
    return student.get_student(db, id_student=id)


@router.delete(
    "/{id}",
    response_model=student_schema.ShowStudent,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def delete_student(id: int, db: Session = Depends(get_db)) -> Any:
    return student.delete_student(db, id_student=id)
