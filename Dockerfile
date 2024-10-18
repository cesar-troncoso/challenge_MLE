# syntax=docker/dockerfile:1.2

# Usa una versión específica de Python (como Python 3.11)
FROM python:3.11

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requisitos al contenedor primero (esto cambia con menos frecuencia)
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
COPY requirements-test.txt requirements-test.txt

# Instalar las dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt && \
    pip install -r requirements-test.txt && \
    pip install anyio==3.6.2

# Copiar el archivo de datos
COPY data/data.csv data/data.csv

# Copiar el resto de los archivos de la aplicación (código fuente)
COPY . .

# Exponer el puerto para la API con FastAPI
EXPOSE 8000

# Comando por defecto para ejecutar la API
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8000"]
