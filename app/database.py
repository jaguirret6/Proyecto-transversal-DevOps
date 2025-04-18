from databases import Database

# URL de conexión para PostgreSQL
DATABASE_URL = "postgresql://devopsdb:devopsdb@localhost:5432/devopsdb"

# Crear una instancia de la base de datos
database = Database(DATABASE_URL)
