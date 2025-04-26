from databases import Database
import sqlalchemy
from sqlalchemy import MetaData

# URL de conexión a SQLite (base en archivo local)
DATABASE_URL = "sqlite:///./test.db"  # Archivo test.db en el mismo directorio

# Objeto Database
database = Database(DATABASE_URL)

# Definición del metadata y engine
metadata = MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  # Necesario para SQLite + async
    echo=True  # Activar logs de todas las consultas SQL
)

# Tabla de usuarios
usuarios = sqlalchemy.Table(
    "usuarios",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nombre", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("edad", sqlalchemy.Integer),
    sqlalchemy.Column("color_favorito", sqlalchemy.String),
)

# Crear la tabla si no existe
metadata.create_all(engine)
