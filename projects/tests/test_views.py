from typing import cast

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from projects.models import ProjectModel


User = get_user_model()


class ProjectViewTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.normal_user = User.objects.create_user(
            username="normal",
            password="normal123",
        )
        self.project = ProjectModel.objects.create(
            title="Proyecto original",
            description="Descripción original",
        )
        self.create_url = reverse("projects:project_create")
        self.detail_url = reverse(
            "projects:project_detail",
            kwargs={"pk": self.project.pk},
        )
        self.update_url = reverse(
            "projects:project_update",
            kwargs={"pk": self.project.pk},
        )
        self.delete_url = reverse(
            "projects:project_delete",
            kwargs={"pk": self.project.pk},
        )

        self.crud_urls = [
            self.create_url,
            self.update_url,
            self.delete_url,
        ]

    def project_form_data(self, **overrides):
        data = {
            "title": "Proyecto nuevo",
            "description": "Descripción del proyecto",
            "github_url": "",
            "order": 0,
            "images-TOTAL_FORMS": 3,
            "images-INITIAL_FORMS": 0,
            "images-MIN_NUM_FORMS": 0,
            "images-MAX_NUM_FORMS": 1000,
            "images-0-order": "0",
            "images-1-order": "0",
            "images-2-order": "0",
        }
        data.update(overrides)
        return data

    def test_project_detail_displays_project(self):
        response = cast(HttpResponse, self.client.get(self.detail_url))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "projects/project_detail.html",
        )
        self.assertContains(
            response,
            self.project.title,
        )

    def test_project_detail_rejects_post(self):
        response = cast(HttpResponse, self.client.post(self.detail_url))

        self.assertEqual(response.status_code, 405)

    def test_anonymous_user_cannot_modify_projects(self):
        for url in self.crud_urls:
            with self.subTest(url=url):
                response = cast(HttpResponse, self.client.post(url))
                self.assertEqual(response.status_code, 302)

    def test_normal_user_cannot_modify_projects(self):
        self.client.force_login(self.normal_user)
        for url in self.crud_urls:
            with self.subTest(url=url):
                response = cast(HttpResponse, self.client.post(url))
                self.assertEqual(response.status_code, 403)

    def test_superuser_can_access_project_crud(self):
        self.client.force_login(self.superuser)
        for url in self.crud_urls:
            with self.subTest(url=url):
                response = cast(HttpResponse, self.client.get(url))
                self.assertEqual(response.status_code, 200)

    def test_superuser_can_create_project(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            self.create_url,
            self.project_form_data(
                title="Proyecto creado",
            ),
        )

        self.assertRedirects(
            response,
            reverse("core:home"),
        )
        project = ProjectModel.objects.get(
            title="Proyecto creado",
        )
        self.assertEqual(
            project.created_by,
            self.superuser,
        )

    def test_superuser_can_update_project(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            self.update_url,
            self.project_form_data(
                title="Proyecto actualizado",
            ),
        )
        self.assertRedirects(
            response,
            reverse("core:home"),
        )
        self.project.refresh_from_db()
        self.assertEqual(
            self.project.title,
            "Proyecto actualizado",
        )

    def test_superuser_can_delete_project(self):
        self.client.force_login(self.superuser)
        project_pk = self.project.pk

        response = self.client.post(
            self.delete_url,
        )
        self.assertRedirects(
            response,
            reverse("core:home"),
        )
        self.assertFalse(
            ProjectModel.objects.filter(
                pk=project_pk,
            ).exists()
        )
