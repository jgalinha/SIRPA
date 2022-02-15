from database import get_db
from db.user import User
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwtoken import create_access_token
from models import student, teacher
from sqlalchemy.orm.session import Session
from tools import crypt

router = APIRouter(tags=["Autenticação"], prefix="/auth")


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    response: Response,
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {"msg": "Dados inválidos!", "code": status.HTTP_404_NOT_FOUND}
            },
        )

    if not crypt.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {"msg": "Dados inválidos!", "code": status.HTTP_404_NOT_FOUND}
            },
        )

    is_teacher = teacher.check_teacher_by_user_id(db, user_id=user.id_utilizador)
    is_student = student.check_student_by_user_id(db, user_id=user.id_utilizador)
    is_super = True if not is_teacher and not is_student else False

    access_token = create_access_token(
        data={
            "sub": user.email,
            "id": user.id_utilizador,
            "username": user.nome_utilizador,
            "isTeacher": is_teacher,
            "isStudent": is_student,
            "isSuper": is_super,
        }
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}
