# Stage 1 Imagen base con Python
FROM python:3.12.10 AS dependencias

# Establecer el directorio de trabajo
WORKDIR /app

COPY ./app ./app
COPY requirements.txt .


# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

#Stage 2 release
FROM python:3.12.10-slim AS release
WORKDIR /app
    
COPY --from=dependencias /app/requirements.txt ./
RUN pip install -r requirements.txt
COPY --from=dependencias /app/ ./
COPY newrelic.ini ./
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
ENV NEW_RELIC_CONFIG_FILE=/app/newrelic.ini




