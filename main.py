from fastapi import FastAPI
from sqlalchemy.orm import Session
from routers import auth_routers
from core.logger import init_logger
from database.session import Base, engine, sessionLocal
from models import user_task
from services.auth_service import seed_default_users

app = FastAPI()

Base.metadata.create_all(bind=engine)
init_logger()

app.include_router(auth_routers.router)


@app.on_event("startup")
def startup_seed_users():
    db: Session = sessionLocal()
    try:
        seed_default_users(db)
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "API de autenticación activa"}

