# Usar la imagen oficial de Python 3.11 como base
FROM python:3.11

# Definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo los archivos esenciales primero (para aprovechar la caché de Docker)
COPY requirements.txt ./

# Instalar dependencias en el sistema global del contenedor
RUN pip install --upgrade --no-cache-dir pip && \
    pip install --no-cache-dir -r requirements.txt

# Luego copiar el resto del código de la aplicación
COPY . .

# Comando de inicio
CMD ["reflex", "run"]


# docker build -t presupuesto:latest .

# docker run --env-file .env -d -p 3000:3000 -p 8000:8000 --name app presupuesto:latest