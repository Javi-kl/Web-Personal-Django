# IMAGEN BASE
FROM python:3.14-slim-bookworm

# VARIABLES DE ENTORNO
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# DEPENDENCIAS DEL SISTEMA
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# CREAR USUARIO SIN PRIVILEGIOS
RUN useradd --create-home --uid 1000 --shell /bin/bash appuser

# DIRECTORIO DE TRABAJO
WORKDIR /app

# DEPENDENCIAS PYTHON
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# CÓDIGO FUENTE
COPY . .

# PREPARAR USUARIO SIN PRIVILEGIOS
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R appuser:appuser /app/staticfiles /app/media
    
USER appuser

# ARCHIVOS ESTÁTICOS
RUN SECRET_KEY=build-time-secret DEBUG=False python manage.py collectstatic --noinput

# PUERTO EXPUESTO
EXPOSE 8000

# COMANDO DE INICIO
CMD ["gunicorn", "personal_web.wsgi:application", "--bind", "0.0.0.0:8000"]
