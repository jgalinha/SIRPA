# -*- coding: utf-8 -*-
"""Student model file

This module define the model operations for the students

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""


from db.alunos import Alunos
from fastapi import HTTPException, status
from icecream import ic
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
                nome=user.nome_utilizador,
                nr_aluno=request.nr_aluno,
            )
            db.add(new_student)
            db.commit()
            db.refresh(new_student)
            return new_student
    except Exception as e:
        ic(user)
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
