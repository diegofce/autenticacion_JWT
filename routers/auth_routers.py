from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.session import get_db
from services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from schemas.user_task import UserCreate, UserOut, Token
from models.user_task import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if len(user.username) < 3 or len(user.username) > 50:
        raise HTTPException(
            status_code=400,
            detail="El usuario debe estar entre 3 y 50 caracteres",
        )
    if len(user.password) < 6 or len(user.password) > 100:
        raise HTTPException(
            status_code=400,
            detail="La contraseña debe estar entre 6 y 100 caracteres",
        )
    if len(user.email) < 5 or len(user.email) > 100:
        raise HTTPException(
            status_code=400,
            detail="El email debe estar entre 5 y 100 caracteres",
        )
    return create_user(user, db)


@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos",
        )
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/admin-only")
def admin_only(current_user: User = Depends(get_current_user)):
    if str(current_user.role) != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado: solo administradores pueden acceder a este recurso",
        )
    return {"message": "Bienvenido, admin!", "username": current_user.username, "role": current_user.role}
