import orm
from icecream import ic
from fastapi import FastAPI
from database import engine
from routers import user, auth
from fastapi.middleware.cors import CORSMiddleware

orm.user.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def index():
    return {"SIRPA API": "Visit docs for more information"}