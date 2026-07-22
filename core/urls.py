from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    home,
)

app_name = "core"
urlpatterns = [
    path("", home, name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
