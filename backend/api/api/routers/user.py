from typing import List

import schemas.user_schema as user_schema
from database import get_db
from fastapi import APIRouter, Depends, status
from models import user
from oauth2 import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(tags=["Utilizadores"], prefix="/user")


@router.get(
    "/",
    response_model=List[user_schema.ShowUser],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
def get_users(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> List[user_schema.ShowUser]:
    """Get all users

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).
        skip (int, optional): rows to skip. Defaults to 0.
        limit (int, optional): limit of rows. Defaults to 100.

    Returns:
        List[user_schema.ShowUser]: list of Users
    """
    users = user.get_users(db, skip, limit)
    return users


@router.post(
    "/", response_model=user_schema.ShowUser, status_code=status.HTTP_201_CREATED
)
def create_user(request: user_schema.UserCreate, db: Session = Depends(get_db)):
    """Create user

    Args:
        request (user_schema.UserCreate): user data
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        user_schema.ShowUser: created user details
    """
    # TODO email validation, password validation
    return user.create_user(db, request)


# @router.get("/{id}/{password}/pubkey", status_code=status.HTTP_200_OK, response_model=user_schema.ShowUser)
# def get_pub_key(id: int, password: str, db: Session = Depends(get_db), current_user: user_schema.UserCreate = Depends(get_current_user)):
#     return user.get_user_pub_key(db, id, password)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.ShowUser,
    dependencies=[Depends(get_current_user)],
)
def get_user(id: int, db: Session = Depends(get_db)):
    """Get user by id

    Args:
        id (int): user id
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        user_schema.ShowUser: user details
    """
    return user.get_user(db, id_utilizador=id)


@router.delete(
    "/{id}",
    response_model=user_schema.ShowUser,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
def delete_user(id: int, db: Session = Depends(get_db)):
    """Delete an user by id

    Args:
        id (int): user id
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        user_schema.ShowUser: deleted user details
    """
    deleted_user = user.delete_user(db, id_utilizador=id)
    return deleted_user


# TODO edit user
