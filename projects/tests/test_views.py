from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from projects.models import ProjectModel


class ProjectCreateViewTest(TestCase):
    """
    Tests para ProjectCreateView.
    """

    def setUp(self):
        """Crear usuarios para los tests."""
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )

        self.normal_user = User.objects.create_user(
            username="normal", password="normal123"
        )

        self.url = reverse("projects:project_create")

    def test_create_requires_superuser(self):
        """
        Test: Solo superusers pueden acceder a crear proyecto.
        """

        # ---------------------------------------------------------------------
        # ESCENARIO 1: Usuario anónimo (sin login)
        # ---------------------------------------------------------------------
        response = self.client.get(self.url)

        self.assertNotEqual(response.status_code, 200)

        # ---------------------------------------------------------------------
        # ESCENARIO 2: Usuario normal (autenticado pero no superuser)
        # ---------------------------------------------------------------------
        self.client.login(username="normal", password="normal123")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

        # ---------------------------------------------------------------------
        # ESCENARIO 3: Superuser (autenticado Y superuser)
        # ---------------------------------------------------------------------
        self.client.logout()
        self.client.login(username="admin", password="admin123")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)


class ProjectUpdateViewTest(TestCase):
    """Tests para ProjectUpdateView."""

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", password="admin123"
        )
        self.normal_user = User.objects.create_user(
            username="normal", password="normal123"
        )
        self.project = ProjectModel.objects.create(
            title="Proyecto Original", description="Descripción original"
        )
        self.url = reverse("projects:project_update", kwargs={"pk": self.project.pk})

    def test_update_requires_superuser(self):
        """
        Test: Solo superusers pueden editar proyectos.
        """
        self.client.login(username="normal", password="normal123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        self.client.logout()
        self.client.login(username="admin", password="admin123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class ProjectDeleteViewTest(TestCase):
    """Tests para ProjectDeleteView."""

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", password="admin123"
        )
        self.normal_user = User.objects.create_user(
            username="normal", password="normal123"
        )
        self.project = ProjectModel.objects.create(title="Proyecto a Borrar")
        self.url = reverse("projects:project_delete", kwargs={"pk": self.project.pk})

    def test_delete_requires_superuser(self):
        """
        Test: Solo superusers pueden borrar proyectos.
        """
        self.client.login(username="normal", password="normal123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        self.client.logout()
        self.client.login(username="admin", password="admin123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
