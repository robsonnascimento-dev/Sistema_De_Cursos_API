from fastapi import APIRouter, HTTPException
from models.user import User, UserCreate
from database.db import get_connection
import uuid

router = APIRouter()

#Rota POST
@router.post("/user", response_model = User)
def cadastr_usuario(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    #essa parte verifica o email
    cursor.execute("select * from usuarios where email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(400, "email já existe")
    novo_usuario ={
        "id": str(uuid.uuid4()),
        "nome": user.nome,
        "email": user.email,
        "senha": user.senha,
        "tipo": "user"
    }
    cursor.execute("""
        insert into usuarios (id, nome, email, senha, tipo)
        values(%s, %s, %s, %s, %s)         
        """, (
        novo_usuario["id"],
        novo_usuario["nome"],
        novo_usuario["email"],
        novo_usuario["senha"],
        novo_usuario["tipo"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

    return novo_usuario

#get ususarios

@router.get("/usuarios")
def listar_usuarios():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return usuarios

#get pelo ID
@router.get("/usuarios/{user_id}")
def procurar_usuarios(user_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("select * from usuarios where id= %s", (user_id))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        raise HTTPException(404, "Usuário não encontrado")
    return user

#METODO PUT (REVISAR)

from models.user import UserUpdate

@router.put("/usuarios/{user_id}")
def atualizar_usuario(user_id: str, user_update: UserUpdate):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    if user_update.nome:
        user["nome"] = user_update.nome
    if user_update.email:
        user["email"] = user_update.email
    if user_update.senha:
        user["senha"] = user_update.senha

    cursor.execute("""
        UPDATE usuarios
        SET nome=%s, email=%s, senha=%s
        WHERE id=%s
    """, (user["nome"], user["email"], user["senha"], user_id))

    conn.commit()
    cursor.close()
    conn.close()

    return user

#METODO DELETE

@router.delete("/usuarios/{user_id}")
def deletar_usuario(user_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))

    if not cursor.fetchone():
        raise HTTPException(404, "Usuário não encontrado")

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Usuário deletado"}

