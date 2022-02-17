# -*- coding: utf-8 -*-
"""Classes router file

This module set the routes for the classes path of the api

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from typing import Any

from database import get_db
from fastapi import APIRouter, Depends, status
from models import classes
from oauth2 import get_active_user, get_current_user
from schemas.class_schema import (
    CreateClass,
    CreateQRCodeClass,
    ReadQRCodeClass,
    ShowClass,
)
from sqlalchemy.orm import Session

router = APIRouter(tags=["Aulas"], prefix="/class")

dependencies = [Depends(get_current_user)]


@router.post("/chekin", status_code=status.HTTP_200_OK)
def read_qrcode(
    request: ReadQRCodeClass,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_active_user),
) -> Any:
    return classes.read_QRCode(db, request, user_id=user_id)


@router.post("/qrcode", status_code=status.HTTP_200_OK, dependencies=dependencies)
def create_qrcode(
    request: CreateQRCodeClass,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_active_user),
):
    return classes.create_QRCode(db, request, user_id=user_id)


@router.post(
    "/",
    response_model=ShowClass,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def create_class(request: CreateClass, db: Session = Depends(get_db)) -> Any:
    """Create class

    Args:
        request (CreateClass): class data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return classes.create_class(db, request)


@router.delete(
    "/{id}",
    response_model=ShowClass,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def remove_class(id: int, db: Session = Depends(get_db)) -> Any:
    """Remove class

    Args:
        id (int): class id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return classes.remove_class(db, class_id=id)
