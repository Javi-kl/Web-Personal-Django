from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField


class Comment(models.Model):
    project = models.ForeignKey(
        "ProjectModel",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Proyecto",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Autor",
    )
    content = models.TextField(
        verbose_name="Contenido",
        max_length=1000,
    )
    created_at = models.DateTimeField(
        verbose_name="Fecha de creación",
        default=timezone.now,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

    def __str__(self) -> str:
        return f"{self.author.username}: {self.content[:50]}..."


class ProjectModel(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)
    description = MarkdownxField(verbose_name="Descripción", default="")
    created_at = models.DateTimeField(
        verbose_name="Fecha y hora de creación", default=timezone.now
    )

    github_url = models.URLField(verbose_name="GitHub", blank=True, null=True)

    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    order = models.PositiveIntegerField(verbose_name="Orden", default=0, blank=True)

    class Meta:
        ordering = ["-order", "-created_at"]
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self) -> str:
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        ProjectModel,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Proyecto",
    )
    image = models.ImageField(
        verbose_name="Imagen",
        upload_to="projects/images/",
    )

    order = models.PositiveIntegerField(
        verbose_name="Orden", default=0, help_text="Orden de aparición (0 = principal)"
    )

    class Meta:
        verbose_name = "Imagen del proyecto"
        verbose_name_plural = "Imágenes del proyecto"

    def __str__(self) -> str:
        return f"Imagen de {self.project.title}"
