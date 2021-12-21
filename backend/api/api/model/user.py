from sqlalchemy.orm import Session

import models, schemas

def get_user(db: Session, id_utilizador: int):
    return db.query(models.User).filter(models.User.id_utilizador == id_utilizador).first()