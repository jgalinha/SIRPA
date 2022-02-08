from fastapi import APIRouter, status, HTTPException, Response
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from schemas import auth_schema as auth
from database import get_db
from db.user import User 
from crypt import Crypt
from jwtoken import create_access_token

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"error": {"msg": "Dados inválidos!", "code": status.HTTP_404_NOT_FOUND}})

    if not Crypt.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"error": {"msg": "Dados inválidos!", "code": status.HTTP_404_NOT_FOUND}})

    access_token = create_access_token(data={"sub": user.email, "id": user.id_utilizador, "username": user.nome_utilizador})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}

