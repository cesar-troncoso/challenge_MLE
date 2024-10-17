# syntax=docker/dockerfile:1.2

# Usa una versión específica de Python (como Python 3.11)
FROM python:3.11

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requisitos al contenedor
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
COPY requirements-test.txt requirements-test.txt

# Copiar el archivo de datos al contenedor
COPY data/data.csv data/data.csv

# Actualizar los repositorios e instalar distutils
RUN apt-get update && apt-get install -y python3-distutils

# Instalar las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
RUN pip install -r requirements-test.txt

# Asegúrate de instalar una versión específica de `anyio` si hay problemas de compatibilidad
RUN pip install anyio==3.6.2

# Copiar todo el contenido de la aplicación al contenedor
COPY . .

# Exponer el puerto si la aplicación necesita uno (por ejemplo, para la API con FastAPI)
EXPOSE 8000

# Comando por defecto para ejecutar pruebas (puedes cambiarlo según tus necesidades)
CMD ["pytest", "tests/"]
