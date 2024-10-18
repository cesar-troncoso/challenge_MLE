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
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
RUN pip install -r requirements-test.txt
RUN pip install anyio==3.6.2

# Copiar solo el archivo de datos (esto puede cambiar con frecuencia)
COPY data/data.csv data/data.csv

# Copiar el resto de los archivos de la aplicación (código fuente)
COPY . .

# Exponer el puerto si la aplicación necesita uno (por ejemplo, para la API con FastAPI)
EXPOSE 8000

# Comando por defecto para ejecutar pruebas (puedes cambiarlo según tus necesidades)
CMD ["pytest", "tests/"]
