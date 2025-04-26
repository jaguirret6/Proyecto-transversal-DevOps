from databases import Database
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy import event
import logging









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

# ————— Configuración común de logging —————
file_handler = logging.FileHandler("db_queries.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
)

# —–– Logger para SQLAlchemy Core/ORM —––—
sqla_logger = logging.getLogger("sqlalchemy.engine")
sqla_logger.setLevel(logging.DEBUG)
sqla_logger.addHandler(file_handler)

# —–– Logger para la librería `databases` (async) —––—
dbs_logger = logging.getLogger("databases")
dbs_logger.setLevel(logging.DEBUG)
dbs_logger.addHandler(file_handler)

# … tu engine, metadata, tablas, etc …

# Callback para capturar SQLAlchemy Core/ORM (opcional)
def log_query(conn, cursor, statement, parameters, context, executemany):
    # usa el logger de sqlalchemy.core
    sqla_logger.debug(f"Ejecutando consulta: {statement} — params: {parameters}")

# Conecta el callback sólo al engine, si lo necesitas
event.listen(engine, "before_cursor_execute", log_query)





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
