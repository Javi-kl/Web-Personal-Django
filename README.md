# Portfolio Personal - Javi-kl 
> Portfolio web con sistema de autenticación, gestión de proyectos y comentarios.
## Stack Tecnológico
- **Django 6.0.2** / Python 3.14
- **PostgreSQL 16** (producción) / SQLite3 (desarrollo)
- **Gunicorn** + **Nginx** (reverse proxy con Let's Encrypt)
- **Podman** (docker-compose compatible)
- django-markdownx (descripción de proyectos en Markdown)
- Pillow + ProjectImage (imágenes por proyecto con orden)
- django-ratelimit
- python-decouple (configuración por entorno)
## Estructura
### Apps:
- core - Home, About, Contacto, Auth (login/registro)
- projects - Portfolio de proyectos con imágenes y comentarios
- personal_web - Configuración del proyecto
### Modelos:
- Contact - Formulario de contacto
- ProjectModel - Proyectos con descripción markdown y enlace a GitHub
- ProjectImage - Imágenes asociadas a proyectos (ordenadas)
- Comment - Comentarios de usuarios en proyectos
### Funcionalidades:
- Portfolio de proyectos (CRUD solo para superuser)
- Múltiples imágenes por proyecto (inline formset)
- Sistema de comentarios (requiere autenticación)
- Formulario de contacto
- Autenticación (login/registro)
## Seguridad
- Variables sensibles fuera del código (python-decouple + .env)
- Rate limiting por IP: login (5/min), registro (5/h), contacto (2/min), comentarios (5/min)
- HTTPS obligatorio en producción (redirección SSL + HSTS)
- Cookies de sesión y CSRF solo sobre HTTPS
- Headers: X-Frame-Options DENY, X-Content-Type-Options, X-XSS-Protection
## Desarrollo local
```bash
git clone https://github.com/Javi-kl/Web-Personal-Django
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # editar valores
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Despliegue en producción
cp .env.example .env.production   # configurar con valores reales
podman-compose up -d
Infraestructura: Nginx (proxy inverso + SSL), Gunicorn (WSGI), PostgreSQL — cada servicio en su contenedor.
Roadmap
- [x] Sistema de contacto
- [x] App de proyectos/portfolio
- [x] Comentarios
- [x] Tests unitarios
- [x] Despliegue en producción
- [x] Imágenes por proyecto
Notas
Proyecto basado inicialmente en ConquerBlocks, ampliado con modelos de datos y lógica de negocio propios. El frontend y la estructura de los tests se generaron con asistencia de IA, priorizando el desarrollo del backend.
---