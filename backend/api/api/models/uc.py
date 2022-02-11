# -*- coding: utf-8 -*-
"""UC model file

This module define the model operations for the UCs

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""


from operator import and_
from typing import List

from db.ucs import UC, InscricoesUC
from fastapi import HTTPException, status
from models import course as Course
from models.student import check_student_by_id
from schemas import nm_schema, uc_schema
from sqlalchemy.orm import Session
from utils import Utils


def _check_uc_exists(db: Session, /, *, name_uc: str) -> bool:
    """Check if a uc name already exists in database

    Args:
        db (Session): database session
        name (str): uc name

    Raises:
        HTTPException: server error

    Returns:
        bool: uc exists
    """
    try:
        uc = db.query(UC).filter(UC.nome_uc == name_uc).all()
        if uc:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error checking if uc exists",
                error=repr(e),
            ),
        )


def _check_uc_exists_by_id(db: Session, /, *, uc_id: int) -> bool:
    """Check if a uc id exists in database

    Args:
        db (Session): database session
        uc_id (int): uc id

    Raises:
        HTTPException: server error

    Returns:
        bool: uc exists
    """
    try:
        uc = db.query(UC).get(uc_id)
        if uc:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error checking if uc exists",
                error=repr(e),
            ),
        )


def update_uc(
    db: Session, /, *, uc_id: int, request: uc_schema.UpdateUC
) -> uc_schema.ShowUC:
    """Update uc details

    Args:
        db (Session): database session
        uc_id (int): uc id
        request (uc_schema.UpdateUC): uc name and number

    Raises:
        HTTPException: uc not fount
        HTTPException: Error updating

    Returns:
        uc_schema.ShowUC: [description]
    """
    uc = db.query(UC).get(uc_id)
    if not uc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"uc with id: {uc_id} not found",
            ),
        )
    uc.nome_uc = request.nome_uc
    uc.descricao = request.descricao
    try:
        db.query(UC).filter(UC.id_uc == uc_id).update(
            {UC.nome_uc: request.nome_uc, UC.descricao: request.descricao}
        )
        db.commit()
        return uc
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                msg=f"Error updating uc: {uc_id}",
                error=repr(e),
            ),
        )


def get_uc_by_number(db: Session, /, *, uc_nr: int) -> uc_schema.ShowUC:
    """Get uc by number

    Args:
        db (Session): database session
        uc_nr (int): uc number

    Returns:
        uc_schema.ShowUC: uc details
    """
    return db.query(UC).filter(UC.id_uc == uc_nr).first()


def get_uc(db: Session, /, *, id_uc: int) -> uc_schema.ShowUC:
    """Query uc by id

    Args:
        db (Session): database session
        id_uc (int): uc id

    Returns:
        uc_schema.ShowUC: uc Detail
    """
    return db.query(UC).get(id_uc)


def get_ucs(
    db: Session, /, *, skip: int = 0, limit: int = 100
) -> List[uc_schema.ShowUC]:
    """Get list of ucs

    Args:
        db (Session): database session
        skip (int, optional): rows to skip. Defaults to 0.
        limit (int, optional): limit of rows. Defaults to 0.

    Returns:
        List[uc_schema.ShowUC]: List of ucs
    """
    return db.query(UC).offset(skip).limit(limit).all()


def delete_uc(db: Session, /, *, id_uc: int) -> uc_schema.ShowUC:
    """Delete uc record and respective user

    Args:
        db (Session): database session
        id_uc (int): uc id

    Raises:
        HTTPException: uc not found
        HTTPException: delete error

    Returns:
        uc_schema.ShowUC: deleted uc details
    """
    uc = db.query(UC).get(id_uc)
    if not uc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"uc with id: {id_uc} not found",
            ),
        )
    try:
        db.delete(uc)  # delete uc record
        db.commit()
        return uc
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                f"Error deleting uc: {id_uc}",
                error=repr(e),
            ),
        )


def create_uc(db: Session, request: uc_schema.CreateUC, /) -> uc_schema.ShowUC:
    """Create a uc and respective user

    Args:
        db (Session): database session
        request (uc_schema.CreateUC): uc and user data

    Raises:
        HTTPException: user exists
        HTTPException: uc exists
        HTTPException: error creating uc

    Returns:
        uc: uc details
    """
    if not Course._check_course_exists_by_id(db, id_course=request.id_curso):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="course don't exists"
        )
    if _check_uc_exists(db, name_uc=request.nome_uc):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="uc already exists"
        )

    try:
        new_uc: UC = UC(
            nome_uc=request.nome_uc,
            descricao=request.descricao,
            id_curso=request.id_curso,
        )
        db.add(new_uc)
        db.commit()
        db.refresh(new_uc)
        return new_uc
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error creating uc",
                error=repr(e),
            ),
        )


def subscribe_uc(
    db: Session, request: nm_schema.UCSubscriptionBase, /
) -> nm_schema.UCSubscriptionBase:
    """Subscribe a student with and UC

    Args:
        db (Session): database session
        request (nm_schema.UCSubscriptionBase): UCSubscrition schema

    Raises:
        HTTPException: UC not found
        HTTPException: Student not found
        HTTPException: Error subscribing

    Returns:
        bool: subscrition successful
    """
    id_student = request.id_aluno
    id_uc = request.id_uc

    if not _check_uc_exists_by_id(db, uc_id=id_uc):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND, f"UC with id: {id_uc} not found!"
            ),
        )

    if not check_student_by_id(db, student_id=id_student):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND, f"Student with id: {id_student} not found!"
            ),
        )

    try:
        new_uc_subscription: InscricoesUC = InscricoesUC(
            id_aluno=id_student, id_uc=id_uc, data_inscricao=request.data_incricao
        )
        db.add(new_uc_subscription)
        db.commit()
        db.refresh(new_uc_subscription)
        return new_uc_subscription
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error subscribing UC",
                error=repr(e),
            ),
        )


def unsubscribeUC(
    db: Session, request: nm_schema.UCunSubscriptionBase, /
) -> nm_schema.UCunSubscriptionBase:
    """Unsubscribe UC

    Args:
        db (Session): database session
        request (nm_schema.UCunSubscriptionBase): unsubscription schema

    Raises:
        HTTPException: Subscription not found
        HTTPException: Error unsubscribing

    Returns:
        nm_schema.UCunSubscriptionBase: subscription
    """
    student_id = request.id_aluno
    uc_id = request.id_uc

    subscrition = (
        db.query(InscricoesUC)
        .filter(and_(InscricoesUC.id_aluno == student_id, InscricoesUC.id_uc == uc_id))
        .first()
    )
    if not subscrition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                "Subscription not found",
            ),
        )
    try:
        db.delete(subscrition)
        db.commit()
        return subscrition
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error unsubscribing",
                error=repr(e),
            ),
        )
