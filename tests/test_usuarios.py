import pytest
from httpx import AsyncClient
from app.main import app  # Asegúrate de que 'app' es tu instancia FastAPI
from databases import Database
from app.database import database, usuarios  # Si tienes una instancia de tu base de datos configurada

@pytest.mark.asyncio
async def test_crear_usuario():
    try:
        # Conectarse a la base de datos
        await database.connect()

        # Usamos AsyncClient para realizar la petición HTTP asincrónica
        async with AsyncClient(app=app, base_url="http://test") as client:
            respuesta = await client.post("/usuarios/", json={
                "nombre": "Juan",
                "edad": 30,
                "color_favorito": "Azul"
            })

        # Verificar que la respuesta sea exitosa
        assert respuesta.status_code == 200

    finally:
        # Desconectarse de la base de datos después de la prueba
        await database.disconnect()


