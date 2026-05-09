from pydantic import BaseModel
from typing import Optional

class Course(BaseModel):
    id: str
    nome: str
    descricao: str
    categoria: str
    carga_horaria: int
    instrutor: str

class CourseCreate(BaseModel):
    nome: str
    descricao: str
    categoria: str
    carga_horaria: int
    instrutor: str

class CourseUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    carga_horaria: Optional[int] = None
    instrutor: Optional[str] = None
