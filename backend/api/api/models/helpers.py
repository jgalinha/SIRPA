# -*- coding: utf-8 -*-
"""UC model file

This module define the model operations for the helpes

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from db.ucs import AnoCurricular
from fastapi import HTTPException, status
from icecream import ic
from schemas.year_schema import CreateYear, ShowYear
from sqlalchemy.orm import Session
from utils import Utils


def year_exists(db: Session, /, *, year: str) -> bool:
    """Check if year exists

    Args:
        db (Session): database session
        year (str): year

    Raises:
        HTTPException: Error checking if year exists

    Returns:
        bool: [description]
    """
    try:
        if db.query(AnoCurricular).filter(AnoCurricular.ano == year).first():
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error checking if year exists",
                error=repr(e),
            ),
        )


def add_year(db: Session, request: CreateYear, /) -> ShowYear:
    """Add curricular year

    Args:
        db (Session): database session
        request (CreateYear): request data

    Raises:
        HTTPException: Year exists
        HTTPException: Error creating year

    Returns:
        ShowYear: inserted data
    """
    year = request.ano
    if year_exists(db, year=year):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail=Utils.error_msg(status.HTTP_302_FOUND, "Year already exists!"),
        )

    try:
        new_year: AnoCurricular = AnoCurricular(ano=year)
        db.add(new_year)
        db.commit()
        db.refresh(new_year)
        ic(new_year.id_ano)
        return new_year
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error registering year!",
                error=repr(e),
            ),
        )


def remove_year(db: Session, /, *, id_year: int) -> ShowYear:
    """Remove year

    Args:
        db (Session): database session
        id_year (int): year id

    Raises:
        HTTPException: Year not found
        HTTPException: Error removing year

    Returns:
        ShowYear: removed data
    """
    year = db.query(AnoCurricular).get(id_year)
    if not year:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(status.HTTP_404_NOT_FOUND, "Year not found"),
        )
    try:
        db.delete(year)
        db.commit()
        return year
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error removing year",
                error=repr(e),
            ),
        )
