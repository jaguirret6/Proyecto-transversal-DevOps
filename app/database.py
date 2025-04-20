from databases import Database
import sqlalchemy
from sqlalchemy import MetaData

# URL de conexión a PostgreSQL
DATABASE_URL = "postgresql://devopsdb:devopsdb@localhost:5432/devopsdb"

# Objeto Database
database = Database(DATABASE_URL)

# Definición del metadata y engine
metadata = MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)

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
