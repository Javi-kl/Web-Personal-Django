# Documentación técnica

Web-Personal-Django es un portfolio personal construido con Django. Permite publicar proyectos con contenido en Markdown e imágenes, ofrece consulta pública y restringe su administración a superusuarios.

## Funcionalidades

- Listado y detalle público de proyectos.
- Contenido Sobre mí integrado en portada.
- Descripciones de proyectos en Markdown.
- Varias imágenes asociadas a cada proyecto.
- Inicio y cierre de sesión con la autenticación de Django.
- Creación, edición y eliminación de proyectos e imágenes por superusuarios.
- Gestión adicional desde el panel de administración.

El proyecto no incluye registro público, formulario de contacto ni comentarios.

## Arquitectura

La aplicación utiliza Python 3.14, Django 6.0.5 y PostgreSQL 16. El despliegue incluido sigue este flujo:

```text
Nginx -> Gunicorn (WSGI) -> Django -> PostgreSQL
```

WhiteNoise gestiona los archivos estáticos desde Django. En la stack completa, Nginx sirve tanto los estáticos recopilados como los archivos multimedia persistentes.

| Componente | Responsabilidad |
|------------|-----------------|
| `core` | Inicio, página "Sobre mí" y autenticación. |
| `projects` | Modelos, formularios, vistas y administración del portfolio. |
| `personal_web` | Configuración global, rutas, plantillas y entradas WSGI/ASGI. |
| `static` | Hoja de estilos e imágenes propias del sitio. |
| `nginx` | Proxy inverso, terminación TLS y servicio de estáticos y media. |

## Modelo de datos

### `ProjectModel`

Representa un proyecto. Contiene título, descripción Markdown, fecha de creación, enlace opcional a GitHub, autor y prioridad de presentación. Los proyectos se ordenan por prioridad descendente y, después, por fecha.

### `ProjectImage`

Representa una imagen asociada a un proyecto. La relación usa borrado en cascada, por lo que las imágenes se eliminan junto con su proyecto.

## Rutas y permisos

| Ruta | Método | Acceso | Descripción |
|------|--------|--------|-------------|
| `/` | GET | Público | Presentación y lista los proyectos. |
| `/login/` | GET, POST | Público | Inicio de sesión. |
| `/logout/` | POST | Autenticado | Cierre de sesión. |
| `/projects/<pk>` | GET | Público | Detalle de un proyecto. |
| `/projects/create/` | GET, POST | Superusuario | Creación de proyectos e imágenes. |
| `/projects/update/<pk>` | GET, POST | Superusuario | Edición de proyectos e imágenes. |
| `/projects/delete/<pk>` | GET, POST | Superusuario | Eliminación de proyectos. |
| `/admin/` | Varios | Personal autorizado | Administración de Django. |

Los usuarios anónimos son redirigidos al login al intentar administrar proyectos. Los usuarios autenticados sin permisos de superusuario reciben una respuesta `403`.

## Configuración

La configuración se obtiene de variables de entorno mediante `python-decouple`. Puede partirse de la plantilla incluida:

```bash
cp .env.example .env
```

| Variable | Obligatoria | Descripción |
|----------|-------------|-------------|
| `SECRET_KEY` | Sí | Clave criptográfica de Django. |
| `DEBUG` | No | Activa el modo de desarrollo. Su valor por defecto es `False`. |
| `ALLOWED_HOSTS` | No | Hosts permitidos, separados por comas. |
| `POSTGRES_DB` | Sí | Nombre de la base de datos. |
| `POSTGRES_USER` | Sí | Usuario de PostgreSQL. |
| `POSTGRES_PASSWORD` | Sí | Contraseña de PostgreSQL. |
| `POSTGRES_HOST` | Sí | `localhost` en ejecución nativa o `db` dentro de Compose. |
| `POSTGRES_PORT` | Sí | Puerto de PostgreSQL, normalmente `5432`. |

PostgreSQL es el único motor de base de datos activo. Para desarrollo nativo, la base de datos y el usuario deben existir antes de ejecutar las migraciones.

## Desarrollo local

Requisitos: Git, Python 3.14, PostgreSQL y soporte para entornos virtuales.

```bash
git clone https://github.com/Javi-kl/Web-Personal-Django.git
cd Web-Personal-Django
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Ajuste las credenciales de `.env`, use `POSTGRES_HOST=localhost` y ejecute:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/`.

## Contenedores

`docker-compose.yml` define tres servicios:

| Servicio | Función |
|----------|---------|
| `db` | PostgreSQL 16 con volumen persistente. |
| `web` | Django servido por Gunicorn. |
| `nginx` | Proxy HTTPS y servicio de archivos estáticos y multimedia. |

Para desarrollo puede iniciarse únicamente `web`; Compose levantará también su dependencia `db`:

```bash
podman compose up -d --build web
podman compose exec web python manage.py migrate --noinput
podman compose exec web python manage.py collectstatic --noinput
podman compose exec web python manage.py createsuperuser
```

La aplicación quedará expuesta en `http://localhost:8000`. Con Docker, sustituya `podman` por `docker`.

Para desplegar la stack completa:

```bash
podman compose up -d --build
podman compose exec web python manage.py migrate --noinput
podman compose exec web python manage.py collectstatic --noinput
```

Las migraciones no se ejecutan automáticamente al iniciar los contenedores. La configuración de Nginx está preparada específicamente para `javikl.dev` y requiere certificados existentes en `/etc/letsencrypt`; debe adaptarse para otros dominios o entornos.

Los datos de PostgreSQL, los estáticos recopilados y los archivos multimedia se conservan en volúmenes. `podman compose down -v` elimina esos datos.

## Tests y CI

La suite utiliza el framework de tests de Django:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Los tests cubren el modelo de proyecto, las vistas públicas, autenticación, permisos del CRUD y rate limiting del login. GitHub Actions ejecuta las comprobaciones, migraciones, recopilación de estáticos y tests contra PostgreSQL 16 en cada push o pull request dirigido a `main`.

## Seguridad

- Los secretos se mantienen fuera del repositorio mediante variables de entorno.
- El CRUD de proyectos está restringido a superusuarios.
- El login limita a cinco las solicitudes POST por minuto e IP.
- Con `DEBUG=False`, Django fuerza HTTPS y habilita HSTS, cookies seguras y cabeceras de protección.
- Gunicorn se publica únicamente en la interfaz local del host dentro de Compose.

## Consideraciones operativas

- El despliegue configurado utiliza WSGI con Gunicorn; la entrada ASGI no se usa en la stack incluida.
- Los archivos multimedia requieren almacenamiento persistente y Nginx en producción.
- `collectstatic` debe ejecutarse tras cambios en archivos estáticos.
- Las migraciones deben aplicarse después de cada despliegue que modifique el esquema.
