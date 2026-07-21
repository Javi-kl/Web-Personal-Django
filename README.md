# Portfolio personal - Javi-kl

[![CI](https://github.com/Javi-kl/Web-Personal-Django/actions/workflows/ci.yml/badge.svg)](https://github.com/Javi-kl/Web-Personal-Django/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0.5-green.svg)](https://www.djangoproject.com/)

Portfolio web desarrollado con Django para presentar y administrar proyectos personales.

## Stack tecnológico

- **Python 3.14** y **Django 6.0.5**
- **PostgreSQL 16**
- **MarkdownX** y **Pillow** para contenidos e imágenes
- **Gunicorn**, **Nginx** y **WhiteNoise** para producción
- **Docker/Podman Compose** para la ejecución en contenedores

## Estructura

| App | Descripción |
|-----|-------------|
| `core` | Página principal, sección "Sobre mí" y autenticación |
| `projects` | Consulta y administración de proyectos e imágenes |
| `personal_web` | Configuración global, rutas, plantillas y despliegue WSGI/ASGI |

| Modelo | App | Descripción |
|--------|-----|-------------|
| `ProjectModel` | `projects` | Proyecto con descripción Markdown y enlace opcional a GitHub |
| `ProjectImage` | `projects` | Imagen asociada a un proyecto |

## Funcionalidades

- Listado y detalle público de proyectos
- Descripciones en Markdown y galerías de imágenes
- Inicio y cierre de sesión
- CRUD de proyectos e imágenes restringido a superusuarios
- Gestión desde el panel de administración de Django

## Seguridad

- Configuración y secretos mediante variables de entorno
- Operaciones administrativas restringidas a superusuarios
- Rate limiting del login: 5 intentos por minuto e IP
- Redirección HTTPS, HSTS, cookies seguras y cabeceras de protección en producción

## Iniciar la aplicación

Se requieren Git, Python, Docker/Podman(Si usas Docker, solo cambia el nombre en los comandos).

### Preparación inicial

```bash
git clone https://github.com/Javi-kl/Web-Personal-Django.git
cd Web-Personal-Django

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

Genera una clave para Django:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Configuración común de `.env`:

```dotenv
SECRET_KEY=pega-aqui-la-clave-generada

POSTGRES_DB=portfolio_db
POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=contraseña-segura
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Para desarrollo local:

```dotenv
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Para producción:

```dotenv
DEBUG=False
ALLOWED_HOSTS=javikl.dev,www.javikl.dev
```

### Levantar los servicios

Desarrollo local:

```bash
podman compose up -d --build web
```

Producción:

```bash
podman compose up -d --build
```

Después de la primera puesta en marcha, tanto en desarrollo como en producción:

```bash
podman compose exec web python manage.py migrate --noinput
podman compose exec web python manage.py collectstatic --noinput
```

Si la base de datos es nueva:

```bash
podman compose exec web python manage.py createsuperuser
```

En desarrollo, la aplicación estará disponible en:

```text
http://localhost:8000
```

### Flujo de desarrollo

Después de modificar código Python:

```bash
podman compose restart web
```

Si modificas los modelos, genera las migraciones:

```bash
podman compose exec web python manage.py makemigrations
podman compose exec web python manage.py migrate
```

Ejecutar los tests:

```bash
podman compose exec web python manage.py test
```

### Actualizar producción

```bash
git pull origin main
podman compose up -d --build
podman compose exec web python manage.py migrate --noinput
podman compose exec web python manage.py collectstatic --noinput
```

### Comandos útiles

```bash
podman compose ps
podman compose logs -f
podman compose down
```

Los datos permanecen almacenados en los volúmenes. No utilices `podman compose down -v` salvo que quieras eliminarlos.

### Infraestructura: 
Nginx (proxy inverso + SSL) → Gunicorn (WSGI) → Django → PostgreSQL, cada servicio en su contenedor.

---

> Nota: Proyecto basado inicialmente en una practica de ConquerBlocks, ampliado con modelos de datos y lógica de negocio propios. 
> El frontend y la estructura de los tests se generaron con asistencia de IA, priorizando el desarrollo del backend.

---
