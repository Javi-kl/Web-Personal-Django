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
from django.db import transaction
from django.views.generic.edit import FormMixin
from django_ratelimit.decorators import ratelimit

from .forms import CommentForm, ProjectImageFormSet, ProjectModelForm
from .models import Comment, ProjectModel


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser  # pyright: ignore[reportAttributeAccessIssue]


class ProjectCreateView(SuperuserRequiredMixin, CreateView):
    model = ProjectModel
    form_class = ProjectModelForm
    template_name = "projects/project_create.html"
    success_url = reverse_lazy("core:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == "POST":
            context["image_formset"] = ProjectImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=context["form"].instance,
            )
        else:
            context["image_formset"] = ProjectImageFormSet(
                instance=context["form"].instance,
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        image_formset = context["image_formset"]
        if not image_formset.is_valid():
            return self.render_to_response(context)

        form.instance.created_by = self.request.user

        with transaction.atomic():  # pyright: ignore[reportGeneralTypeIssues]
            response = super().form_valid(form)

            image_formset.instance = self.object
            image_formset.save()

        return response


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
    form_class = ProjectModelForm
    template_name = "projects/project_update.html"
    success_url = reverse_lazy("core:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["image_formset"] = ProjectImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
            )
        else:
            context["image_formset"] = ProjectImageFormSet(
                instance=self.object,
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        image_formset = context["image_formset"]
        if not image_formset.is_valid():
            return self.render_to_response(context)

        with transaction.atomic():  # pyright: ignore[reportGeneralTypeIssues]
            response = super().form_valid(form)
            image_formset.instance = self.object
            image_formset.save()

        return response


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
