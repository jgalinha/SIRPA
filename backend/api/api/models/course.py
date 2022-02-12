# -*- coding: utf-8 -*-
"""Course model file

This module define the model operations for the courses

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from typing import List

from db.ucs import Cursos, InscricoesCursos
from fastapi import HTTPException, status
from models.helpers import year_exists_by_id
from models.student import check_student_by_id
from schemas import courses_schema, nm_schema
from sqlalchemy import and_
from sqlalchemy.orm import Session
from utils import Utils


def check_course_exists_by_id(db: Session, /, *, id_course: int) -> bool:
    """Check if a course already exists in database by id

    Args:
        db (Session): database session
        id_course (int): course id

    Raises:
        HTTPException: server error

    Returns:
        bool: course exists
    """
    try:
        course = db.query(Cursos).get(id_course)
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


def check_course_exists(db: Session, /, *, name: str) -> bool:
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
    check_course_exists(db, name=request.nome_curso)
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


def get_course_by_id(
    db: Session, /, *, course_id: int
) -> courses_schema.ShowCourseWithUcs:
    """Get course by id

    Args:
        db (Session): database session
        course_id (int): course id

    Returns:
        courses_schema.ShowCourse: Course details
    """
    return db.query(Cursos).get(course_id)


def delete_course_by_id(db: Session, /, *, course_id: int) -> courses_schema.ShowCourse:
    """Delete course

    Args:
        db (Session): databasse session
        course_id (int): course id

    Raises:
        HTTPException: Course not found
        HTTPException: Error deleting course

    Returns:
        courses_schema.ShowCourse: deleted course details
    """
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
    """Update Course by id

    Args:
        db (Session): database session
        course_id (int): course id
        course_data (courses_schema.UpdateCourse): course data

    Raises:
        HTTPException: Course not found
        HTTPException: Error updating course

    Returns:
        courses_schema.ShowCourse: [description]
    """
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


def subscribe_course(
    db: Session, request: nm_schema.CourseSubscriptionBase, /
) -> nm_schema.ShowCourseSubscription:
    """Register student in course

    Args:
        db (Session): database session
        request (nm_schema.CourseSubscriptionBase): request data

    Raises:
        HTTPException: Course not found
        HTTPException: Student not found
        HTTPException: Year not found
        HTTPException: Error subscribing to course

    Returns:
        nm_schema.CourseSubscriptionBase: inserted data
    """
    student_id = request.id_aluno
    course_id = request.id_curso
    year_id = request.id_ano_curricular

    if not check_course_exists_by_id(db, id_course=course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND, f"Course with id: {course_id} not found!"
            ),
        )

    if not check_student_by_id(db, student_id=student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND, f"Student with id: {student_id} not found!"
            ),
        )

    if not year_exists_by_id(db, year_id=year_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND, f"Year with id: {year_id} no found!"
            ),
        )

    try:
        new_subscription: InscricoesCursos = InscricoesCursos(
            id_aluno=student_id, id_curso=course_id, id_ano_curricular=year_id
        )
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        return new_subscription
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT, "Error subscribing to course", error=repr(e)
            ),
        )


def unsubscribe_course(
    db: Session, request: nm_schema.CourseSubscriptionBase, /
) -> nm_schema.ShowCourseSubscription:
    """Unsubscribe from a course

    Args:
        db (Session): database session
        request (nm_schema.CourseSubscriptionBase): subscription data

    Raises:
        HTTPException: Subscription not found
        HTTPException: Error unsubscribing from course

    Returns:
        nm_schema.ShowCourseSubscription: subscription data
    """
    student_id = request.id_aluno
    course_id = request.id_curso
    year_id = request.id_ano_curricular
    subscription = (
        db.query(InscricoesCursos)
        .filter(
            and_(
                InscricoesCursos.id_aluno == student_id,
                InscricoesCursos.id_curso == course_id,
                InscricoesCursos.id_ano_curricular == year_id,
            )
        )
        .first()
    )

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(status.HTTP_404_NOT_FOUND, "Subscrition not found"),
        )

    try:
        db.delete(subscription)
        db.commit()
        return subscription
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error unsubscribing from course",
                error=repr(e),
            ),
        )
