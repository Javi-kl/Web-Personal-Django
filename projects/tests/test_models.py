from django.contrib.auth.models import User
from django.test import TestCase

from projects.models import Comment, ProjectModel


class ProjectModelTest(TestCase):
    """Tests para el modelo ProjectModel."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_create_project(self):
        """
        Test: Crear un proyecto con datos básicos.
        """

        project = ProjectModel.objects.create(
            title="Mi Proyecto Portfolio",
            description="Un proyecto increíble de muestra",
        )

        self.assertEqual(project.title, "Mi Proyecto Portfolio")
        self.assertEqual(project.description, "Un proyecto increíble de muestra")

        self.assertIsNotNone(project.created_at)

        project_id = project.id
        project_from_db = ProjectModel.objects.get(id=project_id)
        self.assertEqual(project_from_db.title, "Mi Proyecto Portfolio")

    def test_project_str(self):
        """
        Test: El método __str__ devuelve el título.
        """
        project = ProjectModel.objects.create(title="Portfolio Web")

        self.assertEqual(project.__str__(), "Portfolio Web")


class CommentModelTest(TestCase):
    """Tests para el modelo Comment."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="comentario_test", password="testpass123"
        )
        self.project = ProjectModel.objects.create(title="Proyecto para comentarios")

    def test_create_comment(self):
        """
        Test: Crear comentario vinculado a proyecto y usuario.
        """
        comment = Comment.objects.create(
            project=self.project,
            author=self.user,
            content="Este es un comentario de prueba",
        )

        self.assertEqual(comment.project, self.project)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, "Este es un comentario de prueba")

        comments_from_project = self.project.comments.all()
        self.assertEqual(comments_from_project.count(), 1)
        self.assertIn(comment, comments_from_project)

    def test_comment_str(self):
        """
        Test: __str__ trunca contenido largo.
        """
        content_largo = "Este es un comentario muy largo que debería truncarse en la representación string"

        comment = Comment.objects.create(
            project=self.project, author=self.user, content=content_largo
        )

        expected_str = f"{self.user.username}: {content_largo[:50]}..."

        self.assertEqual(str(comment), expected_str)

        self.assertIn(self.user.username, str(comment))
