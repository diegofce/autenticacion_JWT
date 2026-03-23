from sqlalchemy import Column, Integer, String, Boolean
from database.session import Base

class User(Base):
    __tablename__ = 'users'
# Crear la tabla de usuarios con los campos necesarios

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default='user')  # 'user' o 'admin'
    is_active = Column(Boolean, default=True)
