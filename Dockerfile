# Usa una imagen base pequeña para que sea rápido de construir
FROM alpine:3.17

# Añade un simple archivo de texto para verificar que el build funciona
RUN echo "Hello, world!" > /hello.txt

# Establece el comando por defecto al iniciar el contenedor
CMD ["cat", "/hello.txt"]
