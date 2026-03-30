# Documentación completa del proyecto Web-Personal-Django

## Resumen del proyecto

Este repositorio contiene un portfolio personal en Django con autenticación básica, gestión de proyectos y sistema de comentarios. El proyecto está preparado para ejecución local y despliegue en producción con PostgreSQL, Gunicorn, Nginx y gestión de estáticos con Whitenoise.

## Stack tecnológico y arquitectura

La aplicación está construida sobre Django 6.0.2 y Python 3.14, utilizando PostgreSQL como base de datos por defecto en `settings.py`. Se usan dependencias adicionales como `django-markdownx` para contenidos en Markdown, `gunicorn` como servidor WSGI en producción, `psycopg2-binary` para PostgreSQL y `whitenoise` para servir estáticos.

### Componentes principales

- `personal_web`: configuración global del proyecto (settings, urls, context processors, WSGI/ASGI).
- `core`: home, página "sobre mí", formulario de contacto y autenticación (login, registro, logout).
- `projects`: CRUD de proyectos de portfolio y sistema de comentarios asociado.

## Estructura del repositorio

Principales archivos y directorios en la raíz del proyecto:

| Elemento | Descripción |
|---------|-------------|
| `manage.py` | Punto de entrada de comandos de Django. |
| `personal_web/` | Configuración del proyecto, `settings.py`, `urls.py`, `context_processor.py`, `wsgi.py`, `asgi.py`. |
| `core/` | Vistas, URLs, formularios, modelos y tests para home, contacto y auth. |
| `projects/` | Vistas, URLs, modelos, formularios y tests de proyectos y comentarios. |
| `static/` | CSS (`matrix_theme.css`), JS (`matrix-rain.js`) e imágenes (avatar). |
| `Dockerfile` | Definición de la imagen Docker con Gunicorn y collectstatic en build. |
| `docker-compose.yml` | Orquestación de contenedores para DB, app web y Nginx. |
| `nginx/nginx.conf` | Reverse proxy hacia Gunicorn y servido de estáticos/media. |
| `.env.example` | Plantilla de variables de entorno. |
| `requirements.txt` | Lista de dependencias Python. |
| `AGENTS.md` | Guía de estilo y comandos rápidos orientada a agentes de IA. |

## Modelos de datos

### Contact (app `core`)

El modelo `Contact` representa mensajes enviados desde el formulario de contacto, con campos `nombre` opcional, `email`, `comentario`, un `created_at` automático y un booleano `contactado` para seguimiento. Está ordenado por fecha de creación descendente y se muestra en formato `email - fecha` en su método `__str__`.

### ProjectModel y Comment (app `projects`)

`ProjectModel` almacena proyectos del portfolio con título, descripción en Markdown (`MarkdownxField`), fecha de creación, URL de GitHub opcional, usuario creador (`created_by`) y un campo `order` para ordenar manualmente.
`Comment` representa comentarios asociados a un proyecto y a un usuario (`author`), con contenido de hasta 1000 caracteres y timestamp de creación.

## Rutas y navegación

### URLs globales

El fichero `personal_web/urls.py` incluye:

- `/` → rutas de `core` (home, sobre mí, contacto, auth).
- `/projects/` → rutas de `projects` (detalle, creación, edición, borrado de proyectos y comentarios).
- `/admin/` → panel de administración de Django.
- `/markdownx/` → endpoints internos de `django-markdownx`.

### Rutas de `core`

En `core/urls.py` se definen:

- `/` → `home`, listado de proyectos recientes en la página principal.
- `/sobre-nosotros/` → `AboutView`, página "Sobre mí".
- `/contacto/` → `ContactFormView`, formulario de contacto.
- `/registro/` → `RegisterView`, formulario de creación de usuario.
- `/login/` → `UserLoginView`, login con `AuthenticationForm`.
- `/logout/` → `UserLogoutView`, cierre de sesión.

### Rutas de `projects`

En `projects/urls.py` se definen:

