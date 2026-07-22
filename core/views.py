from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from projects.models import ProjectModel


def home(request):
    if settings.ABOUT_PATH.exists():
        content = settings.ABOUT_PATH.read_text(encoding="utf-8")
    else:
        content = "Contenido no disponible"

    context = {
        "contenido": content,
        "projects": ProjectModel.objects.all(),
    }
    return render(request, "core/home.html", context)


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
