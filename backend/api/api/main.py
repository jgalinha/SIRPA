from database import engine
from db import alunos as Alunos
from db import docentes as Docentes
from db import ucs as UCs
from db import user as User
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, user

User.Base.metadata.create_all(bind=engine)
Alunos.Base.metadata.create_all(bind=engine)
Docentes.Base.metadata.create_all(bind=engine)
UCs.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Authorization"],
)

app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def index():
    return {"SIRPA API": "Visit docs for more information"}
