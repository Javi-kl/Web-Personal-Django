from typing import cast

from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse

from projects.models import ProjectModel

User = get_user_model()


class PublicViewTest(TestCase):
    def test_home_displays_projects(self):
        ProjectModel.objects.create(
            title="Proyecto visible",
            description="Descripción",
        )
        response = cast(
            HttpResponse,
            self.client.get(
                reverse("core:home"),
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "core/home.html",
        )
        self.assertContains(
            response,
            "Proyecto visible",
        )


class AuthenticationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.login_url = reverse("core:login")
        self.logout_url = reverse("core:logout")
        self.home_url = reverse("core:home")

    def test_superuser_can_log_in(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "admin",
                "password": "admin123",
            },
        )
        self.assertRedirects(
            response,
            self.home_url,
        )
        self.assertEqual(
            self.client.session.get(SESSION_KEY),
            str(self.user.pk),
        )

    def test_authenticated_user_can_logout(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.logout_url,
        )
        self.assertRedirects(
            response,
            self.home_url,
        )
        self.assertNotIn(
            SESSION_KEY,
            self.client.session,
        )
