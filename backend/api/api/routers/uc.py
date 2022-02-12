# -*- coding: utf-8 -*-
"""UC router file

This module set the routes for the ucs path of the api

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from typing import Any, List

from database import get_db
from fastapi import APIRouter, Depends, status
from models import uc
from oauth2 import get_current_user
from schemas import nm_schema, uc_schema
from schemas.schedules_schema import CreateSchedule, ShowSchedule
from sqlalchemy.orm import Session

router = APIRouter(tags=["UC"], prefix="/uc")

dependencies = [Depends(get_current_user)]


@router.get(
    "/number/{number}",
    response_model=uc_schema.ShowUC,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_uc_by_number(number: int, db: Session = Depends(get_db)) -> Any:
    """Get uc by number

    Args:
        number (int): uc number
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.get_uc_by_number(db, uc_nr=number)


@router.post(
    "/create",
    response_model=uc_schema.ShowUC,
    status_code=status.HTTP_201_CREATED,
    dependencies=dependencies,
)
def create_uc(request: uc_schema.CreateUC, db: Session = Depends(get_db)) -> Any:
    """Create uc

    Args:
        request (uc_schema.CreateUC): uc data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.create_uc(db, request)


@router.post(
    "/subscription/",
    response_model=nm_schema.UCSubscriptionBase,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def subscribe_uc(
    request: nm_schema.UCSubscriptionBase, db: Session = Depends(get_db)
) -> Any:
    """Subscribe an UNC

    Args:
        request (nm_schema.UCSubscriptionBase): subscription data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.subscribe_uc(db, request)


@router.delete(
    "/subscription/",
    response_model=nm_schema.UCunSubscriptionBase,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def unsubscribe_uc(
    request: nm_schema.UCunSubscriptionBase, db: Session = Depends(get_db)
) -> Any:
    """Unsubscribe UC

    Args:
        request (nm_schema.UCunSubscriptionBase): subscription data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.unsubscribeUC(db, request)


@router.post(
    "/register/teacher/",
    response_model=nm_schema.TeacherUCBase,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def add_teacher(
    resquest: nm_schema.TeacherUCBase, db: Session = Depends(get_db)
) -> Any:
    """Register teacher in UC

    Args:
        resquest (nm_schema.TeacherUCBase): request data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.add_teacher(db, resquest)


@router.delete(
    "/register/teacher/",
    response_model=nm_schema.TeacherUCBase,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def remove_teacher(
    request: nm_schema.TeacherUCBase, db: Session = Depends(get_db)
) -> Any:
    """Remove teacher from UC

    Args:
        request (nm_schema.TeacherUCBase): request data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.remove_teacher(db, request)


@router.post(
    "/semester",
    response_model=nm_schema.SemesterUCBase,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def register_semester(
    request: nm_schema.SemesterUCBase, db: Session = Depends(get_db)
) -> Any:
    """Register semester in UC

    Args:
        request (nm_schema.SemesterUCBase): request data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.register_semester(db, request)


@router.delete(
    "/semester",
    response_model=nm_schema.SemesterUCBase,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def remove_semester(
    request: nm_schema.SemesterUCBase, db: Session = Depends(get_db)
) -> Any:
    """Remove semester from UC

    Args:
        request (nm_schema.SemesterUCBase): association data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.remove_semester(db, request)


@router.post("/schedule", response_model=ShowSchedule, status_code=status.HTTP_200_OK)
def add_schedule(request: CreateSchedule, db: Session = Depends(get_db)) -> Any:
    """Add schedule to UC

    Args:
        request (CreateSchedule): schedule data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.add_schedule(db, request)


@router.delete(
    "/schedule/{id}", response_model=ShowSchedule, status_code=status.HTTP_200_OK
)
def remove_schedule(id: int, db: Session = Depends(get_db)) -> Any:
    """Remove schedule from UC

    Args:
        id (int): schedule id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.remove_schedule(db, schedule_id=id)


@router.get(
    "/list",
    response_model=List[uc_schema.ShowUC],
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_ucs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """Get List of ucs

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).
        skip (int, optional): rows to skip. Defaults to 0.
        limit (int, optional): limit of rows. Defaults to 100.
    """
    return uc.get_ucs(db, skip=skip, limit=limit)


@router.get(
    "/{id}",
    response_model=uc_schema.ShowUC,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_uc_by_id(id: int, db: Session = Depends(get_db)) -> Any:
    """Get uc by id

    Args:
        id (int): uc id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.get_uc(db, id_uc=id)


@router.delete(
    "/{id}",
    response_model=uc_schema.ShowUC,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def delete_uc(id: int, db: Session = Depends(get_db)) -> Any:
    """Delete uc and user account

    Args:
        id (int): uc id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.delete_uc(db, id_uc=id)


@router.put(
    "/{id}",
    response_model=uc_schema.ShowUC,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def update_uc(
    id: int, request: uc_schema.UpdateUC, db: Session = Depends(get_db)
) -> Any:
    """Update uc name an number

    Args:
        id (int): uc id
        request (uc_schema.UpdateUC): uc name and number
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return uc.update_uc(db, uc_id=id, request=request)
