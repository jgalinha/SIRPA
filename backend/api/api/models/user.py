import schemas.user_schema as user_schema
from sqlalchemy.sql.functions import user
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.user import User
from crypt import Crypt
from fastapi import HTTPException, status
from icecream import ic


def get_user(db: Session, id_utilizador: int):
    return db.query(User).filter(User.id_utilizador == id_utilizador).first()

def check_user_exists(db: Session, nome_utilizador: str, email: str):
    users = db.query(User).filter(or_(User.nome_utilizador == nome_utilizador, User.email == email)).all()
    if users:
        return True
    return False

def get_user_pub_key(db: Session, id_utilizador: int, password: str):
    pub_key = db.query(User).filter(User.id_utilizador == id_utilizador).first().public_key
    #kr = Crypt.load_priv_key(password, pub_key)
    ku = Crypt.load_pub_key(pub_key)
    cipher = Crypt.encrypt(ku, b"Test message")
    ic(cipher)
    priv_key = db.query(User).filter(User.id_utilizador == id_utilizador).first().private_key
    kr = Crypt.load_priv_key(priv_key, password)
    plain = Crypt.decrypt(kr, cipher)
    ic(plain)
    return "bah"

def create_user(db: Session, request: user_schema.User):
    if not check_user_exists(db, request.nome_utilizador, request.email):
            key_pair = Crypt.generate_key_pair(request.password)
            new_user = User(nome_utilizador = request.nome_utilizador,
                                email = request.email,
                                password =  Crypt.bcrypt(request.password),
                                private_key = key_pair[1],
                                public_key = key_pair[0])
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return new_user
    raise HTTPException(status_code=status.HTTP_302_FOUND, detail="user already exists")
