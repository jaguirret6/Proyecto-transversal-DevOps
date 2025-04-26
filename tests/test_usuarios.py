import pytest
from fastapi.testclient import TestClient
from app.main import app  # Aquí importas tu aplicación FastAPI
from app.database import database


client = TestClient(app)

# Test para crear un usuario
def test_create_usuario():
    response = client.post(
        "/usuarios",
        json={"nombre": "Juan", "edad": 25, "color_favorito": "Azul"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data  # Verificar que el 'id' esté presente
    assert data["nombre"] == "Juan"
    assert data["edad"] == 25
    assert data["color_favorito"] == "Azul"
# Test para obtener usuarios
def test_get_usuarios():
    response = client.get("/usuarios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Espera una lista de usuarios

# Test para eliminar un usuario
def test_create_and_delete_usuario():
    # 1. Crear un usuario
    response_create = client.post(
        "/usuarios",
        json={"nombre": "Juan", "edad": 25, "color_favorito": "Azul"}
    )
    created_user = response_create.json()  # Obtiene el usuario creado
    user_id = created_user["id"]  # Obtiene el ID del usuario creado

    # 2. Verificar que el usuario fue creado correctamente
    assert response_create.status_code == 200
    assert "id" in created_user
    assert created_user["nombre"] == "Juan"
    assert created_user["edad"] == 25
    assert created_user["color_favorito"] == "Azul"

    # 3. Eliminar el usuario creado
    response_delete = client.delete(f"/usuarios/{user_id}")
    
    # 4. Verificar que la eliminación fue exitosa
    assert response_delete.status_code == 200

    # 5. Verificar que el usuario ya no existe
    response_check = client.get(f"/usuarios/{user_id}")
    assert response_check.status_code == 404  # Debería devolver 404 porque el usuario fue eliminado



@pytest.fixture(scope="module")
def setup_db():
    # Configurar la base de datos en memoria
    database.connect()
    yield
    # Desconectar después de las pruebas
    database.disconnect()