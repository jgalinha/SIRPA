import schemas, models
from icecream import ic
from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import engine, get_db
from model import user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def index():
    return {"SIRPA API": "Visit docs for more information"}

@app.post("/user", response_model=schemas.ShowUser, tags=["users"], status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(db, request)