from typing import Any, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas.user_schema as user_schema
from models import user
from database import get_db
from oauth2 import get_current_user

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.get("/", response_model=List[user_schema.ShowUser], status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> List[user_schema.ShowUser]:
    users = user.get_users(db, skip, limit)
    return users


@router.post("/", response_model=user_schema.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: user_schema.UserCreate, db: Session = Depends(get_db)):
    # TODO email validation, password validation
    return user.create_user(db, request)

# @router.get("/{id}/{password}/pubkey", status_code=status.HTTP_200_OK, response_model=user_schema.ShowUser)
# def get_pub_key(id: int, password: str, db: Session = Depends(get_db), current_user: user_schema.UserCreate = Depends(get_current_user)):
#     return user.get_user_pub_key(db, id, password)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=user_schema.ShowUser, dependencies=[Depends(get_current_user)])
def get_user(id: int, db: Session =  Depends(get_db)):
    return user.get_user(db, id)

@router.delete("/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def delete_user(id: int, db: Session = Depends(get_db)):
    deleted_user = user.delete_user(db, id)
    ic(deleted_user) 
    return deleted_user

    
# TODO edit user
