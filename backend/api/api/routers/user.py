from typing import List
from fastapi import APIRouter, Depends, responses, status
from sqlalchemy.orm import Session
from orm.user import User
import schemas
import schemas.user_schema as user_schema
from models import user
from database import get_db
from oauth2 import get_current_user

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)

@router.post("/", response_model=user_schema.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: user_schema.User, db: Session = Depends(get_db)):
    # TODO email validation, password validation
    return user.create_user(db, request)

@router.get("/{id}/{password}/pubkey", status_code=status.HTTP_200_OK)
def get_pub_key(id: int, password: str, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return user.get_user_pub_key(db, id, password)

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_users(id: int, db: Session =  Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return user.get_user(db, id)
