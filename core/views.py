from pathlib import Path

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_ratelimit.decorators import ratelimit

from projects.models import ProjectModel


def home(request):
    context = {
        "projects": ProjectModel.objects.all(),
    }
    return render(request, "core/home.html", context)


class AboutView(TemplateView):
    template_name = "core/about_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_path = Path(__file__).parent.parent / "about.md"
        if about_path.exists():
            context["contenido"] = about_path.read_text()
        else:
            context["contenido"] = "Contenido no disponible."
        return context


@method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True), name="dispatch")
class UserLoginView(LoginView):
    template_name = "core/login.html"

    def form_valid(self, form):
        messages.success(self.request, f"Bienvenido {form.get_user().username}")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = "core:home"

    def post(self, request, *args, **kwargs):
        messages.success(request, "Has cerrado sesión.")
        return super().post(request, *args, **kwargs)
