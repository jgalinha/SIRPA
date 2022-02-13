# -*- coding: utf-8 -*-
"""UC model file

This module define the model operations for the UCs

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""


from typing import List

from db.ucs import UC, InscricoesUC, Periodos, SemestresUC, UCDocentes
from fastapi import HTTPException, status
from models.course import check_course_exists_by_id
from models.helpers import semester_exists_by_id
from models.student import check_student_by_id
from models.teacher import check_teacher_by_id
from schemas import nm_schema, uc_schema
from schemas.schedules_schema import CreateSchedule, ShowSchedule
from sqlalchemy import and_
from sqlalchemy.orm import Session
from utils import Utils


def check_if_teacher_in_uc(db: Session, /, *, teacher_id: int, uc_id: int) -> bool:
    """Check if an teacher is in an UC

    Args:
        db (Session): database session
        teacher_id (int): teacher id
        uc_id (int): uc id

    Raises:
        HTTPException: Error checking

    Returns:
        bool: teacher is in
    """
    try:
        is_in = (
            db.query(UCDocentes)
            .filter(
                and_(UCDocentes.id_docente == teacher_id, UCDocentes.id_uc == uc_id)
            )
            .first()
        )
        if is_in:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error checking if teacher is in uc",
                error=repr(e),
            ),
        )


def schedule_exists_by_id(db: Session, schedule_id: int, /) -> bool:
    """Check id schedule exists

    Args:
        db (Session): database session
        schedule_id (int): schedule id

    Raises:
        HTTPException: Error checking schedule

    Returns:
        bool: schedule exists
    """
    try:
        if db.query(Periodos).get(schedule_id):
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error checking if schedule exists",
                error=repr(e),
            ),
        )


def schedule_in_uc(db: Session, /, *, schedule_id: int, uc_id: int) -> bool:
    """Check id schedule is in UC

    Args:
        db (Session): database session
        schedule_id (int): schedule id
        uc_id (int): uc id

    Raises:
        HTTPException: Error checking if schedule is in UC

    Returns:
        bool: is in
    """
    schedule = (
        db.query(Periodos)
        .filter(and_(Periodos.id_periodo == schedule_id, Periodos.id_uc == uc_id))
        .first()
    )
    try:
        if schedule:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error checking if schedule is in uc",
                error=repr(e),
            ),
        )


def check_uc_exists(db: Session, /, *, name_uc: str) -> bool:
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


def check_uc_exists_by_id(db: Session, /, *, uc_id: int) -> bool:
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
    if not check_course_exists_by_id(db, id_course=request.id_curso):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"Course with id: {request.id_curso} not found!",
            ),
        )
    if check_uc_exists(db, name_uc=request.nome_uc):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND, f"UC with name: {request.nome_uc} found!"
            ),
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

    check_uc_exists_by_id(db, uc_id=id_uc)
    check_student_by_id(db, student_id=id_student)
    try:
        new_uc_subscription: InscricoesUC = InscricoesUC(
            id_aluno=id_student, id_uc=id_uc, data_inscricao=request.data_inscricao
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


def add_teacher(
    db: Session, request: nm_schema.TeacherUCBase, /
) -> nm_schema.TeacherUCBase:
    """Add teacher to UC

    Args:
        db (Session): database session
        request (nm_schema.TeacherUCBase): request data

    Raises:
        HTTPException: Error found

    Returns:
        nm_schema.TeacherUCBase: inserted data
    """
    id_teacher = request.id_docente
    id_uc = request.id_uc

    check_uc_exists_by_id(db, uc_id=id_uc)
    check_teacher_by_id(db, teacher_id=id_teacher)
    try:
        new_association: UCDocentes = UCDocentes(
            id_uc=id_uc,
            id_docente=id_teacher,
        )
        db.add(new_association)
        db.commit()
        db.refresh(new_association)
        return new_association
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error registering teacher!",
                error=repr(e),
            ),
        )


def remove_teacher(
    db: Session, request: nm_schema.TeacherUCBase, /
) -> nm_schema.TeacherUCBase:
    """Remove teacher from UC

    Args:
        db (Session): database session
        request (nm_schema.TeacherUCBase): request data

    Raises:
        HTTPException: Regestry not found
        HTTPException: Error removing teacher from UC

    Returns:
        nm_schema.TeacherUCBase: deleted data
    """
    teacher_id = request.id_docente
    uc_id = request.id_uc

    association = (
        db.query(UCDocentes)
        .filter(and_(UCDocentes.id_docente == teacher_id, UCDocentes.id_uc == uc_id))
        .first()
    )

    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                "Registry not found",
            ),
        )
    try:
        db.delete(association)
        db.commit()
        return association
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error removing teacher from UC",
                error=repr(e),
            ),
        )


def register_semester(
    db: Session, request: nm_schema.SemesterUCBase, /
) -> nm_schema.SemesterUCBase:
    """Register semester in UC

    Args:
        db (Session): database session
        request (nm_schema.SemesterUCBase): association data

    Raises:
        HTTPException: UC not found
        HTTPException: Semester not found
        HTTPException: Error association semester with UC

    Returns:
        nm_schema.SemesterUCBase: inserted data
    """
    uc_id = request.id_uc
    semester_id = request.id_semestre

    if not check_uc_exists_by_id(db, uc_id=uc_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"UC with id: {uc_id} not found!",
            ),
        )

    if not semester_exists_by_id(db, semester_id=semester_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"Semester with id: {semester_id} not found!",
            ),
        )

    new_association: SemestresUC = SemestresUC(id_uc=uc_id, id_semestre=semester_id)
    try:
        db.add(new_association)
        db.commit()
        db.refresh(new_association)
        return new_association
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error associating Semester with UC",
                error=repr(e),
            ),
        )


def remove_semester(
    db: Session, request: nm_schema.SemesterUCBase
) -> nm_schema.SemesterUCBase:
    """De-associate a semester from UC

    Args:
        db (Session): database session
        request (nm_schema.SemesterUCBase): association data

    Raises:
        HTTPException: Association not found
        HTTPException: Error de-associating

    Returns:
        nm_schema.SemesterUCBase: removed data
    """
    uc_id = request.id_uc
    semester_id = request.id_semestre
    association = (
        db.query(SemestresUC)
        .filter(
            and_(SemestresUC.id_semestre == semester_id, SemestresUC.id_uc == uc_id)
        )
        .first()
    )
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                "Registry not found",
            ),
        )
    try:
        db.delete(association)
        db.commit()
        return association
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error removing semester from UC",
                error=repr(e),
            ),
        )


def add_schedule(db: Session, request: CreateSchedule, /) -> ShowSchedule:
    """Add schedule to UC

    Args:
        db (Session): database session
        request (CreateSchedule): schedule data

    Raises:
        HTTPException: UC not found
        HTTPException: Error creating schedule

    Returns:
        ShowSchedule: schedule data
    """
    uc_id = request.id_uc
    week_day = request.dia_semana
    start_time = request.hora_inicio
    end_time = request.hora_fim

    if not check_uc_exists_by_id(db, uc_id=uc_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"UC with id: {uc_id} not found!",
            ),
        )

    if (
        db.query(Periodos)
        .filter(
            and_(
                Periodos.id_uc == uc_id,
                Periodos.dia_semana == week_day,
                Periodos.hora_inicio == start_time,
                Periodos.hora_fim == end_time,
            )
        )
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail=Utils.error_msg(
                status.HTTP_302_FOUND, "Schedule already exists for this UC"
            ),
        )
    new_schedule: Periodos = Periodos(
        id_uc=uc_id, dia_semana=week_day, hora_inicio=start_time, hora_fim=end_time
    )
    try:
        db.add(new_schedule)
        db.commit()
        db.refresh(new_schedule)
        return new_schedule
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error creating schedule",
                error=repr(e),
            ),
        )


def remove_schedule(db: Session, /, *, schedule_id: int) -> ShowSchedule:
    """Remove schedule from UC

    Args:
        db (Session): database session
        schedule_id (int): schedule id

    Raises:
        HTTPException: Schedule not found
        HTTPException: Error removing schedule

    Returns:
        ShowSchedule: removed schedule
    """
    schedule = db.query(Periodos).get(schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"Schedule with id: {schedule_id} not found!",
            ),
        )

    try:
        db.delete(schedule)
        db.commit()
        return schedule
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Utils.error_msg(
                status.HTTP_409_CONFLICT,
                "Error removing schedule from UC",
                error=repr(e),
            ),
        )