- `/projects/<int:pk>` → `ProjectDetailView`, detalle del proyecto y comentarios.
- `/projects/create/` → `ProjectCreateView`, creación de proyecto (solo superusuario).
- `/projects/update/<int:pk>` → `ProjectUpdateView`, edición de proyecto (solo superusuario).
- `/projects/delete/<int:pk>` → `ProjectDeleteView`, borrado de proyecto (solo superusuario).
- `/projects/comments/<int:pk>/edit/` → `CommentUpdateView`, edición de comentario (solo superusuario).
- `/projects/comments/<int:pk>/delete/` → `CommentDeleteView`, borrado de comentario (solo superusuario).

## Lógica de vistas y permisos

La home carga todos los proyectos (`ProjectModel.objects.all()`) y los pasa al template `core/home.html`. La página "Sobre mí" usa un `TemplateView` con un contexto mínimo (`titulo`).

Las vistas de autenticación usan vistas genéricas de Django (`FormView` para registro, `LoginView` para login, `LogoutView` para logout) con mensajes flash en castellano. El formulario de contacto utiliza un `FormView` que guarda el `Contact` y muestra un mensaje de éxito.

En `projects`, las vistas de creación, actualización y borrado heredan de `UserPassesTestMixin` a través de `SuperuserRequiredMixin`, de forma que solo un superusuario puede acceder a ellas (403 para otros usuarios autenticados). `ProjectDetailView` mezcla `DetailView` con `FormMixin` para permitir crear comentarios desde la página de detalle y redirigir a login si el usuario no está autenticado.

## Context processors y layout

El `context_processor.get_avatar` inyecta en todas las plantillas la variable `site_avatar` apuntando a `/static/img/avatar.jpeg`. El layout base (`layout_base.html`) incluye un canvas con efecto "matrix rain" usando el JS `matrix-rain.js` y carga el CSS `matrix_theme.css` desde `static`.

## Requisitos previos

- Python 3.14 instalado en el sistema.
- PostgreSQL accesible (local o en contenedor) si se quiere usar la configuración de producción por defecto en `settings.py`.
- `pip` y `venv` para gestionar el entorno virtual.
- Opcional: Docker/Podman y docker-compose/podman-compose para ejecutar la stack contenedorizada.

## Variables de entorno y configuración

El proyecto usa `python-decouple` para leer la configuración desde variables de entorno o ficheros `.env`. El `.env.example` documenta las principales variables:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django (cambiar en producción). | `django-insecure-cambiar-esto-en-produccion` |
| `DEBUG` | Activa modo debug (solo en desarrollo). | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos separados por comas. | `localhost,127.0.0.1` |
| `POSTGRES_DB` | Nombre de la base de datos PostgreSQL. | `portfolio_db` |
| `POSTGRES_USER` | Usuario de la base de datos. | `portfolio_user` |
| `POSTGRES_PASSWORD` | Password de la base de datos. | `cambia-esto` |
| `POSTGRES_HOST` | Host de la base de datos (`db` en Docker). | `.` o `db` |
| `POSTGRES_PORT` | Puerto PostgreSQL. | `5432` |

En `settings.py` la sección `DATABASES` está configurada para usar PostgreSQL leyendo estas variables, y ya no se usa SQLite (comentado).

## Puesta en marcha en local (sin contenedores)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Javi-kl/Web-Personal-Django
cd Web-Personal-Django
```

Esto coincide con el `Quick Start` ya incluido en el README del proyecto.

### 2. Crear y activar entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows PowerShell
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instalará Django 6.0.2, markdownx, Gunicorn, Whitenoise, psycopg2-binary, etc.

### 4. Configurar variables de entorno

Crear un fichero `.env` en la raíz del proyecto copiando desde `.env.example` y ajustando los valores mínimos:

```bash
cp .env.example .env
```

Para usar una base de datos PostgreSQL local:

```env
SECRET_KEY=pon-aqui-una-clave-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=portfolio_db
POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=portfolio_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Crear base de datos y usuario (PostgreSQL)

