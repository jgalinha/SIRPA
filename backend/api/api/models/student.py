# -*- coding: utf-8 -*-
"""Student model file

This module define the model operations for the students

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""


from typing import List

from db.alunos import Alunos
from fastapi import HTTPException, status
from models import user as User
from schemas import student_schema
from sqlalchemy.orm import Session
from utils import Utils


def _check_student_exists(db: Session, /, *, nr_aluno: int) -> bool:
    """Check if a student nr already exists in database

    Args:
        db (Session): database session
        nr_aluno (int): student number

    Raises:
        HTTPException: server error

    Returns:
        bool: student exists
    """
    try:
        student = db.query(Alunos).filter(Alunos.nr_aluno == nr_aluno).all()
        if student:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error checking if student exists",
                error=repr(e),
            ),
        )


def check_student_by_user_id(db: Session, /, *, user_id: int) -> bool:
    """Check if a given user id is student

    Args:
        db (Session): database session
        user_id (int): user id

    Raises:
        HTTPException: error checking student

    Returns:
        bool: is student
    """
    try:
        student = db.query(Alunos).filter(Alunos.id_utilizador == user_id).first()
        if student:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error checking student",
                error=repr(e),
            ),
        )


def check_student_by_id(db: Session, /, *, student_id: int) -> bool:
    """Check if student exists by id

    Args:
        db (Session): database session
        student_id (int): student id

    Raises:
        HTTPException: error checking student

    Returns:
        bool: is student
    """
    try:
        student = db.query(Alunos).get(student_id)
        if student:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error checking student",
                error=repr(e),
            ),
        )


def update_student(
    db: Session, /, *, student_id: int, request: student_schema.UpdateStudent
) -> student_schema.ShowStudent:
    """Update student details

    Args:
        db (Session): database session
        student_id (int): student id
        request (student_schema.UpdateStudent): student name and number

    Raises:
        HTTPException: Student not fount
        HTTPException: Error updating

    Returns:
        student_schema.ShowStudent: [description]
    """
    student = db.query(Alunos).get(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"Student with id: {student_id} not found",
            ),
        )
    student.nome = request.nome
    student.nr_aluno = request.nr_aluno
    try:
        db.query(Alunos).filter(Alunos.id_aluno == student_id).update(
            {"nome": request.nome, "nr_aluno": request.nr_aluno}
        )
        db.commit()
        return student
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                msg=f"Error updating student nr: {request.nr_aluno}",
                error=repr(e),
            ),
        )


def get_student_by_number(
    db: Session, /, *, student_nr: int
) -> student_schema.ShowStudent:
    """Get student by number

    Args:
        db (Session): database session
        student_nr (int): student number

    Returns:
        student_schema.ShowStudent: Student details
    """
    return db.query(Alunos).filter(Alunos.nr_aluno == student_nr).first()


def get_student(db: Session, /, *, id_student: int) -> student_schema.ShowStudent:
    """Query student by id

    Args:
        db (Session): database session
        id_student (int): student id

    Returns:
        student_schema.ShowStudent: Student Detail
    """
    return db.query(Alunos).get(id_student)


def get_students(
    db: Session, /, *, skip: int = 0, limit: int = 100
) -> List[student_schema.ShowStudent]:
    """Get list of students

    Args:
        db (Session): database session
        skip (int, optional): rows to skip. Defaults to 0.
        limit (int, optional): limit of rows. Defaults to 0.

    Returns:
        List[student_schema.ShowStudent]: List of students
    """
    return db.query(Alunos).offset(skip).limit(limit).all()


def delete_student(db: Session, /, *, id_student: int) -> student_schema.ShowStudent:
    """Delete student record and respective user

    Args:
        db (Session): database session
        id_student (int): student id

    Raises:
        HTTPException: student not found
        HTTPException: delete error

    Returns:
        student_schema.ShowStudent: deleted student details
    """
    student = db.query(Alunos).get(id_student)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"Student with id: {id_student} not found",
            ),
        )
    try:
        db.delete(student)  # delete student record
        db.delete(student.utilizador)  # delete student user
        db.commit()
        return student
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                f"Error deleting student: {id_student}",
                error=repr(e),
            ),
        )


def create_student(
    db: Session, request: student_schema.CreateStudent, /
) -> student_schema.ShowStudent:
    """Create a student and respective user

    Args:
        db (Session): database session
        request (student_schema.CreateStudent): student and user data

    Raises:
        HTTPException: user exists
        HTTPException: student exists
        HTTPException: error creating student

    Returns:
        Student: student details
    """
    if User.check_user_exists(
        db,
        nome_utilizador=request.utilizador.nome_utilizador,
        email=request.utilizador.email,
    ):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="user already exists"
        )
    if _check_student_exists(db, nr_aluno=request.nr_aluno):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="student already exists"
        )

    user: User = User.create_user(db, request.utilizador)
    try:
        if user:
            new_student: Alunos = Alunos(
                id_utilizador=user.id_utilizador,
                nome=request.nome,
                nr_aluno=request.nr_aluno,
            )
            db.add(new_student)
            db.commit()
            db.refresh(new_student)
            return new_student
    except Exception as e:
        User.delete_user(db, id_utilizador=user.id_utilizador)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error creating student",
                error=repr(e),
            ),
        )


def today(db: Session, /, *, student_id: int) -> student_schema.TodayStudent:
    """Get list of student classes

    Args:
        db (Session): database session
        student_id (int): student id

    Returns:
        student_schema.TodayStudent: student classes
    """
    today = db.query(Alunos).filter(Alunos.id_aluno == student_id).first()
    return today
