from django.test import TestCase

from projects.models import ProjectModel


class ProjectModelTest(TestCase):
    """Tests para el modelo ProjectModel."""

    def test_project_str(self):
        """
        Test: El método __str__ devuelve el título.
        """
        project = ProjectModel.objects.create(title="Portfolio Web")

        self.assertEqual(str(project), "Portfolio Web")
