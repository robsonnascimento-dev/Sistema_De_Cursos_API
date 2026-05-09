from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    nome: str
    email: str
    senha: str
    tipo: str #user ou adimm

class UserCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