Ejemplo en Linux con usuario postgres:

```bash
sudo -u postgres psql
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'portfolio_pass';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
\q
```

Asegurarse de que `POSTGRES_*` en `.env` coincide con estos valores.

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

Esto creará las tablas para `auth`, `core.Contact`, `projects.ProjectModel` y `projects.Comment`, entre otras.

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

El README ya documenta este paso dentro del bloque de Quick Start.

### 8. Levantar el servidor de desarrollo

```bash
python manage.py runserver
```

La web estará accesible en `http://127.0.0.1:8000/` con estáticos servidos por Django (DEBUG=True).

## Ejecución de tests

El proyecto incluye tests para el formulario de contacto (`core`) y para modelos y vistas de `projects`.

- Para ejecutar todos los tests:

```bash
python manage.py test
```

- Para ejecutar tests de una app concreta:

```bash
python manage.py test core
python manage.py test projects
```

`ContactFormTest` valida que el formulario de contacto guarda los datos y marca `contactado=False` por defecto. `ProjectModelTest` y `CommentModelTest` validan la creación y representación de proyectos y comentarios, y `Project*ViewTest` comprueba que solo superusuarios pueden acceder a las vistas de creación, edición y borrado.

## Puesta en marcha con Docker/Podman (stack completa)

El fichero `docker-compose.yml` orquesta tres servicios: base de datos PostgreSQL (`db`), aplicación Django con Gunicorn (`web`) y Nginx como reverse proxy (`nginx`).

### 1. Preparar `.env`

Asegurarse de que `.env` contiene valores coherentes para `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` y `ALLOWED_HOSTS` (por ejemplo, el dominio o IP pública si se va a exponer el servicio).

### 2. Levantar la stack

Con Podman (recomendado en los comentarios del archivo):

```bash
podman-compose up -d
```

Con Docker clásico:

```bash
docker compose up -d
```

- `db`: usa la imagen `postgres:16-alpine`, con healthcheck `pg_isready` y volumen persistente `postgres_data`.
- `web`: construye la imagen desde el `Dockerfile`, ejecuta Gunicorn en el puerto 8000 y monta volúmenes para el código fuente y los estáticos recopilados.
- `nginx`: expone los puertos 80 y 443, monta `nginx.conf` y el volumen de estáticos `static_volume`.

### 3. Comprobación de servicios

Usar:

```bash
podman ps   # o docker ps
```

Verificar que `portfolio-postgres`, `portfolio-web` y `portfolio-nginx` están en estado `running` y que `db` está `healthy`.

La aplicación quedará accesible en el puerto 80 del host (`http://localhost/` si se ejecuta en local).

## Detalle de Dockerfile (build de la imagen)

El `Dockerfile` usa `python:3.14-slim-bookworm` como base, instala dependencias del sistema (`libpq-dev`, `gcc`), copia `requirements.txt` y las dependencias Python, y luego copia el código fuente.

Durante el build se ejecuta `collectstatic` con `SECRET_KEY` y `DEBUG` de build temporales y `manage.py collectstatic --noinput`, lo que genera los estáticos en `staticfiles` listos para ser servidos por Whitenoise/Nginx. El `CMD` por defecto arranca Gunicorn en `0.0.0.0:8000` usando el módulo WSGI del proyecto.

## Configuración de Nginx

`nginx/nginx.conf` define un `upstream django` apuntando al contenedor `web:8000` y un `server` que escucha en el puerto 80.

- `/static/` se sirve desde `/app/staticfiles/` con headers de caché de un año y `Cache-Control: public`.
- `/media/` se sirve desde `/app/media/`.
- `/` se proxifica a `http://django`, con headers `Host`, `X-Real-IP`, `X-Forwarded-For` y `X-Forwarded-Proto` configurados correctamente.
- Se incluye `mime.types` para que los tipos de archivo (CSS, JS, etc.) se sirvan correctamente.

Para producción real, es necesario cambiar `server_name tu-dominio.com www.tu-dominio.com` por el dominio real y configurar certificados TLS (por ejemplo, con Let’s Encrypt).

