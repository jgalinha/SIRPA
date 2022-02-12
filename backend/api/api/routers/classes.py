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
from oauth2 import get_current_user
from schemas.class_schema import CreateClass, ShowClass
from sqlalchemy.orm import Session

router = APIRouter(tags=["Aulas"], prefix="/class")

dependencies = [Depends(get_current_user)]


@router.post("/", response_model=ShowClass, status_code=status.HTTP_200_OK)
def create_class(request: CreateClass, db: Session = Depends(get_db)) -> Any:
    """Create class

    Args:
        request (CreateClass): class data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return classes.create_class(db, request)


@router.delete("/{id}", response_model=ShowClass, status_code=status.HTTP_200_OK)
def remove_class(id: int, db: Session = Depends(get_db)) -> Any:
    """Remove class

    Args:
        id (int): class id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return classes.remove_class(db, class_id=id)
