# -*- coding: utf-8 -*-
"""Teachers router file

This module set the routes for the teachers path of the api

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""


from typing import Any, List

from database import get_db
from fastapi import APIRouter, Depends, status
from models import teacher
from oauth2 import get_active_user, get_current_user
from schemas import teacher_schema
from sqlalchemy.orm import Session

router = APIRouter(tags=["Docentes"], prefix="/teacher")

dependencies = [Depends(get_current_user)]


@router.get(
    "/today",
    status_code=status.HTTP_200_OK,
    response_model=teacher_schema.TodayTeacher,
    dependencies=dependencies,
)
def teacher_today(
    user_id: int = Depends(get_active_user), db: Session = Depends(get_db)
) -> Any:
    return teacher.today(db, user_id=user_id)


@router.get(
    "/number/{number}",
    response_model=teacher_schema.ShowTeacher,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_teacher_by_number(number: int, db: Session = Depends(get_db)) -> Any:
    """Get teacher by number

    Args:
        number (int): teacher number
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return teacher.get_teacher_by_number(db, teacher_nr=number)


@router.post(
    "/create",
    response_model=teacher_schema.ShowTeacher,
    status_code=status.HTTP_201_CREATED,
    dependencies=dependencies,
)
def create_teacher(
    request: teacher_schema.CreateTeacher, db: Session = Depends(get_db)
) -> Any:
    """Create teacher and respective user account

    Args:
        request (teacher_schema.CreateTeacher): teacher data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return teacher.create_teacher(db, request)


@router.get(
    "/list",
    response_model=List[teacher_schema.ShowTeacher],
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_teachers(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """Get List of teachers

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).
        skip (int, optional): rows to skip. Defaults to 0.
        limit (int, optional): limit of rows. Defaults to 100.
    """
    return teacher.get_teachers(db, skip=skip, limit=limit)


@router.get(
    "/{id}",
    response_model=teacher_schema.ShowTeacher,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_teacher_by_id(id: int, db: Session = Depends(get_db)) -> Any:
    """Get teacher by id

    Args:
        id (int): teacher id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return teacher.get_teacher(db, id_teacher=id)


@router.delete(
    "/{id}",
    response_model=teacher_schema.ShowTeacher,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def delete_teacher(id: int, db: Session = Depends(get_db)) -> Any:
    """Delete teacher and user account

    Args:
        id (int): teacher id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return teacher.delete_teacher(db, id_teacher=id)


@router.put(
    "/{id}",
    response_model=teacher_schema.ShowTeacher,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def update_teacher(
    id: int, request: teacher_schema.UpdateTeacher, db: Session = Depends(get_db)
) -> Any:
    """Update teacher name an number

    Args:
        id (int): teacher id
        request (teacher_schema.UpdateTeacher): teacher name and number
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return teacher.update_teacher(db, teacher_id=id, request=request)
