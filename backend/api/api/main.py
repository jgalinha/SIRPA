from orm import user as User
from orm import alunos as Alunos
from icecream import ic
from fastapi import FastAPI
from database import engine
from routers import user, auth
from fastapi.middleware.cors import CORSMiddleware

User.Base.metadata.create_all(bind=engine)
Alunos.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Authorization"],
)

app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def index():
    return {"SIRPA API": "Visit docs for more information"}