## Gestión de estáticos y seguridad

En `settings.py` se configuran `STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT` y la integración con Whitenoise mediante `WhiteNoiseMiddleware` en `MIDDLEWARE` y la sección `STORAGES` con `CompressedManifestStaticFilesStorage` para empaquetado y versionado de estáticos.

Cuando `DEBUG=False`, se activa una sección de seguridad que fuerza HTTPS (`SECURE_SSL_REDIRECT=True`), marca las cookies como seguras, habilita HSTS durante un año e incluye cabeceras adicionales como `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER` y `X_FRAME_OPTIONS='DENY'`.

## Historial de cambios (a partir de los commits)

El historial de commits muestra la evolución desde un blog inicial hasta el portfolio actual basado en proyectos:

- Inicio del proyecto con una app de blog, vistas basadas en funciones y características como descarga de archivos y thumbnails.
- Migración progresiva a vistas basadas en clases, limpieza de apps redundantes y eliminación completa de la app `blog` (commit con `feat!: eliminar blog app BREAKING CHANGE`).
- Introducción de la app `projects` con CRUD completo y posterior refactor para exigir superusuario en todas las operaciones administrativas sobre proyectos.
- Añadido de campos `github_url` y `order` a `ProjectModel` y creación de la sección de comentarios con `Comment`.
- Incorporación de tests de seguridad para comprobar que solo superusuarios pueden acceder a vistas sensibles.
- Preparación del despliegue: creación de `.env.example`, limpieza de dependencias de desarrollo (debug toolbar, extensions), actualización del README y migración de SQLite a PostgreSQL con configuración de `STORAGES`, Gunicorn y cabeceras de seguridad.
- Creación del `Dockerfile`, actualización de `docker-compose.yml` y adición de `nginx.conf` para una stack de producción validada.

## Notas de estilo de código y herramientas recomendadas

`AGENTS.md` define guías de estilo como longitud máxima de línea 119, indentación de 4 espacios, convención de nombres (PascalCase para modelos, snake_case para funciones/variables, UPPER_SNAKE_CASE para constantes) y ejemplos de patrones para modelos, admin y vistas.

También recomienda herramientas adicionales como `black`, `isort`, `ruff`, `mypy + django-stubs` y `pytest-django` para mejorar la calidad del código, así como una tabla de referencia rápida de comandos de Django (`runserver`, `test`, `makemigrations`, `migrate`, `check`).

## Flujo recomendado de trabajo en un proyecto similar

Tomando este repositorio como ejemplo, una documentación "completa de principio a fin" debería cubrir:

1. **Resumen y objetivos del proyecto** (qué resuelve, para quién va dirigido).
2. **Stack tecnológico y arquitectura** (framework, lenguaje, BD, servicios externos).
3. **Estructura de carpetas y componentes** (apps Django, directorios clave, dónde vive cada cosa).
4. **Modelos de datos y relaciones** (diagramas o descripciones breves de modelos importantes).
5. **Rutas y vistas** (tabla de URLs clave con descripción y permisos).
6. **Requisitos previos y dependencias** (versiones mínimas, sistema operativo, herramientas adicionales).
7. **Configuración de entorno** (.env, variables críticas, modos desarrollo/producción).
8. **Puesta en marcha en local** (paso a paso reproducible desde `git clone` hasta `runserver`).
9. **Ejecución de tests** (qué tests hay, cómo ejecutarlos y qué cubren).
10. **Despliegue** (con y sin contenedores, reverse proxy, certificados, backups de BD).
11. **Seguridad** (auth, permisos, cabeceras, secretos, configuración HTTPS).
12. **Historial de cambios y roadmap** (resumen de commits importantes, tareas pendientes).
13. **Guía de contribución** (flujo de ramas, estilo, cómo abrir PRs/tests necesarios).

Este repositorio ya cubre muchos de estos puntos en código y configuración; la documentación aquí propuesta los hace explícitos y reutilizables para un entorno profesional.