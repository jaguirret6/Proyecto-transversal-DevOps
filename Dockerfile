# Imagen base con Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY ./app ./app
COPY ./tests ./tests
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que corre la app
EXPOSE 8000

# Comando para arrancar Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
####################################################################################


#3.12.10-slim
# ---- Base python ----
    FROM python:3.12.10 AS base
    # Create app directory
    WORKDIR /app
    
    # ---- Dependencies ----
    FROM base AS dependencies  
    COPY gunicorn_app/requirements.txt ./
    # install app dependencies
    RUN pip install -r requirements.txt
    
    # ---- Copy Files/Build ----
    FROM dependencies AS build  
    WORKDIR /app
    COPY . /app
    # Build / Compile if required
    
    # --- Release with Alpine ----
    FROM python:3.6-alpine3.7 AS release  
    # Create app directory
    WORKDIR /app
    
    COPY --from=dependencies /app/requirements.txt ./
    COPY --from=dependencies /root/.cache /root/.cache
    
    # Install app dependencies
    RUN pip install -r requirements.txt
    COPY --from=build /app/ ./
    CMD ["gunicorn", "--config", "./gunicorn_app/conf/gunicorn_config.py", "gunicorn_app:app"]