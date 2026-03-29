from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.views.generic.edit import FormMixin
from django_ratelimit.decorators import ratelimit

from .forms import CommentForm
from .models import Comment, ProjectModel


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProjectCreateView(SuperuserRequiredMixin, CreateView):
    model = ProjectModel
    fields = ["title", "description", "github_url", "order"]
    template_name = "projects/project_create.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProjectDetailView(DetailView, FormMixin):
    model = ProjectModel
    template_name = "projects/project_detail.html"
    context_object_name = "project"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("projects:project_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.select_related("author").all()
        return context

    @method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True))
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('core:login')}?next={request.path}")

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.project = self.object
        comment.save()
        messages.success(self.request, "Comentario publicado correctamente.")
        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdateView(SuperuserRequiredMixin, UpdateView):
    model = ProjectModel
    fields = ["title", "description", "github_url", "order"]
    template_name = "projects/project_update.html"
    success_url = reverse_lazy("core:home")


class ProjectDeleteView(SuperuserRequiredMixin, DeleteView):
    model = ProjectModel
    success_url = reverse_lazy("core:home")
    template_name = "projects/project_delete.html"


class CommentUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "projects/comment_edit.html"

    def get_success_url(self):
        messages.success(self.request, "Comentario actualizado.")
        return reverse("projects:project_detail", kwargs={"pk": self.object.project.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.object.project
        return context


class CommentDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Comment
    template_name = "projects/comment_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Comentario eliminado.")
        return reverse("projects:project_detail", kwargs={"pk": self.object.project.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.object.project
        return context
