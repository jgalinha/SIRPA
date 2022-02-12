# -*- coding: utf-8 -*-
"""UC router file

This module set the routes for the ucs path of the api

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from typing import Any

from database import get_db
from fastapi import APIRouter, Depends, status
from models import helpers
from oauth2 import get_current_user
from schemas.year_schema import CreateYear, ShowYear
from sqlalchemy.orm import Session

router = APIRouter(tags=["Ferramentas"], prefix="/tools")

dependencies = [Depends(get_current_user)]


@router.post("/year", response_model=ShowYear, status_code=status.HTTP_200_OK)
def add_year(request: CreateYear, db: Session = Depends(get_db)) -> Any:
    """Add an year

    Args:
        request (CreateYear): request data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return helpers.add_year(db, request)


@router.delete("/year/{id}", response_model=ShowYear, status_code=status.HTTP_200_OK)
def remove_year(id: int, db: Session = Depends(get_db)) -> Any:
    """Remove a year

    Args:
        id (int): year id
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        Any: [description]
    """
    return helpers.remove_year(db, id_year=id)
