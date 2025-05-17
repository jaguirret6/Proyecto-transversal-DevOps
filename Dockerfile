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

RUN pip install newrelic
COPY newrelic.ini .

COPY --from=dependencias /app/requirements.txt ./
RUN pip install -r requirements.txt
COPY --from=dependencias /app/ ./
EXPOSE 8000
CMD ["newrelic-admin", "run-program", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




