# Portfolio Personal - Javi-kl 
[![CI](https://github.com/Javi-kl/Web-Personal-Django/actions/workflows/ci.yml/badge.svg)](https://github.com/Javi-kl/Web-Personal-Django/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
> Portfolio web con sistema de autenticación, gestión de proyectos y comentarios.
## Stack Tecnológico
- **Django** / Python 3.14
- **PostgreSQL 16** (producción y desarrollo)
- **Gunicorn** + **Nginx** (reverse proxy con Let's Encrypt)
- **Podman** (orquestación de contenedores)
- django-markdownx (descripción de proyectos en Markdown)
- Pillow + ProjectImage (imágenes por proyecto con orden)
- django-ratelimit (protección contra abuso por IP)
- python-decouple (configuración por entorno)
## Estructura

| App | Descripción |
|-----|-------------|
| `core` | Home, Sobre mí, Contacto, Auth (login/registro/logout) |
| `projects` | Portfolio de proyectos con imágenes y comentarios |
| `personal_web` | Configuración global del proyecto (settings, urls, WSGI) |

| Modelo | App | Descripción |
|--------|-----|-------------|
| `Contact` | core | Mensajes del formulario de contacto |
| `ProjectModel` | projects | Proyectos con descripción Markdown y enlace a GitHub |
| `ProjectImage` | projects | Imágenes asociadas a proyectos (ordenadas) |
| `Comment` | projects | Comentarios de usuarios en proyectos |
### Funcionalidades:
- Portfolio de proyectos (CRUD solo para superuser)
- Múltiples imágenes por proyecto (inline formset)
- Sistema de comentarios (requiere autenticación)
- Formulario de contacto con rate limiting
- Autenticación (login/registro/logout)
## Seguridad
- Variables sensibles fuera del código (python-decouple + .env)
- Rate limiting por IP: login (5/min), registro (5/h), contacto (2/min)
- HTTPS obligatorio en producción (redirección SSL + HSTS 1 año)
- Cookies de sesión y CSRF solo sobre HTTPS
- Headers: X-Frame-Options DENY, X-Content-Type-Options nosniff, X-XSS-Protection
- SECURE_PROXY_SSL_HEADER configurado para nginx

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
