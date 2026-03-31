# Portfolio Personal - Javi-kl 
> Portfolio web con sistema de autenticación, gestión de proyectos y comentarios.
## Stack Tecnológico
| Capa | Tecnología |
|------|------------|
| Framework | Django 6.0.2 |
| Lenguaje | Python 3.14 |
| Base de datos | SQLite3 |
| Markdown | markdownx 4.0.9 |
| Imágenes | Django Thumbnails + Pillow | 

## Estructura
### Apps:
- core - Home, About, Contacto, Auth (login/registro)
- projects - Portfolio de proyectos con comentarios
- personal_web - Configuración del proyecto
### Modelos:
- Contact - Formulario de contacto
- ProjectModel - Proyectos con (imagen -> deshabilitadas temporalmente) y descripción markdown
- Comment - Comentarios de usuarios en proyectos
### Funcionalidades:
- Portfolio de proyectos (CRUD solo para superuser)
- Sistema de comentarios (requiere autenticación)
- Formulario de contacto
- Autenticación básica (login/registro)


## Quick Start
```bash
git clone https://github.com/Javi-kl/Web-Personal-Django
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Roadmap
- [x] Sistema de contacto
- [x] App de proyectos/portfolio
- [x] Comentarios
- [x] Tests unitarios
- [x] Despliegue en producción

## Notas

Desarrollado a partir de base ConquerBlocks, extendido con modelos y 
lógica propios. IA usada para frontend y tests base.

---
