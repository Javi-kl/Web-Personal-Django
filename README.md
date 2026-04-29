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
## Desarrollo local
```bash
git clone https://github.com/Javi-kl/Web-Personal-Django
cd Web-Personal-Django
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # editar valores
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
> Nota: Se requiere PostgreSQL local. SQLite está deshabilitado en settings.py.

## Despliegue en producción
```
git pull origin main
docker compose build web
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py collectstatic --noinput
docker compose up -d web
```
### Infraestructura: 
Nginx (proxy inverso + SSL) → Gunicorn (WSGI) → Django → PostgreSQL, cada servicio en su contenedor.
## Tests
```
python manage.py test
python manage.py test -v 2 
```
---
> Nota: Proyecto basado inicialmente en ConquerBlocks, ampliado con modelos de datos y lógica de negocio propios. 
> El frontend y la estructura de los tests se generaron con asistencia de IA, priorizando el desarrollo del backend.

---
