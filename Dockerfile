# Stage 1 Imagen base con Python
FROM python:3.12.10 AS dependencias

WORKDIR /app
# Copiar archivos del proyecto y listado de dependencias
COPY ./app ./app
COPY requirements.txt .
# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2 release
FROM python:3.12.10-slim AS release
WORKDIR /app

# Copiar configfile de new relic
COPY newrelic.ini .
# Copiar dependencias instaladas en stage previo
COPY --from=dependencias /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencias /usr/local/bin /usr/local/bin
COPY --from=dependencias /app/ ./

EXPOSE 8000
# Variable de entorno para config file de new relic
ENV NEW_RELIC_CONFIG_FILE=newrelic.ini
# Comando de ejecución
CMD ["newrelic-admin", "run-program", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


