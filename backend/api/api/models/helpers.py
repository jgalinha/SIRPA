# -*- coding: utf-8 -*-
"""UC model file

This module define the model operations for the helpes

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from db.ucs import AnoCurricular, Semestres
from fastapi import HTTPException, status
from schemas.semester_schema import CreateSemester, ShowSemester
from schemas.year_schema import CreateYear, ShowYear
from sqlalchemy.orm import Session
from utils import Utils


def semester_exists_by_id(db: Session, /, *, semester_id: int) -> bool:
    """Check if a semester exist by id

    Args:
        db (Session): database session
        semester_id (int): semester id

    Raises:
        HTTPException: Error checking semester

    Returns:
        bool: semester exists
    """
    try:
        semester = db.query(Semestres).get(semester_id)
        if semester:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error checking if semester exists!",
                error=repr(e),
            ),
        )


def year_exists_by_id(db: Session, /, *, year_id: int) -> bool:
    """Check if year exists by id

    Args:
        db (Session): database session
        year_id (int): year id

    Raises:
        HTTPException: Error checking year

    Returns:
        bool: year exists
    """
    try:
        year = db.query(AnoCurricular).get(year_id)
        if year:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error checking if year exists!",
                error=repr(e),
            ),
        )


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
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND, f"Year with id: {id_year} not found"
            ),
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


def add_semester(db: Session, request: CreateSemester, /) -> ShowSemester:
    """Add semester

    Args:
        db (Session): database session
        request (CreateSemester): semester data

    Raises:
        HTTPException: Year not found
        HTTPException: Error adding semester

    Returns:
        ShowSemester: inserted data
    """
    year_id = request.id_ano_curricular
    name = request.nome_semestre
    start_date = request.data_inicio
    end_date = request.data_fim

    if not year_exists_by_id(db, year_id=year_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND, f"Year with id: {year_id} not found!"
            ),
        )

    new_semester: Semestres = Semestres(
        id_ano_curricular=year_id,
        nome_semestre=name,
        data_inicio=start_date,
        data_fim=end_date,
    )
    try:
        db.add(new_semester)
        db.commit()
        db.refresh(new_semester)
        return new_semester
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error registering semester!",
                error=repr(e),
            ),
        )


def remove_semester(db: Session, /, *, semester_id: int) -> ShowSemester:
    """Remove semester

    Args:
        db (Session): database session
        semester_id (int): semester id

    Raises:
        HTTPException: Semester not found
        HTTPException: Error removing semester

    Returns:
        ShowSemester: [description]
    """
    semester = db.query(Semestres).get(semester_id)
    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND, f"Semester with id: {semester_id} not found"
            ),
        )

    try:
        db.delete(semester)
        db.commit()
        return semester
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error removing semester",
                error=repr(e),
            ),
        )
