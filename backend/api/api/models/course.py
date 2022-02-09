# -*- coding: utf-8 -*-
"""Course model file

This module define the model operations for the courses

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from typing import List

from db.ucs import Cursos
from fastapi import HTTPException, status
from schemas import courses_schema
from sqlalchemy.orm import Session
from utils import Utils


def _check_course_exists(db: Session, /, *, name: str) -> bool:
    """Check if a course already exists in database

    Args:
        db (Session): database session
        name (str): course name

    Raises:
        HTTPException: server error

    Returns:
        bool: course exists
    """
    try:
        course = db.query(Cursos).filter(Cursos.nome_curso == name).all()
        if course:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error checking if courses exists",
                error=repr(e),
            ),
        )


def list_courses(
    db: Session, /, *, skip: int = 0, limit: int = 100
) -> List[courses_schema.ShowCourse]:
    """Get list of courses

    Args:
        db (Session): database session
        skip (int, optional): rows to skip. Defaults to 0.
        limit (int, optional): limit of rows. Defaults to 0.

    Returns:
        List[courses_schema.ShowCourse]: List of Courses
    """
    return db.query(Cursos).offset(skip).limit(limit).all()


def create_course(
    db: Session, request: courses_schema.CreateCourse, /
) -> courses_schema.ShowCourse:
    """Create a course

    Args:
        db (Session): database session
        request (courses_schema.CreateCourse): course data

    Raises:
        HTTPException: course exists
        HTTPException: error creating course

    Returns:
        courses_schema.ShowCourse: course details
    """
    if _check_course_exists(db, name=request.nome_curso):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail=Utils.error_msg(status.HTTP_302_FOUND, "Course name already exists"),
        )
    try:
        new_course: Cursos = Cursos(
            nome_curso=request.nome_curso, descricao_curso=request.descricao_curso
        )
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT, "Error creating course", error=repr(e)
            ),
        )


def get_course_by_id(db: Session, /, *, course_id: int) -> courses_schema.ShowCourse:
    """Get course by id

    Args:
        db (Session): database session
        course_id (int): course id

    Returns:
        courses_schema.ShowCourse: Course details
    """
    return db.query(Cursos).get(course_id)


def delete_course_by_id(db: Session, /, *, course_id: int) -> courses_schema.ShowCourse:
    course = db.query(Cursos).get(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"Course with id: {course_id} not found",
            ),
        )
    try:
        db.delete(course)
        db.commit()
        return course
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                f"Error deleting course: {course_id}",
                error=repr(e),
            ),
        )


def update_course_by_id(
    db: Session, /, *, course_id: int, course_data: courses_schema.UpdateCourse
) -> courses_schema.ShowCourse:
    course = db.query(Cursos).get(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"Course with id: {course_id} not found",
            ),
        )
    try:
        db.query(Cursos).filter(Cursos.id_curso == course_id).update(
            {
                Cursos.nome_curso: course_data.nome_curso,
                Cursos.descricao_curso: course_data.descricao_curso,
            }
        )
        db.commit()
        return db.query(Cursos).get(course_id)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                f"Error updating course: {course_id}",
                error=repr(e),
            ),
        )
