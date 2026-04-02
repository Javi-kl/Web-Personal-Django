from django.urls import path

from .views import (
    AboutView,
    ContactFormView,
    RegisterView,
    UserLoginView,
    UserLogoutView,
    home,
)

app_name = "core"
urlpatterns = [
    path("", home, name="home"),
    path("sobre-mi/", AboutView.as_view(), name="about_me"),
    path("contacto/", ContactFormView.as_view(), name="contact"),
    path("registro/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
