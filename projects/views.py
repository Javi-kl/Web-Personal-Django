from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.db import transaction

from .forms import ProjectImageFormSet, ProjectModelForm
from .models import ProjectModel


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


class ProjectDetailView(DetailView):
    model = ProjectModel
    template_name = "projects/project_detail.html"
    context_object_name = "project"


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
