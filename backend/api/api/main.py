#!/usr/bin/env python3

from fastapi import FastAPI
from sqlalchemy.orm import Session

import schemas, models
from database import SessionLocal, engine, Base
from model import user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World from dockercompose"}
