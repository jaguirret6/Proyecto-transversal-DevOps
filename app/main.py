from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import database, usuarios, event
from contextlib import asynccontextmanager
import logging

# ----------- LIFESPAN -----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="Mi API", description="API con endpoints, CRUD. Deploy en render y monitoreo en new relic", lifespan=lifespan)
# ----------- ENDPOINTS VARIOS -----------

@app.get("/")
def home():
    return {"mensaje": "API DevOps - Juan Aguirre"}

@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"mensaje": f"Hola, {nombre}!"}

@app.get("/suma")
def suma(a: int, b: int):
    return {"resultado": a + b}

@app.get("/resta")
def resta(a: int, b: int):
    return {"resultado": a - b}

@app.get("/multiplicacion")
def multiplicacion(a: int, b: int):
    return {"resultado": a * b}

@app.get("/division")
def division(a: int, b: int):
    if b == 0:
        return {"error": "No se puede dividir por cero"}
    return {"resultado": a / b}

@app.get("/invertir")
def invertir(texto: str):
    return {"resultado": texto[::-1]}

@app.get("/longitud")
def longitud(texto: str):
    return {"longitud": len(texto)}

@app.get("/mayusculas")
def mayusculas(texto: str):
    return {"resultado": texto.upper()}

@app.get("/minusculas")
def minusculas(texto: str):
    return {"resultado": texto.lower()}

@app.get("/db-status")
async def db_status():
    try:
        await database.execute("SELECT 1")
        return {"status": "Conexión OK a la DB"}
    except Exception as e:
        return {"status": "Error en la conexión", "detalle": str(e)}
    
@app.get("/provocar-error")
def provocar_error():
    raise HTTPException(status_code=500, detail="Error de prueba controlado.")

# ----------- ABM USUARIOS -----------

class UsuarioIn(BaseModel):
    nombre: str
    edad: int
    color_favorito: str

class UsuarioOut(UsuarioIn):
    id: int

@app.post("/usuarios/", response_model=UsuarioOut)
async def crear_usuario(usuario: UsuarioIn):
    query = usuarios.insert().values(
        nombre=usuario.nombre,
        edad=usuario.edad,
        color_favorito=usuario.color_favorito
    )
    user_id = await database.execute(query)
    return {**usuario.model_dump(), "id": user_id}

@app.get("/usuarios/", response_model=list[UsuarioOut])
async def obtener_usuarios():
    query = usuarios.select()
    return await database.fetch_all(query)

@app.get("/usuarios/{id}", response_model=UsuarioOut)
async def obtener_usuario(id: int):
    query = usuarios.select().where(usuarios.c.id == id)
    usuario = await database.fetch_one(query)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{id}", response_model=UsuarioOut)
async def actualizar_usuario(id: int, datos: UsuarioIn):
    query = usuarios.update().where(usuarios.c.id == id).values(
        nombre=datos.nombre,
        edad=datos.edad,
        color_favorito=datos.color_favorito
    )
    await database.execute(query)
    return {**datos.model_dump(), "id": id}

@app.delete("/usuarios/{id}")
async def eliminar_usuario(id: int):
    query = usuarios.delete().where(usuarios.c.id == id)
    resultado = await database.execute(query)
    if resultado == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}
