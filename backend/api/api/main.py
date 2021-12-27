import orm
from icecream import ic
from fastapi import FastAPI
from database import engine
from routers import user, auth

orm.user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def index():
    return {"SIRPA API": "Visit docs for more information"}