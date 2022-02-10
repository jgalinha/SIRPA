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
from schemas import uc_schema
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
