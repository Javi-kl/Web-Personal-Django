from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from projects.models import ProjectModel

from .forms import ContactForm


def home(request):
    context = {
        "projects": ProjectModel.objects.all(),
    }
    return render(request, "core/home.html", context)


class AboutView(TemplateView):
    template_name = "core/about_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Sobre mí"
        return context


class UserLoginView(LoginView):
    template_name = "core/login.html"
    success_url = "/"


class UserLogoutView(LogoutView):
    next_page = "core:home"

    def post(self, request, *args, **kwargs):
        messages.success(request, "Has cerrado sesión.")
        return super().post(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = "core/register.html"
    form_class = UserCreationForm
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("core:home"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ContactFormView(FormView):
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("core:contact")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Mensaje enviado correctamente.")
        return super().form_valid(form)
