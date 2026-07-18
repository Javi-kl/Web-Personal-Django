from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField


class ProjectModel(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)
    description = MarkdownxField(verbose_name="Descripción", default="")
    created_at = models.DateTimeField(verbose_name="Fecha y hora de creación", default=timezone.now)
    objects = models.Manager()

    github_url = models.URLField(verbose_name="GitHub", blank=True, null=True)

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    order = models.PositiveIntegerField(verbose_name="Orden", default=0, blank=True)  # pyright: ignore[reportArgumentType]

    class Meta:
        ordering = ["-order", "-created_at"]
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self) -> str:
        return str(self.title)


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
        verbose_name="Orden",
        default=0,  # pyright: ignore[reportArgumentType]
        help_text="Orden de aparición (0 = principal)",
    )

    class Meta:
        verbose_name = "Imagen del proyecto"
        verbose_name_plural = "Imágenes del proyecto"

    def __str__(self) -> str:
        return f"Imagen de {self.project}"
