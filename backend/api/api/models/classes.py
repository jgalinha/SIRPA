# -*- coding: utf-8 -*-
"""Class model file

This module define the model operations for the Classes

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""

import base64
import json
from datetime import datetime
from typing import Dict

from db.aulas import Aulas, Presencas
from fastapi import HTTPException, status
from models import user
from models.student import get_student_id_by_user_id, get_student_user_id
from models.teacher import get_teacher_nr_by_user_id
from models.uc import (
    check_if_student_in_uc,
    check_if_teacher_in_uc,
    check_uc_exists_by_id,
    schedule_in_uc,
)
from schemas.class_schema import (
    CreateClass,
    CreateQRCodeClass,
    ReadQRCodeClass,
    ShowClass,
)
from sqlalchemy import and_
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
    """Remove class

    Args:
        db (Session): database session
        class_id (int): class id

    Raises:
        HTTPException: Class not found
        HTTPException: Error removing class

    Returns:
        ShowClass: class removed
    """
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


def read_QRCode(db: Session, request: ReadQRCodeClass, /, *, user_id: int):
    try:
        student_id = request.msg.id_aluno
        class_id = request.msg.id_aula
        signature = request.signature
        msg = {"id_aluno": student_id, "id_aula": class_id}
        presenca = (
            db.query(Presencas)
            .filter(
                and_(Presencas.id_aluno == student_id, Presencas.id_aula == class_id)
            )
            .first()
        )
        if presenca:
            raise HTTPException(
                status_code=status.HTTP_302_FOUND,
                detail=Utils.error_msg(
                    status.HTTP_302_FOUND,
                    "Presence already confirmed!",
                ),
            )

        student_user_id = get_student_user_id(db, student_id=student_id)
        class_data = db.query(Aulas).get(class_id)
        teacher_id = get_teacher_nr_by_user_id(db, user_id=user_id)
        if teacher_id != class_data.id_docente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=Utils.error_msg(
                    status.HTTP_404_NOT_FOUND,
                    "Teacher is not from this class",
                ),
            )

        if not check_if_student_in_uc(
            db, student_id=student_id, uc_id=class_data.id_uc
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=Utils.error_msg(
                    status.HTTP_404_NOT_FOUND,
                    "Student is not in UC",
                ),
            )

        pub_key = user.get_ku(db, student_user_id)
        ku = crypt.load_pub_key(pub_key)
        decoded_sig = base64.decodebytes(bytes(signature, "utf-8"))
        check = crypt.verify(ku, bytes(json.dumps(msg), "utf-8"), decoded_sig)
        if check["data"] == "data validated":
            presenca: Presencas = Presencas(
                id_aluno=student_id, id_aula=class_id, confirmacao=datetime.utcnow()
            )
            db.add(presenca)
            db.commit()
            db.refresh(presenca)

            return presenca

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error checking in student",
                error=repr(e),
            ),
        )


def create_QRCode(db: Session, request: CreateQRCodeClass, /, *, user_id: int) -> Dict:
    """Create QRCode data to show to teacher

    Args:
        db (Session): database session
        request (CreateQRCodeClass) data
        user_id (int): user id

    Raises:
        HTTPException: Student not found
        HTTPException: Student not in uc

    Returns:
        Dict: QRCode data
    """
    class_id = request.id_aula
    student_id = get_student_id_by_user_id(db, user_id=user_id)
    password = request.password
    aula = db.query(Aulas).get(class_id)
    uc_id = aula.id_uc

    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                "Student not found",
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

    return {"signature": sign_msg_b64, "msg": msg}
