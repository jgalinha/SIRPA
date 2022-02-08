# -*- coding: utf-8 -*-
"""User model file

This module define the model operations for the users

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""
from crypt import Crypt
from typing import List

import schemas.user_schema as user_schema
from db.user import User
from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from utils import Utils


def check_user_exists(db: Session, /, *, nome_utilizador: str, email: str) -> bool:
    """Check a given username and email exists in db

    Args:
        db (Session): database
        nome_utilizador (str): username
        email (str): email.

    Returns:
        bool: return True if username or email exists
    """
    try:
        user = (
            db.query(User)
            .filter(or_(User.nome_utilizador == nome_utilizador, User.email == email))
            .all()
        )
        if user:
            return True
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error checking if user exists",
                error=repr(e),
            ),
        )


def get_users(
    db: Session, /, *, skip: int = 0, limit: int = 100
) -> List[user_schema.ShowUser]:
    """Get users

    Args:
        db (Session): database session
        skip (int, optional): rows to skip. Defaults to 0.
        limit (int, optional): limit of rows. Defaults to 100.

    Returns:
        List[user_schema.ShowUser]: List of users
    """
    return db.query(User).offset(skip).limit(limit).all()


def delete_user(db: Session, /, *, id_utilizador: int):
    """Delete user from database

    Args:
        db (Session): database
        id_utilizador (int): user id

    Raises:
        HTTPException: 404 user not found
        HTTPException: 500 error when trying to delete user

    Returns:
        User: Deleted user details
    """
    user = db.query(User).get(id_utilizador)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Utils.error_msg(
                status.HTTP_404_NOT_FOUND,
                f"utilizador com id: {id_utilizador} não encontrado",
            ),
        )
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error deleting user: {id_utilizador}",
                error=repr(e),
            ),
        )
    return user


def get_user(db: Session, /, *, id_utilizador: int):
    """Query user by id

    Args:
        db (Session): database
        id_utilizador (int): username

    Returns:
        User: User details
    """
    return db.query(User).filter(User.id_utilizador == id_utilizador).first()


# def get_user_pub_key(db: Session, id_utilizador: int, password: str):
#     pub_key = db.query(User).filter(User.id_utilizador == id_utilizador).first().public_key
#     #kr = Crypt.load_priv_key(password, pub_key)
#     ku = Crypt.load_pub_key(pub_key)
#     cipher = Crypt.encrypt(ku, b"Test message")
#     ic(cipher)
#     priv_key = db.query(User).filter(User.id_utilizador == id_utilizador).first().private_key
#     kr = Crypt.load_priv_key(priv_key, password)
#     plain = Crypt.decrypt(kr, cipher)
#     ic(plain)
#     return "bah"


def create_user(db: Session, request: user_schema.UserCreate, /) -> User:
    """Create and user

    Args:
        db (Session): database
        request (user_schema.UserCreate): user data

    Raises:
        HTTPException: duplicated username or email

    Returns:
        User: details from inserted user
    """
    try:
        if not check_user_exists(
            db, nome_utilizador=request.nome_utilizador, email=request.email
        ):
            key_pair = Crypt.generate_key_pair(request.password)
            new_user = User(
                nome_utilizador=request.nome_utilizador,
                email=request.email,
                password=Crypt.bcrypt(request.password),
                private_key=key_pair[1],
                public_key=key_pair[0],
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="user already exists"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Utils.error_msg(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error creating user",
                error=repr(e),
            ),
        )
