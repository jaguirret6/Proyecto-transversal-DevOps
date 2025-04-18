from fastapi import FastAPI

app = FastAPI(title="Mi API", description="API con 10 endpoints y Swagger")

@app.get("/")
def home():
    return {"mensaje": "¡Bienvenido a la API!"}

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