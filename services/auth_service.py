from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from models.user_task import User
from schemas.user_task import UserCreate
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database.session import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_user(user: UserCreate, db: Session):
    existing_username = db.query(User).filter_by(username=user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=409,
            detail="El nombre de usuario ya está registrado",
        )

    existing_email = db.query(User).filter_by(email=user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="El email ya está registrado",
        )

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter_by(username=username).first()
    if not user or not pwd_context.verify(password, str(user.hashed_password)):
        return None
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(User).filter_by(username=username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


def seed_default_users(db: Session):
    default_users = [
        UserCreate(
            username="user1",
            email="user1@example.com",
            password="password123",
            role="user",
        ),
        UserCreate(
            username="admin1",
            email="admin1@example.com",
            password="adminpass123",
            role="admin",
        ),
    ]

    for user_data in default_users:
        username_exists = db.query(User).filter_by(username=user_data.username).first()
        email_exists = db.query(User).filter_by(email=user_data.email).first()
        if username_exists or email_exists:
            continue
        create_user(user_data, db)
