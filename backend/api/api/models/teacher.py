# -*- coding: utf-8 -*-
"""Teacher model file

This module define the model operations for the teachers

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""


from typing import List

from db.docentes import Docentes
from fastapi import HTTPException, status
from models import user as User
from schemas import teacher_schema
from sqlalchemy.orm import Session
from utils import Utils


def _check_teacher_exists(db: Session, /, *, teacher_nr: int) -> bool:
    """Check if a teacher nr already exists in database

    Args:
        db (Session): database session
        nr_docente (int): teacher number

    Raises:
        HTTPException: server error

    Returns:
        bool: teacher exists
    """
    try:
        teacher = db.query(Docentes).filter(Docentes.nr_docente == teacher_nr).all()
        if teacher:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error checking if teacher exists",
                error=repr(e),
            ),
        )


def update_teacher(
    db: Session, /, *, teacher_id: int, request: teacher_schema.UpdateTeacher
) -> teacher_schema.ShowTeacher:
    """Update teacher details

    Args:
        db (Session): database session
        teacher_id (int): teacher id
        request (teacher_schema.Updateteacher): teacher name and number

    Raises:
        HTTPException: teacher not fount
        HTTPException: Error updating

    Returns:
        teacher_schema.ShowTeacher: [description]
    """
    teacher = db.query(Docentes).get(teacher_id)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"teacher with id: {teacher_id} not found",
            ),
        )
    teacher.nome = request.nome
    teacher.nr_docente = request.nr_docente
    try:
        db.query(Docentes).filter(Docentes.id_docente == teacher_id).update(
            {"nome": request.nome, "nr_docente": request.nr_docente}
        )
        db.commit()
        return teacher
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                msg=f"Error updating teacher nr: {request.nr_docente}",
                error=repr(e),
            ),
        )


def get_teacher_by_number(
    db: Session, /, *, teacher_nr: int
) -> teacher_schema.ShowTeacher:
    """Get teacher by number

    Args:
        db (Session): database session
        teacher_nr (int): teacher number

    Returns:
        teacher_schema.ShowTeacher: teacher details
    """
    return db.query(Docentes).filter(Docentes.nr_docente == teacher_nr).first()


def get_teacher(db: Session, /, *, id_teacher: int) -> teacher_schema.ShowTeacher:
    """Query teacher by id

    Args:
        db (Session): database session
        id_teacher (int): teacher id

    Returns:
        teacher_schema.ShowTeacher: teacher Detail
    """
    return db.query(Docentes).get(id_teacher)


def get_teachers(
    db: Session, /, *, skip: int = 0, limit: int = 100
) -> List[teacher_schema.ShowTeacher]:
    """Get list of teachers

    Args:
        db (Session): database session
        skip (int, optional): rows to skip. Defaults to 0.
        limit (int, optional): limit of rows. Defaults to 0.

    Returns:
        List[teacher_schema.ShowTeacher]: List of teachers
    """
    return db.query(Docentes).offset(skip).limit(limit).all()


def delete_teacher(db: Session, /, *, id_teacher: int) -> teacher_schema.ShowTeacher:
    """Delete teacher record and respective user

    Args:
        db (Session): database session
        id_teacher (int): teacher id

    Raises:
        HTTPException: teacher not found
        HTTPException: delete error

    Returns:
        teacher_schema.ShowTeacher: deleted teacher details
    """
    teacher = db.query(Docentes).get(id_teacher)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"teacher with id: {id_teacher} not found",
            ),
        )
    try:
        db.delete(teacher)  # delete teacher record
        db.delete(teacher.utilizador)  # delete teacher user
        db.commit()
        return teacher
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                f"Error deleting teacher: {id_teacher}",
                error=repr(e),
            ),
        )


def create_teacher(
    db: Session, request: teacher_schema.CreateTeacher, /
) -> teacher_schema.ShowTeacher:
    """Create a teacher and respective user

    Args:
        db (Session): database session
        request (teacher_schema.CreateTeacher): teacher and user data

    Raises:
        HTTPException: user exists
        HTTPException: teacher exists
        HTTPException: error creating teacher

    Returns:
        teacher: teacher details
    """
    if User.check_user_exists(
        db,
        nome_utilizador=request.utilizador.nome_utilizador,
        email=request.utilizador.email,
    ):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="user already exists"
        )
    if _check_teacher_exists(db, teacher_nr=request.nr_docente):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="teacher already exists"
        )

    user: User = User.create_user(db, request.utilizador)
    try:
        if user:
            new_teacher: Docentes = Docentes(
                id_utilizador=user.id_utilizador,
                nome=request.nome,
                nr_docente=request.nr_docente,
            )
            db.add(new_teacher)
            db.commit()
            db.refresh(new_teacher)
            return new_teacher
    except Exception as e:
        User.delete_user(db, id_utilizador=user.id_utilizador)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error creating teacher",
                error=repr(e),
            ),
        )
