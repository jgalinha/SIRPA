# -*- coding: utf-8 -*-
"""Class model file

This module define the model operations for the Classes

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

import base64
import json
from email.mime import base

from db.aulas import Aulas
from fastapi import HTTPException, status
from icecream import ic
from models import user
from models.student import confirm_student_user_id
from models.uc import (
    check_if_student_in_uc,
    check_if_teacher_in_uc,
    check_uc_exists_by_id,
    schedule_in_uc,
)
from schemas.class_schema import CreateClass, CreateQRCodeClass, ShowClass
from sqlalchemy.orm import Session
from tools import crypt
from utils import Utils


def create_class(db: Session, request: CreateClass, /) -> ShowClass:
    """Create a class

    Args:
        db (Session): database session
        request (CreateClass): class data

    Raises:
        HTTPException: UC doens't exists
        HTTPException: Teacher not in UC
        HTTPException: Schedule not in UC
        HTTPException: Error creating class

    Returns:
        ShowClass: class details
    """
    uc_id = request.id_uc
    teacher_id = request.id_docente
    schedule_id = request.id_periodo
    date = request.data
    resume = request.resumo
    summary = request.sumario
    room = request.sala

    if not check_uc_exists_by_id(db, uc_id=uc_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"UC with id: {uc_id} not found!",
            ),
        )

    if not check_if_teacher_in_uc(db, teacher_id=teacher_id, uc_id=uc_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"Teacher with id: {teacher_id} doesn't teach in UC with id {uc_id}",
            ),
        )

    if not schedule_in_uc(db, schedule_id=schedule_id, uc_id=uc_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"UC with id: {uc_id} has no schedule with id: {schedule_id}!",
            ),
        )

    new_class: Aulas = Aulas(
        id_uc=uc_id,
        id_docente=teacher_id,
        id_periodo=schedule_id,
        data=date,
        resumo=resume,
        sumario=summary,
        sala=room,
    )

    try:
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        return new_class
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error creating class",
                error=repr(e),
            ),
        )


def remove_class(db: Session, /, *, class_id: int) -> ShowClass:
    data = db.query(Aulas).get(class_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                "Class not found",
            ),
        )
    try:
        db.delete(data)
        db.commit()
        return data
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error removing class",
                error=repr(e),
            ),
        )


def create_QRCode(db: Session, request: CreateQRCodeClass, /, *, user_id: int):
    class_id = request.id_aula
    student_id = request.id_aluno
    password = request.password
    aula = db.query(Aulas).get(class_id)
    uc_id = aula.id_uc

    if not confirm_student_user_id(db, user_id=user_id, student_id=student_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                "User id and student id don't match",
            ),
        )

    if not check_if_student_in_uc(db, student_id=student_id, uc_id=uc_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                "Student is not in UC",
            ),
        )
    msg = {"id_aluno": student_id, "id_aula": class_id}

    encrypted_kr = user.get_kr(db, user_id)
    kr = crypt.load_priv_key(encrypted_kr, password)
    sign_msg = crypt.sign(kr, bytes(json.dumps(msg), "utf-8"))
    sign_msg_b64 = base64.encodebytes(sign_msg)
    # string_msg = sign_msg_b64.decode("utf-8")
    # pub_key = user.get_ku(db, user_id)
    # ku = crypt.load_pub_key(pub_key)
    # msg_64 = base64.decodebytes(sign_msg_b64)
    # ver_msg = crypt.verify(ku, bytes(json.dumps(msg), "utf-8"), msg_64)
    return {"signature": sign_msg_b64, "msg": msg}
