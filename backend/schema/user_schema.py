# user_schema.py

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal


class UserSchema(BaseModel):
    id: Optional[int] = None  # ⚠️ Ahora es opcional
    name: str
    email: str
    password: str
    rol: Literal['usuario', 'admin', 'moderador']  # 👈 solo permite estos


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    rol: Optional[str] = None  # Valor por defecto si no se proporciona

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str



class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    rol: Optional[Literal['usuario', 'admin', 'moderador']] = None