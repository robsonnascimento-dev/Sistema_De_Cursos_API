from fastapi import APIRouter, HTTPException
from models.course import Course, CourseCreate
from database.db import get_connection
import uuid

router = APIRouter()
# POST
@router.post("/course", response_model= Course)
def criar_curso(course: CourseCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary= True)
    
    cursor.execute("select * from courses where id = %s", (course.id,))
    if cursor.fetchone():
        raise HTTPException(400, "Esse curso já existe")
    novo_curso = {
        "id": str(uuid.uuid4()),
        "nome" : course.nome,
        "descricao": course.descricao,
        "categoria": course.categoria,
        "carga_horaria": course.carga_horaria,
        "instrutor": course.instrutor
    }
    cursor.execute("""
        insert into courses (id, nome, descrição, categoria, carga_horaria, instrutor)
        values(%s,%s,%s,%s,%s,%s)
        """,(
            novo_curso["id"],
            novo_curso["nome"],
            novo_curso["descricao"],
            novo_curso["categoria"],
            novo_curso["carga_horaria"],
            novo_curso["instrutor"]
     ))
    conn.commit()
    cursor.close()
    conn.close()
    
    return novo_curso
# get cursos
@router.get("/findcourse")
def listar_cursos():
    conn= get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("select * from courses")
    curso = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return curso
    
    