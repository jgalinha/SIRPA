# -*- coding: utf-8 -*-
"""Courses router file

This module set the routes for the courses path of the api

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

from typing import Any, List

from database import get_db
from fastapi import APIRouter, Depends, status
from models import course
from oauth2 import get_current_user
from schemas import courses_schema, nm_schema
from sqlalchemy.orm import Session

router = APIRouter(tags=["Cursos"], prefix="/courses")

dependencies = [Depends(get_current_user)]


@router.get(
    "/list",
    response_model=List[courses_schema.ShowCourse],
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def list_courses(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """Get list of courses

    Args:
        db (Session, optional): database session. Defaults to Depends(getattr).
        skip (int, optional): rows to skip. Defaults to 0.
        limit (int, optional): limit of rows. Defaults to 0.
    """
    return course.list_courses(db, skip=skip, limit=limit)


@router.post(
    "/create",
    response_model=courses_schema.ShowCourse,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def create_course(
    request: courses_schema.CreateCourse, db: Session = Depends(get_db)
) -> Any:
    """Create course

    Args:
        request (courses_schema.CreateCourse): course data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return course.create_course(db, request)


@router.post(
    "/subscription",
    response_model=nm_schema.ShowCourseSubscription,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def subscribe_course(
    request: nm_schema.CourseSubscriptionBase, db: Session = Depends(get_db)
) -> Any:
    """Subscribe to a course

    Args:
        request (nm_schema.CourseSubscriptionBase): subscription data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return course.subscribe_course(db, request)


@router.delete(
    "/subscription",
    response_model=nm_schema.ShowCourseSubscription,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def unsubscribe_course(
    request: nm_schema.CourseSubscriptionBase, db: Session = Depends(get_db)
) -> Any:
    """Unsubscribe from a course

    Args:
        request (nm_schema.CourseSubscriptionBase): subscription data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    print("bah")
    return course.unsubscribe_course(db, request)


@router.get(
    "/{id}",
    response_model=courses_schema.ShowCourseWithUcs,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def get_course_by_id(id: int, db: Session = Depends(get_db)) -> Any:
    """Get Course by id

    Args:
        id (int): course id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return course.get_course_by_id(db, course_id=id)


@router.put(
    "/{id}",
    response_model=courses_schema.ShowCourse,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def update_course_by_id(
    id: int, request: courses_schema.UpdateCourse, db: Session = Depends(get_db)
) -> Any:
    """Update course by id

    Args:
        id (int): course id
        request (courses_schema.UpdateCourse): course data to update
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return course.update_course_by_id(db, course_id=id, course_data=request)


@router.delete(
    "/{id}",
    response_model=courses_schema.ShowCourse,
    status_code=status.HTTP_200_OK,
    dependencies=dependencies,
)
def delete_course_by_id(id: int, db: Session = Depends(get_db)) -> Any:
    """Delete course by id

    Args:
        id (int): course id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    return course.delete_course_by_id(db, course_id=id)
