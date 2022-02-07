from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "utilizadores"
    
    id_utilizador = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_utilizador = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    private_key = Column(String)
    public_key = Column(String)