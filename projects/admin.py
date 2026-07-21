from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import ProjectImage, ProjectModel


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    fields = ("image", "order")


@admin.register(ProjectModel)
class ProjectResource(MarkdownxModelAdmin):
    model = ProjectModel
    list_display = ("pk", "title", "order", "created_at")
    ordering = ("order", "created_at")
    editable_list = ["order"]
    inlines = [ProjectImageInline]
